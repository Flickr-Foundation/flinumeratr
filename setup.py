import os

import setuptools


def local_file(name):
    return os.path.relpath(os.path.join(os.path.dirname(__file__), name))


def static_files(dirname):
    return [
        os.path.join(dirname, filename)
        for filename in os.listdir(local_file(f"src/flinumeratr/{dirname}"))
    ]


with open(local_file("requirements.txt")) as f:
    INSTALL_REQUIRES = list(f)


SOURCE = local_file("src")

setuptools.setup(
    name="flinumeratr",
    version="1.0.0",
    author="Flickr Foundation",
    author_email="hello@flickr.org",
    packages=setuptools.find_packages(SOURCE),
    package_data={"flinumeratr": static_files("static") + static_files("templates")},
    package_dir={"": SOURCE},
    url="https://github.com/Flickr-Foundation/flinumeratr",
    install_requires=INSTALL_REQUIRES,
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "flinumeratr = flinumeratr.cli:main",
        ]
    },
)
