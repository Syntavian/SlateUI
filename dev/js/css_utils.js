export function getElementStyleAsNumber(style) {
    return Number(style.replace("px", ""));
}

export function getElementStylesAsNumberSum(...styles) {
    let sum = 0;
    for (let style of styles) {
        sum += Number(style.replace("px", ""));
    }
    return sum;
}

export function px(value) {
    return value + "px";
}
