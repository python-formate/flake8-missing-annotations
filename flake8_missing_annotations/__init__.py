#!/usr/bin/env python3
#
#  __init__.py
"""
A Flake8 plugin to identify missing or incomplete argument annotations.
"""
#
#  Copyright © 2022 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#  OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
#  OR OTHER DEALINGS IN THE SOFTWARE.
#

# stdlib
import ast
import textwrap
from typing import Any, Generator, Iterable, List, NamedTuple, Optional, Tuple, Type

# 3rd party
from domdf_python_tools.paths import PathPlus
from domdf_python_tools.typing import PathLike

__all__ = ["AnnotationVisitor", "Error", "Plugin", "check_file", "indent_join"]

__author__: str = "Dominic Davis-Foster"
__copyright__: str = "2022 Dominic Davis-Foster"
__license__: str = "MIT License"
__version__: str = "0.0.0"
__email__: str = "dominic@davis-foster.co.uk"


def indent_join(iterable: Iterable[str]) -> str:
	"""
	Join an iterable of strings with newlines,
	and indent each line with a tab if there is more then one element.

	:param iterable:
	"""  # noqa: D400

	iterable = list(iterable)

	if len(iterable) > 1:
		if iterable[0] != '':
			iterable.insert(0, '')
		return textwrap.indent(textwrap.dedent('\n'.join(iterable)), '\t')

	else:
		return iterable[0]


class Error(NamedTuple):
	"""
	Represents a problematic function.
	"""

	#: The name of the function
	function: str

	#: The problems with the function's annotations.
	offences: Iterable[str]

	# The line the function starts on
	lineno: int

	# The column the function starts on
	col_offset: Optional[int] = None


class Plugin:
	"""
	A Flake8 plugin to identify missing or incomplete argument annotations.

	:param tree: The abstract syntax tree (AST) to check.
	"""

	name: str = __name__
	version: str = __version__  #: The plugin version

	def __init__(self, tree: ast.Module):
		self._tree = tree

	def run(self) -> Generator[Tuple[int, int, str, Type[Any]], None, None]:
		"""
		Run the plugin.

		Yields four-element tuples, consisting of:

		#. The line number of the error.
		#. The column offset of the error.
		#. The error message.
		#. The class of the plugin raising the error.
		"""

		errors = AnnotationVisitor().check_module(self._tree)

		for error in errors:

			offences = list(error.offences)

			missing_return_type = _no_return_annotation in offences
			if missing_return_type:
				offences.remove(_no_return_annotation)

			if offences:
				yield (
						error.lineno,
						error.col_offset or 0,
						f"MAN001 Function {error.function!r}: {indent_join(offences)}",
						type(self),
						)

			if missing_return_type:
				yield (
						error.lineno,
						error.col_offset or 0,
						f"MAN002 Function {error.function!r} {_no_return_annotation}",
						type(self),
						)


pytest_fixture_whitelist = ["monkeypatch", "capsys", "request", "pytestconfig"]

_no_return_annotation = "missing return annotation"


class AnnotationVisitor(ast.NodeVisitor):
	"""
	AST node visitor to identify missing annotations in functions.
	"""

	# modname: Optional[str]

	_state: List[str]
	_errors: List[Error]

	allowed_no_return_type = {
			"__init__",
			"__exit__",
			"__init_subclass__",
			"__new__",
			"setup_module",
			"teardown_module",
			}

	def __init__(self):
		self._reinit()

	def _reinit(self) -> None:
		self._state = []
		self._errors = []

	def check_module(self, node: ast.Module) -> List[Error]:
		"""
		Check the module (as an abstract syntax tree) for missing annotations.

		:param node:

		:return: A list of functions missing annotations.
		"""

		self._reinit()
		super().visit(node)
		errors = self._errors
		self._reinit()
		return errors

	def visit_ClassDef(self, node: ast.ClassDef) -> None:
		"""
		Visit ``class Foo: ...``.

		:param node: The node being visited.
		"""

		self._state.append(node.name)
		self.generic_visit(node)
		self._state.pop(-1)

	def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
		"""
		Visit ``async def foo(): ...``.

		:param node: The node being visited.
		"""

		self._state.append(node.name)
		self.generic_visit(node)
		self._state.pop(-1)

	def visit_FunctionDef(self, function: ast.FunctionDef) -> None:
		"""
		Visit ``def foo(): ...``.

		:param node: The node being visited.
		"""

		args: ast.arguments = function.args
		function_name: str = function.name

		is_test = function_name.startswith("test_")

		offending_arguments = []

		decorators = function.decorator_list
		is_fixture = False
		if decorators:
			for deco in decorators:
				if isinstance(deco, ast.Name):
					if deco.id == "fixture":
						is_fixture = True
				elif isinstance(deco, ast.Attribute):
					if isinstance(deco.value, ast.Name):
						if deco.value.id == "pytest" and deco.attr == "fixture":
							is_fixture = True
				elif isinstance(deco, ast.Call):
					if isinstance(deco.func, ast.Attribute):
						if isinstance(deco.func.value, ast.Name):
							if deco.func.value.id == "pytest" and deco.func.attr == "fixture":
								is_fixture = True

		arg: ast.arg
		for arg in args.args:
			if arg.annotation is None:
				if arg.arg in {"self", "cls"}:
					continue

				if is_test and arg.arg in pytest_fixture_whitelist:
					continue

				elif is_fixture and arg.arg in pytest_fixture_whitelist:
					continue

				elif function_name in {"__exit__"}:
					continue

				offending_arguments.append(f"argument {arg.arg!r} is missing a type annotation")

		if not is_test and function.returns is None and function_name not in self.allowed_no_return_type:
			offending_arguments.append(_no_return_annotation)

		if offending_arguments:
			# if self.modname:
			# 	function_name = f"{self.modname.strip('.')}{function_name}"
			if self._state:
				function_name = '.'.join((*self._state, function_name))

			error = Error(
					function_name,
					offending_arguments,
					function.lineno + len(decorators),
					function.col_offset,
					)
			self._errors.append(error)

		self._state.append(function.name)
		self.generic_visit(function)
		self._state.pop(-1)


def check_file(filename: PathLike) -> int:
	"""
	Check for missing annotations in ``filename``.

	:param filename:
	"""

	cwd = PathPlus.cwd()
	filename = PathPlus(filename)

	tree = ast.parse(filename.read_text())
	errors = AnnotationVisitor().check_module(tree)

	try:
		rel_filename = filename.relative_to(cwd)
	except ValueError:
		rel_filename = filename

	for error in errors:
		print(f"{rel_filename.as_posix()}:{error.lineno}", end='')
		if error.col_offset is not None:
			print(f":{error.col_offset}", end='')
		print(f": Function {error.function!r}: {indent_join(error.offences)}")

	return bool(errors)
