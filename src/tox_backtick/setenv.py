# Copyright (c) 2023 Damien Nadé
# Copyright (c) 2024 Adam Karpierz
# SPDX-License-Identifier: LGPL-2.1-or-later

"""Things I'd like to add to tox itself"""

from typing import Tuple, Iterator

from tox.config.loader.api import ConfigLoadArgs
from tox.config.set_env import SetEnv

# pylint: disable=protected-access


def set_env_items(self: SetEnv) -> Iterator[Tuple[str, str]]:
    """Yield var _and_ value of a SetEnv object"""
    # start with the materialized ones, maybe we don't need to materialize the
    # raw ones
    yield from self._materialized.items()
    yield from list(self._raw.items())  # iterating over this may trigger
                                        # materialization and change the dict
    while self._needs_replacement:
        line = self._needs_replacement.pop(0)
        expanded_line = self._replacer(line, ConfigLoadArgs([], self._name, self._env_name))
        sub_raw = dict(self._extract_key_value(sub_line)
                       for sub_line in expanded_line.splitlines()
                       if sub_line)
        self._raw.update(sub_raw)
        yield from sub_raw.items()
