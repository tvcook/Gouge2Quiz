from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='gouge2quiz',
      version='1.0',
      description='Command line application that creates a quiz from a PDF',
      url='https://github.com/tvcook/gouge2quiz',
      author='tvcook',
      author_email='tanner.v.cook@gmail.com',
      license='MIT',
      packages=['gouge2quiz'],
      scripts=['bin/gouge2quiz'],
      install_requires=[
          'pdftotext',
      ],
      zip_safe=False)
