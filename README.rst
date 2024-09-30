tox-backtick
============

Backticks tox plugin for tox v.4.x.x.

Overview
========

|package_bold| is a strict fork of Damien Nadé's tox-backtocks_ package
(v.0.4.0) with a fixes allowing to work on Python 3.8 or higher and on
Windows with a little code reformatting and minor improvements.

`PyPI record`_.

`Documentation`_.

Overview below is a copy from the original tox-backtocks_ README.md:

tox-backtocks
-------------

|PyPI version| |Supported Python Version| |License| |PyPI - Downloads|

A refreshed backticks tox plugin

This is a very early stage release. Use it at your own risks.

Here’s the roadmap to 1.0 release and our current status:

-  \[x\] define a ``backquote var`` in ``set_env`` with a
       ``backquoted expression`` (and nothing else) and evaluate it
       through bash, inside the tox virtual environment.
-  \[x\] Make of a ``backquote var`` usable in commands section.
-  \[x\] Allow another variable to be referenced inside the
       ``backquoted expression``
-  \[x\] Strip the trailing newline characters of the
       ``backquoted expression``
-  \[ \] Allow user configure the evaluation of ``backquote expression``
       to be with a shell or not (either fork the command directly, either
       fork a shell and evaluate a possible-complex shell expression)
-  \[ \] Allow a ``backquote var`` value to contain regular string parts
       and a ``backquote expression``
-  \[ \] Allow a ``backquote var`` value to contain more than one
       ``backquote expression``
-  \[ \] Allow user to configure if we should strip the trailing newline
       characters or not.
-  \[x\] Allow another variable to reuse the evaluated
       ``backquoted expression``
-  \[x\] Allow another variable to reuse the evaluated
       ``backquoted expression`` without reevaluating it :) (I mean,
       it’s hacked, but heh, better than nothing)
-  \[x\] If evaluating through a shell, automatically add said shell to
       ``allowlist_externals`` section
-  \[x\] Have a working package
-  \[ \] Write user documentation

.. |PyPI version| image:: https://img.shields.io/pypi/v/tox-backtocks?logo=pypi&style=plastic
   :target: https://pypi.org/project/tox-backtocks/
.. |Supported Python Version| image:: https://img.shields.io/pypi/pyversions/tox-backtocks?logo=python&style=plastic
   :target: https://pypi.org/project/tox-backtocks/
.. |License| image:: https://img.shields.io/pypi/l/tox-backtocks?color=green&logo=GNU&style=plastic
   :target: https://github.com/Anvil/tox-backtocks/blob/main/LICENSE
.. |PyPI - Downloads| image:: https://img.shields.io/pypi/dm/tox-backtocks?color=magenta&style=plastic
   :target: https://pypistats.org/packages/tox-backtocks

Usage
-----

TBD...

Installation
============

Prerequisites:

+ Python 3.9 or higher

  * https://www.python.org/

+ pip and setuptools

  * https://pypi.org/project/pip/
  * https://pypi.org/project/setuptools/

To install run:

  .. parsed-literal::

    python -m pip install --upgrade |package|

Development
===========

Prerequisites:

+ Development is strictly based on *tox*. To install it run::

    python -m pip install --upgrade tox

Visit `Development page`_.

Installation from sources:

clone the sources:

  .. parsed-literal::

    git clone |respository| |package|

and run:

  .. parsed-literal::

    python -m pip install ./|package|

or on development mode:

  .. parsed-literal::

    python -m pip install --editable ./|package|

License
=======

  | |copyright|
  | Copyright (c) 2023 Damien Nadé
  | Licensed under the LGPL-2.1-or-later License
  | https://opensource.org/license/lgpl-2-1
  | Please refer to the accompanying LICENSE file.

Authors
=======

* Damien Nadé <anvil.github+tox-backtocks@livna.org>
* Adam Karpierz <adam@karpierz.net>

.. |package| replace:: tox-backtick
.. |package_bold| replace:: **tox-backtick**
.. |copyright| replace:: Copyright (c) 2024-2024 Adam Karpierz
.. |respository| replace:: https://github.com/karpierz/tox-backtick.git
.. _Development page: https://github.com/karpierz/tox-backtick
.. _PyPI record: https://pypi.org/project/tox-backtick/
.. _Documentation: https://tox-backtick.readthedocs.io/
.. _tox-backtocks: https://pypi.org/project/tox-backtocks/
