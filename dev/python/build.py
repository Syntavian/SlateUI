from python.css_build.css_builder import build_css
from python.css_build.find_required_styles import find_required_styles
from python.debug import debug
from python.directories import *
from python.html_build.html_builder import build_html
from python.js_build.js_builder import build_js
from python.utils.file_utils import transfer


@debug
def build(_path: str = "./") -> None:
    # Create working HTML in public dir from HTML templates in src.
    build_html(_path + SLATE_DIR, _path + HTML_DIR, _path + HTML_OUT_DIR)
    # Transfer the SCSS output in dev to slate.css in build. @SLATE_OMIT_NEXT_LINE
    transfer(CSS_PREBUILD_DIR + "/style.css", SLATE_DIR + "/slate.css")
    # From the built HTML in public determine the required styles to build into optimised CSS.
    style_selectors = find_required_styles(_path + HTML_OUT_DIR)
    # Create the public app CSS using the discovered CSS selectors.
    build_css(SLATE_DIR, CSS_DIR, _path + CSS_OUT_DIR, style_selectors)
    # TODO: run Babel for Slate JS before transfer (dev/js/src --> dev/js/lib).
    # Optimise and transfer Slate JS to build public. @SLATE_OMIT_NEXT_LINE
    build_js(_path + SLATE_DIR, _path + JS_OUT_DIR)
