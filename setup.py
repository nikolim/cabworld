import os
from setuptools import setup, find_packages

setup(
    name="gym_farmworld",
    description="Farmworld Reinforcement Environment",
    long_description="Reinforcement Learning environment"
    "efficiently to their destination. Based on OpenAIGym and Pygame",
    version="0.0.2",
    install_requires=["gym", "pygame", "wheel"],
    author="Nikolai Limbrunner",
    author_email="nikolai.limbrunner@web.de",
    packages=find_packages(),
    package_dir={"gym_farmworld": "gym_farmworld"},
    package_data={
        "": ["*.png"],
        "gym_farmworld/images/": ["gym_farmworld/images/*.png"],
        "gym_farmworld/data/": ["gym_farmworld/data/*.dat"],
    },
)
