# Copyright (c) 2023 Damien Nadé
# Copyright (c) 2025 Steve Hespelt
# Copyright (c) 2024 Adam Karpierz
# SPDX-License-Identifier: LGPL-2.1-or-later

"""A tox plugin that allows backquote expansion in set_env section."""

from .__about__ import * ; del __about__  # type: ignore[name-defined]  # noqa

from tox.config.cli.parser import ToxParser
from tox.config.sets import EnvConfigSet
from tox.plugin import impl
from tox.session.state import State
from tox.tox_env.api import ToxEnv

from .backquote import (SHELL, has_backticks,
    eval_backquote, set_env_backquote_items)
from .setenv import set_env_items


@impl
def tox_add_env_config(env_conf: EnvConfigSet, state: State) -> None:
    """Post process config after parsing."""
    # pylint: disable=unused-argument
    set_env = env_conf["set_env"]
    for _, value in set_env_items(set_env):
        if has_backticks(value):
            # Add bash in order to be able to evaluate backquotes.
            env_conf["allowlist_externals"].append(SHELL)
            return


@impl
def tox_before_run_commands(tox_env: ToxEnv) -> None:
    """Eval and replace backquotes expressions"""
    set_env = tox_env.conf["set_env"]
    dont_strip_nl = (tox_env.options.backtick_no_strip
                     if "backtick_no_strip" in tox_env.options else False)
    set_env.update({var: eval_backquote(tox_env, cmd, var, not dont_strip_nl)
                    for var, cmd in set_env_backquote_items(set_env)})


@impl
def tox_add_option(parser: ToxParser) -> None:
    # have to get the parser for commands that need evaluations of set_env backticks ?
    for cmd in ("run", "exec", "run-parallel", "legacy"):
        run_parser = parser.handlers[cmd]
        if run_parser:
            run_parser[0].add_argument(
                "--backtick-no-strip",  # default is to strip out the \n\r chars
                action="store_true",
                help="do not strip out LF, CR characters from backtick results",
                dest="backtick_no_strip"
            )
