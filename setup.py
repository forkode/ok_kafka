from setuptools import setup


setup(
    name='Ok Kafka',
    version='0.0.1',
    description='Kafka client wrapper with some additional logic',
    long_description=open('readme.md').read(),
    author='Ruslan Zhenetl',
    url='https://github.com/forkode/ok_kafka',
    license='MIT',
    packages=['ok_kafka'],
    install_requires=['jinja2', 'kafka-python', 'PyYAML'],
)
