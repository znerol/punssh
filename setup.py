from setuptools import find_packages
from setuptools import setup

setup(
    name="PunSSH",
    version="0.0.1",
    description="Git based SSH tunnel concentrator / jump host configuration.",
    author="Lorenz Schori",
    author_email="lo@znerol.ch",
    url="https://github.com/znerol/punssh",
    package_dir={"": "src"},
    packages=find_packages("src"),
    entry_points={
        "console_scripts": [
            "punssh-auth = punssh.cli.auth:main",
            "punssh-config = punssh.cli.config:main",
        ]
    },
    install_requires=[
        "Jinja2",
        "pyyaml",
    ],
)
