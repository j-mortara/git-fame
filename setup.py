#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
import sys
from io import open as io_open

try:
    if '--cython' in sys.argv:
        sys.argv.remove('--cython')
        from Cython.Build import cythonize
    else:
        raise ImportError('--cython')
except ImportError:
    def cythonize(*args, **kwargs):
        return []


__author__ = None
__licence__ = None
__version__ = None
src_dir = os.path.abspath(os.path.dirname(__file__))
main_file = os.path.join(src_dir, 'gitfame', '_gitfame.py')
for l in io_open(main_file, mode='r'):
    if any(l.startswith(i) for i in ('__author__', '__licence__')):
        exec(l)
version_file = os.path.join(src_dir, 'gitfame', '_version.py')
with io_open(version_file, mode='r') as fd:
    exec(fd.read())

# Executing makefile commands if specified
if sys.argv[1].lower().strip() == 'make':
    import pymake
    # Filename of the makefile
    fpath = os.path.join(src_dir, 'Makefile')
    pymake.main(['-f', fpath] + sys.argv[2:])
    # Stop to avoid setup.py raising non-standard command error
    sys.exit(0)

extras_require = dict(yaml=['pyyaml'], tabulate=['tabulate'])
extras_require['dev'] = sum(extras_require.values(), ['py-make>=0.1.0'])

README_rst = ''
fndoc = os.path.join(src_dir, 'README.rst')
with io_open(fndoc, mode='r', encoding='utf-8') as fd:
    README_rst = fd.read()
setup(
    name='git-fame',
    version=__version__,
    description='Pretty-print `git` repository collaborators'
                ' sorted by contributions',
    long_description=README_rst,
    license=__licence__.lstrip('[').split(']')[0],
    author=__author__.split('<')[0].strip(),
    author_email=__author__.split('<')[1][1:-1],
    url='https://github.com/casperdcl/git-fame',
    bugtrack_url='https://github.com/casperdcl/git-fame/issues',
    platforms=['any'],
    packages=['gitfame'],
    provides=['gitfame'],
    install_requires=['argopt>=0.3.5'],
    extras_require=extras_require,
    entry_points={'console_scripts': ['git-fame=gitfame:main'], },
    package_data={'gitfame': ['LICENCE', 'git-fame.1']},
    ext_modules=cythonize(["gitfame/_gitfame.py", "gitfame/_utils.py"],
                          nthreads=2),
    classifiers=[
        # Trove classifiers
        # (https://pypi.org/pypi?%3Aaction=list_classifiers)
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Environment :: MacOS X',
        'Environment :: Other Environment',
        'Environment :: Win32 (MS Windows)',
        'Environment :: X11 Applications',
        'Framework :: IPython',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Other Audience',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Operating System :: POSIX :: BSD',
        'Operating System :: POSIX :: BSD :: FreeBSD',
        'Operating System :: POSIX :: Linux',
        'Operating System :: POSIX :: SunOS/Solaris',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: Implementation :: IronPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Desktop Environment',
        'Topic :: Education :: Computer Aided Instruction (CAI)',
        'Topic :: Education :: Testing',
        'Topic :: Office/Business',
        'Topic :: Other/Nonlisted Topic',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Pre-processors',
        'Topic :: Software Development :: User Interfaces',
        'Topic :: System :: Installation/Setup',
        'Topic :: System :: Logging',
        'Topic :: System :: Monitoring',
        'Topic :: System :: Shells',
        'Topic :: Terminals',
        'Topic :: Utilities'
    ],
    keywords='git blame stat stats statistics count author commit commits' \
             ' log shortlog ls-files',
    test_suite='nose.collector',
    tests_require=['nose', 'flake8', 'coverage'],
)
