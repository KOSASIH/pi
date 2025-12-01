from setuptools import setup, find_packages

setup(
    name="quantum-nexus-ai",
    version="1.0.0",
    author="KOSASIH",
    author_email="kosasih@example.com",
    description="Ultimate hyper-tech platform integrating quantum AI, blockchain, and IoT.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/KOSASIH/hyper-pi/tree/main/quantum-nexus-ai",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    keywords="quantum ai blockchain iot hyper-tech",
    python_requires=">=3.9",
    install_requires=[
        "qiskit",
        "tensorflow",
        "web3",
        "fastapi",
        "pydantic",
        "numpy",
    ],
    extras_require={
        "dev": ["pytest", "black", "flake8"],
        "quantum": ["qiskit-aer"],
        "blockchain": ["eth-account"],
    },
    entry_points={
        "console_scripts": [
            "nexus-cli=cli.nexus_cli:main",
        ],
    },
)
