from setuptools import setup, find_packages

setup(
    name="starlistify",
    version="0.0.1",
    entry_points={
        'console_scripts': [
            'starlistify=starlistify.cli:main',
        ],
    },
    exclude_package_data={'': ['test.py']},
    packages=find_packages(),
    include_package_data=True,
)