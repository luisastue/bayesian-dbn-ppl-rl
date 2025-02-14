from setuptools import setup, find_packages

setup(
    name="dbn_ppl_rl",         # Name of your package
    version="1.0.0",              # Version number
    packages=find_packages("src"),  # Look for packages in the "src" directory
    # Define "src" as the root directory for packages
    package_dir={"": "src"},
    install_requires=[            # Add dependencies if necessary
        "gymnasium",
        "numpy",
        "matplotlib"
    ],
)
