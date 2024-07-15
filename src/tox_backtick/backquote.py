# Copyright (c) 2023 Damien Nadé
# Copyright (c) 2024 Adam Karpierz
# SPDX-License-Identifier: LGPL-2.1-or-later

"""Functions related to backquotes detection and evaluation"""


from typing import Any, Optional, Tuple, Callable, Iterator
import sys
import shlex
from pathlib import Path

from tox.tox_env.api import ToxEnv
from tox.execute.api import StdinSource
from .setenv import set_env_items

if sys.platform.startswith("win32"):
    SHELL = "cmd"
    CMD_SW = "/C"
else:
    SHELL = "bash"
    CMD_SW = "-c"

EvalFunc = Callable[[ToxEnv, str, str], str]


def eval_cache_decorator(func: EvalFunc) -> EvalFunc:
    """A cache decorator for eval_backquote"""

    cache: dict[Any, str] = {}

    def _function(tox_env: ToxEnv, cmd: str, var: str) -> str:
        key = (tox_env, cmd)
        try:
            return cache[key]
        except KeyError:
            cache[key] = func(tox_env, cmd, var)
            return cache[key]

    return _function


def has_backticks(string: str) -> Optional[str]:
    """If given parameter is a backquote string, then return the part inside
    the backquotes. Else return None, making the function result booleanish.
    """
    if len(string) > 2 and \
        string.startswith('`') and string.endswith('`'):
        return string[1:-1]
    return None


#@eval_cache_decorator
def eval_backquote(tox_env: ToxEnv, cmd: str, var: str) -> str:
    """Evaluate a command inside a tox environment"""
    args = [(arg[1:-1] if arg.startswith('"') and arg.endswith('"') else arg)
            for arg in shlex.split(cmd, posix=False)]
    outcome = tox_env.execute(cmd=[SHELL, CMD_SW] + args, stdin=StdinSource.OFF,
                              run_id=f"backtick[{var}]", show=False, cwd=Path.cwd())
    return outcome.out.rstrip('\r\n')


def set_env_backquote_items(self) -> Iterator[Tuple[str, str]]:
    for var, value in set_env_items(self):
        if cmd := has_backticks(value):
            yield var, cmd
