export function getElementStylesAsNumberSum(...styles: string[]): number {
    return styles.reduce((sum: number, style: string) => {
        return sum + pxToNumber(style);
    }, 0);
}

export function pxToNumber(px: string): number {
    return Number(px.replace("px", ""));
}

export function toPx(value: number): string {
    return value + "px";
}
