from setuptools import find_packages, setup

DEPS_ALL = open("requirements.txt", encoding="utf-8").readlines()

DEPS_TEST = DEPS_ALL + open("requirements-test.txt", encoding="utf-8").readlines()

setup(
    name="bond-cli",
    version="0.3.0",
    author="Olibra",
    packages=find_packages(),
    scripts=["bond/bond"],
    include_package_data=True,
    description="Bond CLI",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    python_requires=">=3.7",
    setup_requires=["pytest-runner"],
    install_requires=DEPS_ALL,
    tests_require=DEPS_TEST,
)
