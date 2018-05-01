import vincent
world_topo = r'world-countries.topo.json'
geo_data = [{'name': 'countries',
                 'url': world_topo,
                              'feature': 'world-countries'}]

vis = vincent.Map(geo_data=geo_data, scale=200)
#print(dir(vis))
x = vis.to_json()
#print(x)
vis.to_json('bar.json', html_out=True, html_path='bar_template.html')
x = b'<html>\n  <head>\n    <title>Vega Scaffold</title>\n    <script src="http://d3js.org/d3.v3.min.js" charset="utf-8"></script>\n    <script src="http://d3js.org/topojson.v1.min.js"></script>\n    <script src="http://d3js.org/d3.geo.projection.v0.min.js" charset="utf-8"></script>\n    <script src="http://trifacta.github.com/vega/vega.js"></script>\n  </head>\n  <body>\n    <div id="vis"></div>\n  </body>\n<script type="text/javascript">\n// parse a spec and create a visualization view\nfunction parse(spec) {\n  vg.parse.spec(spec, function(chart) { chart({el:"#vis"}).update(); });\n}\nparse("bar.json");\n</script>\n</html>'
x = x.decode('utf8')
with open("bar_template.html", "w") as write_obj:
    write_obj.write(x)
