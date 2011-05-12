import cherrypy
from openerp_tools import OpenERPTools


class app(OpenERPTools):


    @cherrypy.expose
    @cherrypy.tools.mako(filename="index.html")
    def index(self):
        partners = [(p.id, p.name) for p in self.openerp.ResPartner.all()]
        return {'partners': partners}


    @cherrypy.expose
    @cherrypy.tools.mako(filename="view.html")
    def view(self, partner_id=None):
        partner_id = self.validate_openerp_id(partner_id)
        partner = self.openerp.ResPartner.get(partner_id)
        return { 'name' : partner.name
               , 'id'   : partner_id
               , 'email': partner.email or 'Not set'
               }


    @cherrypy.expose
    @cherrypy.tools.mako(filename="edit.html")
    def edit(self, id=None, *args, **kwargs):
        res_id = self.validate_openerp_id(id)
        form = self.openerp_edit_form( ressource_type = 'res.partner'
                                     , res_id = res_id
                                     , fields = ['name', 'email', 'ean13', 'supplier']
                                     , kwargs = kwargs
                                     )
        return { 'form': form
               , 'id'  : res_id
               }

