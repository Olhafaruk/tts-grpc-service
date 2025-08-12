# setup.py
from setuptools import setup, find_packages

setup(
    name="tts_grpc_service",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "grpcio>=1.56.2",
        "grpcio-tools>=1.56.2",
        "gtts==2.4.0",
        "python-dotenv==1.0.0",
        "pytest==8.4.1",
        "python-json-logger==2.0.7",
        "protobuf==4.24.0",
    ],
)
