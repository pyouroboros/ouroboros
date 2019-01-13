from setuptools import setup, find_packages

requirements = ['docker',
                'schedule',
                'prometheus_client',
                'requests',
                'influxdb']

requirements_dev = ['docker',
                    'schedule',
                    'prometheus_client',
                    'influxdb',
                    'requests',
                    'flake8']


def readme():
    with open('./README.md') as f:
        return f.read()


setup(
    name='ouroboros-cli',
    version='0.5.0',
    description='Automatically update running docker containers',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/pyouroboros/ouroboros',
    license='MIT',
    classifiers=['Programming Language :: Python'],
    packages=find_packages(exclude=['doc', 'tests']),
    scripts=['ouroboros'],
    install_requires=requirements,
    tests_require=requirements_dev,
    python_requires='>=3.0'
)
