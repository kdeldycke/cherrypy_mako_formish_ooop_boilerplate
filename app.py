import cherrypy


class app(object):

    def __init__(self, openerp):
        self.openerp = openerp

    @cherrypy.expose
    @cherrypy.tools.mako(filename="index.html")
    def index(self):
        partners = [(p.id, p.name) for p in self.openerp.ResPartner.all()]
        return {'partners': partners}

    @cherrypy.expose
    # TODO: do not expose this when in production
    def default(self, *args, **kwargs):
        return "<html><body><ul><li>args: <code>%s</code></li><li>kwargs: <code>%s</code></li></ul></body></html>" % (args, kwargs)

    @cherrypy.expose
    @cherrypy.tools.mako(filename="view.html")
    def view(self, partner_id=None):
        partner_id = int(partner_id)
        partner = self.openerp.ResPartner.get(partner_id)
        return { 'name' : partner.name
               , 'id'   : partner_id
               , 'email': partner.email
               }

