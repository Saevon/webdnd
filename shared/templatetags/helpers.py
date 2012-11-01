from django import template
from django.conf import settings

from textwrap import dedent
from pybars import Compiler
import logging
import simplejson
logging = logging.getLogger('templatetags')


register = template.Library()
compiler = Compiler()


##################################################
# Settings Helpers
##################################################
@register.simple_tag
def setting(key, default=None):
    '''
    Outputs the value of the setting directly

    {% setting 'DEBUG' %}
    '''
    return get_setting(key, default)

@register.assignment_tag
def setting_var(key, default=None):
    '''
    Sets a variable to the value of the settings

    {% settings_var 'DEBUG' as debug %}
    '''
    return get_setting(key, default)

def get_setting(key, default=None):
    '''
    Helper to get the settings at the given key, logs warnings when undefined settings
    are used
    '''
    if hasattr(settings, key):
        return getattr(settings, key)
    else:
        logging.warn('Setting not found: "%s"' % key)
    if default is None:
        return ''
    return default


##################################################
# JSON Parsing
##################################################
@register.assignment_tag
def json(string):
    '''
    Json serializes a string turning it into an object

    {% json '{ "json": true }"}' as sample %}
    '''
    return simplejson.loads(string)


##################################################
# Working with Dictionaries
##################################################
class DictKeyNode(template.Node):
    def __init__(self, name, key, val='', drop=False):
        self.name = name
        self.key = key
        self.val = val

        self.drop = drop

    def render(self, context):
        if self.drop:
            context[self.name].pop(self.key)
            return ''

        # Allow . seperated attribute access
        val = self.val.split('.')
        value = context[val[0]]
        for key in val[1:]:
            value = getattr(value, key)

        context[self.name][self.key] = value
        return ''

@register.tag
def set_key(parser, token):
    '''
    Sets a key in a dictionary to the given value (variable)

    {% set_key 'dict' 'key' 'variable.attr' %}
    '''
    try:
        tag_name, name, key, val = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires three arguments" % token.contents.split()[0])
    if not (key[0] == key[-1] and key[0] in ('"', "'")):
        raise template.TemplateSyntaxError("%r tag's key should be in quotes" % tag_name)

    return DictKeyNode(name, key[1:-1], val)

@register.tag
def drop_key(parser, token):
    '''
    Removes a key in a dictionary

    {% drop_key 'dict' 'key' %}
    '''
    try:
        tag_name, name, key = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires two arguments" % token.contents.split()[0])
    if not (key[0] == key[-1] and key[0] in ('"', "'")):
        raise template.TemplateSyntaxError("%r tag's key should be in quotes" % tag_name)

    return DictKeyNode(name, key[1:-1], drop=True)


##################################################
# Templating
##################################################

# Client template helpers
class PointerNode(template.Node):
    '''
    A Node that waits to pass a Context to a ClientTemplateNode
    '''

    def __init__(self, name):
        super(PointerNode, self).__init__()
        self.name = name

    def render(self, context):
        ClientTemplateNode.context(self.name, context)
        return ''


class ClientTemplateNode(template.Node):
    TMPL = dedent("""
        %(templates)s
        <script type="text/javascript">
            Templates = {};
            if (Handlebars.templates !== undefined) {
                Templates = Handlebars.templates;
            }
            %(lines)s
        </script>
    """)

    HTML_TMPL = dedent("""
        <script type="text/x-handlebars-template" id="%(name)s-template">
            %(content)s
        </script>
    """)

    LINE_TMPL = dedent("""
        Templates['%(name)s'] = Handlebars.compile($('#%(name)s-template').html());
    """)

    nodes = {}

    def render(self, context):
        lines = []
        templates = []
        for name in ClientTemplateNode.nodes.keys():
            # Ignore templates that have already been output
            if ClientTemplateNode.nodes[name]['done'] == True:
                continue

            nodes = ClientTemplateNode.nodes[name]['nodelist']
            context = ClientTemplateNode.nodes[name]['context']
            lines.append(ClientTemplateNode.LINE_TMPL % {'name': name})

            templates.append(ClientTemplateNode.HTML_TMPL % {
                'name': name,
                'content': dedent(nodes.render(context))
                    # Change the delims
                    .replace('<@', '{{')
                    .replace('@>', '}}')
                    .replace('\n', '\n' + (4 * ' ')),
            })

            # Check off that this template has been added already
            ClientTemplateNode.nodes[name]['done'] = True

        return (ClientTemplateNode.TMPL % {
            'lines': '\n'.join(lines).replace('\n', '\n' + (4 * ' ')),
            'templates': '\n'.join(templates),
        }).replace('\n', '\n' + (self.indent * ' '))

    @staticmethod
    def add(name, nodelist):
        '''
        Adds another template to the template list
        '''
        ClientTemplateNode.nodes[name] = {
            'done': False,
        }
        ClientTemplateNode.nodes[name]['nodelist'] = nodelist

    @staticmethod
    def context(name, context):
        '''
        Saves the context for the given template
        '''
        ClientTemplateNode.nodes[name]['context'] = context

    @staticmethod
    def template(name):
        '''
        Returns the template with the given name
        '''
        nodes = ClientTemplateNode.nodes[name]['nodelist']
        context = ClientTemplateNode.nodes[name]['context']
        tmpl = dedent(nodes.render(context)
            # Change the delims
            .replace('<@', '{{')
            .replace('@>', '}}')
        )

        return tmpl


    @staticmethod
    def get():
        '''
        Singleton Factory
        '''
        return ClientTemplateNode()

@register.tag
def compile_templates(parser, token):
    try:
        tag_name, num = token.split_contents()
    except ValueError:
        # Second argument is optional
        num = 0
    else:
        try:
            num = int(num)
        except ValueError:
            raise template.TemplateSyntaxError('%r tag argument must be an integer' % tag_name)

    node = ClientTemplateNode.get()
    node.indent = num
    return node

@register.tag
def template(parser, token):
    '''
    Adds a new template to the current template list

    {% template 'name' %}
        ...
    {% endtemplate %}
    '''
    try:
        tag_name, name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires a single argument" % token.contents.split()[0])
    if not (name[0] == name[-1] and name[0] in ('"', "'")):
        raise template.TemplateSyntaxError("%r tag's name should be in quotes" % tag_name)
    nodelist = parser.parse(('endtemplate',))
    parser.delete_first_token()
    ClientTemplateNode.add(name[1:-1], nodelist)
    return PointerNode(name[1:-1])

@register.simple_tag
def render_template(name, args):
    '''
    Renders a template serverside with the given args

    {% render_template dict %}
    OR
    {% render_template '{"json": true}' %}
    '''
    # Accept either a dict or a JSON serializable string
    if type(args) != dict:
        args = simplejson.loads(args)

    tmpl = compiler.compile(ClientTemplateNode.template(name))
    return tmpl(args)



