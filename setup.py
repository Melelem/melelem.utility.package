import argparse


# NOTE: Whenever a change is made to the soffos module, you must update its package version!
# Set the version to be the 24hr, UTC+0 datetime stamp:
#   1. by hand (see: https://www.utctime.net/).
#   2. run this script with version arg ('python setup.py -v').
YEAR, MONTH, DAY = 22, 10, 24  # date
HOUR, MINUTE, SECOND = 10, 13, 19  # time

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument(
    '-v', '--version', action='store_true', help='set version as utc now')
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

    from soffos import DATA_DIR

    with open('README.md', 'r', encoding='utf-8') as readme:
        long_description = readme.read()

    with open('requirements.txt', 'r', encoding='utf-8') as requirements:
        install_requires = [str(r) for r in parse_requirements(requirements)]

    # Walk through data directory and get relative file paths.
    data_files, root_dir = [], os.path.dirname(__file__)
    for (dir_path, dir_names, file_names) in os.walk(DATA_DIR):
        rel_data_dir = os.path.relpath(dir_path, root_dir)
        data_files += [os.path.join(rel_data_dir, file_name) for file_name in file_names]

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
        packages=find_packages(exclude=['tests', 'tests.*']),
        install_requires=install_requires,
        include_package_data=True,
        data_files=[(str(DATA_DIR), data_files)],
        python_requires='>=3.7.*'
    )
