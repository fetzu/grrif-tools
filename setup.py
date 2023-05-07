from setuptools import setup, find_packages

setup(
    name="grrif_tools",
    description="An unofficial set of tools for Cool Cats™.",
    author="Julien 'fetzu' Bono", 
    url="https://fetzu.ch/",
    version="0.5.1",
    download_url="https://github.com/fetzu/grrif_tools",
    packages=find_packages(include=['grrif_tools','grrif_tools.*']),
    license="License :: OSI Approved :: MIT License",
    install_requires=[
        "Requests==2.30.0",
        "beautifulsoup4==4.11.1",
        "titlecase==2.4",
    ],
    entry_points={"console_scripts": ["grrif_tools=grrif_tools.cli:main"]},
)