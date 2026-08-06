The Basics of make:model
========================

Sometimes the cleanest place to begin is the data structure itself. If the
model is the first structure you know your application will contain, then
``flask make:model`` is a very nice place to start.

If you are newer to web development, a model is the part of your web
application that stores your data in a structured way.  This approach is
especially useful when the data shape is the clearest thing in
your head and you want to start there before thinking about controllers,
routes, or views.  As a data engineer and mathematician, this is where I
find myself starting a project.

Make a Basic Model
------------------

.. youtube_embed:: make-a-basic-model

If I were building the cooker application we have been working on from scratch,
I would start by thinking, *"A cooking application will need a place to store
all the recipes."*  Consequently, my first thought would be to build a
``Recipe`` model. The simplest way to scaffold out a model is with
this command:

.. code-block:: bash

   flask make:model Recipe


.. admonition:: For those following along

   If you have been following this documentation from the beginning, you already
   created a ``Recipe`` model earlier.  We did this either with
   ``flask make:view recipes.index -rcm`` or
   ``flask make:controller RecipeController --crud -m``.  Because of this you will
   receive a warning in the terminal saying that the ``Recipe`` model already
   exists.

   .. rst-class:: terminal-warning
   .. code-block:: text

      ⚠️  Warning: Model Already Exists
         - Model Recipe already exists
         - No changes were made to the existing model

      ⚠️  Warning: One or more make model steps produced a warning or failure.

   Don't be alarmed if you see this; it's **not a problem**.  This warning
   means Flask-Commands is protecting the file that already exists instead
   of overwriting it.

   If you are seeing this warning and you would like to run the above command
   without the warning simply spin up a fresh project with
   something like:

   .. code-block:: bash

      flask new example_model_the_basics

   then cd into your new project

   .. code-block:: bash

      cd example_model_the_basics

   and now you can run your model building command without any warnings

   .. code-block:: bash

      flask make:model Recipe

This generates:

- ``app/models/recipe.py``
- and registers the model in ``app/models/__init__.py``

The registration part is important because it helps with clean imports into
other parts of our application, mainly in controller files.  It also helps
Flask-Commands locate your application's data structures.  We have already
seen how important it is for Flask-Commands to know about your data structure
when you ask Flask-Commands to generate models based on relationships between
the data structures.  But I'm getting ahead of myself.  For now, let's take a
closer look at the model file and see what we can do with a freshly generated
model file.

What the Model Includes
-----------------------

.. youtube_embed:: what-the-model-includes

Let's look at the model file ``app/models/recipe.py`` that was generated
for us and understand each line.

.. code-block:: python

    from app import db
    from datetime import datetime, timezone

    class Recipe(db.Model):
        __tablename__ = 'recipes'

        # Columns
        id = db.Column(db.Integer, primary_key=True)
        created_at = db.Column(db.DateTime(timezone=True),
                               index=True,
                               default=lambda: datetime.now(timezone.utc))
        updated_at = db.Column(db.DateTime(timezone=True),
                               default=lambda: datetime.now(timezone.utc),
                               onupdate=lambda: datetime.now(timezone.utc))

        # Methods
        @classmethod
        def create(cls, attributes):
            """Create an instance from mapped attributes, save it to the database,
            and return it."""
            valid_attributes = {
                attribute.key
                for attribute in cls.__mapper__.column_attrs
            }
            invalid_attributes = sorted(
                set(attributes) - valid_attributes
            )
            if invalid_attributes:
                invalid_names = ", ".join(invalid_attributes)
                raise AttributeError(
                    f"Unknown {cls.__name__} "
                    f"attribute(s): {invalid_names}"
                )

            instance = cls()
            for attribute, value in attributes.items():
                setattr(instance, attribute, value)

            db.session.add(instance)
            db.session.commit()
            return instance

        def update(self, attributes):
            """Update mapped attributes, save changes to the database,
            and return this instance."""
            valid_attributes = {
                attribute.key
                for attribute in self.__mapper__.column_attrs
            }
            invalid_attributes = sorted(
                set(attributes) - valid_attributes
            )
            if invalid_attributes:
                invalid_names = ", ".join(invalid_attributes)
                raise AttributeError(
                    f"Unknown {type(self).__name__} "
                    f"attribute(s): {invalid_names}"
                )

            for attribute, value in attributes.items():
                setattr(self, attribute, value)

            db.session.commit()
            return self

        def delete(self):
            """Delete this instance from the database."""
            db.session.delete(self)
            db.session.commit()

        def __repr__(self):
            """Model representation for Code Debugging"""
            return f'<Recipe id:{self.id}>'



While the generated model file might look a little scary 🫣 at first, it is
actually a small and useful starting point.  This is one of the main features
I wanted from Flask-Commands.  When I am building a new data structure, the
first mental hurdle is often just getting the model file started with the
right shape.

Let's go through each line of this model file and debunk the mystery.
The first observation is to notice that a model is just a Python class that
extends ``db.Model``.  After declaring the class name we define the table name.
As a convention Flask-Commands uses the plural version of the singular model
name.  After that there are three columns that every new model file ships with:

- ``id``
- ``created_at``
- ``updated_at``

The first column is an integer column called ``id``.  The ``id`` column
is your table's unique identifier on each row in your table, and is used to
make relationships between models.  The next two columns are datetime columns:
``created_at`` and ``updated_at``.  When a new instance is created and stored in
the database, these datetimes are set to populate without you doing any
additional work.  In addition, if you modify the instance, ``updated_at``
will receive a new timestamp when you save the changes to the database.

Being able to save changes to the database is exactly where the last part of
the model comes into play. In addition to the three columns, there are four
methods that finish off our class definition:

- ``create``
- ``update``
- ``delete``
- ``__repr__``

When you want a new model instance, ``create`` is a handy class method that
accepts a dictionary of mapped model attributes. It first validates the
attribute names, then creates and saves the new instance in the database.
Finally, ``create`` returns the new instance.

If you have never seen a class method before, it is called a little differently
than a normal instance method. Instead of calling it on an existing model
instance, you call it directly on the model class. We will see this in action
in an upcoming section.

Next is ``update``, which also accepts a dictionary of mapped model attributes.
Similar to ``create``, the ``update`` method first validates the attribute
names.  After validating, it applies the changes to the existing instance,
saves them in the database, and before ending returns the updated instance.

Both ``create`` and ``update`` raise an ``AttributeError`` before changing
anything if the dictionary contains an attribute that is not mapped on the
model. This helps catch misspelled or unexpected attribute names instead of
silently ignoring them.

The final database-changing method is ``delete``, which removes an instance
from the database.  Remember there is no coming back from delete 💣!

Finally, ``__repr__`` is a great tool for debugging.  It is the magic 🪄 method
that runs when you print a model instance.

The generated model gives you a clean base, but it is by no means the complete
finished data structure. Right now, ``Recipe`` can be stored in the
database, but it does not yet describe anything about a recipe.

The next step is to add the columns that make the model meaningful. We will
start with one simple column, ``name``, and then update the database so the
schema matches the Python model.

Edit the Model and Migrate the Database
---------------------------------------

.. youtube_embed:: edit-the-model-and-migrate-the-database

At some point you will want to modify your model by adding new columns, changing
the structure of your columns, or deleting columns.

I will briefly demonstrate how to add a column to a model, and then I will send
you off to learn more about model manipulation from other sources, since this is
not a feature of Flask-Commands.

In our ``Recipe`` model, let's update the columns by adding a ``name`` column.
To do this we just add the following line of code to the model class.

.. code-block:: python

   name = db.Column(db.String(128), nullable=False)

That was easy; however, changing the Python model file does not automatically
change the database schema by itself.  That is where a database migration
comes into play.

.. admonition:: Thank you Miguel Grinberg for Flask-Migrate

   Thanks to Miguel Grinberg we can use
   `Flask-Migrate <https://flask-migrate.readthedocs.io/>`_ to make this
   process seamless!  Miguel's package Flask-Migrate is amazing at keeping
   track of all the database changes and applying them,  so you can focus on
   the final shape of your model file.

   If you use ``flask new myproject`` to build your application, then
   Flask-Migrate is already wired up.  Otherwise, you will need to visit
   Miguel's documentation to learn how to wire up Flask-Migrate.

Once you update the model, you can easily generate a migration using the
following terminal commands:

.. code-block:: bash

   flask db migrate -m "create recipes table"
   flask db upgrade

That is the Flask-Migrate part of the workflow, and it is one of the reasons I
like the default project scaffold so much.  When you ran ``flask new myproject``
Flask-Commands wires up Flask-Migrate and Flask-SQLAlchemy for you so you can
just focus on your application's database development.

.. admonition:: One small note

   If you created the project with the ``--no-db`` option like this
   ``flask new myproject --no-db``, then the database and migration pieces
   are intentionally not there.

   In this case, you will need to wire up both Flask-Migrate and
   Flask-SQLAlchemy if you wish to have a persistent database for your
   application.

At this point, the Python model and the database schema agree with each
other. The ``Recipe`` class has a ``name`` column, and the database has been
upgraded to store that column.

Now we can give the model a test drive 🏎️ in the terminal.

Create, Update, and Delete a Recipe
-----------------------------------

.. youtube_embed:: create-update-and-delete-a-recipe

Now that the ``Recipe`` model has a ``name`` column and the database has been
migrated, we can use the model to start building out instances and persist them
in our database.  For me, this is the fun part 🥳.

As we saw in the :ref:`Run the New Project <run-the-new-project>`
section of Starting a Project, the easiest way to start the application is to
cd into the root project directory and run:

.. code-block:: bash

   ./run.sh

That helper starts the application and opens a Flask shell for you in a
separate terminal window.

If you prefer, you can do this manually by activating your virtual
environment and running ``flask shell``. In other words, first cd into your
project's root directory and run the following commands:

.. code-block:: bash

   source venv/bin/activate
   flask shell

Inside the flask shell, there is some magic happening for you that gives you
instant access to all your models without having to write import statements.
Normally, to access a model, you would have to write something like
``from app.models import Recipe``.  However, with the way Flask-Commands sets
up your project, and with the default settings of Flask-SQLAlchemy, everything
just works!

For those interested, the magic details are as follows:

- First, the generated project imports ``app.models`` during app startup in
  ``create_app`` found in  ``app/__init__.py``.
- That makes registered models like ``Recipe`` known to Flask-SQLAlchemy.
- Then, according to the
  `Flask-SQLAlchemy documentation <https://flask-sqlalchemy.palletsprojects.com/en/stable/api/>`_
  the ``add_models_to_shell`` attribute is set to ``True`` by default, which
  means our models are all imported into ``flask shell`` automatically.

The shortened version is this: once you are inside the Flask shell, you can type
``Recipe`` and the interpreter will know that this is your ``Recipe`` model.

Without further delay, let's now create a ``Recipe`` instance by making a
salad recipe:

.. code-block:: pycon

   >>> recipe = Recipe.create({'name': 'salad'})
   >>> print(recipe)
   <Recipe id:1>
   >>> Recipe.query.count()
   1

Here we create our first instance of ``Recipe`` by calling ``create`` directly
on the ``Recipe`` class and giving it a dictionary containing the attributes
for our new recipe. The class method creates the instance, saves it in the
database, and returns it to us.

Notice that typing ``print(recipe)`` shows the friendly debugging
representation from ``__repr__``.  The representation shows an ``id`` of ``1``
instead of ``None`` because ``create`` commits the recipe to the database
before returning it. The final line, ``Recipe.query.count()``, confirms that
the database now contains one recipe.

We can also see ``updated_at`` do its quiet little bit of magic 🪄. First, save
the current timestamp:

.. code-block:: pycon

   >>> original_updated_at = recipe.updated_at
   >>> original_updated_at
   datetime.datetime(2026, 5, 12, 9, 55, 58, 577798)

Now let's change the recipe's name and see if ``updated_at`` changes.

.. code-block:: pycon

   >>> updated_recipe = recipe.update({'name': 'fruit salad'})
   >>> updated_recipe is recipe
   True
   >>> recipe.name
   'fruit salad'
   >>> updated_recipe.name
   'fruit salad'
   >>> recipe.updated_at > original_updated_at
   True
   >>> recipe.updated_at
   datetime.datetime(2026, 5, 12, 9, 57, 32, 343438)

The ``update`` method applies the dictionary of attributes to the existing
instance, commits the changes, and returns that same instance. You do not have
to assign the return value, but you can if it is useful for your application.

Because ``updated_recipe is recipe`` returns ``True``, we know both variables
refer to the same in-memory instance. They therefore both contain the new
``'fruit salad'`` name. In addition, notice that ``updated_at`` has also
changed because SQLAlchemy executed the column's ``onupdate`` function when
the change was committed.

The attribute validation also protects us from misspelled attribute names.
For example:

.. code-block:: pycon

   >>> recipe.update({'naem': 'green salad'})
   Traceback (most recent call last):
   ...
   AttributeError: Unknown Recipe attribute(s): naem
   >>> recipe.name
   'fruit salad'

Because ``naem`` is not a mapped attribute on ``Recipe``, ``update`` raises an
``AttributeError`` before changing the instance or committing anything.

Finally, we can delete the recipe:

.. code-block:: pycon

   >>> recipe.delete()
   >>> print(recipe)
   <Recipe id:1>
   >>> Recipe.query.count()
   0

The Python object still exists in memory, so ``recipe`` can still print as
``<Recipe id:1>``. But the database row is gone, which is why
``Recipe.query.count()`` returns ``0``.

At this point, you have seen the full model-only workflow. We created a
``Recipe`` model, added a real column, migrated the database, created an
instance, updated it, and deleted it.

That is enough when all you need is the data structure itself. But web
applications do not live in a Flask shell. Personally, I could play in the Flask
shell all day and would probably love a web app that was nothing more than
a Flask shell. However, everyone else expects routes, controllers, and
templates, as we have seen in prior chapters, to view and manipulate the data
structures.

To do this, we will carry over the ``--crud`` option from ``make:controller``
into our new ``make:model`` world. In the next section, we will start from
the same model-first idea, but let Flask-Commands build the rest of the
resource around the model for us.


