from directories import *
from html_builder import build_html
from css_builder import build_css
from js_builder import build_js
from find_required_styles import find_required_styles
from transfer_file import transfer

def build(path = "./"):
    # Create working HTML in public dir from HTML templates in src.
    build_html(path + HTML_DIR, path + HTML_OUT_DIR)
    # Transfer the SCSS output in dev to slate.css in build. @SLATE_OMIT_NEXT_LINE
    transfer(CSS_PREBUILD_DIR + "/style.css", SLATE_CSS_DIR + "/slate.css")
    # From the built HTML in public determine the required styles to build into optimised CSS.
    style_selectors = find_required_styles(path + HTML_OUT_DIR)
    # Create the public app CSS using the discovered CSS selectors.
    build_css((SLATE_CSS_DIR, BUILD_CSS_DIR), path + CSS_OUT_DIR, style_selectors)
    # TODO: run Babel for Slate JS before transfer (dev/js/src --> dev/js/lib).
    # Optimise and transfer Slate JS to build public. @SLATE_OMIT_NEXT_LINE
    build_js(path + JS_DIR, path + JS_OUT_DIR)
