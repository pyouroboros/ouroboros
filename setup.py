from setuptools import setup, find_packages
from pyouroboros import VERSION

requirements = ['docker>=3.7.0',
                'schedule>=0.5.0',
                'prometheus_client>=0.5.0',
                'requests>=2.21.0',
                'influxdb>=5.2.1']

requirements_dev = ['docker>=3.7.0',
                    'schedule>=0.5.0',
                    'prometheus_client>=0.5.0',
                    'requests>=2.21.0',
                    'influxdb>=5.2.1',
                    'flake8']


def readme():
    with open('./README.md') as f:
        return f.read()


setup(
    name='ouroboros-cli',
    version=VERSION,
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
