<%inherit file="base.mako"/>

<%block name="title">Partner list</%block>

<ul>
% for (id, name) in partners:
    <li><a href="/view/${id}">${name}</a> (<a href="/edit/${id}">edit</a>)</li>
% endfor
</ul>

