from setuptools import setup, find_packages

requirements = ['docker',
                'schedule',
                'prometheus_client',
                'requests']

requirements_dev = ['docker',
                    'schedule',
                    'prometheus_client',
                    'requests',
                    'pytest >= 3.6',
                    'pytest-cov',
                    'pytest-mock',
                    'codecov',
                    'flake8']


def readme():
    with open('./README.md') as f:
        return f.read()


setup(
    name='ouroboros-cli',
    version='0.4.2',
    description='Automatically update running docker containers',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/circa10a/ouroboros',
    license='MIT',
    classifiers=['Programming Language :: Python'],
    packages=find_packages(exclude=['doc', 'tests']),
    scripts=['ouroboros'],
    install_requires=requirements,
    tests_require=requirements_dev,
    python_requires='>=3.0'
)
