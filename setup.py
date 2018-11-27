import codecs
import os
from setuptools import find_packages, setup

from plenario_client.__version__ import VERSION


here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, 'README.md'), encoding='utf8') as fh:
    long_description = fh.read()


setup(
    name='plenario-client',
    version=VERSION,
    description='The Official Python Client of the Array of Things API',
    long_description=long_description,
    url='https://github.com/UrbanCCD-UChicago/plenario-client-py',
    author='Vince Forgione',
    author_email='vforgione@uchicago.edu',
    license='Apache-2.0',
    python_requires='>=3.6',
    install_requires=[
        'requests'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    packages=find_packages(where='.', exclude=['tests', 'docs'])
)