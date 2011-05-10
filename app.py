import cherrypy


class app(object):

    def __init__(self, openerp):
        self.openerp = openerp

    @cherrypy.expose
    def index(self):
        partner_names = [p.name for p in self.openerp.ResPartner.all()]
        return {'partner_names': partner_names}

