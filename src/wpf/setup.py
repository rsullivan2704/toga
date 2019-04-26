#/usr/bin/env python
import io
import re

from setuptools import setup, find_packages

with io.open('toga_wpf/__init__.py', encoding='utf8') as version_file:
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file.read(), re.M)
    if version_match:
        version = version_match.group(1)
    else:
        raise RuntimeError("Unable to find version string.")


with io.open('README.rst', encoding='utf8') as readme:
    long_description = readme.read()


setup(
    name='toga-wpf',
    version=version,
    description='A Microsoft .Net backend for the Toga widget toolkit using the Windows Presentation Foundation API.',  # noqa: E501
    long_description=long_description,
    author='Robert J Sullivan',
    author_email='robertjonsullivan@gmail.com',
    url='http://pybee.org/toga',
    packages=find_packages(exclude='tests'),
    python_requires='>=3.5',
    install_requires=[
        'pythonnet',
        'toga-core==%s' % version,
        'arrow',
    ],
    tests_require=[
        'toga-dummy==%s' % version
    ],
    license='New BSD',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: Microsoft :: Windows :: Windows 7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development',
        'Topic :: Software Development :: User Interfaces',
        'Topic :: Software Development :: Widget Sets',
    ],
    test_suite='tests',
)
