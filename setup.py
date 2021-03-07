import os
from setuptools import setup, find_packages

setup(
    name="gym_farmworld",
    description="Farmworld Reinforcement Environment",
    long_description="Reinforcement Learning environment"
    "efficiently to their destination. Based on OpenAIGym and Pygame",
    version="0.0.1",
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
    data_files=[
        ("/gym_farmworld/images", [os.path.join("gym_farmworld/images/", "map_gen.png")]),
        (
            "/gym_farmworld/images",
            [os.path.join("gym_farmworld/images/", "small_map_gen.png")],
        ),
        ("/gym_farmworld/images", [os.path.join("gym_farmworld/images/", "cab.png")]),
        (
            "/gym_farmworld/images",
            [os.path.join("gym_farmworld/images/", "person_1.png")],
        ),
        (
            "/gym_farmworld/images",
            [os.path.join("gym_farmworld/images/", "person_2.png")],
        ),
        (
            "/gym_farmworld/images",
            [os.path.join("gym_farmworld/images/", "person_3.png")],
        ),
        ("/gym_farmworld/data", [os.path.join("gym_farmworld/data/small_map.dat")]),
        ("/gym_farmworld/data", [os.path.join("gym_farmworld/data/map.dat")]),
    ],
)
