<%def name="breadcrumb()">
    <%
        breadcrumb_items = [cherrypy.request.base]
        for p in [i for i in cherrypy.request.path_info.split("/") if len(i) > 0]:
            breadcrumb_items.append(os.path.join(breadcrumb_items[-1], p))
    %>
    % for item in breadcrumb_items:
        &gt; <a href="${item}">${item}</a>
    % endfor
</%def>


<%def name="render_date(d)">
    %if d:
        <%
            LOCAL_DATE_FORMAT = "%d/%m/%Y"
        %>
        ${d.strftime(LOCAL_DATE_FORMAT)}
    %endif
</%def>


<%def name="render_datetime(d)">
    %if d:
        <%
            LOCAL_DATETIME_FORMAT = "%d/%m/%Y %H:%M"
        %>
        ${d.strftime(LOCAL_DATETIME_FORMAT)}
    %endif
</%def>


<%def name="render_eta(d)">
    %if d:
        <%
            from datetime import date
            delta = d - date.today()
        %>
        ${delta.days} days
    %endif
</%def>
