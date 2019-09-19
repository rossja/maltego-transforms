# Maltego Transforms

A collection of local transforms for Maltego. 
In general, these are written in Python, and use the [Maltego TRX Library](https://github.com/paterva/maltego-trx)

## Usage

Since we're using the Maltego TRX library, we have access to the `project.py` provided by Paterva.
This lets us run transforms directly from the command line, and set up a debug-mode transform server (among other things)

Since that's the case, here's some useful commands:

### List the available transforms:

This can be done by calling the `list` function:

~~~shell
$ python3 project.py list
= Transform Server URLs =
/run/dorkgithubrsakey/: DorkGithubRsaKey


= Local Transform Names =
dorkgithubrsakey: DorkGithubRsaKey
~~~

### Run a local transform from the command line:

To run a transform, you need to call the transform by name (obtained by running the `list` command).
You also need to pass in any parameters the script requires, and provide a set of parameters that can be mapped back by the Maltego TRX response object. All this really means is you need to pass in some params to the transforms, like so:

~~~shell
$ python3 project.py local dorkgithubrsakey "bank" "field1=field1 value#field2=field2 value"
~~~

The above will run the transform named `dorkgithubrsakey`, which we can see in the list maps to the DorkGithubRsaKey class. This class requires a search term, which in the example above is the string `bank`. It also needs to have some values and fields for the response object, which are provided in the second parameter.

## Running a Debug-Mode Transform Server

You can run a debug mode transform server by using the `runserver` function. This will start up a flask application that provides mappings to the transforms available:

~~~shell
$ python3 project.py runserver

=== Maltego Transform Server: v1.3.4 ===

= Transform Server URLs =
/run/dorkgithubrsakey/: DorkGithubRsaKey


= Local Transform Names =
dorkgithubrsakey: DorkGithubRsaKey


 * Serving Flask app "maltego_trx.server" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
INFO:werkzeug: * Running on http://0.0.0.0:8080/ (Press CTRL+C to quit)
INFO:werkzeug: * Restarting with stat

=== Maltego Transform Server: v1.3.4 ===

= Transform Server URLs =
/run/dorkgithubrsakey/: DorkGithubRsaKey


= Local Transform Names =
dorkgithubrsakey: DorkGithubRsaKey


WARNING:werkzeug: * Debugger is active!
INFO:werkzeug: * Debugger PIN: 133-700-303
~~~