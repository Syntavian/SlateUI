(function(){function r(e,n,t){function o(i,f){if(!n[i]){if(!e[i]){var c="function"==typeof require&&require;if(!f&&c)return c(i,!0);if(u)return u(i,!0);var a=new Error("Cannot find module '"+i+"'");throw a.code="MODULE_NOT_FOUND",a}var p=n[i]={exports:{}};e[i][0].call(p.exports,function(r){var n=e[i][1][r];return o(n||r)},p,p.exports,r,e,n,t)}return n[i].exports}for(var u="function"==typeof require&&require,i=0;i<t.length;i++)o(t[i]);return o}return r})()({1:[function(require,module,exports){
function _createForOfIteratorHelper(o, allowArrayLike) { var it = typeof Symbol !== "undefined" && o[Symbol.iterator] || o["@@iterator"]; if (!it) { if (Array.isArray(o) || (it = _unsupportedIterableToArray(o)) || allowArrayLike && o && typeof o.length === "number") { if (it) o = it; var i = 0; var F = function F() {}; return { s: F, n: function n() { if (i >= o.length) return { done: true }; return { done: false, value: o[i++] }; }, e: function e(_e) { throw _e; }, f: F }; } throw new TypeError("Invalid attempt to iterate non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method."); } var normalCompletion = true, didErr = false, err; return { s: function s() { it = it.call(o); }, n: function n() { var step = it.next(); normalCompletion = step.done; return step; }, e: function e(_e2) { didErr = true; err = _e2; }, f: function f() { try { if (!normalCompletion && it["return"] != null) it["return"](); } finally { if (didErr) throw err; } } }; }

function _unsupportedIterableToArray(o, minLen) { if (!o) return; if (typeof o === "string") return _arrayLikeToArray(o, minLen); var n = Object.prototype.toString.call(o).slice(8, -1); if (n === "Object" && o.constructor) n = o.constructor.name; if (n === "Map" || n === "Set") return Array.from(o); if (n === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)) return _arrayLikeToArray(o, minLen); }

function _arrayLikeToArray(arr, len) { if (len == null || len > arr.length) len = arr.length; for (var i = 0, arr2 = new Array(len); i < len; i++) { arr2[i] = arr[i]; } return arr2; }

var switchButtons = document.querySelectorAll(".active,.inactive");

function switchClicked(button) {
  if (button.classList.contains("active") || button.classList.contains("inactive")) {
    button.classList.toggle("active");
    button.classList.toggle("inactive");
  }
}

function initialiseSwitch(button) {
  button.addEventListener("click", function (e) {
    return switchClicked(button);
  });
}

var _iterator = _createForOfIteratorHelper(switchButtons),
    _step;

try {
  for (_iterator.s(); !(_step = _iterator.n()).done;) {
    var button = _step.value;
    initialiseSwitch(button);
  }
} catch (err) {
  _iterator.e(err);
} finally {
  _iterator.f();
}
},{}],2:[function(require,module,exports){
function _createForOfIteratorHelper(o, allowArrayLike) { var it = typeof Symbol !== "undefined" && o[Symbol.iterator] || o["@@iterator"]; if (!it) { if (Array.isArray(o) || (it = _unsupportedIterableToArray(o)) || allowArrayLike && o && typeof o.length === "number") { if (it) o = it; var i = 0; var F = function F() {}; return { s: F, n: function n() { if (i >= o.length) return { done: true }; return { done: false, value: o[i++] }; }, e: function e(_e) { throw _e; }, f: F }; } throw new TypeError("Invalid attempt to iterate non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method."); } var normalCompletion = true, didErr = false, err; return { s: function s() { it = it.call(o); }, n: function n() { var step = it.next(); normalCompletion = step.done; return step; }, e: function e(_e2) { didErr = true; err = _e2; }, f: function f() { try { if (!normalCompletion && it["return"] != null) it["return"](); } finally { if (didErr) throw err; } } }; }

function _unsupportedIterableToArray(o, minLen) { if (!o) return; if (typeof o === "string") return _arrayLikeToArray(o, minLen); var n = Object.prototype.toString.call(o).slice(8, -1); if (n === "Object" && o.constructor) n = o.constructor.name; if (n === "Map" || n === "Set") return Array.from(o); if (n === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)) return _arrayLikeToArray(o, minLen); }

function _arrayLikeToArray(arr, len) { if (len == null || len > arr.length) len = arr.length; for (var i = 0, arr2 = new Array(len); i < len; i++) { arr2[i] = arr[i]; } return arr2; }

var imageCarousels = document.querySelectorAll(".image-carousel");
var currentButtonTheme = "";

function px(value) {
  return value + "px";
}

function cycleCarousel(index, offset, maxDimension) {
  var imageCarouselElement = imageCarousels[index];
  var maxIndex = 0;
  var maxPosition = 0;

  for (var i = 0; i < imageCarouselElement.querySelectorAll(".image,.placeholder").length; i++) {
    var child = imageCarouselElement.querySelectorAll(".image,.placeholder")[i];

    if (Number(child.style.zIndex) > maxIndex) {
      maxIndex = Number(child.style.zIndex);
      maxPosition = i;
    }
  }

  if (imageCarouselElement.querySelectorAll(".image,.placeholder")[maxPosition + offset].classList.contains("placeholder")) {
    return;
  }

  var pastMax = false;

  var _iterator = _createForOfIteratorHelper(imageCarouselElement.querySelectorAll(".image,.placeholder")),
      _step;

  try {
    for (_iterator.s(); !(_step = _iterator.n()).done;) {
      var _child = _step.value;

      if (!pastMax) {
        if (_child.style.zIndex == maxIndex || offset < 0 && Number(_child.style.zIndex) - offset == maxIndex) {
          pastMax = true;
        }

        _child.style.zIndex = Number(_child.style.zIndex) - offset;
      } else {
        _child.style.zIndex = Number(_child.style.zIndex) + offset;
      }

      if (_child.style.zIndex < 0) {
        _child.style.display = "none";
      } else {
        _child.style.display = "flex";
      }

      _child.style.width = maxDimension + maxDimension / 2 * (Number(_child.style.zIndex) / maxIndex) + "px";
      _child.style.height = maxDimension + maxDimension / 2 * (Number(_child.style.zIndex) / maxIndex) + "px";
      _child.style.minWidth = maxDimension + maxDimension / 2 * (Number(_child.style.zIndex) / maxIndex) + "px";
      _child.style.minHeight = maxDimension + maxDimension / 2 * (Number(_child.style.zIndex) / maxIndex) + "px";
    }
  } catch (err) {
    _iterator.e(err);
  } finally {
    _iterator.f();
  }

  if (imageCarouselElement.querySelectorAll(".image,.placeholder")[maxPosition + offset + 1].classList.contains("placeholder")) {
    imageCarouselElement.children[imageCarouselElement.children.length - 1].classList.add("disabled");
  } else {
    imageCarouselElement.children[imageCarouselElement.children.length - 1].classList.remove("disabled");
  }

  if (imageCarouselElement.querySelectorAll(".image,.placeholder")[maxPosition + offset - 1].classList.contains("placeholder")) {
    imageCarouselElement.children[0].classList.add("disabled");
  } else {
    imageCarouselElement.children[0].classList.remove("disabled");
  }
}

function initialiseImageCarousel(index) {
  var imageCarouselElement = imageCarousels[index];
  var childCount = imageCarouselElement.children.length;
  var zIndexOffset = Math.floor(childCount / 2 - 0.5);
  var maxImageSize = 0;
  var maxCarouselSize = 0;
  var margin = getComputedStyle(imageCarouselElement.children[0]).marginLeft; // Keep the max number of images in a carousel <= 5

  if (zIndexOffset > 2) {
    zIndexOffset = 2;
  }

  for (var i = 0; i < zIndexOffset; i++) {
    var placeholder = document.createElement("div");
    placeholder.classList.add("placeholder");
    placeholder.style.marginLeft = margin;
    placeholder.style.marginRight = margin;
    imageCarouselElement.prepend(placeholder);
    placeholder = document.createElement("div");
    placeholder.classList.add("placeholder");
    placeholder.style.marginLeft = margin;
    placeholder.style.marginRight = margin;
    imageCarouselElement.append(placeholder);
  } // let carouselStyle = getComputedStyle(imageCarouselElement);


  for (var _i = 0; _i < imageCarouselElement.children.length; _i++) {
    var style = getComputedStyle(imageCarouselElement.children[_i]);

    if (Number(style.height.replace("px", "")) > maxImageSize) {
      maxImageSize = Number(style.height.replace("px", ""));
    }

    if (Number(style.width.replace("px", "")) > maxImageSize) {
      maxImageSize = Number(style.width.replace("px", ""));
    }
  }

  for (var _i2 = 0; _i2 < imageCarouselElement.children.length; _i2++) {
    var zIndex = -Math.abs(_i2 - Math.floor(imageCarouselElement.children.length / 2)) + zIndexOffset;
    imageCarouselElement.children[_i2].style.zIndex = zIndex;

    if (zIndex < 0) {
      imageCarouselElement.children[_i2].style.display = "none";
    }

    var newSize = maxImageSize + maxImageSize / 2 * (zIndex / zIndexOffset);
    maxCarouselSize = maxCarouselSize < newSize ? newSize : maxCarouselSize;
    var formattedSize = px(newSize);
    imageCarouselElement.children[_i2].style.width = formattedSize;
    imageCarouselElement.children[_i2].style.height = formattedSize;
    imageCarouselElement.children[_i2].style.minWidth = formattedSize;
    imageCarouselElement.children[_i2].style.minHeight = formattedSize;
  }

  for (var _i3 = 0; _i3 < imageCarouselElement.children.length; _i3++) {
    imageCarouselElement.children[_i3].style.marginLeft = px(-maxCarouselSize / 4);
    imageCarouselElement.children[_i3].style.marginRight = px(-maxCarouselSize / 4);
  }

  var leftButton = document.createElement("div");
  var rightButton = document.createElement("div");
  var leftButtonStyle = getComputedStyle(imageCarouselElement, "::before");
  var rightButtonStyle = getComputedStyle(imageCarouselElement, "::after");
  leftButton.textContent = leftButtonStyle.content.slice(1, leftButtonStyle.content.length - 1);

  if (currentButtonTheme) {
    leftButton.classList.value = currentButtonTheme;
  } else {
    leftButton.classList.add("button", "fill");
  }

  leftButton.style.fontSize = leftButtonStyle.fontSize;
  leftButton.style.fontWeight = leftButtonStyle.fontWeight;
  leftButton.style.zIndex = zIndexOffset + 1;
  rightButton.textContent = rightButtonStyle.content.slice(1, rightButtonStyle.content.length - 1);

  if (currentButtonTheme) {
    rightButton.classList.value = currentButtonTheme;
  } else {
    rightButton.classList.add("button", "fill");
  }

  rightButton.style.fontSize = rightButtonStyle.fontSize;
  rightButton.style.fontWeight = rightButtonStyle.fontWeight;
  rightButton.style.zIndex = zIndexOffset + 1;
  imageCarouselElement.prepend(leftButton);
  imageCarouselElement.append(rightButton);
  leftButton.addEventListener("click", function (e) {
    return cycleCarousel(index, -1, maxImageSize);
  });
  rightButton.addEventListener("click", function (e) {
    return cycleCarousel(index, 1, maxImageSize);
  });
}

function resetCarousel(index) {
  var imageCarouselElement = imageCarousels[index];
  currentButtonTheme = imageCarouselElement.querySelectorAll(".button")[0].classList.value;

  var _iterator2 = _createForOfIteratorHelper(imageCarouselElement.querySelectorAll(".placeholder,.button")),
      _step2;

  try {
    for (_iterator2.s(); !(_step2 = _iterator2.n()).done;) {
      var child = _step2.value;
      child.parentElement.removeChild(child);
    }
  } catch (err) {
    _iterator2.e(err);
  } finally {
    _iterator2.f();
  }

  var _iterator3 = _createForOfIteratorHelper(imageCarouselElement.querySelectorAll(".image")),
      _step3;

  try {
    for (_iterator3.s(); !(_step3 = _iterator3.n()).done;) {
      var _child2 = _step3.value;
      _child2.style = "";
    }
  } catch (err) {
    _iterator3.e(err);
  } finally {
    _iterator3.f();
  }

  initialiseImageCarousel(index);
}

function resetCarousels() {
  for (var i = 0; i < imageCarousels.length; i++) {
    resetCarousel(i);
  }
}

for (var i = 0; i < imageCarousels.length; i++) {
  initialiseImageCarousel(i);
}

window.addEventListener("resize", function (e) {
  resetCarousels();
});
},{}],3:[function(require,module,exports){
function _createForOfIteratorHelper(o, allowArrayLike) { var it = typeof Symbol !== "undefined" && o[Symbol.iterator] || o["@@iterator"]; if (!it) { if (Array.isArray(o) || (it = _unsupportedIterableToArray(o)) || allowArrayLike && o && typeof o.length === "number") { if (it) o = it; var i = 0; var F = function F() {}; return { s: F, n: function n() { if (i >= o.length) return { done: true }; return { done: false, value: o[i++] }; }, e: function e(_e) { throw _e; }, f: F }; } throw new TypeError("Invalid attempt to iterate non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method."); } var normalCompletion = true, didErr = false, err; return { s: function s() { it = it.call(o); }, n: function n() { var step = it.next(); normalCompletion = step.done; return step; }, e: function e(_e2) { didErr = true; err = _e2; }, f: function f() { try { if (!normalCompletion && it["return"] != null) it["return"](); } finally { if (didErr) throw err; } } }; }

function _unsupportedIterableToArray(o, minLen) { if (!o) return; if (typeof o === "string") return _arrayLikeToArray(o, minLen); var n = Object.prototype.toString.call(o).slice(8, -1); if (n === "Object" && o.constructor) n = o.constructor.name; if (n === "Map" || n === "Set") return Array.from(o); if (n === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)) return _arrayLikeToArray(o, minLen); }

function _arrayLikeToArray(arr, len) { if (len == null || len > arr.length) len = arr.length; for (var i = 0, arr2 = new Array(len); i < len; i++) { arr2[i] = arr[i]; } return arr2; }

var containers = document.querySelectorAll(".layout-row-center-middle");

function updateLayout() {
  var _iterator = _createForOfIteratorHelper(containers),
      _step;

  try {
    for (_iterator.s(); !(_step = _iterator.n()).done;) {
      var container = _step.value;
      var containerChildren = container.children;

      if (containerChildren.length % 2 === 0) {
        console.warn("A layout center middle component has even children");
      }

      var centerElementIndex = Math.floor(containerChildren.length / 2);

      for (var i = 0; i < containerChildren.length; i++) {
        if (i !== centerElementIndex) {
          containerChildren[i].style.width = '';
          containerChildren[i].style.minWidth = '';
          containerChildren[i].style.maxWidth = '';
        }
      }

      var containerStyle = getComputedStyle(container);

      if (containerStyle.flexDirection === 'row') {
        var containerWidth = Number(containerStyle.width.replace("px", ''));
        var centerWidth = Number(getComputedStyle(containerChildren[centerElementIndex]).width.replace("px", ''));
        var outsideElementMaxWidth = (containerWidth - centerWidth) / 2 / centerElementIndex;

        for (var _i = 0; _i < containerChildren.length; _i++) {
          if (_i !== centerElementIndex) {
            containerChildren[_i].style.width = outsideElementMaxWidth + "px";
            containerChildren[_i].style.minWidth = outsideElementMaxWidth + "px";
            containerChildren[_i].style.maxWidth = outsideElementMaxWidth + "px";
          }
        }
      }
    }
  } catch (err) {
    _iterator.e(err);
  } finally {
    _iterator.f();
  }
}

updateLayout();
window.addEventListener("resize", function (e) {
  updateLayout();
});
},{}],4:[function(require,module,exports){
"use strict";

require("./theme_styles");

require("./button_styles");

require("./image_styles");

require("./layout_styles");

require("./scroll_styles");

require("./sticky_styles");
},{"./button_styles":1,"./image_styles":2,"./layout_styles":3,"./scroll_styles":5,"./sticky_styles":6,"./theme_styles":7}],5:[function(require,module,exports){
var scrollBar = document.getElementById("scroll-bar");
var scrollHandle = document.getElementById("scroll-handle");
var isScrollBarActive = false;

function updateScrollBar() {
  if (scrollBar && scrollHandle) {
    if (!isScrollBarActive) {
      var scrollBarStyle = getComputedStyle(scrollBar);
      scrollHandle.style.height = Number(scrollBarStyle.height.replace("px", "")) * window.innerHeight / document.body.scrollHeight + "px";
      scrollHandle.style.top = Number(scrollBarStyle.height.replace("px", "")) * window.scrollY / document.body.scrollHeight + "px";
    }
  }
}

if (document.body.classList.contains("no-scrollbar")) {
  if (!scrollBar) {
    scrollBar = document.createElement("div");
    scrollBar.id = "scroll-bar";
    scrollBar.classList.add("scroll-bar");
    document.body.appendChild(scrollBar);
  }

  if (!scrollHandle) {
    scrollHandle = document.createElement("div");
    scrollHandle.id = "scroll-handle";
    scrollHandle.classList.add("scroll-handle");
    scrollBar.appendChild(scrollHandle);
  }
}

updateScrollBar();

if (scrollBar && scrollHandle) {
  window.addEventListener("resize", function (e) {
    updateScrollBar();
  });
  scrollHandle.addEventListener("mousedown", function (e) {
    if (e.button === 0) {
      isScrollBarActive = true;
    }
  }, {
    passive: false
  });
  document.addEventListener("mousemove", function (e) {
    if (isScrollBarActive) {
      e.preventDefault();
      var scrollBarStyle = getComputedStyle(scrollBar);
      var targetPosition = Number(scrollHandle.style.top.replace("px", "")) + e.movementY;
      var targetMax = Number(scrollBarStyle.height.replace("px", "")) * (document.body.scrollHeight - window.innerHeight) / document.body.scrollHeight;

      if (targetPosition < 0) {
        targetPosition = 0;
      } else if (targetPosition > targetMax) {
        targetPosition = targetMax;
      }

      scrollHandle.style.top = targetPosition + "px";
      window.scroll({
        top: Number(scrollHandle.style.top.replace("px", "")) * document.body.scrollHeight / Number(scrollBarStyle.height.replace("px", "")),
        left: 0,
        behavior: "instant"
      });
    }
  }, {
    passive: false
  });
  document.addEventListener("mouseup", function (e) {
    isScrollBarActive = false;
  }, {
    passive: false
  });
  document.addEventListener("scroll", function (e) {
    updateScrollBar();
  }, {
    passive: false
  });
  var observer = new ResizeObserver(function () {
    updateScrollBar();
  });
  document.querySelectorAll('textarea').forEach(function (element) {
    observer.observe(element);
  });
}
},{}],6:[function(require,module,exports){
"use strict";

var _utils = require("./utils.js");

function _createForOfIteratorHelper(o, allowArrayLike) { var it = typeof Symbol !== "undefined" && o[Symbol.iterator] || o["@@iterator"]; if (!it) { if (Array.isArray(o) || (it = _unsupportedIterableToArray(o)) || allowArrayLike && o && typeof o.length === "number") { if (it) o = it; var i = 0; var F = function F() {}; return { s: F, n: function n() { if (i >= o.length) return { done: true }; return { done: false, value: o[i++] }; }, e: function e(_e) { throw _e; }, f: F }; } throw new TypeError("Invalid attempt to iterate non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method."); } var normalCompletion = true, didErr = false, err; return { s: function s() { it = it.call(o); }, n: function n() { var step = it.next(); normalCompletion = step.done; return step; }, e: function e(_e2) { didErr = true; err = _e2; }, f: function f() { try { if (!normalCompletion && it["return"] != null) it["return"](); } finally { if (didErr) throw err; } } }; }

function _unsupportedIterableToArray(o, minLen) { if (!o) return; if (typeof o === "string") return _arrayLikeToArray(o, minLen); var n = Object.prototype.toString.call(o).slice(8, -1); if (n === "Object" && o.constructor) n = o.constructor.name; if (n === "Map" || n === "Set") return Array.from(o); if (n === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)) return _arrayLikeToArray(o, minLen); }

function _arrayLikeToArray(arr, len) { if (len == null || len > arr.length) len = arr.length; for (var i = 0, arr2 = new Array(len); i < len; i++) { arr2[i] = arr[i]; } return arr2; }

var sticky = document.querySelectorAll(".sticky");

function updateBanners() {
  var _iterator = _createForOfIteratorHelper(sticky),
      _step;

  try {
    for (_iterator.s(); !(_step = _iterator.n()).done;) {
      var element = _step.value;
      var elementStyle = getComputedStyle(element);

      if (elementStyle.position != "fixed") {
        if (element.getBoundingClientRect().top < 0) {
          var placeholder = document.createElement("div");
          placeholder.style.height = (0, _utils.getElementStylesAsNumberSum)(elementStyle.height) + "px";
          placeholder.style.width = (0, _utils.getElementStylesAsNumberSum)(elementStyle.width, elementStyle.marginLeft, elementStyle.marginRight) + "px";
          placeholder.style.display = elementStyle.display;
          placeholder.className = "sticky-placeholder";
          element.style.position = "fixed";
          element.style.zIndex = 99;
          elementStyle = getComputedStyle(element);
          element.setAttribute("originalPosition", (0, _utils.getElementStyleAsNumber)(elementStyle.top));
          element.style.top = "0px";
          element.parentElement.insertBefore(placeholder, element);
        }
      } else {
        element.style.top = "0px";
        var _placeholder = element.parentElement.children[Array.prototype.indexOf.call(element.parentElement.children, element) - 1];
        _placeholder.style.height = (0, _utils.getElementStylesAsNumberSum)(elementStyle.height) + "px";
        _placeholder.style.width = (0, _utils.getElementStylesAsNumberSum)(elementStyle.width, elementStyle.marginLeft, elementStyle.marginRight) + "px";

        if (window.scrollY <= Number(element.getAttribute("originalPosition"))) {
          element.style.top = Number(element.getAttribute("originalPosition")) - window.scrollY + "px";
        }
      }
    }
  } catch (err) {
    _iterator.e(err);
  } finally {
    _iterator.f();
  }
}

function resetBanners() {
  var _iterator2 = _createForOfIteratorHelper(sticky),
      _step2;

  try {
    for (_iterator2.s(); !(_step2 = _iterator2.n()).done;) {
      var element = _step2.value;
      element.removeAttribute('style');
      element.removeAttribute('originalPosition');

      if (Array.prototype.indexOf.call(element.parentElement.children, element) - 1 >= 0) {
        var placeholder = element.parentElement.children[Array.prototype.indexOf.call(element.parentElement.children, element) - 1];

        if (placeholder.classList.contains("sticky-placeholder")) {
          element.parentElement.removeChild(placeholder);
        }
      }
    }
  } catch (err) {
    _iterator2.e(err);
  } finally {
    _iterator2.f();
  }

  updateBanners();
}

updateBanners();
document.addEventListener("scroll", function (e) {
  updateBanners();
}, {
  passive: false
});
window.addEventListener("resize", function (e) {
  resetBanners();
}, {
  passive: false
});
},{"./utils.js":8}],7:[function(require,module,exports){
function _createForOfIteratorHelper(o, allowArrayLike) { var it = typeof Symbol !== "undefined" && o[Symbol.iterator] || o["@@iterator"]; if (!it) { if (Array.isArray(o) || (it = _unsupportedIterableToArray(o)) || allowArrayLike && o && typeof o.length === "number") { if (it) o = it; var i = 0; var F = function F() {}; return { s: F, n: function n() { if (i >= o.length) return { done: true }; return { done: false, value: o[i++] }; }, e: function e(_e) { throw _e; }, f: F }; } throw new TypeError("Invalid attempt to iterate non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method."); } var normalCompletion = true, didErr = false, err; return { s: function s() { it = it.call(o); }, n: function n() { var step = it.next(); normalCompletion = step.done; return step; }, e: function e(_e2) { didErr = true; err = _e2; }, f: function f() { try { if (!normalCompletion && it["return"] != null) it["return"](); } finally { if (didErr) throw err; } } }; }

function _unsupportedIterableToArray(o, minLen) { if (!o) return; if (typeof o === "string") return _arrayLikeToArray(o, minLen); var n = Object.prototype.toString.call(o).slice(8, -1); if (n === "Object" && o.constructor) n = o.constructor.name; if (n === "Map" || n === "Set") return Array.from(o); if (n === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)) return _arrayLikeToArray(o, minLen); }

function _arrayLikeToArray(arr, len) { if (len == null || len > arr.length) len = arr.length; for (var i = 0, arr2 = new Array(len); i < len; i++) { arr2[i] = arr[i]; } return arr2; }

var elementQuery = "body,div,p,span,a,h1,h2,h3,h4,h5,h6,select,button,.button,.fill,.box,.inline-box,.background,.break,.link,.gradient,.gradient-hover-animation,.form-input,[class^='.shadow'],input,.image,textarea,.scroll-handle,[class^='.border'],canvas,.canvas";
var themeSwitchers = document.querySelectorAll(".theme-selector");
var themedElements = document.querySelectorAll(elementQuery);
var currentTheme = "";

function switchElementThemes(newTheme) {
  themedElements = document.querySelectorAll(elementQuery);

  var _iterator = _createForOfIteratorHelper(themedElements),
      _step;

  try {
    for (_iterator.s(); !(_step = _iterator.n()).done;) {
      var element = _step.value;
      element.classList.remove(currentTheme);
      element.classList.add(newTheme);
    }
  } catch (err) {
    _iterator.e(err);
  } finally {
    _iterator.f();
  }

  currentTheme = newTheme;
}

function updateThemeSwitchers() {
  var _iterator2 = _createForOfIteratorHelper(themeSwitchers),
      _step2;

  try {
    for (_iterator2.s(); !(_step2 = _iterator2.n()).done;) {
      var button = _step2.value;
      var style = getComputedStyle(button);
      var select = button.querySelector("select");
      select.style.width = Number(style.width.replace("px", "")) + 18 + "px";
      select.style.height = Number(style.height.replace("px", "")) + 18 + "px";
    }
  } catch (err) {
    _iterator2.e(err);
  } finally {
    _iterator2.f();
  }
}

function initialiseThemeSwitcher(button) {
  var label = document.createElement("span");
  label.textContent = getComputedStyle(button, "::before").content.replaceAll('"', '');
  button.appendChild(label);
  var themes = getComputedStyle(button, "::after").content;
  var select = document.createElement("select");
  var style = getComputedStyle(button);
  select.style.width = style.width;
  select.style.height = style.height;

  var _iterator3 = _createForOfIteratorHelper(themes.replaceAll('\\"', '').replaceAll('"', '').replaceAll(' ', '').replaceAll('(', '').replaceAll(')', '').split(',')),
      _step3;

  try {
    for (_iterator3.s(); !(_step3 = _iterator3.n()).done;) {
      var string = _step3.value;
      var splitString = string.split(':');

      if (splitString.length === 4) {
        var text = splitString[0];
        var option = document.createElement("option");

        if (currentTheme === "") {
          currentTheme = text;
        }

        text = text[0].toUpperCase() + text.slice(1);
        option.textContent = text;
        option.value = text;
        select.appendChild(option);
      }
    }
  } catch (err) {
    _iterator3.e(err);
  } finally {
    _iterator3.f();
  }

  button.appendChild(select);
  themedElements = document.querySelectorAll(elementQuery);

  var _iterator4 = _createForOfIteratorHelper(themedElements),
      _step4;

  try {
    for (_iterator4.s(); !(_step4 = _iterator4.n()).done;) {
      var element = _step4.value;
      element.classList.add(currentTheme);
    }
  } catch (err) {
    _iterator4.e(err);
  } finally {
    _iterator4.f();
  }

  button.addEventListener("mouseleave", function (e) {
    select.blur();
  });
  select.addEventListener("change", function (e) {
    switchElementThemes(select.value.toLowerCase());
  });
  window.addEventListener("resize", function (e) {
    updateThemeSwitchers();
  });
}

var _iterator5 = _createForOfIteratorHelper(themeSwitchers),
    _step5;

try {
  for (_iterator5.s(); !(_step5 = _iterator5.n()).done;) {
    var button = _step5.value;
    initialiseThemeSwitcher(button);
  }
} catch (err) {
  _iterator5.e(err);
} finally {
  _iterator5.f();
}
},{}],8:[function(require,module,exports){
"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.getElementStyleAsNumber = getElementStyleAsNumber;
exports.getElementStylesAsNumberSum = getElementStylesAsNumberSum;

function getElementStyleAsNumber(style) {
  return Number(style.replace("px", ""));
}

function getElementStylesAsNumberSum() {
  var sum = 0;

  for (var _len = arguments.length, styles = new Array(_len), _key = 0; _key < _len; _key++) {
    styles[_key] = arguments[_key];
  }

  for (var _i = 0, _styles = styles; _i < _styles.length; _i++) {
    var style = _styles[_i];
    sum += Number(style.replace("px", ""));
  }

  return sum;
}
},{}]},{},[4]);
