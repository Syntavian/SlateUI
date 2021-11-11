import { getElementStyleAsNumber, getElementStylesAsNumberSum } from './utils.js';

let banners = document.querySelectorAll(".banner");

function updateBanners() {
    for (let banner of banners) {
        if (banner.classList.contains("sticky")) {
            let bannerStyle = getComputedStyle(banner);
            if (bannerStyle.position != "fixed") {
                if (banner.getBoundingClientRect().top < 0) {
                    banner.parentElement.style.height = getElementStylesAsNumberSum(bannerStyle.height, bannerStyle.marginTop, bannerStyle.marginBottom, bannerStyle.paddingTop, bannerStyle.paddingBottom) + "px";
                    banner.style.position = "fixed";
                    bannerStyle = getComputedStyle(banner);
                    banner.setAttribute("originalpostion", getElementStyleAsNumber(bannerStyle.top));
                    banner.style.top = "0px";
                }
            } else {
                banner.parentElement.style.height = getElementStylesAsNumberSum(bannerStyle.height, bannerStyle.marginTop, bannerStyle.marginBottom, bannerStyle.paddingTop, bannerStyle.paddingBottom) + "px";
                if (window.scrollY <= Number(banner.getAttribute("originalpostion"))) {
                    banner.style.top = Number(banner.getAttribute("originalpostion")) - window.scrollY + "px";
                }
            }
        }
    }
}

document.addEventListener("scroll", function (e) {
    updateBanners();
}, {
    passive: false
});
