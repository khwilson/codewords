# Codewords

A simple implementation of the game Codewords

## Installation instructions

To run, you should be able to pip install this:

```
pip install .
crun serve --host localhost --port 12345
```

and then open up a web browser at `http://localhost:12345`

## WSGI Instructions

This app is structured as a Flask app. The Flask app itself is a WSGI
app, you just need to write the wrapper (e.g., for use with gunicorn).
Search teh googlez for instructions.
