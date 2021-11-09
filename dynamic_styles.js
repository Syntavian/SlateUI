let switchButtons = document.querySelectorAll(".active,.inactive");

let themeSwitchers = document.querySelectorAll(".theme-selector");

let themedElements = document.querySelectorAll("body,div,p,span,a,h1,h2,h3,h4,h5,h6,select,.fill,.box,.inline-box,.background,.break,.link,.gradient,.gradient-hover-animation,[class^='.shadow']");

let imageCarousels = document.querySelectorAll(".image-carousel");

let scrollBar = document.getElementById("scroll-bar");
let scrollHandle = document.getElementById("scroll-handle");

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

let isScrollBarActive = false;

let currentTheme = "";

function updateScrollBar() {
    if (scrollBar && scrollHandle) {
        if (!isScrollBarActive) {
            let scrollBarStyle = getComputedStyle(scrollBar);
    
            scrollHandle.style.height = Number(scrollBarStyle.height.replace("px", "")) * window.innerHeight / document.body.scrollHeight + "px";  
            scrollHandle.style.top = Number(scrollBarStyle.height.replace("px", "")) * window.scrollY / document.body.scrollHeight + "px";  
        }
    }
}

function switchClicked(button) {
    if (button.classList.contains("active") || button.classList.contains("inactive")) {
        button.classList.toggle("active");
        button.classList.toggle("inactive");
    }
}

function initialiseSwitch(button) {
    button.addEventListener("click", e => switchClicked(button));
}

function switchElementThemes(newTheme) {
    for (let element of themedElements) {
        element.classList.remove(currentTheme);
        element.classList.add(newTheme);
    }

    currentTheme = newTheme;
}

function updateThemeSwitchers() {
    for (let button of themeSwitchers) {
        let style = getComputedStyle(button);
        let select = button.querySelector("select");
        select.style.width = Number(style.width.replace("px", "")) + 18 + "px";
        select.style.height = Number(style.height.replace("px", "")) + 18 + "px";
    }
}

function initialiseThemeSwitcher(button) {
    let label = document.createElement("span");
    label.textContent = getComputedStyle(button, "::before").content.replaceAll('"', '');
    button.appendChild(label);
    let themes = getComputedStyle(button, "::after").content;
    let select = document.createElement("select");
    let style = getComputedStyle(button);
    select.style.width = style.width;
    select.style.height = style.height;
    for (let string of themes.replaceAll('\\"', '').replaceAll('"', '').replaceAll(' ', '').replaceAll('(', '').replaceAll(')', '').split(',')) {
        let splitString = string.split(':');
        if (splitString.length === 3) {
            let text = splitString[0];
            let option = document.createElement("option");
            if (currentTheme === "") {
                currentTheme = text;
            }
            text = text[0].toUpperCase() + text.slice(1);
            option.textContent = text;
            option.value = text;
            select.appendChild(option);
        }
    }

    button.appendChild(select);

    themedElements = document.querySelectorAll("body,div,p,span,a,h1,h2,h3,h4,h5,h6,select,.fill,.box,.inline-box,.background,.link,.gradient,.gradient-hover-animation");

    for (let element of themedElements) {
        element.classList.add(currentTheme);
    }

    button.addEventListener("mouseleave", e => {select.blur();});
    select.addEventListener("change", e => {switchElementThemes(select.value.toLowerCase());});
    window.addEventListener("resize", e => {
        updateThemeSwitchers(); 
    });
}

const imageCarouselData = [];

function cycleCarousel(index, offset, maxDimension) {
    let imageCarouselElement = imageCarouselData[index].element;
    let maxIndex = 0;
    let maxPosition = 0;

    for (let i = 0; i < imageCarouselElement.querySelectorAll(".image,.placeholder").length; i++) {
        let child = imageCarouselElement.querySelectorAll(".image,.placeholder")[i];
        if (Number(child.style.zIndex) > maxIndex) {
            maxIndex = Number(child.style.zIndex);
            maxPosition = i;
        }
    }

    if (imageCarouselElement.querySelectorAll(".image,.placeholder")[maxPosition + offset].classList.contains("placeholder")) {
        return;
    }

    let pastMax = false;

    for (let child of imageCarouselElement.querySelectorAll(".image,.placeholder")) {
        if (!pastMax) {
            if (child.style.zIndex == maxIndex || (offset < 0 && Number(child.style.zIndex) - offset == maxIndex)) {
                pastMax = true;
            }
            child.style.zIndex = Number(child.style.zIndex) - offset;
        } else {
            child.style.zIndex = Number(child.style.zIndex) + offset;
        }

        if (child.style.zIndex < 0) {
            child.style.display = "none";
        } else {
            child.style.display = "flex";
        }

        child.style.width = maxDimension + maxDimension / 2 * (Number(child.style.zIndex) / maxIndex) + "px";
        child.style.height = maxDimension + maxDimension / 2 * (Number(child.style.zIndex) / maxIndex) + "px";
    }
}

function initialiseImageCarousel(imageCarouselElement, index) {
    let childCount = imageCarouselElement.children.length;
    let zIndexOffset = Math.floor(childCount / 2 - 0.5);
    let maxDimension = 0;

    if (zIndexOffset > 2) {
        zIndexOffset = 2;
    }

    for (let i = 0; i < zIndexOffset; i++) {
        let placeholder = document.createElement("div");
        placeholder.classList.add("placeholder");
        placeholder.style.marginLeft = "-1.5em";
        placeholder.style.marginRight = "-1.5em";
        imageCarouselElement.prepend(placeholder);

        placeholder = document.createElement("div");
        placeholder.classList.add("placeholder");
        placeholder.style.marginLeft = "-1.5em";
        placeholder.style.marginRight = "-1.5em";
        imageCarouselElement.append(placeholder);
    }

    for (let i = 0; i < imageCarouselElement.children.length; i++) {
        let style = getComputedStyle(imageCarouselElement.children[i]);

        if (Number(style.height.replace("px", "")) > maxDimension) {
            maxDimension = Number(style.height.replace("px", ""));
        }
        if (Number(style.width.replace("px", "")) > maxDimension) {
            maxDimension = Number(style.width.replace("px", ""));
        }
    }

    for (let i = 0; i < imageCarouselElement.children.length; i++) {

        let zIndex = -Math.abs(i - Math.floor(imageCarouselElement.children.length / 2)) + zIndexOffset;
        imageCarouselElement.children[i].style.zIndex = zIndex;

        if (zIndex < 0) {
            imageCarouselElement.children[i].style.display = "none";
        }

        imageCarouselElement.children[i].style.width = maxDimension + maxDimension / 2 * (zIndex / zIndexOffset) + "px";
        imageCarouselElement.children[i].style.height = maxDimension + maxDimension / 2 * (zIndex / zIndexOffset) + "px";
    }

    let leftButton = document.createElement("div");
    let rightButton = document.createElement("div");

    let leftButtonStyle = getComputedStyle(imageCarouselElement, "::before");
    let rightButtonStyle = getComputedStyle(imageCarouselElement, "::after");

    leftButton.textContent = leftButtonStyle.content.slice(1,leftButtonStyle.content.length - 1);
    leftButton.classList.add("button");
    leftButton.style.fontSize = leftButtonStyle.fontSize;
    leftButton.style.fontWeight = leftButtonStyle.fontWeight;
    leftButton.style.zIndex = zIndexOffset + 1;

    rightButton.textContent = rightButtonStyle.content.slice(1,rightButtonStyle.content.length - 1);
    rightButton.classList.add("button");
    rightButton.style.fontSize = rightButtonStyle.fontSize;
    rightButton.style.fontWeight = rightButtonStyle.fontWeight;
    rightButton.style.zIndex = zIndexOffset + 1;

    imageCarouselElement.prepend(leftButton);
    imageCarouselElement.append(rightButton);

    imageCarouselData.push({index: index, element: imageCarouselElement, position: 0});

    leftButton.addEventListener("click", e => cycleCarousel(index, -1, maxDimension));
    rightButton.addEventListener("click", e => cycleCarousel(index, 1, maxDimension));
}

for (let button of switchButtons) {
    initialiseSwitch(button);
}

for (let i = 0; i < imageCarousels.length; i++) {
    initialiseImageCarousel(imageCarousels[i], i);
}

for (let button of themeSwitchers) {
    initialiseThemeSwitcher(button);
}

updateScrollBar();

if (scrollBar && scrollHandle) {
    window.addEventListener("resize", e => {
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
    
            let scrollBarStyle = getComputedStyle(scrollBar);
    
            let targetPosition = Number(scrollHandle.style.top.replace("px", "")) + e.movementY;
    
            let targetMax = Number(scrollBarStyle.height.replace("px", "")) * (document.body.scrollHeight - window.innerHeight) / document.body.scrollHeight;
    
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
}
