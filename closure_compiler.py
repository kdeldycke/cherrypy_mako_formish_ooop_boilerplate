#!/usr/bin/python
# Base on: http://code.google.com/closure/compiler/docs/api-tutorial1.html

import httplib, urllib, sys, os

# Concatenate all JS files to one string
js_code = []
current_folder = os.path.dirname(__file__)
for js_file in sys.argv[1:]:
    js_path = os.path.join(current_folder, js_file)
    f = open(js_path, 'r')
    js_code.append(f.read())

params = urllib.urlencode([
    ('js_code', '\n\n'.join(js_code)),
    ('compilation_level', 'SIMPLE_OPTIMIZATIONS'),
#    ('compilation_level', 'ADVANCED_OPTIMIZATIONS'),
    ('output_format', 'text'),
    ('output_info', 'compiled_code'),
  ])

headers = { "Content-type": "application/x-www-form-urlencoded" }
conn = httplib.HTTPConnection('closure-compiler.appspot.com')
conn.request('POST', '/compile', params, headers)
response = conn.getresponse()
data = response.read()
print data
conn.close
