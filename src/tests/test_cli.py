import pytest


def test_cli_invoke(bare_app):
    @bare_app.cli.command('hello')
    def hello_command():
        click.echo('Hello, World!')

    runner = bare_app.test_cli_runner()
    # invoke with command name
    result = runner.invoke(args=['hello'])
    assert 'Hello' in result.output
    # invoke with command object
    result = runner.invoke(hello_command)
    assert 'Hello' in result.output
