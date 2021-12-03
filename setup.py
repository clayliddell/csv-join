from setuptools import setup

setup(
    name='csv-join',
    version='0.2.0',
    description='A tool for joining CSV file.',
    author='Clayton Liddell',
    author_email='account+github@clayliddell.com',
    url='https://github.com/clayliddell/csv-join',
    license='MIT',
    packages=['csvjoin'],
    install_requires=[
        'pandas>=1.3.0',
    ],
    entry_points = {
        'console_scripts': ['csv-join=csvjoin.__main__:main'],
    },
)
