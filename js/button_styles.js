let switchButtons = document.querySelectorAll(".active,.inactive");

function switchClicked(button) {
    if (button.classList.contains("active") || button.classList.contains("inactive")) {
        button.classList.toggle("active");
        button.classList.toggle("inactive");
    }
}

function initialiseSwitch(button) {
    button.addEventListener("click", e => switchClicked(button));
}

for (let button of switchButtons) {
    initialiseSwitch(button);
}
