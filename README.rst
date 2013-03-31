django-ajax-blocks
==================

This Django app allows the user to render templates partially and serve the
result via JSON. This enables faster template rendering and less bandwidth
usage.

The app is an alpha currently and mainly to demonstrate the idea but it should
work well enough.

Consider the following example using a single view::

    from django.utils.text import mark_safe
    from ajax_blocks import TemplateResponse

    def page(request):
        p = int(request.GET.get('page', 1))
        if p == 1:
            title = 'Welcome to my site'
            content = mark_safe('Hi, <a href="/?page=2">Click me</a>')
        else:
            title = 'Loaded via AJAX'
            content = 'Impressive, now try forward and back buttons'
        c = {'title': title, 'content': content}
        return TemplateResponse(request, 'page.html', c, ajax_blocks=('title', 'content'))

and this template::

    {% load static %}
    <html>
      <script type="text/javascript" src="http://code.jquery.com/jquery-1.9.1.min.js"></script>
      <script type="text/javascript" src="{% static 'ajax_blocks/helpers.js' %}"></script>
      <script type="text/javascript">
      $(document).ready(function(){
        $('a').click(function(ev) {
          render_ajax_blocks(ev.target.href);
          return false;
        });
      });
      </script>
    <head>
      <title data-block="title">{% block title %}{{ title }}{% endblock title %}</title>
    </head>
    <body data-block="content">{% block content %}{{ content }}{% endblock content %}</body>
    </html>

The first request is normally served as HTML. When the user clicks the link only
the *title* and *content* blocks are rendered on the server and returned as JSON.
The history updates via *pushState* on the client side and as such enables the
forward and back buttons to work properly. While this example is somewhat minimal
it already cuts bandwidth down to a third.

The included *helpers.js* only serves as a simple example, a realworld application
might wanna use something better suited to their needs.

More complicated examples include template inheritance which also works, if not
you found a bug. If that's the case please let me know!

Todo
----

 * Tests
 * Better JS integration

Installation
------------

First, install the app with your favorite package manager, e.g.::

    pip install django-ajax-blocks

Alternatively, use the `repository on Github`_.

Then configure your Django site to use the app:

#. Add ``'ajax_blocks'`` to your ``INSTALLED_APPS`` setting.

.. _`repository on Github`: https://github.com/apollo13/django-ajax-blocks/

