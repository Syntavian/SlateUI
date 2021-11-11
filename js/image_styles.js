const imageCarouselData = [];

let imageCarousels = document.querySelectorAll(".image-carousel");

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

for (let i = 0; i < imageCarousels.length; i++) {
    initialiseImageCarousel(imageCarousels[i], i);
}
