import click


@click.group()
def cli():
    pass


@cli.command('serve')
@click.argument('database')
@click.option('--host', '-h', type=str, nargs=1, default='localhost',
              help="The host to run the app on")
@click.option('--port', '-p', type=int, nargs=1, default=8888,
              help="The port to run the app on")
@click.option('--debug/--no-debug', default=False,
              help="Run the app in debug mode (NOT FOR PRODUCTION)")
def serve_command(database, host, port, debug):
    from .app import app
    app.config['SQLALCHEMY_DATABASE_URI'] = database
    app.run(host=host, port=port, debug=debug)


@cli.command('create')
@click.argument('database')
def create_db_command(database):
    from .app import app, db
    app.config['SQLALCHEMY_DATABASE_URI'] = database
    db.create_all()
