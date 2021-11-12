import { getElementStyleAsNumber, getElementStylesAsNumberSum } from './utils.js';

let sticky = document.querySelectorAll(".sticky");

function updateBanners() {
    for (let element of sticky) {
        let elementStyle = getComputedStyle(element);
        if (elementStyle.position != "fixed") {
            if (element.getBoundingClientRect().top < 0) {
                element.parentElement.style.height = getElementStylesAsNumberSum(elementStyle.height, elementStyle.marginTop, elementStyle.marginBottom, elementStyle.paddingTop, elementStyle.paddingBottom) + "px";
                element.parentElement.style.width = getElementStylesAsNumberSum(elementStyle.width, elementStyle.marginRight, elementStyle.marginLeft) + "px";
                element.style.position = "fixed";
                element.style.zIndex = 99;
                elementStyle = getComputedStyle(element);
                element.setAttribute("originalpostion", getElementStyleAsNumber(elementStyle.top));
                element.style.top = "0px";
            }
        } else {
            element.style.top = "0px";
            element.parentElement.style.height = getElementStylesAsNumberSum(elementStyle.height, elementStyle.marginTop, elementStyle.marginBottom, elementStyle.paddingTop, elementStyle.paddingBottom) + "px";
            element.parentElement.style.width = getElementStylesAsNumberSum(elementStyle.width, elementStyle.marginRight, elementStyle.marginLeft) + "px";
            if (window.scrollY <= Number(element.getAttribute("originalpostion"))) {
                element.style.top = Number(element.getAttribute("originalpostion")) - window.scrollY + "px";
            }
        }
    }
}

function resetBanners() {
    for (let element of sticky) {
        element.removeAttribute('style');
        element.removeAttribute('originalpostion');
        element.parentElement.removeAttribute('style');
        element.parentElement.removeAttribute('style');
    }

    updateBanners();
}

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
