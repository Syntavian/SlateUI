let containers = document.querySelectorAll(".layout-row-center-middle");

function updateLayout() {
    for (const container of containers) {
        const containerChildren = container.children;
        if (containerChildren.length % 2 === 0) {
            console.warn(`A layout center middle component has even children`);
        }

        const centerElementIndex = Math.floor(containerChildren.length / 2);
        for (let i = 0; i < containerChildren.length; i++) {
            if (i !== centerElementIndex) {
                containerChildren[i].style.width = '';
                containerChildren[i].style.minWidth = '';
                containerChildren[i].style.maxWidth = '';
            }
        }

        const containerStyle = getComputedStyle(container);
        if (containerStyle.flexDirection === 'row') {
            const containerWidth = Number(containerStyle.width.replace("px", ''));
            const centerWidth = Number(getComputedStyle(containerChildren[centerElementIndex]).width.replace("px", ''));
            const outsideElementMaxWidth = (containerWidth - centerWidth) / 2 / centerElementIndex;

            for (let i = 0; i < containerChildren.length; i++) {
                if (i !== centerElementIndex) {
                    containerChildren[i].style.width = outsideElementMaxWidth + "px";
                    containerChildren[i].style.minWidth = outsideElementMaxWidth + "px";
                    containerChildren[i].style.maxWidth = outsideElementMaxWidth + "px";
                }
            }
        }
    }
}

updateLayout();

window.addEventListener("resize", e => {
    updateLayout();
});
