from setuptools import setup, find_packages

setup(
    name="safedev",
    version="1.0",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "safedev": ["rules.json"]
    },
    install_requires=["colorama", "tqdm", "aiohttp"],
    entry_points={
        "console_scripts": [
            "safedev=safedev.cli:cli"
        ]
    }
)