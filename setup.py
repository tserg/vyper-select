from setuptools import find_packages, setup

setup(
    name="vyper-select",
    description="Manage multiple Vyper compiler versions.",
    url="https://github.com/tserg/vyper-select",
    author="tserg",
    version="0.0.1.a1",
    packages=find_packages(),
    python_requires=">=3.7",
    license="AGPL-3.0",
    long_description=open("README.md", encoding="utf8").read(),
    entry_points={
        "console_scripts": [
            "vyper-select = vyper_select.__main__:vyper_select",
            "vyper = vyper_select.__main__:vyper",
        ]
    },
    install_requires=[
        'pysha3'
    ]
)
