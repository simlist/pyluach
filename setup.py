from setuptools import setup
import io

with open('README.rst', 'r', encoding='utf-8') as readme:
      long_description = readme.read()

setup(name='pyluach',
      version='1.4.0',
      author='MS List',
      author_email='simlist@gmail.com',
      packages=['pyluach', ],
      url='https://github.com/simlist/pyluach',
      license='MIT',
      description=("""Pyluach is a Python package for manipulating Hebrew dates,
                    Gregorian-Hebrew calendar conversions, getting the weekly
                    parsha, and other Jewish calendar related calculations."""
                  ),
      long_description=long_description,
      python_requires=">=3.4",
      classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3 :: Only',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'Programming Language :: Python :: 3.10',
      ],
      keywords=['hebrew', 'calendar', 'jewish', 'luach', 'gregorian',
                  'julian', 'days', 'dates', 'date', 'conversion',
                  'parsha', 'holiday']
      )