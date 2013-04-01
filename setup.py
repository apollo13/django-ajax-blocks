import codecs
import re
from os import path
from setuptools import setup, find_packages


def read(*parts):
    return open(path.join(path.dirname(__file__), *parts)).read()


setup(
    name='django-ajax-blocks',
    description='Partial page loads with AJAX',
    long_description=read('README.rst'),
    version='0.1a2',
    url='http://github.com/apollo13/django-ajax-blocks',
    author='Florian Apolloner',
    author_email='florian@apolloner.eu',
    license='BSD',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
)
