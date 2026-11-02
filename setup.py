#!/usr/bin/env python3
"""XP Terminal RPG — Package Setup"""

from setuptools import setup, find_packages
from pathlib import Path

long_description = ""
readme = Path(__file__).parent / "README.md"
if readme.exists():
    long_description = readme.read_text(encoding="utf-8")

setup(
    name="xp-terminal-rpg",
    version="1.0.0",
    description="Terminal Coding RPG — turn every commit into XP",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="XP Project",
    url="https://github.com/belentani7/xp",
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=[],  # stdlib only!
    entry_points={
        "console_scripts": [
            "xp=engine.rpg:main",
        ],
    },
    package_data={
        "": [
            "database/*.sql",
            "config/*.yaml",
            "hooks/*",
            "display/*.sh",
            "ascii/*.txt",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Games/Entertainment :: Role-Playing",
        "Topic :: Software Development :: Version Control :: Git",
    ],
    keywords="git rpg gamification xp terminal coding",
)
