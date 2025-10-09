from setuptools import setup, find_packages

setup(
    name="checkmagic",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests",
        "ipython"
    ],
    python_requires='>=3.8',
    description="Python homeworks check system integrated into Jupyter Notebook.",
    author="kluwik",
    url="https://github.com/kluwik/checkmagic",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
