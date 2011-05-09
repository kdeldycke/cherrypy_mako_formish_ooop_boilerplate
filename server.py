import cherrypy

cherrypy.config.update({'server.socket_host': '127.0.0.1',
                        'server.socket_port': 8081,
                       })

class HelloWorld(object):
    def index(self):
        return "Hello World!"
    index.exposed = True

cherrypy.quickstart(HelloWorld())
