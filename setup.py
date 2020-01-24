import subprocess
from setuptools import setup, find_packages
from os import path, environ


def readme():
    here = path.abspath(path.dirname(__file__))
    with open(path.join(here, 'README.md')) as f:
        return f.read()


def get_dev_build_number():
    travis_build = environ.get('TRAVIS_BUILD_NUMBER')

    if travis_build:
        return '.dev{}'.format(travis_build)
    else:
        try:
            ver = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD'])
            return '+local.{}'.format(ver.decode('ascii').strip())
        except Exception:
            return ''


setup(name='cmf_watcher',
      version='0.1{}'.format(get_dev_build_number()),
      description='Monitors a Crash Move Folder and invokes actions accordingly',
      long_description=readme(),
      long_description_content_type="text/markdown",
      url='http://github.com/mapaction/cmf_watcher',
      author='MapAction',
      author_email='github@mapaction.com',
      license='GPL3',
      packages=find_packages(),
      install_requires=[
          'watchdog',
          'mapactionpy_controller'
      ],
      test_suite='unittest',
      tests_require=['unittest'],
      zip_safe=False,
      classifiers=[
          "Development Status :: 2 - Pre-Alpha",
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
          "Operating System :: OS Independent",
      ])
