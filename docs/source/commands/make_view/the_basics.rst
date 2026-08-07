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

Suppose you want an ``about`` page for your company:

.. code-block:: bash

   flask make:view about

That’s it. You now have a new template at:

- ``app/templates/about.html``

Nice and simple 😌.

- No route.
- No controller.
- No model.
- Just the file.

If you open the new template file, it will look something like this:

.. code-block:: html+jinja

   {% extends "base.html" %}

   {% block title %}{{ super() }}{% endblock title %}

   {% block content %}
       <div>
           Your future self is your most important user.
       </div>
   {%- endblock content %}

At first this might look a little odd, expecally if you are new to Jinja.
The contents of this file are a mixture of Jinja and HTML.  Let's go throught
this line by line.  There are three sections in this file.

1)  The first line tells Jinja that this template extends ``base.html``.  You
might be thinking "What is ``base.html``?" I know I would.  For now think of
``base.html`` as your blueprint on how to structure all your html files. We will
look at it's content below.

2) The second section is the title which is what appears on the tab as the
webpages name.  Inside the block tags ``{% block title %}...{% endblock title %}``
you see ``{{ super() }}`` this is saying take whatever the base.html has
insides it's block title and use that.  You can modify this by doing something
like the following:

.. code-block:: html+jinja

   {% block title %}About | {{ super() }}{% endblock title %}

Then the tab will have the title of "About | " followed by whatever
the ``base.html`` has in it's title section.

3) The third section is where most of your work will be places.  It's the
block of content ``{% block title %}...{% endblock title %}`` which is what
shows up on the page.

Lets now disect ``base.html`` which is located in the app template directory.
This file provides the shared HTML document structure. This way all your html
pages have a uniform structure. The file is more Jinja and HTML

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

For those familar with HTML this is a boilerplate HTML file which a few
changes.  Inside the title tags we create a block for title content and
prepopulate it with the applications name (in title case) which is found in
your ``.env`` file.  Also we make a block for metadata with nothing in it.  We
add in a style block and put in tailwind.  The v=time.time() is use as a
browser cache buster so as you are developing your style file updates.
You can remove `` v=time.time()`` when you are finished making changes to
your website for the time being.  I have never gotten to that point myself.
The block content is where you will put all of your main content for the page.
Finally the script block is where you would add any javascript files.

A key concept to note here is that if you add anything inside one of the blocks
in the ``base.html`` then that will populate to all of your html files that
extend ``base.html`` which should be all of your html files.  For example, you
will want your style sheet on every page so instead of writing the line
``<link rel="stylesheet" href="{{ url_for('static', filename='tailwind.min.css', v=time.time()) }}">``
over and over again in each file you just put it in.  If you add a javascript
library to base then you will have that same javascript library on every single
page which may or may not be what you want.  The warning is to be careful with
what you change in ``base.html``

So now that we have debunked the mistory of a view template it may sound a
little underwhelming at first, but sometimes that is exactly what you want.
Maybe you are making a basic page. Maybe you are sketching something out.
Maybe you just want the file on disk first and want to think about the wiring
after your coffee ☕️ kicks in.

The important thing to know is this: the template now exists, but it does
**not** appear anywhere in your application yet. You cannot just type
``/about`` into the browser and expect it to work, because the view has not
been wired up to a route or a controller.

Understand the ``mains`` Namespace
----------------------------------

.. youtube_embed:: understand-the-mains-namespace

Before we wire up that ``about`` page, we should talk about ``mains``.

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
