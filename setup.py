import os
from setuptools import setup, find_packages

setup(name='gym_cabworld',
      version='0.2',
      install_requires=['gym', 'pygame'],
      author='Nikolai Limbrunner',
      author_email='nikolai.limbrunner@web.de',
      packages=find_packages(),
      package_dir={'gym_cabworld': 'gym_cabworld'},
      package_data={
          '': ['*.png'], },
      data_files=[
        ('/home/niko/Info/gym-cabworld', [os.path.join('gym_cabworld/images/', 'map_gen.png')]),
        ('/home/niko/Info/gym-cabworld', [os.path.join('gym_cabworld/images/', 'cab.png')]),
        ('/home/niko/Info/gym-cabworld', [os.path.join('gym_cabworld/images/', 'person_1.png')]),
        ('/home/niko/Info/gym-cabworld', [os.path.join('gym_cabworld/images/', 'person_2.png')]),
        ('/home/niko/Info/gym-cabworld', [os.path.join('gym_cabworld/images/', 'person_3.png')]),
    ],
)
