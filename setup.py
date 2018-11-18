from setuptools import setup


setup(
    name='levmatch',
    version='0.1',
    description='Levenstein distance command line tool',
    url='http://github.com/arthur-hav/levmatch',
    author='ArthurHavlicek',
    author_email='arthurhavlicek@gmail.com',
    license='MIT',
    packages=['levmatch'],
    install_requires=[
        'fuzzywuzzy[speedup]',
    ],
    zip_safe=False,
    scripts=['bin/levmatch']
)