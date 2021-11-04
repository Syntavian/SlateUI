let switchButtons = document.querySelectorAll(".active,.inactive");

let themeSwitchers = document.querySelectorAll(".theme-selector");

let themedElements = document.querySelectorAll("body,div,p,span,a,h1,h2,h3,h4,h5,h6,select,.fill,.box,.inline-box,.background,.break,.link,.gradient,.gradient-hover-animation,[class^='.shadow']");

const scrollBar = document.getElementById("scroll-bar");
const scrollHandle = document.getElementById("scroll-handle");

let isScrollBarActive = false;

let currentTheme = "";

function updateScrollBar() {
    if (!isScrollBarActive) {
        let scrollBarStyle = getComputedStyle(scrollBar);

        scrollHandle.style.height = Number(scrollBarStyle.height.replace("px", "")) * window.innerHeight / document.body.scrollHeight + "px";  
        scrollHandle.style.top = Number(scrollBarStyle.height.replace("px", "")) * window.scrollY / document.body.scrollHeight + "px";  
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

function initialiseThemeSwitcher(button) {

    let style = getComputedStyle(button);

    let label = document.createElement("span");
    label.textContent = getComputedStyle(button, "::before").content.replaceAll('"', '');
    button.appendChild(label);

    let themes = getComputedStyle(button, "::after").content;

    let select = document.createElement("select");

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
}

updateScrollBar();

for (let button of switchButtons) {
    initialiseSwitch(button);
}

for (let button of themeSwitchers) {
    initialiseThemeSwitcher(button);
}

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