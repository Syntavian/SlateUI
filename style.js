let buttons = document.getElementsByClassName("switch");

function switchClicked(button) {
    if (button.classList.contains("clicked"))
        button.classList.remove("clicked")
    else
        button.classList.add("clicked")
}

for (let i = 0; i < buttons.length; i++) {
    buttons[i].addEventListener("click", e => {switchClicked(buttons[i]);}, false);
}