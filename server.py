import os
import sys
import cherrypy

# Import the local copy of the OOOP module
current_folder = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(current_folder, 'lib', 'ooop'))
from ooop import OOOP



CONF_NAME = 'server.conf'



class WebPublisher(object):
    def index(self):
        html = ''
        html += self.header()
        html += "<h1>OpenERP Web Publishing Module</h1>"
        # Let's get some info from a demo OpenERP instance
        # Some doc on OOOP: http://www.slideshare.net/raimonesteve/connecting-your-python-app-to-openerp-through-ooop
        o = OOOP( user   = 'admin'
                , pwd    = 'admin'
                , dbname = 'kev_test'
                , uri    = 'http://localhost'
                , port   = 8069 # We are targetting the HTTP web service here
                )
        html += "<p>Connection to web service established at: %s</p>" % (repr(o).replace('<', '&lt;').replace('>', '&gt;'))
        partners = o.ResPartner.all()
        html += "<ul>"
        for partner in partners:
          html += "<li>%s</li>" % partner.name
        html += "</ul>"
        html += self.footer()
        return html

    def header(self):
        return """<html>
                    <head>
                      <title></title>
                    </head>
                    <body>
               """

    def footer(self):
        return "</body>"

    # Some class config
    index.exposed = True



if __name__ == '__main__':
    conf_file = os.path.join(current_folder, CONF_NAME)
    cherrypy.quickstart(WebPublisher(), config=conf_file)

