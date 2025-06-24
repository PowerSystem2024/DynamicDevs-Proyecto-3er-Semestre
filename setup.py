from setuptools import setup, find_packages

setup(
    name="enertech",
    version="0.1.0",
    packages=find_packages(where="enertech"),  # Busca paquetes en la carpeta `enertech`
    package_dir={"": "enertech"},  # Define la raíz del paquete
    install_requires=[  # Dependencias
        "psycopg2-binary>=2.9.5",  # psycopg2
    ],
    python_requires=">=3.8",  # Versión mínima de Python
)
