import re

from setuptools import find_packages, setup

install_requires = [
    "boto3",
]

docs_require = [
    "sphinx>=1.4.0",
]

tests_require = [
    "coverage==5.3",
    "pytest==9.0.3",
    "moto[ssm]==5.2.4",
    "mock",
    "django-environ<0.4.2",
    # Linting
    "ruff",
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
    python_requires=">=3.11",
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
        "Framework :: Django :: 4.2",
        "Framework :: Django :: 5.2",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
    ],
    zip_safe=False,
)
