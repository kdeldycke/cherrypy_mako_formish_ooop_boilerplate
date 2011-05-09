import os
import cherrypy

CONF_NAME = 'server.conf'



class HelloWorld(object):
    def index(self):
        return "Hello World!"
    index.exposed = True


if __name__ == '__main__':
    conf_file = os.path.join(os.path.dirname(__file__), CONF_NAME)
    cherrypy.quickstart(HelloWorld(), config=conf_file)

