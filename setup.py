from setuptools import setup, find_packages

setup(
    name="git-metrics",
    version="1.0.0",
    description="Ferramenta para análise de métricas de repositórios Git",
    author="Jean Alves",
    author_email="jean.alves@parceirosec.com.br",
    packages=find_packages(),
    install_requires=[
        "gitpython>=3.1.0",
        "pandas>=1.3.0",
        "typer>=0.4.0",
        "rich>=10.0.0",
        "openpyxl>=3.0.0",
        "python-dateutil>=2.8.0"
    ],
    entry_points={
        "console_scripts": [
            "git-metrics=src.main:app"
        ]
    },
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Version Control :: Git",
    ]
) 