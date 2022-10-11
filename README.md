# soffos.package

:exclamation: WARNING: This repo is public. DO NOT put any code containing IP or secret settings.


## Pip Install

To pip install the soffos package, run:

```
pip install git+https://github.com/Soffos-EDU/soffos.package.git
```

NOTE: Installing via git only works if this repo is public. If this repo is made to be private in the future, then an SSH key will need to be attached to this repo and supplied during the
pip install:

```
pip install git+ssh://github.com/Soffos-EDU/soffos.package.git
```

## Version Control

### Where is the package version specified?

Pip relies on the `setup.py` file to declare and setup the soffos package. During setup, the version number of the soffos package is set. The version is set to be current UTC datetime stamp, denoting when the package was updated. The version number is in the format:

`{year}.{month}.{day}.{hour}.{minute}.{second}`

For example: The UTC datetime stamp of `5/10/2022 10:55:28` is formatted to `22.10.5.10.55.28`.

### How can I update the package version?

For convenience, `setup.py` accepts a command line argument that auto-sets the version as UTC now:

```
python setup.py --version
```

Alternatively, if you're using VS code, you can launch the "Update Version" configuration, which will call the above command for you (see `.vscode/launch.json`).

### Why should I update the package version?

When pip installing, pip will only know that a new version of the package is available if you **set a new package version number higher than the old one**. Pip does not look at your code and compare the differences between the old and new code. If you make an update to the code of the soffos package and forget to update the version number, pip will not know to install the new code. 

## Package Releases

### What is a package release?

GitHub has a feature called "releases" which allows you to take a snapshot of a repo at the current
moment in time and attach a tag to that snapshot.

### Why should I create a package release?

This is important to do if you want to pip install a version of the soffos package that will be unaffected by future changes (which may be breaking changes). This is particularly important for the production environment. If a specific release of the package is not pip installed, then the latest soffos package will always be installed during build time and could introduce breaking changes.

### How do I select a package release when pip installing?

You need to specify the tag of the release you wish to pip install:

```
git+https://github.com/Soffos-EDU/soffos.package.git@22.9.20.13.12.33
```

### How do I create a new package release?

1. Go to the package's repo;
1. Click "releases";
1. Click "Draft a new release";
1. Click "Choose a tag";
   1. For the tag, enter whatever is the current version number of the package (look at `setup.py`).
   For example: `22.10.5.10.55.28`.
1. Click "Publish Release".

## Repo Structure.

### Unit Tests

The unit tests are contained in the `tests` directory. Tests are ignored when pip installing the
soffos package.

### Requirements

All required packages should be specified in the `requirements.txt` file. These will be
auto-installed when installing the soffos package.

### Package

Everything you wish included in the soffos package should be contained in the `soffos` directory.
NOTE: that soffos package has a special folder called `data`. Here is where you should put any
resource files (non-python) you wish to be included in the pip install. For example, a file called
`stopwords.json`. There is some code in `setup.py` that walks through the directory and includes all
the files contained within.
