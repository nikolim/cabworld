import os
from setuptools import setup, find_packages

setup(
    name="gym_cabworld",
    description="Cabworld Reinforcement Environment",
    long_description="Reinforcement Learning environment with the goal of teaching cabs to bring passengers "
    "efficiently to their destination. Based on OpenAIGym and Pygame",
    version="1.0.2",
    install_requires=["gym", "pygame", "wheel"],
    author="Nikolai Limbrunner",
    author_email="nikolai.limbrunner@web.de",
    packages=find_packages(),
    package_dir={"gym_cabworld": "gym_cabworld"},
    package_data={
        "": ["*.png"],
        "gym_cabworld/images/": ["gym_cabworld/images/*.png"],
        "gym_cabworld/data/": ["gym_cabworld/data/*.dat"],
    },
    data_files=[
        ("/gym_cabworld/images", [os.path.join("gym_cabworld/images/", "map_gen.png")]),
        (
            "/gym_cabworld/images",
            [os.path.join("gym_cabworld/images/", "small_map_gen.png")],
        ),
        ("/gym_cabworld/images", [os.path.join("gym_cabworld/images/", "cab.png")]),
        (
            "/gym_cabworld/images",
            [os.path.join("gym_cabworld/images/", "person_1.png")],
        ),
        (
            "/gym_cabworld/images",
            [os.path.join("gym_cabworld/images/", "person_2.png")],
        ),
        (
            "/gym_cabworld/images",
            [os.path.join("gym_cabworld/images/", "person_3.png")],
        ),
        ("/gym_cabworld/data", [os.path.join("gym_cabworld/data/small_map.dat")]),
        ("/gym_cabworld/data", [os.path.join("gym_cabworld/data/map.dat")]),
    ],
)
