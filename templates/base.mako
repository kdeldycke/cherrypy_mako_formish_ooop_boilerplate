<%namespace name="widgets" file="widgets.mako"/>

<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
        <title><%block name="title">Default title</%block> | OpenERP Web Publishing Module</title>
        <link rel="stylesheet" type="text/css" href="/static/formish.css" type="text/css"/>
        <link rel="stylesheet" type="text/css" href="/static/style.css" type="text/css"/>
        <link rel="shortcut icon" href="/favicon.png"/>
        <script src="/static/formish.js" type="text/javascript"></script>
    </head>
    <body>
        <h1>${self.title()}</h1>
        ${widgets.breadcrumb()}
        ${self.body()}
    </body>
</html>
