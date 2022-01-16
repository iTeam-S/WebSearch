import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="websearch-python",                  # This is the name of the package
    version="1.2.1",                      # The initial release version
    author="iTeam-$",                         # Full name of the author
    description="Module allowing you to do various searches for links on the Web",
    long_description=long_description,  # Long description read from the readme
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),  # List of all modules to be installed
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],                      # Information to filter the project on PyPi website
    python_requires='>=3.6',
    py_modules=["websearch"],                      # Name of the python package
    install_requires=[
        "BeautifulSoup4", "requests", "gevent", "flask"],  # depandance
    include_package_data=True,         # Include all data file with the package
    package_data={'': ['*.json']},
    scripts=['bin/websearch']
)
