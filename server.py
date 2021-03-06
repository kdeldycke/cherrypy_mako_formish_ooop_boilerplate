# coding=UTF-8

### Some global variables
CONF_NAME         = 'server.conf'
LIB_DIRNAME       = 'lib'
TEMPLATES_DIRNAME = 'templates'
DEBUG             = True


# Import all stuff we need
import os
import sys
import socket
import cherrypy
import datetime
from mako.template import Template
from mako.lookup   import TemplateLookup
import schemaish, validatish, formish
from formish.renderer import _default_renderer
from pkg_resources import resource_filename

# Import the local copy of the OOOP module
current_folder = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(current_folder, LIB_DIRNAME, 'ooop'))
from ooop import OOOP

# Transform relative path to absolute
template_folder = os.path.join(current_folder, TEMPLATES_DIRNAME)



class MakoHandler(cherrypy.dispatch.LateParamPageHandler):
    """ Callable which sets response.body.
        Source: http://tools.cherrypy.org/wiki/Mako
    """

    def __init__(self, template, next_handler):
        self.template = template
        self.next_handler = next_handler

    def __call__(self):
        env = globals().copy()
        env.update(self.next_handler())
        return self.template.render(**env)



class MakoLoader(object):

    def __init__(self):
        self.lookups = {}

    def __call__(self, filename, directories=[template_folder], module_directory=None,
                 collection_size=-1, output_encoding='utf-8', input_encoding='utf-8',
                 encoding_errors='replace'):
        # Always add formish's Mako templates
        directories.append(resource_filename('formish', 'templates/mako'))
        # Find the appropriate template lookup.
        key = (tuple(directories), module_directory)
        try:
            lookup = self.lookups[key]
        except KeyError:
            lookup = TemplateLookup(directories=directories,
                                    module_directory=module_directory,
                                    collection_size=collection_size,
                                    input_encoding=input_encoding,
                                    output_encoding=output_encoding,
                                    encoding_errors=encoding_errors)
            self.lookups[key] = lookup
        cherrypy.request.lookup = lookup
        # Replace the current handler.
        cherrypy.request.template = t = lookup.get_template(filename)
        cherrypy.request.handler = MakoHandler(t, cherrypy.request.handler)



def redirect_home_on_error(status, message, traceback, version):
    """ Callable to redirect to home page on any HTTP error
    """
    home_url = "http://www.example.com"
    # This is an ugly intermediate page to go back to the parent app and escape from the iframe we supposed to be in.
    return """
            <html>
                <body onload="window.top.location.href = '%s';">
                    <h1>Redirecting to the parent website...</h1>
                </body>
            </html>
        """ % home_url



def main():
    # Here is the default config for statix content
    conf = { '/static': { 'tools.staticdir.on' : True
                        , 'tools.staticdir.dir': os.path.join(current_folder, 'static')
                        }
           , '/static/formish.css': { 'tools.staticfile.on'      : True
                                    , 'tools.staticfile.filename': resource_filename('formish', 'css/formish.css')
                                    }
           , '/static/formish.js' : { 'tools.staticfile.on'      : True
                                    , 'tools.staticfile.filename': resource_filename('formish', 'js/formish.js')
                                    }
           , '/favicon.png'       : { 'tools.staticfile.on'      : True
                                    , 'tools.staticfile.filename': os.path.join(current_folder, 'static/favicon.png')
                                    }
           }

    # Desactivate encoding to bypass CherryPy 3.2 new defaults (see: http://www.cherrypy.org/wiki/UpgradeTo32#Responseencoding)
    cherrypy.config.update({'tools.encode.on': False})

    # Load and apply the global config file
    conf_file = os.path.join(current_folder, CONF_NAME)
    cherrypy.config.update(conf_file)

    # Only show default error page and traceback in debug mode
    if DEBUG:
        cherrypy.config.update({'autoreload.on': True})
    else:
        cherrypy.config.update({ 'autoreload.on'          : False
                               , 'request.show_tracebacks': False
                               , 'error_page.default'     : os.path.join(current_folder, 'static/error.html')
                               # Alternatively, we can call a method to handle generic HTTP errors
                               #, 'error_page.default'     : redirect_home_on_error
                               # Treat 503 connectivity errors as maintenance
                               , 'error_page.503'         : os.path.join(current_folder, 'static/maintenance.html')
                               })

    # Monkey patch convertish to let it unfold multiple checkbox widgets encoded with dottedish
    from convertish.convert import NumberToStringConverter
    from dottedish.dottedlist import DottedList, unwrap_list
    legacy_to_type = NumberToStringConverter.to_type
    def to_type_wrapper(self_class, value, converter_options={}):
        # Force decoding of dotted notation
        if type(value) == DottedList:
            value = unwrap_list(value)
            if type(value) == type([]) and len(value) == 1:
                value = value[0]
        return legacy_to_type(self_class, value, converter_options)
    NumberToStringConverter.to_type = to_type_wrapper

    from convertish.convert import DateToStringConverter
    # Monkey patch convertish again, but this time to parse our french-localized dates
    legacy_parseDate = DateToStringConverter.parseDate
    def parseDate_wrapper(self_class, value):
        return legacy_parseDate(self_class, '-'.join(value.strip().split('/')[::-1]))
    DateToStringConverter.parseDate = parseDate_wrapper
    # This patch mirror the one above, to let convertish render our datetime object with our localized format
    def from_type_replacement(self_class, value, converter_options={}):
        return value is None and None or value.strftime('%d/%m/%Y')
    DateToStringConverter.from_type = from_type_replacement

    # Open a connection to our local OpenERP instance
    try:
        openerp = OOOP( user   = 'admin'
                    , pwd    = 'admin'
                    , dbname = 'kev_test'
                    , uri    = 'http://localhost'
                    , port   = 8069 # We are targetting the HTTP web service here
                    )
    except (socket.timeout, socket.error):
        raise cherrypy.HTTPError(503)

    # Setup our Mako decorator
    loader = MakoLoader()
    cherrypy.tools.mako = cherrypy.Tool('on_start_resource', loader)

    # Let the default formish Mako renderer look at our local directory fisrt
    # This let us ovveride default formish Mako templates
    _default_renderer.lookup.directories.insert(0, template_folder)

    # Import our application logic
    from app import app

    # Start the CherryPy server
    cherrypy.quickstart(app(openerp), config=conf)



if __name__ == '__main__':
    main()

