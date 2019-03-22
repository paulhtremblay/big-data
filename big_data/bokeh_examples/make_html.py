from bokeh.plotting import figure
from bokeh.embed import components

def make_head(title):
    return """
<!DOCTYPE html>
<html lang="en">
  
  <head>
    
      <meta charset="utf-8">
      <title>Bokeh Plot</title>
      
      
        
          
        <link rel="stylesheet" href="https://cdn.pydata.org/bokeh/release/bokeh-1.0.4.min.css" type="text/css" />
        
        
          
        <script type="text/javascript" src="https://cdn.pydata.org/bokeh/release/bokeh-1.0.4.min.js"></script>
        <script type="text/javascript">
            Bokeh.set_log_level("info");
        </script>
        
      
      
    
  </head>
    """.format(
            title = title)

def main():
    h = make_head('test')
    plot = figure()
    plot.circle([1,2], [3,4])
    script, div = components(plot)
    f = h
    f +=  '<body>'
    f +=  div
    f += script
    f += '</body>\n<html>'
    print(f)


if __name__ == '__main__':
    main()
