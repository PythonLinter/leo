
import re
from os.path import join, dirname
from setuptools import setup, find_packages


# reading package version (same way the sqlalchemy does)
with open(join(dirname(__file__), 'leo', '__init__.py')) as v_file:
    package_version = re.compile(r".*__version__ = '(.*?)'", re.S).match(v_file.read()).group(1)


dependencies = [
    'restfulpy >= 0.41.3',
    'ujson',
    'aiohttp',
    'pymongo',

    # Deployment
    'gunicorn',

    # testing
    'requests',
    'webtest',
    'nose'
]


setup(
    name="leo",
    version=package_version,
    author="Vahid Mardani",
    author_email="mehdi@carrene.com",
    install_requires=dependencies,
    packages=find_packages(),
    test_suite="leo.tests",
    entry_points={
        'console_scripts': [
            'leo = leo:leo.cli_main'
        ]
    },
    message_extractors={'leo': [
        ('**.py', 'python', None),
    ]},
)
