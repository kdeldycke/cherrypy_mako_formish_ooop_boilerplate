import cherrypy


class app(object):

    def __init__(self, openerp):
        self.openerp = openerp

    @cherrypy.expose
    @cherrypy.tools.mako(filename="index.html")
    def index(self):
        partner_names = [p.name for p in self.openerp.ResPartner.all()]
        return {'partner_names': partner_names}

    @cherrypy.expose
    # TODO: do not expose this when in production
    def default(self, *args, **kwargs):
        return "<html><body><ul><li>args: <code>%s</code></li><li>kwargs: <code>%s</code></li></ul></body></html>" % (args, kwargs)

