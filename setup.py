import os
from setuptools import setup, find_packages

setup(name='gym_cabworld',
      description='Cabworld Reinforcement Environment',
      long_description='Reinforcement Learning Environment an environment with the goal of teaching cabs to bring passengers efficiently to their destination. Based on OpenAIGym and Pygame',
      version='0.9.2',
      install_requires=['gym', 'pygame', 'wheel'],
      author='Nikolai Limbrunner',
      author_email='nikolai.limbrunner@web.de',
      packages=find_packages(),
      package_dir={'gym_cabworld': 'gym_cabworld'},
      package_data={
          '': ['*.png'], },
	data_files=[
        ('/home/niko/Info/gym-cabworld', [os.path.join('gym_cabworld/images/', 'map_gen.png')]),
        ('/home/niko/Info/gym-cabworld', [os.path.join('gym_cabworld/images/', 'small_map_gen.png')]),
        ('/home/niko/Info/gym-cabworld', [os.path.join('gym_cabworld/images/', 'cab.png')]),
        ('/home/niko/Info/gym-cabworld', [os.path.join('gym_cabworld/images/', 'person_1.png')]),
        ('/home/niko/Info/gym-cabworld', [os.path.join('gym_cabworld/images/', 'person_2.png')]),
        ('/home/niko/Info/gym-cabworld', [os.path.join('gym_cabworld/images/', 'person_3.png')]),
        ('/home/niko/Info/gym-cabworld', [os.path.join('map.dat')]),
         ('/home/niko/Info/gym-cabworld', [os.path.join('small_map.dat')]),
    ],
)
