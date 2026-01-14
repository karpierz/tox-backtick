# Copyright (c) 2025 Steve Hespelt
# Copyright (c) 2024 Adam Karpierz
# SPDX-License-Identifier: LGPL-2.1-or-later

from unittest import TestCase
import sys
import os
import shutil
import subprocess
import tempfile
from textwrap import dedent

from iniconfig import IniConfig

from tox.session.cmd.run.parallel import ENV_VAR_KEY as TOX_PARALLEL_ENV


class ToxTestCase(TestCase):
    """A TestCase for testing tox configs. 99% 'borrowed' from tox_factor.

    This class creates a temporary directory, writing the provided contents to
    the tox config file. The `.config` attribute contains the parsed ini config.

    The test case also provides the `.tox_call()` method for calling tox with
    the config, and `.tox_envlist()`, which is useful for testing the expected
    env list.

    Note that the test case doesn't change the working directory or environment.

    Attributes:
        ini_contents: The contents that will be written to the tox config. This
            must be set by a test case subclass.
        ini_filename: The file name to write the tox config contents to. This
            defaults to 'tox.ini'.
        ini_filepath: The full path of the temporary tox config file. This is
            generated during the test case class setup.
        config: The parsed ini tox config. This is created during the test case
            class setup.
        setup_contents: The contents that will be written to the package setup
            module.
        setup_filepath: The full path of the temporary setup module. This is
            generated during the test case class setup.
    """

    ini_contents = None
    ini_filename = "tox.ini"
    tox_workdir  = ".tox_tests"

    setup_contents = None

    @classmethod
    def setUpClass(cls):
        super(ToxTestCase, cls).setUpClass()

        assert cls.ini_contents is not None, (
            "`{cls.__module__}.{cls.__name__}.ini_contents` has not been set."
            .format(cls=cls))

        # We can't use the `TemporaryDirectory` context manager since the setup
        # functions do not wrap the execution of the `test_*` methods. The
        # directory would have been deleted before the tests are even ran.
        cls._temp_dir = tempfile.mkdtemp()
        cls.ini_filepath = os.path.join(cls._temp_dir, cls.ini_filename)

        with open(cls.ini_filepath, "w") as ini_file:
            ini_file.write(dedent(cls.ini_contents))

        cls.config = IniConfig(cls.ini_filepath)

        # Create package setup module
        cls.setup_filepath = os.path.join(cls._temp_dir, "setup.py")
        if cls.setup_contents is not None:
            with open(cls.setup_filepath, "w") as setup_file:
                setup_file.write(dedent(cls.setup_contents))

    @classmethod
    def tearDownClass(cls):
        del cls.config
        shutil.rmtree(cls._temp_dir)
        super(ToxTestCase, cls).tearDownClass()

    def tox_call(self, *arguments):
        base = (sys.executable, "-m", "tox",
                "--conf", self.ini_filepath, "--workdir", self.tox_workdir)
        return self._tox_call(*base, *arguments)

    def _tox_call(self, *arguments):
        # Remove TOX_PARALLEL_ENV from the subprocess environment variables.
        # See: https://github.com/tox-dev/tox/issues/1275
        env = os.environ.copy()
        env.pop(TOX_PARALLEL_ENV, None)

        proc = subprocess.Popen(
            arguments, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
        stdout, stderr = proc.communicate()

        return proc.returncode, stdout.decode("utf-8"), stderr.decode("utf-8")

    def tox_envlist(self, arguments=None):
        arguments = arguments or []
        returncode, stdout, stderr = self.tox_call("-l",  *arguments)

        self.assertEqual(returncode, 0, stderr)

        return [env for env in stdout.strip().splitlines()]
