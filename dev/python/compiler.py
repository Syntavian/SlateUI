from html_compiler import compile_html
from css_compiler import compile_css
from js_compiler import compile_js

HTML_DIR = ""
CSS_DIR = ""
JS_DIR = ""

HTML_OUT_DIR = ""
CSS_OUT_DIR = ""
JS_OUT_DIR = ""

def compile(path = ""):
    compile_html(path + HTML_DIR, HTML_OUT_DIR)
    compile_css(path + CSS_DIR, CSS_OUT_DIR)
    compile_js(path + JS_DIR, JS_OUT_DIR)
