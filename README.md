# Sample-Efficient Bayesian Model-Based Reinforcement Learning Using DBN and PPL Models

## Overview
This project explores the application of Bayesian model-based reinforcement learning (RL) in high-stakes environments, particularly in healthcare decision-making for sepsis treatment. The research focuses on using Dynamic Bayesian Networks (DBNs) and Probabilistic Programming Languages (PPLs) to define highly taileored and structured models that approximate the simulation MDP to improve sample efficiency and interpretability compared to model-free RL approaches.

## Features
- **Simulation Environment**: based on [OberstSepsisEnv by Luo et al. (2024)](https://arxiv.org/abs/2405.18610), implemented locally using Openai Gym
- **DBN Models** implemented in Python: 
  - `FullDBN`: no facorization introduced
  - `MediumDBN`: moderate factorization of the transition probability space
  - `SimpleDBN`: highly factored MDP model
- **PPL Models** implemented in `Gen.jl`:
  - `SimplePPL`: highly tailored model based on expert knowledge
  - `SoftmaxPPL`: more general model that defines transition probabilities of vital signs with softmax functions
- **Thompson Sampling** implemented in Python and Julia
- **Baseline Comparisons** implemented in Python:
  - Q-Learning
  - DQN using `stable-baselines3`
- **Evaluation Metrics**: 
  - Sample Efficiency
  - Asymptotic Rewards
  - Cumulative Rewards
  - Learning Curve Plots

## Project Structure 
```
# Project Structure
src/dbn_ppl_rl/                     # Main source directory
    data/                           # Data files
        raw/                        # Produced by the runs
        processed/                  # Needed for metrics and plots
    models/             
        ppl/                        # PPL models in Julia
        dbn/                        # DBN models in Python
    planning/                       # Planning algorithms in python
    plot/                           # Plot utilities
    plots/                          # Generated plots
    sepsis_env/                     # Simulation environment
    main.jl                         # Main Julia script
    run_dbn_100.ipynb               # To run Thompson Sampling with DBN models with batch size 100
    run_dbn_every.ipynb             # To run Thompson Sampling with DBN models with batch size 1
    run_ppl_100.ipynb               # To run Thompson Sampling with PPL models with batch size 100
    run_ppl_every.ipynb             # To run Thompson Sampling with PPL models with batch size 1
    run_qlearning.ipynb             # Q-Learning runs
    run_dqn.ipynb                   # DQN runs
    run_compute_dqn_mean.ipynb      # Processes DQN run data
    run_compute_qlearning_mean.ipynb # Processes Q-Learning run data
    run_compute_ts_mean.ipynb       # Processes Thompson Sampling run data
    plot_ts.ipynb                   # To generate plots based on processed data
    results_ts.ipynb                # To generate metrics based on processed data

Manifest.toml                       # Julia package manifest
Project.toml                        # Julia dependencies
setup.py                            # Python setup script
README.md                           # Project documentation
```

## Installation

#### **Python Setup**
Install the package and dependencies:
   ```bash
   pip install -e .
   ```
#### **Julia Setup**
1. Ensure you have Julia installed:  
   Download and install Julia from [julialang.org](https://julialang.org/downloads/)

2. Set up the Julia environment:
   ```julia
   using Pkg
   Pkg.instantiate()  # Install required dependencies
   ```

Additional dependencies might be needed to install:
#### Python Requirements
- Python Version: `>=3.8`
- Required Python Packages:
  - `gymnasium`
  - `numpy`
  - `matplotlib`

#### Julia Requirements
- Julia Version: `>=1.6`
- Required Julia Packages:
  - `CairoMakie`
  - `Gen`
  - `JSON3`
  - `Printf`
  - `PyCall`
  - `Revise`
  - `Serialization`
  - `Statistics`



## Usage
Sample usage is provided in the `run_*.ipynb` files.
- PPL models: `models/ppl/evaluate/ppl_run.jl` contains the functions used for thompson sampling with the models defined in `models/ppl/model`
- DBN models: `models/dbn/evaluate/thompson_sampling.py` contains the functions used for thompson sampling with the models defined in `models/dbn/model`

## Contributors
- Luisa Stückelberger (University of Zurich)
- Supervisors: Prof. Dr. Giorgia Ramponi, Marius Furter
