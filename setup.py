import ez_setup
ez_setup.use_setuptools()

from setuptools import setup, find_packages

setup(name='unroll',
      version='0.1.0',
      author='Zulko',
    description='',
    long_description=open('README.rst').read(),
    license='see LICENSE.txt',
    keywords="Piano, rolls, transcription, MIDI, video, sheet music",
    packages= find_packages(exclude='docs'),
    install_requires=['numpy', 'music21', 'moviepy'])
