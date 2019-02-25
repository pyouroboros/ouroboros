from setuptools import setup, find_packages
from pyouroboros import VERSION


def read(filename):
    with open(filename) as f:
        return f.read()


def get_requirements(filename="requirements.txt"):
    """returns a list of all requirements"""
    requirements = read(filename)
    return list(filter(None, [req.strip() for req in requirements.split() if not req.startswith('#')]))


setup(
    name='ouroboros-cli',
    version=VERSION,
    maintainer='circa10a',
    maintainer_email='caleblemoine@gmail.com',
    description='Automatically update running docker containers',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    url='https://github.com/pyouroboros/ouroboros',
    license='MIT',
    classifiers=['Programming Language :: Python',
                 'Programming Language :: Python :: 3.6',
                 'Programming Language :: Python :: 3.7'],
    packages=find_packages(),
    scripts=['ouroboros'],
    install_requires=get_requirements(),
    python_requires='>=3.6.2'
)
