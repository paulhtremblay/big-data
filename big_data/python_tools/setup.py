import sys, os
from distutils.core import setup
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

#script_name1 =  os.path.join('scripts', 'asciimath2fo.py')
#script_name2 =  os.path.join('scripts', 'asciimath2html.py')


setup(name="python_big_data_tools",
    version= ".23" ,
    description="tools to manipulate data",
    long_description=read('README.rst'),
    author="Paul Tremblay",
    author_email="Paul Henry Tremblay <paultremblay@gmail.com> ",
    license = 'BSD',
    url = "https://sourceforge.net/projects/asciimathpython/",
    classifiers=[
        "Topic :: Big Data",
        "License :: OSI Approved :: BSD License",
        "Development Status :: 3 - Development",
        "Programming Language :: Python",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
    ],
    platforms='any',
    packages=['big_data_tools', 'big_data_tools/bokeh_tools'],
    #scripts=[script_name1, script_name2],
    data_files=[('map_data',
        ['big_data_tools/bokeh_tools/data/cb_2017_us_county_5m.zip',
        'big_data_tools/bokeh_tools/data/cb_2017_us_state_5m.zip'
        ])],

    )
