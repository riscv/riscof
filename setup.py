import os
import codecs
from setuptools import setup, find_packages

import riscof

# Base directory of package
here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    with codecs.open(os.path.join(here, *parts), 'r') as fp:
        return fp.read()


#Long Description

long_description = read('README.md')
version = "1.4.0"

with open("requirements.txt", "r") as reqfile:
    requirements = reqfile.readlines()

setup(name="riscof",
      version=version,
      description="RiscV Compliance Framework by Incoresemi Ltd.",
      long_description=long_description,
      classifiers=[
          "Programming Language :: Python :: 3.7",
          "Licence :: OSI Approved :: BSD licence",
          "Development Status :: 2 - Pre-Alpha"
      ],
      author='S Pawan Kumar',
      author_email='spawan1999@gmail.com',
      license='BSD',
      packages=find_packages(),
      package_dir={'riscof': 'riscof/'},
      package_data={'riscof': ['suite/*', 'suite/env/*', 'schemas/*']},
      data_files=[('riscof/framework/', ['riscof/framework/database.yaml'])],
      install_requires=requirements,
      entry_points={
          "console_scripts": ["riscof=riscof.main:execute"],
      })