CherryPy + Mako + Formish + OOOP boilerplate
============================================

This project is my boilerplate codebase I created to integrate some Python
components with the goal of publishing [OpenERP](http://www.openerp.com/)
content on the web.

This stack is composed of:

* [CherryPy](http://www.cherrypy.org/) to serve web content,
* it use [Mako](http://www.makotemplates.org/) for HTML templating,
* [Formish](https://github.com/ish) for HTML form generation and validation,
* [OOOP](https://github.com/lasarux/ooop) to talk to OpenERP server via web
  services.

This project contains the experiments I did while working at
[Smile](http://www.smile.fr/), when I explored the possibility of integrating
these components. This code was a proof-of-concept that we leveraged later for
a highly specific OpenERP project.

Because of the highly experimental nature of this project, it contains lots of
stupid and failed attempts. The whole code base should be thoroughly cleaned up
before it can be considered reusable.


How-to install this app
-----------------------

1. Install system dependencies using your favorite package manager. Here is the
   example for an Ubuntu machine:

        $ apt-get install python-dev

1. Initialize the buildout environment:

        $ python ./bootstrap.py --distribute

1. Run buildout itself:

        $ ./bin/buildout

1. Run the following command to run the server:

        $ ./bin/web_publisher

1. Go to the following URL in your browser:

        http://localhost:8081


Documentation
-------------

Here is a list of useful external documentation and references to help you work
in this environment:

* CherryPy Tools code snippets: http://tools.cherrypy.org/wiki/TitleIndex
* Some CherryPy notes: http://helpful.knobs-dials.com/index.php/CherryPy
* An example of CherryPy application: http://bitbucket.org/Lawouach/twiseless
* Mako documentation: http://www.makotemplates.org/docs/
* Formish documentation: http://ish.io/embedded/formish/
* Formish examples: http://test.ish.io/
* OOOP examples: http://www.slideshare.net/raimonesteve/connecting-your-python-app-to-openerp-through-ooop


TODO
----

* Profile the code with CherryPy built-in methods ?

* Add a CSS compressor and combinator to save few bytes and queries.

* Add the hash of the compiled.js file to its name (force cache invalidation).

* Release dottedish 0.6.1 to Pypi and remove our ugly patch.

* Use consistent localized dates accross datepickers, HTML, formish and OpenERP.

* Update formish to make its internal messages translatable (errors, etc...).

* Make a bug report to formish regarding multi-checkbox widget data deserialization (see: http://github.com/kdeldycke/cherrypy_mako_formish_ooop_boilerplate/commit/1ce33061c8f33a18c73c285021e69477fca0f50c ) ? Here are some relevent debug messages:

    formish.Sequence(name='option_list', attr=schemaish.Sequence(schemaish.Integer()))
    schemaish.Sequence(schemaish.Integer())
    schemaish.Integer()
    <function string_converter at 0x3018a28>
    <convertish.convert.IntegerToStringConverter object at 0x34557d0>
    <bound method IntegerToStringConverter.to_type of <convertish.convert.IntegerToStringConverter object at 0x3455490>>
    <DottedList "[[u'3'], [u'4']]">

* Clean and tidy up all that crappy code.

* Use CherryPy tools decorator to factorize code.

* Leverage CherryPy cache tools. Example: http://www.cherrypy.org/wiki/Caching and http://docs.cherrypy.org/dev/refman/lib/caching.html

* Add aggressive caching of static images.


Author
------

 * [Kevin Deldycke](http://kevin.deldycke.com) - `kevin@deldycke.com`


License
-------

This code is free software: you can redistribute it and/or modify it under the
terms of the GNU General Public License as published by the Free Software
Foundation, version 2.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU General Public License for more details.

For full details, please see the file named COPYING in the top directory of the
source tree. You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.


Embedded external projects
--------------------------

This tool uses external softwares, scripts, libraries and artworks:

    OOOP
    Copyright (c) 2010-211, Pedro Gracia <pedro.gracia@impulzia.com>, http://www.impulzia.com
    Released under the GNU GPL v3 license.
    Source: http://github.com/lasarux/ooop

    Crystal Project Icons
    Copyright (c) 2006-2007, Everaldo Coelho <everaldo@everaldo.com>, http://www.everaldo.com
    Released under the LGPL license.
    Source: http://www.kde-look.org/content/show.php/Crystal+Project?content=60475

    Buildout's bootstrap.py
    Copyright (c) 2006 Zope Corporation and Contributors
    Distributed under the Zope Public License, version 2.1 (ZPL).
    Source: http://svn.zope.org/repos/main/zc.buildout/trunk/bootstrap/bootstrap.py

