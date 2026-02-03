"""
Smoke tests for the CLI module.

These tests ensure that the CLI module and its main
entry functions can be imported without errors.
No interactive input is tested here.
"""

def test_cli_module_imports():
    """
    CLI module should be importable without raising exceptions.
    """
    import cli.cli  # noqa: F401


def test_run_cli_function_exists():
    """
    run_cli function should exist in the CLI module.
    """
    from cli.cli import run_cli

    assert callable(run_cli)
