from flask import render_template, send_from_directory

from ._app import app


@app.route("/")
def index():
    """ The landing page """
    return render_template("index.html")


@app.route("/css/<path:css_path>")
def css_route(css_path):
    """ A basic route to send static css.

    This should be moved to nginx before you deploy!
    """
    return send_from_directory('css', css_path)


@app.route("/js/<path:js_path>")
def js_route(js_path):
    """ A basic route to send static js.

    This should be moved to nginx before you deploy!
    """
    return send_from_directory('js', js_path)
