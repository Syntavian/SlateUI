let switchButtons = document.querySelectorAll(".active,.inactive");

let themeSwitchers = document.querySelectorAll(".theme-selector");

let themedElements = document.querySelectorAll(".fill,.themed,.background,.link,.gradient,.gradient-hover-animation");

let currentTheme = "";

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

    console.log(themes.replaceAll('\\"', '').replaceAll('"', '').replaceAll(' ', '').split('),'));

    for (let theme of themes.replaceAll('\\"', '').replaceAll('"', '').replaceAll(' ', '').split('),')) {
        let option = document.createElement("option");
        let text = theme.replaceAll('(', '').replaceAll(')', '').split(':')[0];
        console.log(text);
        if (currentTheme === "") {
            currentTheme = text;
        }
        text = text[0].toUpperCase() + text.slice(1);
        option.textContent = text;
        option.value = text;
        select.appendChild(option);
    }

    button.appendChild(select);

    for (let element of themedElements) {
        element.classList.add(currentTheme);
    }

    button.addEventListener("mouseleave", e => {select.blur();});
    select.addEventListener("change", e => {switchElementThemes(select.value.toLowerCase());});

    console.log(themes);
}

for (let button of switchButtons) {
    initialiseSwitch(button);
}

for (let button of themeSwitchers) {
    initialiseThemeSwitcher(button);
}