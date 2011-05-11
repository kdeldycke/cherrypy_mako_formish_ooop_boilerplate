### Some global variables
CONF_NAME         = 'server.conf'
LIB_DIRNAME       = 'lib'
TEMPLATES_DIRNAME = 'templates'
DEBUG             = True


# Import all stuff we need
import os
import sys
import cherrypy
from mako.template import Template
from mako.lookup   import TemplateLookup
import schemaish, validatish, formish
from pkg_resources import resource_filename


# Import the local copy of the OOOP module
current_folder = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(current_folder, LIB_DIRNAME, 'ooop'))
from ooop import OOOP



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

    def __call__(self, filename, directories=[TEMPLATES_DIRNAME], module_directory=None,
                 collection_size=-1, output_encoding='utf-8', encoding_errors='replace'):
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
                                    output_encoding=output_encoding,
                                    encoding_errors=encoding_errors)
            self.lookups[key] = lookup
        cherrypy.request.lookup = lookup
        # Replace the current handler.
        cherrypy.request.template = t = lookup.get_template(filename)
        cherrypy.request.handler = MakoHandler(t, cherrypy.request.handler)



def main():
    # Here is the default config for statix content
    conf = { '/static': { 'tools.staticdir.on' : True
                        , 'tools.staticdir.dir': os.path.join(current_folder, 'static')
                        }
           , '/favicon.png': { 'tools.staticfile.on'      : True
                             , 'tools.staticfile.filename': os.path.join(current_folder, 'static/favicon.png')
                             }
           }
    # Load and apply the global config file
    conf_file = os.path.join(current_folder, CONF_NAME)
    cherrypy.config.update(conf_file)
    # Only show default error page and traceback in debug mode
    if not DEBUG:
        cherrypy.config.update({ 'error_page.default'     : os.path.join(current_folder, 'static/error.html')
                               , 'request.show_tracebacks': False
                               })
    # Open a connection to our local OpenERP instance
    # Some doc: http://www.slideshare.net/raimonesteve/connecting-your-python-app-to-openerp-through-ooop
    openerp = OOOP( user   = 'admin'
                  , pwd    = 'admin'
                  , dbname = 'kev_test'
                  , uri    = 'http://localhost'
                  , port   = 8069 # We are targetting the HTTP web service here
                  )
    # Setup our Mako decorator
    loader = MakoLoader()
    cherrypy.tools.mako = cherrypy.Tool('on_start_resource', loader)
    # Import our application logic
    from app import app
    # Start the CherryPy server
    cherrypy.quickstart(app(openerp), config=conf)



if __name__ == '__main__':
    main()

