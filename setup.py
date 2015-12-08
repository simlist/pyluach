from setuptools import setup, find_packages
import io

setup(name='pyluach',
      version='0.2.0dev',
      author='MS List',
      author_email='simlist@gmail.com',
      packages= ['pyluach',],
      url='https://github.com/simlist/pyluach',
      license='MIT',
      description=('''Package for manipulating Hebrew dates and
                    Gregorian-Hebrew conversion'''),
      long_description=io.open('README.rst').read(),
      classifiers = ['Development Status :: 2 - Pre-Alpha',
                     'Intended Audience :: Developers',
                     'License :: OSI Approved :: MIT License',
                     'Programming Language :: Python :: 2'],
      keywords = [' hebrew calendar luach gregorian julian days conversion']
      )