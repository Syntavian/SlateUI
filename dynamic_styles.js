let switchButtons = document.querySelectorAll(".active,.inactive");

let themeSwitchers = document.querySelectorAll(".theme-selector");

function switchClicked(button) {
    if (button.classList.contains("active") || button.classList.contains("inactive")) {
        button.classList.toggle("active");
        button.classList.toggle("inactive");
    }
}

function initialiseSwitch(button) {
    button.addEventListener("click", e => switchClicked(button));
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

    for (let theme of themes.replaceAll('\\"', '').replaceAll('"', '').replaceAll('(', '').replaceAll(')', '').replaceAll(' ', '').split(',')) {
        let option = document.createElement("option");
        let text = theme.split(':')[0];
        text = text[0].toUpperCase() + text.slice(1);
        option.textContent = text;
        select.appendChild(option);
    }

    
    button.appendChild(select);

    button.addEventListener("mouseleave", e => {select.blur();});

    console.log(themes);
}

for (let button of switchButtons) {
    initialiseSwitch(button);
}

for (let button of themeSwitchers) {
    initialiseThemeSwitcher(button);
}