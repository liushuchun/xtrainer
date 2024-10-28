import os
from setuptools import setup, find_packages
import pkg_resources

# Path to the requirements file
requirements_path = os.path.join(os.path.dirname(__file__), "requirements.txt")

# Read the requirements from the requirements file
if os.path.exists(requirements_path):
    with open(requirements_path, 'r') as f:
        install_requires = [str(r) for r in pkg_resources.parse_requirements(f)]
else:
    install_requires = []

setup(
    name="xtrainer",
    version="1.0.0",
    description="Enjoy the finetune of Diffusion models!",
    author="Liushuchun",
    packages=find_packages(),
    install_requires=install_requires,
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    package_data={"xtrainer": ["tokenizer_configs/**/**/*.*"]},
    python_requires='>=3.6',
)