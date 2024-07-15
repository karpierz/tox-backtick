# Copyright (c) 2023 Damien Nadé
# Copyright (c) 2024 Adam Karpierz
# SPDX-License-Identifier: LGPL-2.1-or-later

"""A tox plugin that allows backquote expansion in set_env section.
"""

from .__about__ import * ; del __about__  # noqa

from tox.config.sets import EnvConfigSet
from tox.plugin import impl
from tox.session.state import State
from tox.tox_env.api import ToxEnv

from .backquote import SHELL, has_backticks, \
    eval_backquote, set_env_backquote_items
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
    set_env.update({var: eval_backquote(tox_env, cmd, var)
                    for var, cmd in set_env_backquote_items(set_env)})
