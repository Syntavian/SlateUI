let switchButtons: HTMLElement[] = Array.from(
    document.querySelectorAll(".active,.inactive")
);

function switchClicked(button: HTMLElement) {
    if (
        button.classList.contains("active") ||
        button.classList.contains("inactive")
    ) {
        button.classList.toggle("active");
        button.classList.toggle("inactive");
    }
}

function initialiseSwitch(button: HTMLElement) {
    button.addEventListener("click", (e) => switchClicked(button));
}

for (let button of switchButtons) {
    initialiseSwitch(button);
}
