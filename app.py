import cherrypy
import schemaish, validatish, formish
from openerp_tools import OpenERPTools


class app(OpenERPTools):


    @cherrypy.expose
    # TODO: do not expose this when in production
    def default(self, *args, **kwargs):
        return "<html><body><ul><li>args: <code>%s</code></li><li>kwargs: <code>%s</code></li></ul></body></html>" % (args, kwargs)


    @cherrypy.expose
    @cherrypy.tools.mako(filename="index.html")
    def index(self):
        partners = [(p.id, p.name) for p in self.openerp.ResPartner.all()]
        return {'partners': partners}


    @cherrypy.expose
    @cherrypy.tools.mako(filename="view.html")
    def view(self, partner_id=None):
        partner_id = int(partner_id)
        partner = self.openerp.ResPartner.get(partner_id)
        return { 'name' : partner.name
               , 'id'   : partner_id
               , 'email': partner.email or 'Not set'
               }


    @cherrypy.expose
    @cherrypy.tools.mako(filename="edit.html")
    def edit(self, id=None, *args, **kwargs):
        # Parse and clean-up URL parameters
        try:
            res_id = int(id)
        except TypeError:
            res_id = None

        # If required parameters are not there, redirect to the base app
        if res_id is None:
            # Redirect to Partner's list
            raise cherrypy.HTTPRedirect('/')
        
        form = self.openerp_edit_form( ressource_type = 'res.partner'
                                     , res_id = res_id
                                     , fields = ['name', 'email', 'ean13', 'supplier']
                                     , kwargs = kwargs
                                     )

        # Print the default edit form
        return { 'form': form
               , 'id'  : res_id
               }

