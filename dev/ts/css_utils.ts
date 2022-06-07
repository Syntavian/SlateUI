export function getElementStyleAsNumber(style: string): number {
    return Number(style.replace("px", ""));
}

export function getElementStylesAsNumberSum(...styles: string[]): number {
    let sum = 0;
    for (let style of styles) {
        sum += Number(style.replace("px", ""));
    }
    return sum;
}

export function px(value: number): string {
    return value + "px";
}
