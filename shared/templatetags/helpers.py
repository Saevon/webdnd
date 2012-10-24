from django import template
from django.conf import settings

from textwrap import dedent, TextWrapper
from pprint import pformat
import logging
logging = logging.getLogger('templatetags')

register = template.Library()


class NullNode(template.Node):
    def render(*args, **kwargs):
        return ''

@register.simple_tag
def setting(k, default=None):
    return get_setting(k, default)

@register.assignment_tag
def setting_var(k, default=None):
    return get_setting(k, default)

def get_setting(k, default=None):
    if hasattr(settings, k):
        return getattr(settings, k)
    else:
        logging.warn('Setting not found: "%s"' % k)
    if default is None:
        return ''
    return default


# Client template helpers

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
            nodes = ClientTemplateNode.nodes[name]
            lines.append(ClientTemplateNode.LINE_TMPL % {'name': name})

            templates.append(ClientTemplateNode.HTML_TMPL % {
                'name': name,
                'content': dedent(nodes.render(context))
                    # Change the delims
                    .replace('<%', '{{')
                    .replace('%>', '}}')
                    .replace('\n', '\n' + (4 * ' ')),
            })

        # Clear it for the next use
        ClientTemplateNode.nodes = {}

        return (ClientTemplateNode.TMPL % {
            'lines': '\n'.join(lines).replace('\n', '\n' + (4 * ' ')),
            'templates': '\n'.join(templates),
        }).replace('\n', '\n' + (self.indent * ' '))

    @staticmethod
    def add(name, nodelist):
        ClientTemplateNode.nodes[name] = nodelist

    @staticmethod
    def get():
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
    try:
        tag_name, name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires a single argument" % token.contents.split()[0])
    if not (name[0] == name[-1] and name[0] in ('"', "'")):
        raise template.TemplateSyntaxError("%r tag's name should be in quotes" % tag_name)
    nodelist = parser.parse(('endtemplate',))
    parser.delete_first_token()
    ClientTemplateNode.add(name[1:-1], nodelist)
    return NullNode()




