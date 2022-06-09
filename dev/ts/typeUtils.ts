export function querySelectorAllResultToArray(
    querySelectorAllResult: NodeListOf<Element>
): HTMLElement[] {
    const resultArray = Array.from(querySelectorAllResult);
    if (resultArray.every((element) => !!elementToHTMLElement(element))) {
        return resultArray as HTMLElement[];
    }
}

export function elementToHTMLElement(element: Element): HTMLElement {
    if (element instanceof HTMLElement) {
        return element;
    } else {
        throw new Error("elementToHTMLElement: element is not an HTMLElement");
    }
}
