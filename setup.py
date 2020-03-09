from setuptools import setup, find_packages

DEPS_ALL = open('requirements.txt').readlines()

DEPS_TEST = DEPS_ALL + open('requirements-test.txt').readlines()

setup(
    name='bond-cli',
    version='0.0.1',
    author='Olibra',
    packages=find_packages(),
    include_package_data=True,
    description='Bond CLI',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    python_requires='>=3.6',
    setup_requires=['pytest-runner'],
    install_requires=DEPS_ALL,
    tests_require=DEPS_TEST
)
