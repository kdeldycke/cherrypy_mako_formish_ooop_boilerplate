import cherrypy
import schemaish, validatish, formish
import webob
from dottedish.api import dotted, flatten
from urllib import urlencode



class app(object):


    def __init__(self, openerp):
        self.openerp = openerp


    def build_request(self, data, rawdata=False):
        """ Copied from formish/tests/testish/testish/lib/forms.py
        """
        e = {'REQUEST_METHOD': 'POST'}
        request = webob.Request.blank('/', environ=e)
        fields = []
        if rawdata is True:
            for d in data:
                fields.append(d)
        else:
            d = dotted(data)
            for k, v in flatten(d):
                fields.append((k, v))
        request.body = urlencode(fields)
        return request


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
    def edit(self, partner_id=None, *args, **kwargs):

        # Parse and clean-up URL parameters
        try: 
            partner_id = int(partner_id)
        except TypeError:
            partner_id = None

        # If required parameters are not there, redirect to the base app
        if partner_id is None:
            # Redirect to Partner's list
            raise cherrypy.HTTPRedirect('/')

        # Get partner's data
        partner = self.openerp.ResPartner.get(partner_id)

        # Define the edit form and its constraints
        schema = schemaish.Structure()
        schema.add('id'   , schemaish.Integer())
        schema.add('name' , schemaish.String(title='Partner name'  , validator=validatish.Required()))
        schema.add('email', schemaish.String(title='Partner E-mail', validator=validatish.Email()))
        form = formish.Form(schema, 'partner_edit_form')
        form['id'].widget = formish.Hidden()
        form.defaults = { 'name' : partner.name
                        , 'id'   : partner.id
                        , 'email': partner.email or ''
                        }

        # Get the HTTP method
        http_method = cherrypy.request.method.upper()
        # Process Partner's data sent by the user
        if http_method == 'POST':
            try:
                form_data = form.validate(self.build_request(kwargs))
            except formish.FormError, e:
                form_data = {}
            # Update values if necessary
            object_updated = False
            for (property_name, new_value) in form_data.items():
                if getattr(partner, property_name) != new_value:
                    setattr(partner, property_name, new_value)
                    object_updated = True
            if object_updated:
                partner.save()

        # Print the default edit form
        return { 'form': form
               , 'id'  : partner_id
               }

