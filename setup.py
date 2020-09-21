import re

from setuptools import find_packages, setup

install_requires = [
    "boto3",
    "six>=1.1",
]

docs_require = [
    "sphinx>=1.4.0",
]

tests_require = [
    "coverage==5.3",
    "pytest==3.0.5",
    "moto==1.3.16",
    "mock",
    "django-environ<0.4.2",
    # Linting
    "isort==4.2.5",
    "flake8==3.0.3",
    "flake8-blind-except==0.1.1",
    "flake8-debugger==1.4.0",
    "flake8-imports==0.1.1",
]

with open("README.rst") as fh:
    long_description = re.sub(
        "^.. start-no-pypi.*^.. end-no-pypi", "", fh.read(), flags=re.M | re.S
    )

setup(
    name="param-store",
    version="0.2.2",
    description="Parameter store for secrets",
    long_description=long_description,
    url="https://github.com/labd/python-param-store",
    author="Lab Digital B.V.",
    author_email="opensource@labdigital.nl",
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require={
        "docs": docs_require,
        "test": tests_require,
    },
    use_scm_version=True,
    entry_points={},
    package_dir={"": "src"},
    packages=find_packages("src"),
    include_package_data=True,
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 1.7",
        "Framework :: Django :: 1.8",
        "Framework :: Django :: 1.9",
        "Framework :: Django :: 1.10",
        "Framework :: Django :: 1.11",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
    zip_safe=False,
)
