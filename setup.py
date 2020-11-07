from setuptools import setup 

setup(name='gym_cabworld', 
      version='0.2', 
      install_requires=['gym', 'pygame'],
      author='Nikolai Limbrunner', 
      author_email='nikolai.limbrunner@web.de',
      packages=['gym_cabworld'], 
      package_dir={'gym_cabworld':'gym_cabworld'},
      package_data = {
        # If any package contains *.txt or *.rst files, include them:
        'gym_cabworld': ['images/*.png'],
    },)

