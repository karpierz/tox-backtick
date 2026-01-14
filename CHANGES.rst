Changelog
=========

2.0.1 (2026-01-10)
------------------
- Fixed compatibility bug for tox version 4.33.0+.
- Bypass shlex usage if command string begins with +
- Added backtick_no_strip option.
- Added some tests to confirm new behaviour.
- | `All of the above was done thanks to the patch from Steve Hespelt.
    <https://github.com/karpierz/tox-backtick/pull/1>`_
  | Thank you very much, Steve (SteveHespelt@Github) for the patch!
- | Some changes in testing to ensure compatibility with Windows and
  | discontinuation of pytest in favour of unittest only.
- Prepared and marked the package as typed.
- 100% code coverage (also thanks to Steve's tests ;).
- Version number alignment (-> 2.x.x).
- Copyright year update.
- The documentation has been moved from Read the Docs to GitHub Pages.
- Added the 'tool.tox.env.cleanup' test environment.
- Setup update (mainly dependencies) and bug fixes.

0.8.0 (2025-09-01)
------------------
- Made the package typed.
- Setup update (mainly dependencies).

0.6.5 (2025-07-07)
------------------
- Setup update (mainly dependencies).

0.6.4 (2025-06-11)
------------------
- Setup update (mainly dependencies).

0.6.3 (2025-05-15)
------------------
- The distribution is now built using 'build' instead of 'setuptools'.
- Setup update (mainly dependencies) (due to regressions in tox and setuptools).

0.6.1 (2025-05-04)
------------------
- Setup update (mainly dependencies).

0.6.0 (2025-04-28)
------------------
- Added support for Python 3.14
- Dropped support for Python 3.9 (due to compatibility issues).
- Updated Read the Docs' Python version to 3.13
- Updated tox's base_python to version 3.13
- Setup update (mainly dependencies).

0.5.10 (2025-03-21)
-------------------
- Added support for PyPy 3.11
- Dropped support for PyPy 3.9
- Setup update (mainly dependencies).

0.5.9 (2025-03-15)
------------------
- Setup update (mainly dependencies).

0.5.8 (2025-02-14)
------------------
- Setup update (mainly dependencies).

0.5.7 (2025-01-25)
------------------
- Setup update (mainly dependencies).

0.5.6 (2025-01-20)
------------------
- Copyright year update.
- Setup update (mainly dependencies).

0.5.5 (2024-12-13)
------------------
- Source distribution (\*.tar.gz now) is compliant with PEP-0625.
- Setup update (mainly dependencies).

0.5.4 (2024-11-13)
------------------
- 100% code linting.
- Tox configuration is now in native (toml) format.
- Setup update (mainly dependencies).

0.5.1 (2024-10-09)
------------------
- Dropped support for Python 3.8
- Setup update (mainly dependencies).

0.4.6 (2024-08-13)
------------------
- Added support for Python 3.13
- Corrected licence information in README.rst
- Setup update (mainly dependencies).

0.4.4 (2024-01-26)
------------------
- Cleanup.

0.4.1 (2024-01-24)
------------------
- First functional release.

0.0.0 (2024-01-22)
------------------
- Initial commit.
