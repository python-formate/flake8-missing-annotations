===========================
flake8-missing-annotations
===========================

.. start short_desc

**Experimental Flake8 plugin to identify missing or incomplete argument annotations.**

.. end short_desc

This plugin identifies functions like this, where one or more annotations is missing:

.. code-block:: python

	def foo(a, b, c: int):
		pass


For functions whose names start with ``test_``, it ignores common pytest fixtures which have no easy annotation
(e.g. ``monkeypatch``, ``capsys``).
It also ignores missing return types for those functions, since the return type is almost always unimportant.

See `sco1/flake8-annotations <https://github.com/sco1/flake8-annotations>`_
for a plugin with a broader scope than this one.

.. start shields

.. list-table::
	:stub-columns: 1
	:widths: 10 90

	* - Tests
	  - |actions_linux| |actions_windows| |actions_macos|
	* - Activity
	  - |commits-latest| |commits-since| |maintained|
	* - QA
	  - |codefactor| |actions_flake8| |actions_mypy|
	* - Other
	  - |license| |language| |requires|

.. |actions_linux| image:: https://github.com/python-formate/flake8-missing-annotations/workflows/Linux/badge.svg
	:target: https://github.com/python-formate/flake8-missing-annotations/actions?query=workflow%3A%22Linux%22
	:alt: Linux Test Status

.. |actions_windows| image:: https://github.com/python-formate/flake8-missing-annotations/workflows/Windows/badge.svg
	:target: https://github.com/python-formate/flake8-missing-annotations/actions?query=workflow%3A%22Windows%22
	:alt: Windows Test Status

.. |actions_macos| image:: https://github.com/python-formate/flake8-missing-annotations/workflows/macOS/badge.svg
	:target: https://github.com/python-formate/flake8-missing-annotations/actions?query=workflow%3A%22macOS%22
	:alt: macOS Test Status

.. |actions_flake8| image:: https://github.com/python-formate/flake8-missing-annotations/workflows/Flake8/badge.svg
	:target: https://github.com/python-formate/flake8-missing-annotations/actions?query=workflow%3A%22Flake8%22
	:alt: Flake8 Status

.. |actions_mypy| image:: https://github.com/python-formate/flake8-missing-annotations/workflows/mypy/badge.svg
	:target: https://github.com/python-formate/flake8-missing-annotations/actions?query=workflow%3A%22mypy%22
	:alt: mypy status

.. |requires| image:: https://dependency-dash.repo-helper.uk/github/python-formate/flake8-missing-annotations/badge.svg
	:target: https://dependency-dash.repo-helper.uk/github/python-formate/flake8-missing-annotations/
	:alt: Requirements Status

.. |codefactor| image:: https://img.shields.io/codefactor/grade/github/python-formate/flake8-missing-annotations?logo=codefactor
	:target: https://www.codefactor.io/repository/github/python-formate/flake8-missing-annotations
	:alt: CodeFactor Grade

.. |license| image:: https://img.shields.io/github/license/python-formate/flake8-missing-annotations
	:target: https://github.com/python-formate/flake8-missing-annotations/blob/master/LICENSE
	:alt: License

.. |language| image:: https://img.shields.io/github/languages/top/python-formate/flake8-missing-annotations
	:alt: GitHub top language

.. |commits-since| image:: https://img.shields.io/github/commits-since/python-formate/flake8-missing-annotations/v0.0.0
	:target: https://github.com/python-formate/flake8-missing-annotations/pulse
	:alt: GitHub commits since tagged version

.. |commits-latest| image:: https://img.shields.io/github/last-commit/python-formate/flake8-missing-annotations
	:target: https://github.com/python-formate/flake8-missing-annotations/commit/master
	:alt: GitHub last commit

.. |maintained| image:: https://img.shields.io/maintenance/yes/2025
	:alt: Maintenance

.. end shields

Installation
--------------

.. start installation

``flake8-missing-annotations`` can be installed from GitHub.

To install with ``pip``:

.. code-block:: bash

	$ python -m pip install git+https://github.com/python-formate/flake8-missing-annotations

.. end installation
