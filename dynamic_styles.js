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

function initialiseImageCarousel(ic) {
    let childCount = ic.children.length;

    let zIndexOffset = Math.floor(childCount / 2 - 0.5);
    if (zIndexOffset > 2) {
        zIndexOffset = 2;
    }

    for (let i = 0; i < childCount; i++) {
        let zIndex = -Math.abs(i - Math.floor(childCount / 2)) + zIndexOffset;
        ic.children[i].style.zIndex = zIndex;
        if (zIndex < 0) {
            ic.children[i].style.display = "none";
        }
    }

    let leftButton = document.createElement("div");
    let rightButton = document.createElement("div");

    let leftButtonStyle = getComputedStyle(ic, "::before");
    let rightButtonStyle = getComputedStyle(ic, "::after");

    leftButton.textContent = leftButtonStyle.content.slice(1,leftButtonStyle.content.length - 1);
    leftButton.style.fontSize = leftButtonStyle.fontSize;
    leftButton.style.zIndex = zIndexOffset + 1;

    rightButton.textContent = rightButtonStyle.content.slice(1,rightButtonStyle.content.length - 1);
    rightButton.style.fontSize = rightButtonStyle.fontSize;
    rightButton.style.zIndex = zIndexOffset + 1;

    ic.prepend(leftButton);
    ic.append(rightButton);
}

for (let button of switchButtons) {
    initialiseSwitch(button);
}

for (let button of themeSwitchers) {
    initialiseThemeSwitcher(button);
}

for (let ic of imageCarousels) {
    initialiseImageCarousel(ic);
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
