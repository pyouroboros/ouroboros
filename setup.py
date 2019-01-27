from setuptools import setup, find_packages
from pyouroboros import VERSION

requirements = ['docker>=3.7.0',
                'apscheduler>=3.5.3',
                'prometheus_client>=0.5.0',
                'requests>=2.21.0',
                'influxdb>=5.2.1',
                'apprise>=0.5.2']


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
    classifiers=['Programming Language :: Python',
                 'Programming Language :: Python :: 3.6',
                 'Programming Language :: Python :: 3.7'],
    packages=find_packages(),
    scripts=['ouroboros'],
    install_requires=requirements,
    python_requires='>=3.6.2'
)
