# Copyright (c) 2023 Damien Nadé
# Copyright (c) 2025 Steve Hespelt
# Copyright (c) 2024 Adam Karpierz
# SPDX-License-Identifier: LGPL-2.1-or-later

"""Functions related to backquotes detection and evaluation"""

from typing import TypeAlias, Any
from collections.abc import Callable, Iterator
import sys
import shlex
from pathlib import Path
import logging

from tox.tox_env.api import ToxEnv
from tox.execute.api import StdinSource
from .setenv import set_env_items

EvalFunc: TypeAlias = Callable[[ToxEnv, str, str], str]

log = logging.getLogger(__name__)

if sys.platform.startswith("win32"):
    SHELL = "cmd"
    CMD_SW = "/C"
else:
    SHELL = "bash"
    CMD_SW = "-c"


def eval_cache_decorator(func: EvalFunc) -> EvalFunc:
    """A cache decorator for eval_backquote"""
    cache: dict[Any, str] = {}
    def _function(tox_env: ToxEnv, cmd: str, var: str) -> str:
        key = (tox_env, cmd)
        try:
            result = cache[key]
        except KeyError:
            result = cache[key] = func(tox_env, cmd, var)
        return result
    return _function


def has_backticks(string: str) -> str | None:
    """Returns the string part inside the backquotes.

    If given parameter is a backquote string, then return the part inside
    the backquotes. Else return None, making the function result booleanish.
    """
    if len(string) > 2 and string.startswith('`') and string.endswith('`'):
        return string[1:-1]
    else:
        return None


# @eval_cache_decorator
def eval_backquote(tox_env: ToxEnv, cmd: str, var: str, strip_nl: bool) -> str:
    """Evaluate a command inside a tox environment.

    Because of how bash -c works, we need to provide for using the entire
    text within the backticks as the 1 string used by -c. As this string has
    already been interpolated by tox, somewhat handy when constructing if-then-else
    tests on tox/env variables. See the tests/ for some examples.
    """
    args = [cmd[1:]] if cmd.startswith('+') else [
            (arg[1:-1] if arg.startswith('"') and arg.endswith('"') else arg)
            for arg in shlex.split(cmd, posix=False)]
    outcome = tox_env.execute(cmd=[SHELL, CMD_SW] + args, stdin=StdinSource.OFF,
                              run_id=f"backtick[{var}]", show=False, cwd=Path.cwd())
    log.debug(f"tox-backtick eval_backquote variable: {var}, "
              f"replacement value: {outcome.out}")
    return outcome.out.rstrip("\r\n") if strip_nl else outcome.out


def set_env_backquote_items(self: Any) -> Iterator[tuple[str, str]]:
    for var, value in set_env_items(self):
        if cmd := has_backticks(value):
            yield var, cmd
