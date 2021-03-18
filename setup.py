import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="SciExpeM_API",
    version="2.0.2.2",
    author="Edoardo Ramalli",
    author_email="edoardo.ramalli@polimi.it",
    description="Python wrapper for SciExpeM EndPoints",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/edoardoramalli/SciExpeM_API",
    packages=setuptools.find_packages(),
    install_requires=['requests', 'django', 'simplejson', 'pandas'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Chemistry",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Software Development :: Interpreters",
        "Topic :: Software Development :: Libraries :: Application Frameworks",

    ],
    include_package_data=True,
)
