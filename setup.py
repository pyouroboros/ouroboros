from setuptools import setup, find_packages

setup(
    name='ouroboros',
    version='0.1.3',
    url='https://github.com/circa10a/ouroboros',
    classifiers=['Programming Language :: Python'],
    packages=find_packages(exclude=['tests']),
    scripts=['ouroboros/ouroboros'],
    install_requires=['schedule', 'docker'],
    tests_require=['pytest', 'pytest-mock', 'pytest-cov', 'codecov']
)
