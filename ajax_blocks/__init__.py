import json

from django.template.base import TextNode
from django.template.loader_tags import BlockNode, ExtendsNode, BLOCK_CONTEXT_KEY, BlockContext
from django.template.response import TemplateResponse as DjangoTemplateResponse


def find_extends_node(nodelist):
    """Finds the ExtendsNode if existant."""
    for node in nodelist:
        if not isinstance(node, TextNode):
            if isinstance(node, ExtendsNode):
                return node
            return # ExtendsNode has to be the first node!


def render_partial(template, context, ajax_blocks):
    """Render the requested blocks into a dictionary."""
    templates = [template]

    # Find all templates in the inheritance chain.
    while template:
        extends_node = find_extends_node(template.nodelist)
        if extends_node:
            template = extends_node.get_parent(context)
            templates.append(template)
        else:
            break

    # Ensure we have the proper BlockContext.
    if not BLOCK_CONTEXT_KEY in context.render_context:
        context.render_context[BLOCK_CONTEXT_KEY] = BlockContext()
    block_context = context.render_context[BLOCK_CONTEXT_KEY]

    # Collect all the BlockNodes and fill the structure.
    for template in templates:
        extends_node = find_extends_node(template.nodelist)
        if extends_node:
            block_context.add_blocks(extends_node.block)
        else: # Root template
            blocks = dict([(n.name, n) for n in
                           template.nodelist.get_nodes_by_type(BlockNode)])
            block_context.add_blocks(blocks)

    res = {}
    for name in ajax_blocks:
        res[name] = block_context.get_block(name).render(context)
    return res


class TemplateResponseMixin(object):
    def __init__(self, request, *args, **kwargs):
        self.ajax_blocks = kwargs.pop('ajax_blocks', [])
        if request.is_ajax():
            # mimetype overrides content_type but is deprecated,
            # get rid of it and override content_type instead.
            kwargs.pop('mimetype', None)
            kwargs['content_type'] = 'application/json'
        super(TemplateResponseMixin, self).__init__(request, *args, **kwargs)

    @property
    def rendered_content(self):
        if self._request.is_ajax():
            template = self.resolve_template(self.template_name)
            context = self.resolve_context(self.context_data)
            res = render_partial(template, context, self.ajax_blocks)
            res = {'blocks': res, 'url': self._request.get_full_path()}
            return json.dumps(res)
        else:
            return super(TemplateResponseMixin, self).rendered_content


class TemplateResponse(TemplateResponseMixin, DjangoTemplateResponse):
    pass
