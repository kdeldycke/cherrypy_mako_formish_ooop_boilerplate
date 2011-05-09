import os
import sys
import cherrypy

# Import the local copy of the OOOP module
current_folder = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(current_folder, 'lib', 'ooop'))
from ooop import OOOP



CONF_NAME = 'server.conf'



class WebPublishing(object):
    def index(self):
        html = ''
        html += self.header()
        html += "<h1>OpenERP Web Publishing Module</h1>"
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
    cherrypy.quickstart(WebPublishing(), config=conf_file)

