import click


@click.group()
def cli():
    pass


@cli.command('serve')
@click.option('--host', '-h', type=str, nargs=1, default='localhost',
              help="The host to run the app on")
@click.option('--port', '-p', type=int, nargs=1, default=8888,
              help="The port to run the app on")
@click.option('--debug/--no-debug', default=False,
              help="Run the app in debug mode (NOT FOR PRODUCTION)")
def serve_command(host, port, debug):
    from .app import app
    app.run(host=host, port=port, debug=debug)
