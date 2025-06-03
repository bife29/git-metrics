from setuptools import setup, find_namespace_packages

setup(
    name="git-metrics",
    version="0.1.0",
    description="Ferramenta para análise de métricas de repositórios Git",
    author="Jean Alves",
    author_email="jean.alves@parceirosec.com.br",
    package_dir={"": "src"},
    packages=find_namespace_packages(where="src"),
    include_package_data=True,
    install_requires=[
        "gitpython>=3.1.42",
        "pandas>=2.2.1",
        "typer>=0.9.0",
        "rich>=13.7.0",
        "python-dateutil>=2.8.2",
        "openpyxl>=3.1.2",
        "flask>=3.0.2",
        "plotly>=5.19.0",
        "dash>=2.15.0",
        "flask-cors>=4.0.0",
        "werkzeug>=3.0.1"
    ],
    entry_points={
        "console_scripts": [
            "git-metrics=main:app",
            "git-metrics-web=web.__main__:main"
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