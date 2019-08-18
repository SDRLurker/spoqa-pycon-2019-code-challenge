import os
from app import app
from flask import render_template
import markdown2
from bs4 import BeautifulSoup
import urllib.parse

STYLE = """<style>
.blinking{
    animation:blinkingText 2.0s infinite;
}

@keyframes blinkingText{
    0%{     color: #000;    }
    49%{    color: transparent; }
    50%{    color: transparent; }
    99%{    color:transparent;  }
    100%{   color: #000;    }
}
</style>"""
def get_md_contents():
    text = "PYTHONISTAS"
    filename = os.path.join(app.root_path, '..', 'README.md')
    with open(filename) as f:
        text = ""
        for line in f.readlines():
            text += line
    extras = ["fenced-code-blocks","target-blank-links","tables"]
    html = markdown2.markdown(text, extras=extras)
    html = "<html><head></head><body>%s</body></html>" % html
    soup = BeautifulSoup(html, features="html.parser")
    text = ""
    for line in str(soup).split("\n"):
         if line.find("PYTHONISTAS") >= 0:
             text += "<span class='blinking'>" + line + "</span>"
         else:
             text += line
    text = text.replace("<head>", "<head>"+STYLE)
    return text

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def path_func(path):
    return get_md_contents()
