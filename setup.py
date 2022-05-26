import argparse


# NOTE: Whenever a change is made to the soffos module, you must update its package version!
# Set the version to be the 24hr, UTC+0 datetime stamp:
#   1. by hand (see: https://www.utctime.net/).
#   2. run this script with version arg ('python setup.py -v').
YEAR, MONTH, DAY = 22, 5, 26  # date
HOUR, MINUTE, SECOND = 12, 54, 34  # time


arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('-v', '--version', action='store_true', help='set version as utc now')
known_args, unknown_args = arg_parser.parse_known_args()

if known_args.version:
    from datetime import datetime
    import re

    with open('setup.py', 'r+', encoding='utf-8') as this:
        # Read setup.py.
        setup = this.read()

        # Set version as datetime utc now.
        now = datetime.utcnow()
        setup = re.sub(
            r'.*YEAR\s*,\s*MONTH\s*,\s*DAY\s*=\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)(.*\s)'
            r'.*HOUR\s*,\s*MINUTE\s*,\s*SECOND\s*=\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)(.*)',
            f'YEAR, MONTH, DAY = {str(now.year)[-2:]}, {now.month}, {now.day}\\4'
            f'HOUR, MINUTE, SECOND = {now.hour}, {now.minute}, {now.second}\\8',
            setup
        )

        # Rewrite setup.py.
        this.seek(0)
        this.write(setup)
        this.truncate()
else:
    from pkg_resources import parse_requirements
    from setuptools import setup, find_packages
    import os

    with open('README.md', 'r', encoding='utf-8') as readme:
        long_description = readme.read()

    with open('requirements.txt', 'r', encoding='utf-8') as requirements:
        install_requires = [str(r) for r in parse_requirements(requirements)]

    setup(
        name='soffos',
        version=f'{YEAR}.{MONTH}.{DAY}.{HOUR}.{MINUTE}.{SECOND}',
        author='Stefan Kairinos',
        author_email='stefan.kairinos@soffos.ai',
        description='Soffos\' utilities.',
        long_description=long_description,
        long_description_content_type='text/markdown',
        url='https://github.com/Soffos-EDU/soffos.package',
        classifiers=[
            'Programming Language :: Python :: 3',
            'Operating System :: OS Independent'
        ],
        packages=find_packages(),
        install_requires=install_requires,
        python_requires='==3.7.*'
    )
