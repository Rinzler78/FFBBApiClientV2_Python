============
Contributing
============

Welcome to the ``ffbb_api_client_v2`` contributor's guide.

This document covers the development workflow, conventions, and processes
for contributing to the project. All contributions — code, docs, tests,
bug reports — are appreciated.

All users and contributors are expected to be **open, considerate,
reasonable, and respectful**. When in doubt, the `Python Software
Foundation's Code of Conduct`_ is a good reference.


Issue Reports
=============

If you experience bugs or general issues with ``ffbb_api_client_v2``,
please check the `issue tracker`_. If you don't find anything useful
there, feel free to open a new issue.

New issue reports should include:

- Your operating system and Python version
- Steps to reproduce the problem (minimal example preferred)
- Expected vs. actual behavior


Development Setup
=================

1. Clone the repository::

    git clone https://github.com/Rinzler78/FFBBApiClientV2_Python.git
    cd FFBBApiClientV2_Python

2. Create and activate a virtual environment::

    python3 -m venv .venv
    source .venv/bin/activate

3. Install the package in editable mode with test dependencies::

    pip install -e ".[testing]"

4. Install pre-commit hooks (format, lint, commit message validation)::

    pip install pre-commit
    pre-commit install
    pre-commit install --hook-type commit-msg

5. Verify your setup::

    pytest tests/ -x -q -n auto


Code Contributions
==================

Branch Workflow
---------------

This project follows **Git Flow**:

- ``master`` — production branch (releases only)
- ``develop`` — integration branch
- ``feature/<name>`` — feature branches (branch from ``develop``)
- ``release/v<X.Y.Z>`` — release branches
- ``hotfix/<name>`` — hotfix branches

**Rules:**

- Never push directly to ``master`` or ``develop``
- Always create a Pull Request targeting ``develop``
- Keep branches short-lived and focused

Implement Your Changes
----------------------

1. Create a feature branch from ``develop``::

    git checkout develop
    git pull origin develop
    git checkout -b feature/my-feature

2. Make your changes. Add tests for new functionality.

3. Run the test suite::

    pytest tests/ -x -q -n auto

   Or use tox for a full check::

    tox

4. Commit using `Conventional Commits`_ format::

    git commit -m "feat(client): add new search endpoint"

   Common prefixes: ``feat``, ``fix``, ``docs``, ``test``, ``refactor``,
   ``chore``, ``perf``, ``ci``, ``build``.

   The ``commitizen`` pre-commit hook validates your commit message
   automatically.

5. Push and open a Pull Request::

    git push -u origin feature/my-feature

   Then open a PR targeting ``develop`` on GitHub.


Running Tests
-------------

.. code-block:: bash

    # Unit tests with parallel execution
    pytest tests/ -x -q -n auto

    # With coverage report
    pytest tests/ --cov=ffbb_api_client_v2 --cov-branch -q

    # Full tox run (lint + tests + build)
    tox


Documentation
=============

Documentation is built with Sphinx_ and lives in the ``docs/`` directory.
Source files use reStructuredText_.

To build the docs locally::

    tox -e docs
    python3 -m http.server --directory docs/_build/html


Maintainer Tasks
================

Releases
--------

1. Create a release branch from ``develop``::

    git checkout -b release/v1.5.0 develop

2. Update ``CHANGELOG.md`` (move Unreleased items to the new version).

3. Merge into ``master`` via PR, then tag::

    git tag -a v1.5.0 -m "Release v1.5.0"
    git push origin v1.5.0

4. CI automatically publishes to PyPI and creates a GitHub Release.

5. Merge ``master`` back into ``develop``.


.. _issue tracker: https://github.com/Rinzler78/FFBBApiClientV2_Python/issues
.. _Conventional Commits: https://www.conventionalcommits.org/
.. _Python Software Foundation's Code of Conduct: https://www.python.org/psf/conduct/
.. _Sphinx: https://www.sphinx-doc.org/en/master/
.. _reStructuredText: https://www.sphinx-doc.org/en/master/usage/restructuredtext/
