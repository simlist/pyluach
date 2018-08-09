from setuptools import setup
import io

setup(name='pyluach',
      version='0.3.2.dev2',
      author='MS List',
      author_email='simlist@gmail.com',
      packages=['pyluach', ],
      url='https://github.com/simlist/pyluach',
      license='MIT',
      description=("""Pyluach is a Python package for manipulating Hebrew dates,
                    Gregorian-Hebrew calendar conversions, and other Jewish
                    calendar related calculations.""),
      long_description=io.open('README.rst').read(),
      classifiers=['Development Status :: 3 - Alpha',
                     'Intended Audience :: Developers',
                     'License :: OSI Approved :: MIT License',
                     'Programming Language :: Python :: 2.7',
                     'Programming Language :: Python :: 3'],
      keywords=['hebrew', 'calendar', 'jewish', 'luach', 'gregorian',
                  'julian', 'days', 'dates', 'date', 'conversion',
                  'parsha', 'holiday']
      )
