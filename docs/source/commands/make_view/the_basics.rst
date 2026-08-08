The Basics of make:view
=======================

Now for the fun part of this package 🎉.

Before we do anything else, **make sure you are at the root of your new
project**. This is not a correctional behavioral choice. This is a life-saving
choice to make sure you do not create a ton of files in the wrong place 😥.

The ``flask make:view`` command generates template files under
``app/templates/``. At its simplest, Flask-Commands just makes a view file.
But it can also help wire that view into your application with a route, a
controller, and even a model if you want to keep going.

That is one of the reasons I like this command so much: you can start small
and let the structure grow as your app grows.

When you are new to web development, it helps to think of these three pieces
like this: the route is the address, the controller is the logic, and the view
is the HTML the browser eventually sees. Flask-Commands helps wire those
pieces together so you do not have to build that plumbing from scratch every
time.

The optional generator flags are:

- ``-c / --generate-controller`` or ``--controller NAME``
  Creates or extends a controller **class** in your application.
- ``-r / --generate-route`` or ``--route PATH``
  Adds a blueprint route for the view. This works for custom naming and for
  RESTful actions.
- ``-m / --generate-model`` or ``--model NAME``
  Seeds a SQLAlchemy model with boilerplate columns: ``id``, ``created_at``,
  and ``updated_at``.

Let’s ease into this one step at a time.

Create a Simple Template
------------------------

.. youtube_embed:: create-a-simple-template-with-flask-make-view

Suppose you want an ``about`` page for your company.  To create the template,
type this in the terminal:

.. code-block:: bash

   flask make:view about

That’s it. You now have a new template at:

- ``app/templates/about.html``

Nice and simple 😌.

- No route.
- No controller.
- No model.
- Just the file.

That may sound a little underwhelming at first, but sometimes a single file is
exactly where you want to begin. Maybe you are sketching out a page. Maybe you
want to experiment with the HTML before thinking about URLs and controllers.
Maybe you just want the file on disk first and want to think about the wiring ⚡️
after your coffee ☕️ kicks in.

Whatever the reason, Flask-Commands is happy to start small.  The template
file now exists; however, it does **not** appear anywhere in your application
yet.  You cannot just type ``/about`` into the browser and expect it to work,
because the view has not been wired up to a route or a controller.

We will wire this file into the application shortly. For now, let’s look at
exactly what was created, because there is a little more to this file than
first meets the eye 👀.

Read the Generated Child Template
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. youtube_embed:: read-the-generated-child-template

When you open ``app/templates/about.html``, you will find something similar
to the following:

.. code-block:: html+jinja

   {% extends "base.html" %}

   {% block title %}{{ super() }}{% endblock title %}

   {% block content %}
       <div>
           Your future self is your most important user.
       </div>
   {%- endblock content %}

The only difference may be the saying between the ``div`` tags. I like to
keep things fresh, so I designed Flask-Commands to randomly select one of its
sayings when it creates the file. The saying is simply starter content, so you
can smile at it, ponder its wisdom, and then replace it with the page you
actually intended to build 😄.

At first glance, this file may look a little mysterious—especially if Jinja is
new to you. My reaction would be something like, “Wait a minute—you just sold
me the wrong thing! It says ``.html``, but I only see one lonely ``div``
element in this whole document 😤. We asked for a page, and Flask-Commands
handed us a few curly braces and a philosophical observation about our future
self. What happened to ``<!DOCTYPE html>``? Where are ``<head>`` and
``<body>``? Did Flask-Commands forget the rest of the page? 😨”

Fortunately, as we will see in a minute, nothing has gone missing. This
template is a **child template** that inherits all those important HTML tags
from a shared document structure. But I’m getting ahead of myself. For now,
let’s focus on the contents of this file: it contains both HTML and Jinja.

Before walking through the file, there are two pieces of Jinja syntax worth
recognizing:

- ``{% ... %}`` tells Jinja to do something, such as extend another template
  or define a block.
- ``{{ ... }}`` tells Jinja to evaluate an expression and place its result
  into the rendered HTML.

With those two small decoder rings in hand 🕵️, the generated template becomes
much less mysterious. It has three important parts:

1. It extends ``base.html``.
2. It defines the title for the browser tab.
3. It provides the visible content for the page.

The file is short because it does not need to repeat an entire HTML document.
We will go through each line in detail, but for now remember that the shared
document structure lives in one place. That means you do not have to edit every
view file when you want to change a fundamental part of your application’s
HTML structure.

Understand Jinja Template Inheritance
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. youtube_embed:: understand-jinja-template-inheritance

The first line of the generated view tells Jinja where to find that shared
structure:

.. code-block:: html+jinja

   {% extends "base.html" %}

This small line does a great deal of work.

To understand inheritance, think of ``base.html`` as the standard model of a
car. It defines the overall structure and includes the standard equipment
that every version receives.

A child template is like a custom order for one particular car. It tells the
factory which standard features to keep, which features to replace, and which
optional features to add.

When Flask renders the child template, Jinja acts like the factory. It begins
with the standard model from ``base.html``, applies the choices from the child
template, and delivers one complete, customized HTML page.  In our analogy,
this page is the finished car ready for the user to drive away 🏎️.

The blocks in ``base.html`` are the available customization points. A child
template can:

- leave a block alone and inherit its standard contents;
- override a block and call ``super()`` to keep the standard contents before
  adding something new;
- override a block without ``super()`` to replace the standard contents
  completely.

This gives every page a consistent foundation without forcing every page to
look or behave exactly the same.

Customize the Title and Content Blocks
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. youtube_embed:: customize-the-title-and-content-blocks

The generated title block looks like this:

.. code-block:: html+jinja

   {% block title %}{{ super() }}{% endblock title %}

The ``super()`` function asks Jinja to use the contents of the same block from
``base.html``. When we dive into ``base.html``, we will see that this block is
configured to be the application name converted to title case.

Suppose the application is named ``Flask Commands``. The generated title block
will keep that title exactly as it is.

You can retain the application name while adding a page-specific title:

.. code-block:: html+jinja

   {% block title %}About | {{ super() }}{% endblock title %}

The browser tab will now display:

.. code-block:: text

   About | Flask Commands

You can also replace the inherited title completely by leaving out
``super()``:

.. code-block:: html+jinja

   {% block title %}About Our Company{% endblock title %}

The content block works the same way:

.. code-block:: html+jinja

   {% block content %}
       <div>
           Your future self is your most important user.
       </div>
   {%- endblock content %}

When Jinja renders the page, this ``div`` is placed wherever ``base.html``
defines its ``content`` block. This is where most of the page-specific HTML
will live.

Notice the dash at the beginning of ``{%- endblock content %}``. That dash
tells Jinja to trim the whitespace immediately before the tag. It helps keep
the final rendered HTML tidy without changing the visual layout of the page.

At this point, you are probably thinking, “Okay, I understand what this child
template is trying to accomplish, but how do all these puzzle pieces fit
together to make the complete HTML document I am used to seeing?” Let's now
dive into the ``base.html`` file and find out.

Meet the Base Template
~~~~~~~~~~~~~~~~~~~~~~

.. youtube_embed:: meet-the-base-template

Now open ``app/templates/base.html`` and look at the standard model our
views are customizing:

.. code-block:: html+jinja

   <!DOCTYPE html>
   <html lang="en">
   <head>
       <meta charset="UTF-8">
       <meta name="viewport" content="width=device-width, initial-scale=1.0">
       <title>{% block title %}{{ config['APP_NAME'] | title }}{% endblock title %}</title>
       {%- block metadata %}{% endblock metadata %}
       {%- block styles %}
           <link rel="stylesheet" href="{{ url_for('static', filename='tailwind.min.css', v=time.time()) }}">
       {%- endblock styles %}
   </head>
   <body>
       {%- block content %}{% endblock content %}
       {%- block scripts %}{% endblock scripts %}
   </body>
   </html>

If you are already familiar with HTML, most of this should feel comfortably
ordinary. That is intentional. The base template is a standard HTML document
with five carefully placed Jinja blocks:

- ``title`` provides the browser-tab title. Its default value is the
  application name from Flask’s configuration, converted to title case.
- ``metadata`` provides a place for page-specific metadata inside ``<head>``.
- ``styles`` provides the shared stylesheet and a place for additional or
  replacement styles.
- ``content`` provides the main page-specific HTML inside ``<body>``.
- ``scripts`` provides a place for JavaScript immediately before
  ``</body>``.

Some blocks contain useful defaults, while others begin empty. An empty block
is not unfinished. It is a reserved customization point waiting for a child
template that needs it.

The real advantage is not merely that ``base.html`` saves a few lines of
typing. It gives the entire application one dependable document structure.
When something genuinely belongs on every page, you have one place to put it.

That power deserves a small warning label ⚠️: changes to ``base.html`` can
affect every template that extends it. Shared navigation, fonts, or styles may
belong there. A script needed by one unusually enthusiastic page probably
does not.

Inherit, Add, or Replace Styles
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. youtube_embed:: inherit-add-or-replace-styles

The ``styles`` block contains Tailwind by default:

.. code-block:: html+jinja

   {%- block styles %}
       <link rel="stylesheet" href="{{ url_for('static', filename='tailwind.min.css', v=time.time()) }}">
   {%- endblock styles %}

As we have already seen, a child template has three choices.

First, it can leave the block alone. In this case Tailwind will be inherited
automatically, which is what the generated view does.

Second, it can keep Tailwind and add another stylesheet by calling
``super()``:

.. code-block:: html+jinja

   {% block styles %}
       {{ super() }}
       <link rel="stylesheet" href="{{ url_for('static', filename='about.css') }}">
   {%- endblock styles %}

Jinja renders the inherited Tailwind stylesheet first and then adds
``about.css``.

Third, the child can replace Tailwind by overriding the block without calling
``super()``:

.. code-block:: html+jinja

   {% block styles %}
       <link rel="stylesheet" href="{{ url_for('static', filename='about.css') }}">
   {%- endblock styles %}

Now only ``about.css`` is included for that page.

This is why Tailwind lives *inside* the block. The child template can inherit
it, add to it, or replace it without modifying the shared base template.

One thing that might leave you scratching your head 🤔 is the ``v=time.time()``
argument.  This adds the current timestamp to the stylesheet
URL as a query parameter. During development, this prevents the browser from
continuing to serve an older cached copy after you change the CSS.

The generated application factory registers a context processor inside
``create_app()`` in ``app/__init__.py``. This exposes Python’s ``time`` module
to every Jinja template renered by the application, allowing each template
to call ``time.time()`` without importing it or passing it explicitly
to every ``render_template()`` call.

For production, you may eventually want to replace the changing timestamp
with a release or asset version so the browser can cache the stylesheet
efficiently. I say *eventually* because a website is never truly finished; it
merely reaches a point where we stop touching it long enough to deploy 😄.

Use Metadata and Scripts
~~~~~~~~~~~~~~~~~~~~~~~~

.. youtube_embed:: use-metadata-and-scripts

The ``metadata`` block lives inside ``<head>`` and begins empty. A child
template can use it to add page-specific information:

.. code-block:: html+jinja

   {% block metadata %}
       <meta name="description" content="Learn more about our company.">
   {% endblock metadata %}

This gives the ``about`` page its own description without placing that
description on every other page.

The ``scripts`` block follows the same idea:

.. code-block:: html+jinja

   {% block scripts %}
       <script src="{{ url_for('static', filename='about.js') }}"></script>
   {% endblock scripts %}

In ``base.html``, the ``scripts`` block appears immediately before
``</body>``. Keeping it there allows the browser to encounter the page content
before loading page-specific JavaScript.

If every page needs the same metadata, stylesheet, or script, place it in the
corresponding block in ``base.html``. If only one page needs it, override the
block in that child template. When you want the shared content *and* the
page-specific addition, call ``super()``.

That is the quiet strength of template inheritance: one shared structure,
small focused child templates, and enough flexibility for every page to become
itself.

Our ``about.html`` file now makes much more sense—but it is still only a file.
To make it appear in the browser, we need to connect it to the rest of the
application. Before we do that, we should meet the namespace Flask-Commands
uses for main document-style pages.

Understand the ``mains`` Namespace
----------------------------------

.. youtube_embed:: understand-the-mains-namespace

Flask-Commands gives you a built-in namespace called ``mains`` for the main
document-style pages in your application. Think things like:

- landing page
- about page
- contact page
- terms page
- privacy page

In other words, the pages that feel like the “main” pages of the site.

There are a couple things to notice here:

- the template folder is ``mains`` with an ``s``
- the controller is ``MainController`` in the singular

That is by design.

So when you see something like:

.. code-block:: text

   app/templates/mains/
   app/controllers/main_controller.py
   app/routes/mains/

you are looking at the built-in organizing namespace Flask-Commands created
for those main document pages.

This is also why ``mains`` is a little special. It helps organize your
internal project structure, but it is **not** meant to be a public URL
segment.

So ``mains`` helps keep things tidy on disk, while the public URL can still
stay nice and clean.

Wire a Page Explicitly
----------------------

.. youtube_embed:: wire-a-page-explicitly

Now let’s wire up that ``about`` page.

If you already know exactly how you want the page wired, you can say so
directly:

.. code-block:: bash

   flask make:view about --route /about --controller MainController

In this example, ``MainController`` is a natural fit because a fresh
Flask-Commands project already ships with a ``MainController`` and a
``mains`` namespace.

This command:

- creates ``app/templates/about.html``
- adds an ``about`` method to ``MainController``
- updates the ``mains`` routes file with a ``GET`` route at ``/about``

So the pieces line up like this:

- route: ``/about``
- controller method: ``MainController().about()``
- view: ``app/templates/about.html``

A browser request for ``/about`` hits the route, the route calls the
controller method, and the controller renders the view.

This is the “say exactly what you mean” version of the command. This method is
very clear, very direct, and very surgical 👨‍⚕️. It also involves a bit of typing.

Use Generator Flags
-------------------

.. youtube_embed:: use-generator-flags-with-make-view

Sometimes, and for me most of the time, I just want to see a starter page in
the browser all wired up and I really don't want to type a ton.  In my
opinion, that is not asking too much.  This is where generator flags come to
the rescue, turning the long command above into a few short concept flags 🎉.
Let's start with ``-r`` and ``-c``, which you can combine into an even shorter
command ``-rc``.

The same general result as above can be written like this:

.. code-block:: bash

   flask make:view about -rc

Here:

- ``-r`` means generate the **route** URL for me from the name
- ``-c`` means generate the **controller** and add the method

Much shorter. Much easier to remember.

I think of it like this: if I want the page to actually work, I probably need
a **route** and a **controller**. So ``-rc`` becomes a nice little habit 😌.

This is one of the small pleasures of the package. Once the naming conventions
are familiar, the short flags become very easy to remember.

Use ``mains`` Intentionally
---------------------------

.. youtube_embed:: use-mains-intentionally

Now let’s use the ``mains`` namespace on purpose.

Suppose you want that same ``about`` page to live under ``mains`` so your
templates stay a little more organized:

.. code-block:: bash

   flask make:view mains.about --route /about -c

This creates:

- ``app/templates/mains/about.html``

and also:

- adds an ``about`` method to ``MainController``
- updates the ``mains`` routes file with a ``GET`` route at ``/about``

This is a nice pattern because it keeps the template organized under
``mains``, but the route still stays clean at ``/about`` because you
explicitly told Flask-Commands the route you wanted.

Now compare that with this:

.. code-block:: bash

   flask make:view mains.about -rc

This time, because you did **not** explicitly provide the route,
Flask-Commands generates the route for you. And since ``mains`` is an
internal organizing namespace for main document pages, it does **not** become
part of the public URL.

So the URL is still:

- ``/about``

not:

- ``/mains/about``

That is an important distinction.

When you explicitly say:

.. code-block:: bash

   --route /about

you are in charge of the route.

When you rely on:

.. code-block:: bash

   -r

Flask-Commands generates the route for you, but it still respects the idea
that ``mains`` is an internal namespace and not a public URL segment.

That means dot notation can affect more than just the template path. It can
also shape the controller and route wiring around the page, while still
keeping the public URL clean for the ``mains`` namespace.

I would have given the shortened version earlier, but we did not know about
``mains`` yet. Now we do so we can use the cool kids 😎 shortcuts.

A Quick Peek at Nested Views
----------------------------

.. youtube_embed:: a-quick-peek-at-nested-views

Dot notation also becomes handy when you want to organize reusable templates.

For example:

.. code-block:: bash

   flask make:view components.accordions
   flask make:view components.checkboxes
   flask make:view components.selects

These create:

- ``app/templates/components/accordions.html``
- ``app/templates/components/checkboxes.html``
- ``app/templates/components/selects.html``


Because we did not add any generator flags, these are just templates. That is
usually exactly what you want for Jinja macros, included templates, or little
reusable building blocks.

So before we ever get into nested resources like ``recipes.comments.index``,
dot notation is already helping keep the template structure nice and tidy.

When ``make:view`` Is the Right Starting Point
----------------------------------------------

.. youtube_embed:: when-make-view-is-the-right-starting-point

A view-first workflow makes sense when the page is the clearest thing in your
head.

For example, maybe you know:

- you need an ``about`` page
- you need a ``contact`` page
- you want to create the template first and worry about wiring second
- you want to build outward from the page instead of starting from the model

That is where ``flask make:view`` really shines ☀️.

It lets you start small and add structure only when you need it.  Sometimes
the simplest step is the best first step. You do not have to jump straight
into models, controllers, and RESTful actions just because you wanted one
page on disk.  However, if you want to wire everything up and see a single page,
Flask-Commands has a simple command for that using the ``-rc`` optional flags.

With the basic flow down, we can now talk about the smarter behavior hiding
behind the command.
