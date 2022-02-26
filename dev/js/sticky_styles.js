import { getElementStyleAsNumber, getElementStylesAsNumberSum } from './utils.js';

let sticky = document.querySelectorAll(".sticky");

function updateBanners() {
    for (let element of sticky) {
        let elementStyle = getComputedStyle(element);
        if (elementStyle.position != "fixed") {
            if (element.getBoundingClientRect().top < 0) {

                let placeholder = document.createElement("div");
                placeholder.style.height = getElementStylesAsNumberSum(elementStyle.height) + "px";
                placeholder.style.width = getElementStylesAsNumberSum(elementStyle.width, elementStyle.marginLeft, elementStyle.marginRight) + "px";
                placeholder.style.display = elementStyle.display;
                placeholder.className = "sticky-placeholder";

                element.style.position = "fixed";
                element.style.zIndex = 99;
                elementStyle = getComputedStyle(element);
                element.setAttribute("originalPosition", getElementStyleAsNumber(elementStyle.top));
                element.style.top = "0px";

                element.parentElement.insertBefore(placeholder, element);
            }
        } else {
            element.style.top = "0px";
            let placeholder = element.parentElement.children[Array.prototype.indexOf.call(element.parentElement.children, element) - 1];

            placeholder.style.height = getElementStylesAsNumberSum(elementStyle.height) + "px";
            placeholder.style.width = getElementStylesAsNumberSum(elementStyle.width, elementStyle.marginLeft, elementStyle.marginRight) + "px";

            if (window.scrollY <= Number(element.getAttribute("originalPosition"))) {
                element.style.top = Number(element.getAttribute("originalPosition")) - window.scrollY + "px";
            }
        }
    }
}

function resetBanners() {
    for (let element of sticky) {
        element.removeAttribute('style');
        element.removeAttribute('originalPosition');

        if (Array.prototype.indexOf.call(element.parentElement.children, element) - 1 >= 0) {
            let placeholder = element.parentElement.children[Array.prototype.indexOf.call(element.parentElement.children, element) - 1];
            if (placeholder.classList.contains("sticky-placeholder")) {
                element.parentElement.removeChild(placeholder);
            }
        }
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
