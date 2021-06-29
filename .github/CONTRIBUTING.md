# Contributing Guide

Its great to see your here!

- You need to first fork and clone the project to start working on it.
Always work on a new branch, and open a PR to the `main` branch.
Keep the `main` branch of your fork in sync with the origin.
If you are a GitHub beginner, and wondering how to do the above stuff,
then please read [GitHub's documentation](https://docs.github.com/en/get-started/quickstart/fork-a-repo).

- This project uses `poetry` for package management.
It is very simple and intuitive to use.
This guide will show you how to setup your project environment.
If you dont have poetry [install it](https://python-poetry.org/docs/#installation).

- Move into your cloned project directory and run the following commands.

    ```shell
    poetry config virtualenvs.in-project true
    poetry install
    ```

- The virtual environment will be created in a `.venv` folder
inside your project directory.
In your code editor set the python interpretor path to `./.venv/bin/python`

- Activate `poetry` shell.

    ```shell
    poetry shell
    ```

- Setup pre-commit hooks.

    ```shell
    pre-commit install
    ```

- Common commands that you will be running.

    ```shell
    make fmt # format your code, and sort your imports
    make clean # delete python cache and other such stuff
    pre-commit run -a # run pre-commit hooks for all files
    pre-commit run # run pre-commit hooks only for staged changes
    poetry show --tree # see the dependency graph for the project
    pytest # run tests and see the code coverage
    # after running pytest open htmlcov/index.html to see coverage report
    ```

To work on this project you must have some knowledge of Selenium.
An idea about different tools such as pre-commit, tox, black etc will be helpful.
To know more about something, just google search and go through the official docs.
