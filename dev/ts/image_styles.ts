import { px } from "./css_utils";

let imageCarousels = document.querySelectorAll(".image-carousel");
let currentButtonTheme = "";

function cycleCarousel(index, offset, maxDimension) {
    let imageCarouselElement = imageCarousels[index];
    let maxIndex = 0;
    let maxPosition = 0;

    for (
        let i = 0;
        i < imageCarouselElement.querySelectorAll(".image,.placeholder").length;
        i++
    ) {
        let child = imageCarouselElement.querySelectorAll(
            ".image,.placeholder"
        )[i];
        if (Number(child.style.zIndex) > maxIndex) {
            maxIndex = Number(child.style.zIndex);
            maxPosition = i;
        }
    }

    if (
        imageCarouselElement
            .querySelectorAll(".image,.placeholder")
            [maxPosition + offset].classList.contains("placeholder")
    ) {
        return;
    }

    let pastMax = false;

    for (let child of imageCarouselElement.querySelectorAll(
        ".image,.placeholder"
    )) {
        if (!pastMax) {
            if (
                child.style.zIndex == maxIndex ||
                (offset < 0 && Number(child.style.zIndex) - offset == maxIndex)
            ) {
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

        child.style.width =
            maxDimension +
            (maxDimension / 2) * (Number(child.style.zIndex) / maxIndex) +
            "px";
        child.style.height =
            maxDimension +
            (maxDimension / 2) * (Number(child.style.zIndex) / maxIndex) +
            "px";
        child.style.minWidth =
            maxDimension +
            (maxDimension / 2) * (Number(child.style.zIndex) / maxIndex) +
            "px";
        child.style.minHeight =
            maxDimension +
            (maxDimension / 2) * (Number(child.style.zIndex) / maxIndex) +
            "px";
    }

    if (
        imageCarouselElement
            .querySelectorAll(".image,.placeholder")
            [maxPosition + offset + 1].classList.contains("placeholder")
    ) {
        imageCarouselElement.children[
            imageCarouselElement.children.length - 1
        ].classList.add("disabled");
    } else {
        imageCarouselElement.children[
            imageCarouselElement.children.length - 1
        ].classList.remove("disabled");
    }
    if (
        imageCarouselElement
            .querySelectorAll(".image,.placeholder")
            [maxPosition + offset - 1].classList.contains("placeholder")
    ) {
        imageCarouselElement.children[0].classList.add("disabled");
    } else {
        imageCarouselElement.children[0].classList.remove("disabled");
    }
}

function initialiseImageCarousel(index) {
    let imageCarouselElement = imageCarousels[index];
    let childCount = imageCarouselElement.children.length;
    let zIndexOffset = Math.floor(childCount / 2 - 0.5);
    let maxImageSize = 0;
    let maxCarouselSize = 0;
    let margin = getComputedStyle(imageCarouselElement.children[0]).marginLeft;

    // Keep the max number of images in a carousel <= 5.
    if (zIndexOffset > 2) {
        zIndexOffset = 2;
    }

    for (let i = 0; i < zIndexOffset; i++) {
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

    // let carouselStyle = getComputedStyle(imageCarouselElement);

    for (let i = 0; i < imageCarouselElement.children.length; i++) {
        let style = getComputedStyle(imageCarouselElement.children[i]);

        if (Number(style.height.replace("px", "")) > maxImageSize) {
            maxImageSize = Number(style.height.replace("px", ""));
        }
        if (Number(style.width.replace("px", "")) > maxImageSize) {
            maxImageSize = Number(style.width.replace("px", ""));
        }
    }

    for (let i = 0; i < imageCarouselElement.children.length; i++) {
        let zIndex =
            -Math.abs(
                i - Math.floor(imageCarouselElement.children.length / 2)
            ) + zIndexOffset;
        imageCarouselElement.children[i].style.zIndex = zIndex;

        if (zIndex < 0) {
            imageCarouselElement.children[i].style.display = "none";
        }

        let newSize =
            maxImageSize + (maxImageSize / 2) * (zIndex / zIndexOffset);
        maxCarouselSize = maxCarouselSize < newSize ? newSize : maxCarouselSize;
        let formattedSize = px(newSize);

        imageCarouselElement.children[i].style.width = formattedSize;
        imageCarouselElement.children[i].style.height = formattedSize;
        imageCarouselElement.children[i].style.minWidth = formattedSize;
        imageCarouselElement.children[i].style.minHeight = formattedSize;
    }

    for (let i = 0; i < imageCarouselElement.children.length; i++) {
        imageCarouselElement.children[i].style.marginLeft = px(
            -maxCarouselSize / 4
        );
        imageCarouselElement.children[i].style.marginRight = px(
            -maxCarouselSize / 4
        );
    }

    let leftButton = document.createElement("div");
    let rightButton = document.createElement("div");

    let leftButtonStyle = getComputedStyle(imageCarouselElement, "::before");
    let rightButtonStyle = getComputedStyle(imageCarouselElement, "::after");

    leftButton.textContent = leftButtonStyle.content.slice(
        1,
        leftButtonStyle.content.length - 1
    );
    if (currentButtonTheme) {
        leftButton.classList.value = currentButtonTheme;
    } else {
        leftButton.classList.add("button", "fill");
    }
    leftButton.style.fontSize = leftButtonStyle.fontSize;
    leftButton.style.fontWeight = leftButtonStyle.fontWeight;
    leftButton.style.zIndex = zIndexOffset + 1;

    rightButton.textContent = rightButtonStyle.content.slice(
        1,
        rightButtonStyle.content.length - 1
    );
    if (currentButtonTheme) {
        rightButton.classList.value = currentButtonTheme;
    } else {
        rightButton.classList.add("button", "fill");
    }
    rightButton.style.fontSize = rightButtonStyle.fontSize;
    rightButton.style.fontWeight = rightButtonStyle.fontWeight;
    rightButton.style.zIndex = zIndexOffset + 1;

    imageCarouselElement.prepend(leftButton);
    imageCarouselElement.append(rightButton);

    leftButton.addEventListener("click", (e) =>
        cycleCarousel(index, -1, maxImageSize)
    );
    rightButton.addEventListener("click", (e) =>
        cycleCarousel(index, 1, maxImageSize)
    );
}

function resetCarousel(index) {
    let imageCarouselElement = imageCarousels[index];
    currentButtonTheme =
        imageCarouselElement.querySelectorAll(".button")[0].classList.value;

    for (let child of imageCarouselElement.querySelectorAll(
        ".placeholder,.button"
    )) {
        child.parentElement.removeChild(child);
    }

    for (let child of imageCarouselElement.querySelectorAll(".image")) {
        child.style = "";
    }

    initialiseImageCarousel(index);
}

function resetCarousels() {
    for (let i = 0; i < imageCarousels.length; i++) {
        resetCarousel(i);
    }
}

for (let i = 0; i < imageCarousels.length; i++) {
    initialiseImageCarousel(i);
}

window.addEventListener("resize", (e) => {
    resetCarousels();
});
