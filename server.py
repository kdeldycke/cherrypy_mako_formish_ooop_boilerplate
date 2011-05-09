import os
import sys
import cherrypy

# Import the local copy of the OOOP module
current_folder = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(current_folder, 'lib', 'ooop'))
from ooop import OOOP



CONF_NAME = 'server.conf'



class HelloWorld(object):
    def index(self):
        html = "Hello World!"
        return html
        
    index.exposed = True



if __name__ == '__main__':
    conf_file = os.path.join(current_folder, CONF_NAME)
    cherrypy.quickstart(HelloWorld(), config=conf_file)

