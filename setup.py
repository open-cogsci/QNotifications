#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This file is part of QNotifications.

QNotifications is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

QNotifications is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with QNotifications.  If not, see <http://www.gnu.org/licenses/>.
"""

from setuptools import setup, find_packages
import QNotifications

setup(
	name='python-qnotifications',
	version=QNotifications.__version__,
	description='Pretty in-app notifications for PyQt',
	author='Daniel Schreij',
	author_email='dschreij@gmail.com',
	url='https://github.com/dschreij/QNotifications',
	packages=find_packages('.'),
	install_requires=[
		'qtpy',
	],
	classifiers=[
		'Intended Audience :: Developers',
		'Topic :: Desktop Environment',
		'Topic :: Communications :: Email',
		'Operating System :: MacOS :: MacOS X',
		'Operating System :: Microsoft :: Windows',
		'Operating System :: POSIX',
		'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
		'Programming Language :: Python :: 2',
		'Programming Language :: Python :: 3',
	],
)
