from setuptools import setup, find_packages


def readme():
    with open('./README.md') as f:
        return f.read()


def read_reqs(requirements):
    with open(requirements) as f:
        return f.read().splitlines()


setup(
    name='ouroboros-cli',
    version='0.3.4',
    description='Automatically update running docker containers',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/circa10a/ouroboros',
    license='MIT',
    classifiers=['Programming Language :: Python'],
    packages=find_packages(exclude=['doc', 'tests']),
    scripts=['ouroboros/ouroboros'],
    install_requires=read_reqs(requirements='./requirements.txt'),
    tests_require=read_reqs(requirements='./requirements-dev.txt'),
    python_requires='>=3.0'
)
