CherryPy + Mako + Formish + OOOP boilerplate
============================================

This is an ugly hack to publish some [OpenERP](http://www.openerp.com/) content
on the web.

It is based on:

* [CherryPy](http://www.cherrypy.org/) web server,
* use [Mako](http://www.makotemplates.org/) for HTML templating,
* [Formish](https://github.com/ish) for HTML form generation and validation,
* [OOOP](https://github.com/lasarux/ooop) to talk to OpenERP server via web services.

This project contains the experimental code I produced while I explored the
feasability of integrating these components. I produce this code while working
for [Smile](http://www.smile.fr/). This code was a proof-of-concept that we
leveraged later for a customer project.



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

