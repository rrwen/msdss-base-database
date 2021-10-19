# Developer Notes for msdss-base-database

Richard Wen  
rrwen.dev@gmail.com

## Install

Setup and install a development environment:

1. Install [git](https://git-scm.com/)
2. Install [Anaconda Python 3](https://www.anaconda.com/distribution/)
3. Install [GraphViz](https://www.graphviz.org/)
4. Clone this repository `git clone`
5. Move to the cloned folder `cd msdss-base-database`
6. Install python dependencies with `bin\install.bat` or `bin/install.sh`

In Mac OS (with [Homebrew](https://brew.sh/) installed):

```
brew install git graphviz -y
git clone https://www.github.com/rrwen/msdss-base-database
cd msdss-base-database
chmod +x bin/install.sh
source bin/install.sh
```

In Linux (Ubuntu):

```
apt install git graphviz -y
git clone https://www.github.com/rrwen/msdss-base-database
cd msdss-base-database
chmod +x bin/install.sh
source bin/install.sh
```

In Windows (with [Chocolatey](https://chocolatey.org/) installed):

```
choco install git graphviz -y
git clone https://www.github.com/rrwen/msdss-base-database
cd msdss-base-database
bin\install
```

## Virtual Python Environment

A [conda environment](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-with-commands) will also be created with `bin/install`, which installs the environment defined by `env.yml`.

If you are opening a new terminal, you will need to use `bin/activate` to activate the environment.

In Linux/Mac OS:

```
source bin/activate.sh
```

In Windows:

```
bin\activate
```

**Note**: The environment exists inside the `tmp/` folder.

## Package Management

The package can be reinstalled or uninstalled locally using the scripts in the `bin` folder.

This is particularly useful when you add or remove package dependencies in `setup.cfg`.

For example, you may want to run `bin/reinstall_package` after you edit the package dependencies to ensure that all dependencies are met after the changes.

### Reinstalling the package

The package can be reinstalled in your virtual environment by running `bin/reinstall_package`.

In Linux/Mac OS:

```
source bin/reinstall_package.sh
```

In Windows:

```
bin\reinstall_package
```

### Uninstalling the package

The package can be uninstalled from your virtual environment using `bin/uninstall_package`.

In Linux/Mac OS:

```
source bin/uninstall_package.sh
```

In Windows:

```
bin\uninstall_package
```

## Documentation

The documentation is automatically built with [sphinx](http://www.sphinx-doc.org/en/master/).

### Building the documentation

You can build the documentation files into the `docs` folder by running `bin/build_docs`.

In Linux/Mac OS:

```
source bin/build_docs.sh
```

In Windows:

```
bin\build_docs
```

### Rebuilding the documentation

You can also completely rebuild the docs (reinstalling the package, and removing existing documentation) with `bin/rebuild_docs`.

In Linux/Mac OS:

```
source bin/rebuild_docs.sh
```

In Windows:

```
bin\rebuild_docs
```

## Setting up a Test Database

A default [PostgreSQL](https://www.postgresql.org/) database can be setup for testing:

1. Install [PostgreSQL v11+](https://www.postgresql.org/)
2. Enter the `psql` console with your `<user>` and an existing `<database>`
3. Create a user named `msdss`  with password `msdss123` using `CREATE USER`
4. Create a database named `msdss` owned by user `msdss` with `CREATE DATABASE`
5. You can now use the test user `msdss`, password `msdss123`, and database `msdss` for testing purposes

In a command line terminal, enter the `psql` console with:

```
psql -U <user> -d <database>
```

Inside the `psql` console:

```
CREATE USER msdss WITH PASSWORD 'msdss123';
CREATE DATABASE msdss WITH OWNER msdss;
```

Exit the `psql` console with:

```
\q
```

**Note**: Do not use this database in production or outside of your local network as it is strictly for development purposes only

## Publishing to the Python Package Index (PyPi)

When the package is ready, you can publish it to [PyPi](https://pypi.org/) so that it is publicly available and `pip` installable:

1. Remove any existing version builds in the `dist/` folder
2. Build the current package distribution files in `dist/` with `setup.py sdist`
3. Upload the package to PyPi with `twine`
4. You will be prompted for your user name and password on PyPi
5. Your package should be available at https://pypi.org/project/msdss-base-database

In Linux/Mac OS:

```
rm -rf dist
python setup.py sdist
twine upload dist/*
```

In Windows:

```
rmdir /s /q dist\
python setup.py sdist
twine upload dist/*
```

**Note**: You will need to a registered account on [PyPi](https://pypi.org/) to publish packages.