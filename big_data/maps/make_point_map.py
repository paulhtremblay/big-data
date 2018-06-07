import pprint
pp = pprint.PrettyPrinter(indent=4)
import json

d = {
  "$schema": "https://vega.github.io/schema/vega/v3.json",
  "width": 900,
  "height": 560,
  "padding": {"top": 0, "left": 0, "right": 0, "bottom": 0},
  "signals": [],
  "data": [

  {
    "name": "states",
    "url": "us-10m.json",
    "format": {"type": "topojson", "feature": "states"},
    "transform": [
      {
        "type": "geopath",
        "projection": "projection1"
      }
    ]
  },
  {
      "name":"points",
      "values":[
        {"longitude": "-89.23450472", "latitude": 31.95376472, "num":55},
        {"longitude": "-95.01792778", "latitude": 30.68586111, "num":10}
  ],
  "transform": [
    {
      "type": "geopoint",
      "projection": "projection1",
      "fields": ["longitude", "latitude"]
    }
  ]
  }
],
  "scales": [
  {"name":"size",
  "type":"linear",
  "domain": {"data": "points", "field": "num"},
          "range": [16, 1000]
  }
  ],
 "projections": [
  {
    "name": "projection1",
    "type": "albersUsa",
    "scale": 1200,
    "translate": [{"signal": "width / 2"}, {"signal": "height / 2"}]
  }
],
"marks": [
  {
    "type": "path",
    "from": {"data": "states"},
    "encode": {
      "enter": {
        "fill": {"value": "#dedede"},
        "stroke": {"value": "white"}
      },
      "update": {
        "path": {"field": "path"}
      }
    }
  },
{
"type": "symbol",
  "from": {"data": "points"},
  "encode": {
    "enter": {
      "fill": {"value": "steelblue"},
      "fillOpacity": {"value": 0.8},
      "stroke": {"value": "white"},
      "strokeWidth": {"value": .1},
   "color": {"field": "num", "type": "ordinal"}
    },
    "update": {
      "x": {"field": "x"},
      "y": {"field": "y"}
    }
  }
}

]
}

def make_json(data):
    d['data'][1]['values'] = data
    with open('temp_data/map_points.json', 'w') as write_obj:
        json.dump(d, write_obj)

def make_html():
    with open('temp_data/map_points.html', 'w') as write_obj:
        write_obj.write("""<html>
<head>
  <script src="https://cdn.jsdelivr.net/npm/vega@3.3.1"></script>

  <script type="text/javascript">
    var view;

    vega.loader()
      .load('map_points.json')
      .then(function(data) { render(JSON.parse(data)); });

    function render(spec) {
      view = new vega.View(vega.parse(spec))
        .renderer('canvas')  // set renderer (canvas or svg)
        .initialize('#view') // initialize view within parent DOM container
        .hover()             // enable hover encode set processing
        .run();
    }
  </script>
</head>
<body>
  <div id="view"></div>
</body>

</html>""")

def make_map(data):
    make_html()
    make_json(data)

def main():
    data = [ {'num': 55, 'latitude': 31.95376472, 'longitude': '-89.23450472'},
            {'num': 10, 'latitude': 30.68586111, 'longitude': '-95.01792778'},
            {'num': 30, 'latitude': 32.68586111, 'longitude': '-92.01792778'}
            ]
    make_map(data)

if __name__ == '__main__':
    main()

