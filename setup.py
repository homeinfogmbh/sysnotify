#! /usr/bin/env python3

from setuptools import setup

setup(
    name='sysnotify',
    use_scm_version={
        "local_scheme": "node-and-timestamp"
    },
    setup_requires=['setuptools_scm'],
    install_requires=[
        'emaillib',
        'hwdb',
        'peewee',
        'setuptools'
    ],
    author='HOMEINFO - Digitale Informationssysteme GmbH',
    author_email='<info at homeinfo dot de>',
    maintainer='Richard Neumann',
    maintainer_email='<r dot neumann at homeinfo priod de>',
    packages=['sysnotify'],
    entry_points={
        'console_scripts': [
            'sysnotify = sysnotify.watchdog:check_systems'
        ]
    },
    license='GPLv3',
    description='A notification system for digital signage systems.'
)
