# Copyright 2018 Red Hat, Inc. and others. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import io
import os
from setuptools import Command
from setuptools import find_packages
from setuptools import setup
import textwrap
from odltools import __version__


with io.open('README.rst', 'rt', encoding='utf8') as f:
    readme = f.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()


class CleanCommand(Command):
    """Custom clean command to tidy up the project root."""
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        os.system('rm -vrf ./build ./dist ./.tox ./*.pyc ./*.tgz ./*.egg-info')


setup(
    name='odltools',
    version=__version__,
    description='NetVirt tools for troubleshooting OpenDaylight and '
                'OpenStack integration',
    long_description=readme,
    long_description_content_type='text/x-rst; charset=UTF-8',
    url='http://github.com/shague/odltools',
    author='Sam Hague',
    author_email='shague@gmail.com',
    license='Apache License, Version 2.0',
    packages=find_packages(exclude=['tests']),
    install_requires=requirements,
    platforms=['All'],
    python_requires='>=2.7',
    keywords='development',
    zip_safe=False,
    entry_points={'console_scripts': ['odltools=odltools.__main__:main']},
    classifiers=textwrap.dedent('''
        Development Status :: 1 - Planning
        Environment :: Console
        Environment :: OpenStack
        Intended Audience :: Developers
        Intended Audience :: Information Technology
        Intended Audience :: System Administrators
        License :: OSI Approved :: Apache Software License
        Natural Language :: English
        Operating System :: OS Independent
        Programming Language :: Python
        Programming Language :: Python :: 2
        Programming Language :: Python :: 2.7
        Programming Language :: Python :: 3
        Programming Language :: Python :: 3.3
        Programming Language :: Python :: 3.4
        Programming Language :: Python :: 3.5
        Programming Language :: Python :: 3.6
        Topic :: Software Development
        Topic :: System :: Networking
        Topic :: System :: Systems Administration
        Topic :: Utilities
        ''').strip().splitlines(),
    cmdclass={
        'clean': CleanCommand,
    }
)
