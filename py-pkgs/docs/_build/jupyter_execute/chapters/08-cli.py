(08-cli)=
# Packages with a Command Line Interface

Many Python packages include a command line interface (CLI) - that is, functionality you can access directly from the command line, without having to start up a Python session. The `cookiecutter` tool weve used throughout this book is one such example. CLIs can help users more effectivaly interact with your software, are often easier to use with virtual machines, and can make it easier to automate processes via scripting. Luckily, it's quite easy to configure Python packages to include a CLI, especially if you're using the `poetry` package manager tool. In this chapter, we'll walk through setting up a very simple Python Package that includes a CLI.

(08-cli-structure)=
## CLI Package Structure

As we've seen throughout this book, Python packages follow a standard structure and you can quickly set this structure up using the [UBC-MDS cookiecutter template](https://github.com/UBC-MDS/cookiecutter-ubc-mds) and `poetry`:

```bash
$ cookiecutter https://github.com/UBC-MDS/cookiecutter-ubc-mds.git
$ poetry init
```

```{tip}
If you're unfamiliar with the `cookiecutter` + `poetry` workflow, go back and check out the chapter {ref}`02-whole-game`.
```

With these two commands, you end up with a structure that looks something like this:

```bash
pypkgs
├── CONDUCT.rst
├── CONTRIBUTING.rst
├── CONTRIBUTORS.rst
├── docs
├── pypkgs
│   ├── __init__.py
│   └── pypkgs.py
├── .gitignore
├── LICENSE
├── pyproject.toml
├── .readthedocs.yml
├── README.md
└── tests
    ├── __init__.py
    └── test_pypkgs.py
```

We will continue to build off the `pypkgs` package we've developed throughout this book, but the instructions below will generalise to any package. To create a basic CLI for our package, there's not too much more we have to do to this structure! First, we need to add a script that will contain our CLI code. Let's go ahead and do that now by adding a new Python module called `cli.py` to the `pypkgs` subdirectory now, so that our directory structure becomes:

```bash
pypkgs
├── CONDUCT.rst
├── CONTRIBUTING.rst
├── CONTRIBUTORS.rst
├── docs
├── pypkgs
│   ├── __init__.py
│   ├── cli.py  #  <-- We added our script here!
│   └── pypkgs.py
├── .gitignore
├── LICENSE
├── pyproject.toml
├── .readthedocs.yml
├── README.md
└── tests
    ├── __init__.py
    └── test_pypkgs.py
```

```{note}
You can call your CLI script anything you like, and put it anywhere in your package directory that you like, but the set up shown above is  common.
```

While our CLI module is empty for now, let's go ahead and configure `poetry` to incorporate the CLI into our future package build. All we need to do is give our CLI an alias and point `poetry` to the location of the code we want to run when that alias is used at the CL. To do this, we need to add the following in the `pyproject.toml` file:

```
[tool.poetry.scripts]
pypkgs = "pypkgs.cli:main"
```

This syntax points `poetry` to executable scripts that should be installed when your package is being installed. In our case, we are pointing the the `cli.py` module and the `main()` function within it (which doesn't exist yet but we'll create it shortly). You can read more about this configuration in the [`poetry` documentation](https://python-poetry.org/docs/pyproject/#scripts). The `pypkgs` on the left of the equals sign is the alias you will use to access your CLI, e.g., we will be able to type at the CL `$ pypkgs <args>`. You can call it anything you like, it doesn't have to be the same as your package name, but it should typically be short and sweet! In the next section we'll build up the syntax and code to actually create a working CLI.

```{hint}
If you're using `Setuptools` isntead of `poetry` to develop your package, the CLI configuration can be a little more involved, check out [this documentation](https://python-packaging.readthedocs.io/en/latest/command-line-scripts.html#command-line-scripts) to learn more. 
```

(08-cli-tools)=
## CLI Tools and Code

There are many ways to set up your `cli.py` script, I'm going to show, what in my opinion, is the simplest here. Go ahead and open up `cli.py` in an editor of your choice. Let's first make sure that everything is working by creating a `main()` function (this could be called anything, but we'll call it main here and have specified that in `pyproject.toml`) in `cli.py` by adding the following text into the file:

```python
def main():
    print("Coming to you from the command line!")
```

Now, we can re-install our package and test it by using our previously specified CLI alias of `pypkgs`:

```bash
$ poetry install
$ pypkgs
Coming to you from the command line!
```

Great, looks like everything is working so far. But we are going to want to create more complicated CLIs than this, in particular, CLIs that can accept arguments! There are many tools available to help build Python CLI's, popular ones include:

- [`argparse`](https://docs.python.org/3/library/argparse.html) (part of the Python standard library)
- [`click`](https://click.palletsprojects.com/en/7.x/)
- [`docopt`](http://docopt.org/)
- [`fire`](https://google.github.io/python-fire/guide/)

All of these different packages share the same goal - to turn Python code into a CLI. Here, we'll be using `argparse` because it is part of the Python standard library and is easy and intuitive to use for simple CLIs. 

The goal of this chapter is not to teach the syntax of `argparse` (which the [official `argparse` documenation](https://docs.python.org/3/library/argparse.html#module-argparse) does an excellent job of already). Rather, here we wish to show how easy it is to incorporate a CLI into your Python package. We will leverage a simple CLI example from the [official `argparse` documenation](https://docs.python.org/3/library/argparse.html#module-argparse) that takes in a list of numbers and provides either the sum or the max of those numbers based on the command given.

To create this functionality, simply copy-paste the following code into `cli.py` and we'll then walk through it step-by-step:

```
import argparse


def main():
    args = parse_args()
    print(args.accumulate(args.integers))


def parse_args():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('integers', metavar='N', type=int, nargs='+',
                        help='an integer for the accumulator')
    parser.add_argument('--sum', dest='accumulate', action='store_const',
                        const=sum, default=max,
                        help='sum the integers (default: find the max)')
    return parser.parse_args()

```

In the code above, the first thing we are doing is importing the `argparse` module which we will use to help parse CL arguments. We then have our `main()` function, which is the function that will be called when we execute our package CLI with the alias `pypks`. The way `poetry` and Python CLIs currently work, we can't pass argument directly to this function, so instead, we define another function `parse_args()` to parse any CL arguments, and this is called within `main()`. 

As for the `parse_args()` function, it contains a bunch of `argparse`-specific syntax for creating an object that can parse CL arguments. Briefly, the first line (`parser = ...`) sets up the parsing object which will hold all the information necessary to parse the command line into Python data types. We then add two passable arguments, the first is "integers", which must be of type `int` and can accept any arbitrary number of integers from the CL. The second argument is "--sum", this is an optional argument which returns the sum of the passed integers, otherwise the maximum of the passed integers is returned. In addition, all `argparse` object come with an optional help argument (specified with `-h` or `--help`), which will return a summary of all possible CL arguments and their help description (if provided). Check out the [documentation](https://docs.python.org/3/library/argparse.html#module-argparse) for a more comprehensive walkthrough of this example.

We can test out our brand new CL by re-installing our package and checking the help documentation:

```
$ poetry install
$ pypkgs --help
usage: pypkgs [-h] [--sum] N [N ...]

Process some integers.

positional arguments:
  N           an integer for the accumulator

optional arguments:
  -h, --help  show this help message and exit
  --sum       sum the integers (default: find the max)
```

It seems to be working! Let's see if we can calculate the maximum and the sum of a set of integers:

```
$ pypkgs 1 2 3 4 5
5
$ pypkgs --sum 1 2 3 4 5
16
```

Awesome! We've implemented a basic CLI here to show how this functionality can be accommodated in Python packages. You can check out a more complicated Python package CLI, called [`PyWebCat`](https://github.com/UNCG-DAISY/PyWebCAT), that I wrote to interface with some open-source coastal video footage, following the above guidelines and structure. I also encourage you to take a look at the CLIs of any larger, open-source Python packages you use (like [`cookiecutter`](https://github.com/cookiecutter/cookiecutter) for example) to better understand how to write effective CLIs.