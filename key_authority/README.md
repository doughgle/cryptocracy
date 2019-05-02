# Key Authority Service

From the `key-authority` sub-directory, execute the `flask` command:

```bash
key_authority$ flask
Usage: flask [OPTIONS] COMMAND [ARGS]...

  A general utility script for Flask applications.

  Provides commands from Flask, extensions, and the application. Loads the
  application defined in the FLASK_APP environment variable, or from a
  wsgi.py file. Setting the FLASK_ENV environment variable to 'development'
  will enable debug mode.

    $ export FLASK_APP=hello.py
    $ export FLASK_ENV=development
    $ flask run

Options:
  --version  Show the flask version
  --help     Show this message and exit.

Commands:
  init-db  Drop and re-create all tables.
  routes   Show the routes for the app.
  run      Runs a development server.
  shell    Runs a shell in the app context.
```

Notice that the sub-command init-db is available.

## Start the server

```bash
key_authority/ka_service$ export FLASK_APP=ka_service
key_authority/ka_service$ export FLASK_ENV=development
key_authority/ka_service$ flask run
 * Serving Flask app "ka_service" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 321-385-633
```
