import setuptools

from setuptools.command.install import install
with open("README.md", "r") as fh:
    long_description = fh.read()




setuptools.setup(
    name="SciExpeM_API",
    version="1.0.0",
    author="Edoardo Ramalli",
    author_email="edoardo.ramalli@polimi.it",
    description="Python wrapper for SciExpeM",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/edoardoramalli/SciExpeM_API",
    packages=setuptools.find_packages(),
    install_requires=['requests', 'django'],
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    include_package_data=True,
)
