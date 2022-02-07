from html_builder import build_html
from css_builder import build_css
from js_builder import build_js
from find_required_styles import find_required_styles

HTML_DIR = "build/html"
CSS_PREBUILD_DIR="dev/css"
CSS_DIRS = ["build/slate_ui", 'build/css']
JS_PREBUILD_DIR = "dev/js"
JS_DIR = "build/js"

HTML_OUT_DIR = "build/app/public"
CSS_OUT_DIR = "build/app/public/css"
JS_OUT_DIR = "build/app/public/js"

def build(path = "./"):
    build_html(path + HTML_DIR, path + HTML_OUT_DIR)
    style_selectors = find_required_styles(path + HTML_OUT_DIR)
    build_css([path + DIR for DIR in CSS_DIRS], path + CSS_OUT_DIR, style_selectors)
    build_js(path + JS_DIR, path + JS_OUT_DIR)
