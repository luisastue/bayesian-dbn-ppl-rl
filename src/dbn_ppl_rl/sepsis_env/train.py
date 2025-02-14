from multiprocessing import Pool, cpu_count
from stable_baselines3 import DQN
from itertools import product
import os
import dill as pickle
import stable_baselines3 as sb3
from dbn_ppl_rl.sepsis_env.sepsis_types import *
from dbn_ppl_rl.sepsis_env.sepsis_gym import *
import numpy as np
from typing import List
import matplotlib.pyplot as plt


class Training:
    def __init__(self, model, nr_iterations: int, env, episodes: list, name: str, info: dict,):
        self.model = model
        self.nr_iterations = nr_iterations
        self.env = env
        self.episodes = episodes
        self.info = info
        self.info["name"] = name
        self.info["date"] = str(np.datetime64('now'))
        self.policy = None

    def save(self, directory="data/dqn"):
        os.makedirs(directory, exist_ok=True)
        model_path = os.path.join(
            directory, f"{self.info['name']}_model.zip")
        object_path = os.path.join(
            directory, f"{self.info['name']}_object.pkl")

        self.model.save(model_path)
        self.info['model_path'] = model_path
        mod = self.model
        self.model = None

        with open(object_path, 'wb') as file:
            pickle.dump(self, file)

        self.model = mod
        return object_path, model_path

    def retrain(self, env, n_iter: int):
        self.model.set_env(env)
        reward_callback = CustomLoggingCallback()
        self.model.learn(n_iter, callback=reward_callback)
        self.episodes.extend(reward_callback.episodes)
        self.nr_iterations += n_iter
        self.env = env
        self.info["nr_retrained"] = self.info.get("retrained", 0) + 1
        self.save()
        return self

    def get_policy(self):
        if self.policy is None:
            self.policy = {state:  ACTIONS[self.model.predict(state_ix, deterministic=True)[
                0]] for state_ix, state in enumerate(STATES)}
        return self.policy

    def evaluate_policy(self, n_episodes: int):
        pol = self.get_policy()
        test_eps = [run_episode(pol) for _ in range(n_episodes)]
        return np.mean([np.sum(ep.rewards) for ep in test_eps])

    @staticmethod
    def load(object_path: str):
        with open(object_path, 'rb') as file:
            training = pickle.load(file)

        if 'model_path' in training.info:
            try:
                training.model = sb3.DQN.load(training.info['model_path'])
            except Exception as e:
                print(
                    f"Failed to load DQN model: {e}. Trying to load PPO model.")
                training.model = sb3.PPO.load(training.info['model_path'])
        else:
            raise ValueError(
                "Model path not found in the saved MDPOpt object.")

        return training


class CustomLoggingCallback(sb3.common.callbacks.BaseCallback):
    def __init__(self, verbose=0):
        super(CustomLoggingCallback, self).__init__(verbose)
        self.episodes = []
        self.evaluation = None
        self.current_rewards = []

    def _on_step(self) -> bool:
        # Collect rewards at each step
        reward = self.locals["rewards"][0]
        self.current_rewards.append(reward)

        # Check if the episode has ended
        done = self.locals["dones"]
        if done:
            self.episodes.append(Episode(None, self.current_rewards, None))
            self.current_rewards = []  # Reset for the next episode

        return True  # Continue training


def train_dqn(env, nr_iter, name):
    model = sb3.DQN("MlpPolicy", env, verbose=0)
    reward_callback = CustomLoggingCallback()
    model.learn(nr_iter, callback=reward_callback)
    optimization = Training(model, nr_iter, env,
                            reward_callback.episodes, f"DQN-{name}", {})
    optimization.save()
    return optimization


def train_ppo(env, nr_iter, name):
    model = sb3.PPO("MlpPolicy", env, verbose=0)
    reward_callback = CustomLoggingCallback()
    model.learn(nr_iter, callback=reward_callback)
    optimization = Training(model, nr_iter, env,
                            reward_callback.episodes, f"PPO-{name}", {})
    optimization.save()
    return optimization


def train_and_log_rewards(task):
    metric, params, run, n_steps = task

    # Initialize callback
    callback = CustomLoggingCallback()

    # Create and train the model
    model = DQN(
        "MlpPolicy",
        true_env,
        buffer_size=params["buffer_size"],
        batch_size=params["batch_size"],
        train_freq=params["train_freq"],
        gradient_steps=params["gradient_steps"],
        exploration_fraction=params["exploration_fraction"],
        exploration_final_eps=params["exploration_final_eps"],
        target_update_interval=params["target_update_interval"],
        learning_rate=1e-4,
        gamma=0.99,
        verbose=0,
    )

    model.learn(total_timesteps=n_steps, callback=callback)
    optimization = Training(model, n_steps, true_env,
                            callback.episodes, f"{metric}-{run}", {
                                "params": params,
                                "learning_rate": 1e-4,
                                "gamma": 0.99,
                            })
    optimization.save()
    return optimization


def create_tasks(param_grids):
    tasks = []
    for goal, param_grid in param_grids.items():
        param_combinations = list(product(*param_grid.values()))
        param_names = list(param_grid.keys())
        for combination in param_combinations:
            params = dict(zip(param_names, combination))
            tasks.append((goal, params))
    return tasks

# Function to process a single task


def process_task(task):
    goal, params = task
    return train_and_log_rewards(params)
