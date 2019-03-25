from bokeh.plotting  import figure, show
import numpy as np

def plot_func():
    x = np.linspace(0,1,100)
    print(x)
    y = [x * x for x in x]
    print(y)

if __name__ == '__main__':
    p = plot_func()
    show(p)

