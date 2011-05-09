### Some global variables
CONF_NAME         = 'server.conf'
LIB_DIRNAME       = 'lib'
TEMPLATES_DIRNAME = 'templates'


# Import all stuff we need
import os
import sys
import cherrypy

# Init Mako template parser and some of its utilities
from mako.template import Template
from mako.lookup   import TemplateLookup
lookup = TemplateLookup( directories     = [TEMPLATES_DIRNAME]
                       , output_encoding = 'utf-8'
                       , encoding_errors = 'replace'
                       )

# Import the local copy of the OOOP module
current_folder = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(current_folder, LIB_DIRNAME, 'ooop'))
from ooop import OOOP



class WebPublisher(object):

    @cherrypy.expose
    def index(self):
        # Let's get some info from a demo OpenERP instance
        # Some doc on OOOP: http://www.slideshare.net/raimonesteve/connecting-your-python-app-to-openerp-through-ooop
        o = OOOP( user   = 'admin'
                , pwd    = 'admin'
                , dbname = 'kev_test'
                , uri    = 'http://localhost'
                , port   = 8069 # We are targetting the HTTP web service here
                )
        partner_names = [p.name for p in o.ResPartner.all()]
        t = lookup.get_template("index.html")
        return t.render(partner_names=partner_names)



def main():
    conf_file = os.path.join(current_folder, CONF_NAME)
    cherrypy.quickstart(WebPublisher(), config=conf_file)



if __name__ == '__main__':
    main()

