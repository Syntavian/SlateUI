let switchButtons = Array.from(document.querySelectorAll(".active,.inactive"));
function switchClicked(button1) {
    if (button1.classList.contains("active") || button1.classList.contains("inactive")) {
        button1.classList.toggle("active");
        button1.classList.toggle("inactive");
    }
}
function initialiseSwitch(button2) {
    button2.addEventListener("click", (e)=>switchClicked(button2));
}
for (let button of switchButtons)initialiseSwitch(button);
function getElementStyleAsNumber(style) {
    return Number(style.replace("px", ""));
}
function getElementStylesAsNumberSum(...styles) {
    let sum = 0;
    for (let style of styles)sum += Number(style.replace("px", ""));
    return sum;
}
function px(value) {
    return value + "px";
}
let imageCarousels = document.querySelectorAll(".image-carousel");
let currentButtonTheme = "";
function cycleCarousel(index, offset, maxDimension) {
    let imageCarouselElement = imageCarousels[index];
    let maxIndex = 0;
    let maxPosition = 0;
    for(let i1 = 0; i1 < imageCarouselElement.querySelectorAll(".image,.placeholder").length; i1++){
        let child = imageCarouselElement.querySelectorAll(".image,.placeholder")[i1];
        if (Number(child.style.zIndex) > maxIndex) {
            maxIndex = Number(child.style.zIndex);
            maxPosition = i1;
        }
    }
    if (imageCarouselElement.querySelectorAll(".image,.placeholder")[maxPosition + offset].classList.contains("placeholder")) return;
    let pastMax = false;
    for (let child of imageCarouselElement.querySelectorAll(".image,.placeholder")){
        if (!pastMax) {
            if (child.style.zIndex == maxIndex || offset < 0 && Number(child.style.zIndex) - offset == maxIndex) pastMax = true;
            child.style.zIndex = Number(child.style.zIndex) - offset;
        } else child.style.zIndex = Number(child.style.zIndex) + offset;
        if (child.style.zIndex < 0) child.style.display = "none";
        else child.style.display = "flex";
        child.style.width = maxDimension + maxDimension / 2 * (Number(child.style.zIndex) / maxIndex) + "px";
        child.style.height = maxDimension + maxDimension / 2 * (Number(child.style.zIndex) / maxIndex) + "px";
        child.style.minWidth = maxDimension + maxDimension / 2 * (Number(child.style.zIndex) / maxIndex) + "px";
        child.style.minHeight = maxDimension + maxDimension / 2 * (Number(child.style.zIndex) / maxIndex) + "px";
    }
    if (imageCarouselElement.querySelectorAll(".image,.placeholder")[maxPosition + offset + 1].classList.contains("placeholder")) imageCarouselElement.children[imageCarouselElement.children.length - 1].classList.add("disabled");
    else imageCarouselElement.children[imageCarouselElement.children.length - 1].classList.remove("disabled");
    if (imageCarouselElement.querySelectorAll(".image,.placeholder")[maxPosition + offset - 1].classList.contains("placeholder")) imageCarouselElement.children[0].classList.add("disabled");
    else imageCarouselElement.children[0].classList.remove("disabled");
}
function initialiseImageCarousel(index) {
    let imageCarouselElement = imageCarousels[index];
    let childCount = imageCarouselElement.children.length;
    let zIndexOffset = Math.floor(childCount / 2 - 0.5);
    let maxImageSize = 0;
    let maxCarouselSize = 0;
    let margin = getComputedStyle(imageCarouselElement.children[0]).marginLeft;
    if (zIndexOffset > 2) zIndexOffset = 2;
    for(let i5 = 0; i5 < zIndexOffset; i5++){
        let placeholder = document.createElement("div");
        placeholder.classList.add("placeholder");
        placeholder.style.marginLeft = margin;
        placeholder.style.marginRight = margin;
        imageCarouselElement.prepend(placeholder);
        placeholder = document.createElement("div");
        placeholder.classList.add("placeholder");
        placeholder.style.marginLeft = margin;
        placeholder.style.marginRight = margin;
        imageCarouselElement.append(placeholder);
    }
    for(let i2 = 0; i2 < imageCarouselElement.children.length; i2++){
        let style = getComputedStyle(imageCarouselElement.children[i2]);
        if (Number(style.height.replace("px", "")) > maxImageSize) maxImageSize = Number(style.height.replace("px", ""));
        if (Number(style.width.replace("px", "")) > maxImageSize) maxImageSize = Number(style.width.replace("px", ""));
    }
    for(let i3 = 0; i3 < imageCarouselElement.children.length; i3++){
        let zIndex = -Math.abs(i3 - Math.floor(imageCarouselElement.children.length / 2)) + zIndexOffset;
        imageCarouselElement.children[i3].style.zIndex = zIndex;
        if (zIndex < 0) imageCarouselElement.children[i3].style.display = "none";
        let newSize = maxImageSize + maxImageSize / 2 * (zIndex / zIndexOffset);
        maxCarouselSize = maxCarouselSize < newSize ? newSize : maxCarouselSize;
        let formattedSize = px(newSize);
        imageCarouselElement.children[i3].style.width = formattedSize;
        imageCarouselElement.children[i3].style.height = formattedSize;
        imageCarouselElement.children[i3].style.minWidth = formattedSize;
        imageCarouselElement.children[i3].style.minHeight = formattedSize;
    }
    for(let i4 = 0; i4 < imageCarouselElement.children.length; i4++){
        imageCarouselElement.children[i4].style.marginLeft = px(-maxCarouselSize / 4);
        imageCarouselElement.children[i4].style.marginRight = px(-maxCarouselSize / 4);
    }
    let leftButton = document.createElement("div");
    let rightButton = document.createElement("div");
    let leftButtonStyle = getComputedStyle(imageCarouselElement, "::before");
    let rightButtonStyle = getComputedStyle(imageCarouselElement, "::after");
    leftButton.textContent = leftButtonStyle.content.slice(1, leftButtonStyle.content.length - 1);
    if (currentButtonTheme) leftButton.classList.value = currentButtonTheme;
    else leftButton.classList.add("button", "fill");
    leftButton.style.fontSize = leftButtonStyle.fontSize;
    leftButton.style.fontWeight = leftButtonStyle.fontWeight;
    leftButton.style.zIndex = zIndexOffset + 1;
    rightButton.textContent = rightButtonStyle.content.slice(1, rightButtonStyle.content.length - 1);
    if (currentButtonTheme) rightButton.classList.value = currentButtonTheme;
    else rightButton.classList.add("button", "fill");
    rightButton.style.fontSize = rightButtonStyle.fontSize;
    rightButton.style.fontWeight = rightButtonStyle.fontWeight;
    rightButton.style.zIndex = zIndexOffset + 1;
    imageCarouselElement.prepend(leftButton);
    imageCarouselElement.append(rightButton);
    leftButton.addEventListener("click", (e)=>cycleCarousel(index, -1, maxImageSize));
    rightButton.addEventListener("click", (e)=>cycleCarousel(index, 1, maxImageSize));
}
function resetCarousel(index) {
    let imageCarouselElement = imageCarousels[index];
    currentButtonTheme = imageCarouselElement.querySelectorAll(".button")[0].classList.value;
    for (let child of imageCarouselElement.querySelectorAll(".placeholder,.button"))child.parentElement.removeChild(child);
    for (let child1 of imageCarouselElement.querySelectorAll(".image"))child1.style = "";
    initialiseImageCarousel(index);
}
function resetCarousels() {
    for(let i6 = 0; i6 < imageCarousels.length; i6++)resetCarousel(i6);
}
for(let i = 0; i < imageCarousels.length; i++)initialiseImageCarousel(i);
window.addEventListener("resize", (e)=>{
    resetCarousels();
});
let containers = document.querySelectorAll(".layout-row-center-middle");
function updateLayout() {
    for (const container of containers){
        const containerChildren = container.children;
        if (containerChildren.length % 2 === 0) console.warn(`A layout center middle component has even children`);
        const centerElementIndex = Math.floor(containerChildren.length / 2);
        for(let i7 = 0; i7 < containerChildren.length; i7++)if (i7 !== centerElementIndex) {
            containerChildren[i7].style.width = "";
            containerChildren[i7].style.minWidth = "";
            containerChildren[i7].style.maxWidth = "";
        }
        const containerStyle = getComputedStyle(container);
        if (containerStyle.flexDirection === "row") {
            const containerWidth = Number(containerStyle.width.replace("px", ""));
            const centerWidth = Number(getComputedStyle(containerChildren[centerElementIndex]).width.replace("px", ""));
            const outsideElementMaxWidth = (containerWidth - centerWidth) / 2 / centerElementIndex;
            for(let i8 = 0; i8 < containerChildren.length; i8++)if (i8 !== centerElementIndex) {
                containerChildren[i8].style.width = outsideElementMaxWidth + "px";
                containerChildren[i8].style.minWidth = outsideElementMaxWidth + "px";
                containerChildren[i8].style.maxWidth = outsideElementMaxWidth + "px";
            }
        }
    }
}
updateLayout();
window.addEventListener("resize", (e)=>{
    updateLayout();
});
let scrollBar = document.getElementById("scroll-bar");
let scrollHandle = document.getElementById("scroll-handle");
let isScrollBarActive = false;
function updateScrollBar() {
    if (scrollBar && scrollHandle) {
        if (!isScrollBarActive) {
            let scrollBarStyle = getComputedStyle(scrollBar);
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
    window.addEventListener("resize", (e)=>{
        updateScrollBar();
    });
    scrollHandle.addEventListener("mousedown", function(e) {
        if (e.button === 0) isScrollBarActive = true;
    }, {
        passive: false
    });
    document.addEventListener("mousemove", function(e) {
        if (isScrollBarActive) {
            e.preventDefault();
            let scrollBarStyle = getComputedStyle(scrollBar);
            let targetPosition = Number(scrollHandle.style.top.replace("px", "")) + e.movementY;
            let targetMax = Number(scrollBarStyle.height.replace("px", "")) * (document.body.scrollHeight - window.innerHeight) / document.body.scrollHeight;
            if (targetPosition < 0) targetPosition = 0;
            else if (targetPosition > targetMax) targetPosition = targetMax;
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
    document.addEventListener("mouseup", function(e) {
        isScrollBarActive = false;
    }, {
        passive: false
    });
    document.addEventListener("scroll", function(e) {
        updateScrollBar();
    }, {
        passive: false
    });
    const observer = new ResizeObserver(()=>{
        updateScrollBar();
    });
    document.querySelectorAll("textarea").forEach((element)=>{
        observer.observe(element);
    });
}
let sticky = document.querySelectorAll(".sticky");
function updateBanners() {
    for (let element of sticky){
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
            if (window.scrollY <= Number(element.getAttribute("originalPosition"))) element.style.top = Number(element.getAttribute("originalPosition")) - window.scrollY + "px";
        }
    }
}
function resetBanners() {
    for (let element of sticky){
        element.removeAttribute("style");
        element.removeAttribute("originalPosition");
        if (Array.prototype.indexOf.call(element.parentElement.children, element) - 1 >= 0) {
            let placeholder = element.parentElement.children[Array.prototype.indexOf.call(element.parentElement.children, element) - 1];
            if (placeholder.classList.contains("sticky-placeholder")) element.parentElement.removeChild(placeholder);
        }
    }
    updateBanners();
}
updateBanners();
document.addEventListener("scroll", function(e) {
    updateBanners();
}, {
    passive: false
});
window.addEventListener("resize", function(e) {
    resetBanners();
}, {
    passive: false
});
const elementQuery = "body,div,p,span,a,h1,h2,h3,h4,h5,h6,select,button,.button,.fill,.box,.inline-box,.background,.break,.link,.gradient,.gradient-hover-animation,.form-input,[class^='.shadow'],input,.image,textarea,.scroll-handle,[class^='.border'],canvas,.canvas";
let themeSwitchers = document.querySelectorAll(".theme-selector");
let themedElements = document.querySelectorAll(elementQuery);
let currentTheme = "";
function switchElementThemes(newTheme) {
    themedElements = document.querySelectorAll(elementQuery);
    for (let element of themedElements){
        element.classList.remove(currentTheme);
        element.classList.add(newTheme);
    }
    currentTheme = newTheme;
}
function updateThemeSwitchers() {
    for (let button1 of themeSwitchers){
        let style = getComputedStyle(button1);
        let select = button1.querySelector("select");
        select.style.width = Number(style.width.replace("px", "")) + 18 + "px";
        select.style.height = Number(style.height.replace("px", "")) + 18 + "px";
    }
}
function initialiseThemeSwitcher(button2) {
    let label = document.createElement("span");
    label.textContent = getComputedStyle(button2, "::before").content.replaceAll('"', "");
    button2.appendChild(label);
    let themes = getComputedStyle(button2, "::after").content;
    let select = document.createElement("select");
    let style = getComputedStyle(button2);
    select.style.width = style.width;
    select.style.height = style.height;
    for (let string of themes.replaceAll('\\"', "").replaceAll('"', "").replaceAll(" ", "").replaceAll("(", "").replaceAll(")", "").split(",")){
        let splitString = string.split(":");
        if (splitString.length === 4) {
            let text = splitString[0];
            let option = document.createElement("option");
            if (currentTheme === "") currentTheme = text;
            text = text[0].toUpperCase() + text.slice(1);
            option.textContent = text;
            option.value = text;
            select.appendChild(option);
        }
    }
    button2.appendChild(select);
    themedElements = document.querySelectorAll(elementQuery);
    for (let element of themedElements)element.classList.add(currentTheme);
    button2.addEventListener("mouseleave", (e)=>{
        select.blur();
    });
    select.addEventListener("change", (e)=>{
        switchElementThemes(select.value.toLowerCase());
    });
    window.addEventListener("resize", (e)=>{
        updateThemeSwitchers();
    });
}
for (let button1 of themeSwitchers)initialiseThemeSwitcher(button1);
