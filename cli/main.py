import click
from cli.server import server


@click.group()
def cli():
    """
    Manage servers
    """


cli.add_command(server)