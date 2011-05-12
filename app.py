import cherrypy
import schemaish, validatish, formish
from server import build_request


class app(object):


    def __init__(self, openerp):
        self.openerp = openerp


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
        # Edit form configuration
        SHOWN_FIELDS = ['name', 'email', 'ean13']
        OPENERP_RESSOURCE = 'res.partner'

        # Parse and clean-up URL parameters
        try: 
            res_id = int(id)
        except TypeError:
            res_id = None

        # If required parameters are not there, redirect to the base app
        if res_id is None:
            # Redirect to Partner's list
            raise cherrypy.HTTPRedirect('/')

        # Get the ressource we're going to edit and its fields
        ooop_res_name = 'ResPartner'
        ressource = getattr(self.openerp, ooop_res_name).get(res_id)
        fields = getattr(ressource, 'fields')

        # Set the default list of fields to show in the form
        shown_fields = SHOWN_FIELDS
        # If no fields are specified, show all
        if not len(shown_fields):
            shown_fields = fields.keys()
 
        # Generate Formish's schema based on OpenERP data model
        schema = schemaish.Structure()
        # Always add the current ressource ID
        schema.add('res_id', schemaish.Integer())
        # Generate an automattic form schema
        for f_id in shown_fields:
            
            f_struct = fields[f_id]
            f_type = f_struct['ttype']

            # OpenERP's type to Formish's schema type mapping
            field_type_mapping = { 'char'      : 'String'
                                 , 'boolean'   : 'Boolean'
                                 , 'date'      : 'Date'
                                 #, 'float'    : 'Float'
                                 #, XXX        : 'Integer'
                                 #, XXX        : 'Decimal'
                                 #, XXX        : 'Time'
                                 #, XXX        : 'Sequence'
                                 #, XXX        : 'Tuple'
                                 #, XXX        : 'DateTime'
                                 #, XXX        : 'File'
                                 #, 'selection': XXX
                                 #, 'many2one' : XXX
                                 #, 'one2many' : XXX
                                 #, 'many2many': XXX
                                 }

            # Create in Schemaish an alter-ego to OpenERP field
            f_type = f_struct['ttype']
            if f_type not in field_type_mapping:
                # Ignore unknown OpenERP types
                break
            s_class = getattr(schemaish, field_type_mapping[f_type])

            # OpenERP's field properties to Schemaish's fields properties
            field_property_mapping = { 'string'  : {'property': 'title'}
                                     , 'help'    : {'property': 'description'}
                                     #, '': 'validator'
                                     #, '': 'default'
                                     , 'required': {'validator': 'Required'}
                                     , 'size'    : {'validator': 'Length', 'param': 'max'}
                                     }

            # Migrate schema properties from OpenERP to Schemaish
            s_props = {}
            for (f_prop_id, s_prop) in field_property_mapping.items():
                 if f_prop_id in f_struct.keys():
                      f_value = f_struct[f_prop_id]
                      # This field property translates to a native property
                      if 'property' in s_prop.keys():
                          s_props[s_prop['property']] = f_value
                      # This field property translates to a validator
                      elif 'validator' in s_prop.keys():
                          v_class = getattr(validatish, s_prop['validator'])
                          v_param = {}
                          if 'param' in s_prop.keys():
                              v_param[s_prop['param']] = f_value
                          s_props['validator'] = v_class(**v_param)

            # Add the field to the schema
            s = s_class(**s_props)
            schema.add(f_id, s)

        # Build the form
        form = formish.Form(schema, '%s_form' % ooop_res_name)
        form['res_id'].widget = formish.Hidden()
        
        # Get current OpenERP's object values and set them as form's defaults
        form.defaults = {'res_id': res_id}
        for f_id in shown_fields:
            f_value = getattr(ressource, f_id)
            f_type = fields[f_id]['ttype']
            if f_type == 'char' and f_value is False:
                f_value = ''
            form.defaults[f_id] = f_value

        # Get the HTTP method
        http_method = cherrypy.request.method.upper()
        # Process Partner's data sent by the user
        if http_method == 'POST':
            try:
                form_data = form.validate(build_request(kwargs))
                # Do not try to update our ressource ID
                del form_data['res_id']
            except formish.FormError, e:
                form_data = {}
            # Update values if necessary
            object_updated = False
            for (property_name, new_value) in form_data.items():
                if getattr(ressource, property_name) != new_value:
                    setattr(ressource, property_name, new_value)
                    object_updated = True
            if object_updated:
                ressource.save()

        # Print the default edit form
        return { 'form': form
               , 'id'  : res_id
               }

