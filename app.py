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
        SHOWN_FIELDS = ['name', 'email', 'ean13', 'supplier']
        SHOWN_FIELDS = []
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
            # Format: {'openerp_type': ('schemaish_type', [default_validator_1, default_validator_2])}
            field_type_mapping = { 'char'      : {'t': 'String' , 'v_list': [{'validator_name': 'String'}]}
                                 , 'boolean'   : {'t': 'Boolean', 'v_list': []}
                                 , 'date'      : {'t': 'Date'   , 'v_list': []}
                                 , 'float'     : {'t': 'Float'  , 'v_list': [{'validator_name': 'Number'}]}
                                 #, XXX        : {'t': 'Integer', 'v_list': [{'validator_name': 'Integer'}]}
                                 #, XXX        : {'t': 'Decimal', 'v_list': [{'validator_name': 'Number'}]}
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
                continue
            s_class = getattr(schemaish, field_type_mapping[f_type]['t'])

            # OpenERP's field properties to Schemaish's fields properties
            field_property_mapping = { 'string'  : {'property_name': 'title'}
                                     , 'help'    : {'property_name': 'description'}
                                     #, '': 'default'
                                     , 'required': {'validator_name': 'Required'}
                                     , 'size'    : {'validator_name': 'Length', 'param_name': 'max'}
                                     }

            # Migrate schema properties from OpenERP to Schemaish
            s = {'validator_list': field_type_mapping[f_type]['v_list']}
            for (f_prop_id, s_prop) in field_property_mapping.items():
                 if f_prop_id in f_struct.keys():
                      f_value = f_struct[f_prop_id]
                      # This field property translates to a native property
                      if 'property_name' in s_prop.keys():
                          s[s_prop['property_name']] = f_value
                      # This field property translates to a validator
                      elif 'validator_name' in s_prop.keys():
                          updated_validator = s_prop
                          if 'param_name' in s_prop.keys():
                              updated_validator['param_value'] = f_value
                          s['validator_list'] = s['validator_list'] + [updated_validator]

            # Add some special validators in some cases
            if f_id == 'website':
                s['validator_list'] = s['validator_list'] + [{'validator_name': 'URL', 'param_name': 'with_scheme', 'param_value': True}]
            elif f_id == 'email':
                s['validator_list'] = s['validator_list'] + [{'validator_name': 'Email'}]

            # Collapse all validators into a compound one
            validator_object_list = []
            for v in s['validator_list']:
                v_param = {}
                if 'param_name' in v.keys():
                    v_param[v['param_name']] = v['param_value']
                v_class = getattr(validatish, v['validator_name'])
                validator_object_list.append(v_class(**v_param))
            del s['validator_list']
            s['validator'] = validatish.All(*validator_object_list)
            # Add the field to the schema
            schema.add(f_id, s_class(**s))

        # Build the form
        form = formish.Form(schema, '%s_form' % ooop_res_name)
        form['res_id'].widget = formish.Hidden()
        
        # Get current OpenERP's object values and set them as form's defaults
        form.defaults = {'res_id': res_id}
        for f_id in shown_fields:
            # Set default widget type
            f_type = fields[f_id]['ttype']
            if f_type == 'boolean':
                form[f_id].widget = formish.Checkbox()
            elif f_type == 'date':
                form[f_id].widget = formish.DateParts(day_first=True)
            # Set default widget value
            f_value = getattr(ressource, f_id)
            if f_type == 'char' and f_value is False:
                f_value = ''
            elif f_type == 'date' and f_value is False:
                f_value = None
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

