from setuptools import setup

# pylama:skip=1
setup(name='rsparam',
      version='0.1.14',
      description='Revit shared parameters utility',
      long_description='Command line Tool for managing Revit Shared Parameters',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Utilities',
      ],
      keywords='autodesk revit parameter cli',
      url='https://github.com/eirannejad/rsparam',
      author='Ehsan Iran-Nejad',
      author_email='eirannejad@gmail.com',
      license='MIT',
      packages=['rsparam'],
      install_requires=[
          'docopt',
          'colorful',
          'tabulate',
      ],
      entry_points={
          'console_scripts': [
              'rsparam = rsparam.cli:main',
              ],
          },
      zip_safe=False)
