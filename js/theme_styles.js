let themeSwitchers = document.querySelectorAll(".theme-selector");
let themedElements = document.querySelectorAll("body,div,p,span,a,h1,h2,h3,h4,h5,h6,select,.fill,.box,.inline-box,.background,.break,.link,.gradient,.gradient-hover-animation,.form-input,[class^='.shadow']");
let currentTheme = "";

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

    themedElements = document.querySelectorAll("body,div,p,span,a,h1,h2,h3,h4,h5,h6,select,.fill,.box,.inline-box,.background,.break,.link,.gradient,.gradient-hover-animation,.form-input,[class^='.shadow']");

    for (let element of themedElements) {
        element.classList.add(currentTheme);
    }

    button.addEventListener("mouseleave", e => {select.blur();});
    select.addEventListener("change", e => {switchElementThemes(select.value.toLowerCase());});
    window.addEventListener("resize", e => {
        updateThemeSwitchers(); 
    });
}

for (let button of themeSwitchers) {
    initialiseThemeSwitcher(button);
}
