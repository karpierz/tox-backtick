# Copyright (c) 2025 Steve Hespelt
# Copyright (c) 2024 Adam Karpierz
# SPDX-License-Identifier: LGPL-2.1-or-later

import unittest
import sys
import os
import re
import shutil

from .test import ToxTestCase


class ToxTestCaseTests(unittest.TestCase):

    def test_error_message(self):
        class Dummy(ToxTestCase):
            pass

        with self.assertRaises(AssertionError) as excinfo:
            Dummy.setUpClass()

        self.assertEqual(
            str(excinfo.exception),
            "`tests.test_plugin.Dummy.ini_contents` has not been set.",
        )

    def test_tox_envlist(self):
        class Dummy(ToxTestCase):
            ini_contents = r"""
            [tox]
            envlist = py39,py312

            [testenv:lint]
            """

            def runTest(self):
                # fixes a Python 2 compatibility issue when instantiating a
                # test case outside of a test suite
                pass  # pragma: no cover

        testcase = Dummy()

        try:
            testcase.setUpClass()
            envlist = testcase.tox_envlist()
        finally:
            testcase.tearDownClass()

        # by default, tox does not list testenvs not present in `envlist`.
        self.assertEqual(envlist, ["py39", "py312"])

    def test_tox_call(self):
        class Dummy(ToxTestCase):
            ini_contents = r"""
            [testenv:lint]
            commands = {env_python} -c "print('clean')"
            """
            setup_contents = """
            from setuptools import setup

            setup(name='test')
            """

            def runTest(self):
                # fixes a Python 2 compatibility issue when instantiating a
                # test case outside of a test suite
                pass  # pragma: no cover

        testcase = Dummy()

        try:
            testcase.setUpClass()
            returncode, stdout, stderr = testcase.tox_call("run", "-e", "lint")
        finally:
            testcase.tearDownClass()

        self.assertEqual(returncode, 0)
        self.assertIn("lint: OK", stdout)

    def test_tox_call_no_setup_module(self):
        class Dummy(ToxTestCase):
            ini_contents = r"""
            [testenv:lint]
            commands = {env_python} -c "print('clean')"
            """

            def runTest(self):
                # fixes a Python 2 compatibility issue when instantiating a
                # test case outside of a test suite
                pass  # pragma: no cover

        testcase = Dummy()

        try:
            testcase.setUpClass()
            returncode, stdout, stderr = testcase.tox_call("run", "-e", "lint")
        finally:
            testcase.tearDownClass()

        self.assertEqual(returncode, 0)
        self.assertIn("lint: OK", stdout)


    def test_argument_present(self):
        class Dummy(ToxTestCase):
            ini_contents = r"""
            [testenv:lint]
            commands = {env_python} -c "print('clean')"
            """
            setup_contents = """
            from setuptools import setup

            setup(name='test')
            """

            def runTest(self):
                # fixes a Python 2 compatibility issue when instantiating a
                # test case outside of a test suite
                pass  # pragma: no cover

        testcase = Dummy()

        try:
            testcase.setUpClass()
            returncode, stdout, stderr = testcase.tox_call("run", "--help")
        finally:
            testcase.tearDownClass()

        self.assertEqual(returncode, 0)
        self.assertIn("--backtick-no-strip", stdout)

    @unittest.skipIf(sys.platform == "win32" and not shutil.which("bash.exe"),
                     "This test is skipped on Windows because bash.exe is unavailable!")
    def test_backtick_simple1(self):
        class Dummy(ToxTestCase):
            ini_contents = r"""
            [testenv:lint]
            set_env=TODAY=`bash -c /bin/date`
            commands = {env_python} -c "print('TODAY: \{0}'.format('{env:TODAY:no-date-set}'))"
            """
            setup_contents = """
            from setuptools import setup

            setup(name='test')
            """

            def runTest(self):
                # fixes a Python 2 compatibility issue when instantiating a
                # test case outside of a test suite
                pass  # pragma: no cover

        testcase = Dummy()

        try:
            testcase.setUpClass()
            returncode, stdout, stderr = testcase.tox_call("run", "-e", "lint")
        finally:
            testcase.tearDownClass()

        self.assertEqual(returncode, 0)
        # a date-like string detected >= 2025-07-01
        date_re = r"TODAY.*(AM|PM).* 2[0-1]\d{2}"
        match = re.search(date_re, stdout)
        self.assertIsNotNone(match, f"Expected date-like string in output: "
                                    f"{stdout} because of backtick evaluation.")

    @unittest.skipIf(sys.platform == "win32" and not shutil.which("bash.exe"),
                     "This test is skipped on Windows because bash.exe is unavailable!")
    def test_backtick_not_stripped(self):
        class Dummy(ToxTestCase):
            ini_contents = r"""
            [testenv:lint]
            set_env=TODAY=`bash -c /bin/date`
            commands = {env_python} -c "print('TODAY: \{0} NEXT LINE'.format('{env:TODAY:no-date-set}'))"
            """
            setup_contents = """
            from setuptools import setup

            setup(name='test')
            """

            def runTest(self):
                # fixes a Python 2 compatibility issue when instantiating a
                # test case outside of a test suite
                pass  # pragma: no cover

        testcase = Dummy()

        try:
            testcase.setUpClass()
            # because of the preservaction of newline chars in the backtick
            # evaluation output, there will be parsing errors
            returncode, stdout, stderr = testcase.tox_call("run", "--backtick-no-strip", "-e", "lint")
        finally:
            testcase.tearDownClass()

        self.assertNotEqual(returncode, 0)
        self.assertIn("unterminated string literal", stderr)

    # Ugh. Can't seemingly parametrize just 1 test method in a class, so we
    # have to use a separate test method.
    @unittest.skipIf(sys.platform == "win32" and not shutil.which("bash.exe"),
                     "This test is skipped on Windows because bash.exe is unavailable!")
    def test_backtick_literal_not_stripped(self):
        """
        Test that backtick evaluation uses the entire string as a literal due to the leading + character
        :return:
        """
        class Dummy(ToxTestCase):
            ini_contents = r"""
            [testenv:lint]
            set_env=TEST1=`+bash -c 'if [ "$VAR_NOT_SET" != "NONE" ] ; then echo 30 ; else echo 5 ; fi'`
            commands = {env_python} -c "print('TEST1:\{0}VALUE'.format('{env:TEST1:0}'))"
            """

            setup_contents = """
            from setuptools import setup

            setup(name='test')
            """

            def runTest(self):
                # fixes a Python 2 compatibility issue when instantiating a
                # test case outside of a test suite
                pass  # pragma: no cover

        testcase = Dummy()

        try:
            testcase.setUpClass()
            os.environ.pop("VAR_NOT_SET", None)
            returncode, stdout, stderr = testcase.tox_call("run", "-e", "lint", "--backtick-no-strip")
        finally:
            testcase.tearDownClass()

        self.assertEqual(returncode, 1, f"Expected return code {1} but got {returncode}. "
                                        f"stdout: {stdout}, stderr: {stderr}")
        self.assertIn("unterminated string literal", stderr)

    @unittest.skipIf(sys.platform == "win32" and not shutil.which("bash.exe"),
                     "This test is skipped on Windows because bash.exe is unavailable!")
    def test_backtick_literal_stripped(self):
        """
        Test that backtick evaluation uses the entire string as a literal due to the leading + character
        :return:
        """
        class Dummy(ToxTestCase):
            ini_contents = r"""
            [testenv:lint]
            set_env=TEST1=`+bash -c 'if [ "$VAR_NOT_SET" != "NONE" ] ; then echo 30 ; else echo 5 ; fi'`
            commands = {env_python} -c "print('TEST1:\{0}VALUE'.format('{env:TEST1:0}'))"
            """

            setup_contents = """
            from setuptools import setup

            setup(name='test')
            """

            def runTest(self):
                # fixes a Python 2 compatibility issue when instantiating a
                # test case outside of a test suite
                pass  # pragma: no cover

        testcase = Dummy()

        try:
            testcase.setUpClass()
            os.environ.pop("VAR_NOT_SET", None)
            #  default action is to strip NL, CR from any backtick output
            returncode, stdout, stderr = testcase.tox_call("run", "-e", "lint")
        finally:
            testcase.tearDownClass()

        self.assertEqual(returncode, 0, f"Expected return code {0} but got {returncode}. "
                                        f"stdout: {stdout}, stderr: {stderr}")
        self.assertIn("TEST1:30", stdout)
        match = re.search(r"TEST1:30VALUE", stdout)  # did the newline get stripped
        self.assertIsNotNone(match, f"Expected TEST1:30VALUE with no NL, CR chars "
                                    f"at the end of backtick output: {stdout}")
