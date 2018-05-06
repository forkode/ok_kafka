from setuptools import setup


setup(
    name='Ok Kafka',
    version='0.0.1',
    description='Kafka client wrapper with some additional logic',
    long_description=open('readme.md').read(),
    author='Ruslan Zhenetl',
    url='http://gitlab.fewerwords.org/forkard/ok_kafka',
    license='MIT',
    packages=['ok_kafka'],
    install_requires=['kafka-python'],
)
