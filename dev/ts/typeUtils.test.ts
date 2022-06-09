import {
    elementToHTMLElement,
    querySelectorAllResultToArray,
} from "./typeUtils";

describe("querySelectorAllResultToArray()", () => {
    test("should return the queried elements if they are HTMLElements", () => {
        const element = document.createElement("div");
        element.className = "test";
        document.body.appendChild(element);
        const queriedElements = document.querySelectorAll(".test");

        expect(querySelectorAllResultToArray(queriedElements)).toStrictEqual([
            element,
        ]);
    });

    test("should throw an error if an element is not an HTMLElement", () => {
        const element = document.createElementNS(
            "http://www.w3.org/2000/svg",
            "svg"
        );
        element.id = "test";
        document.body.appendChild(element);
        const queriedElements = document.querySelectorAll("#test");

        expect(() =>
            querySelectorAllResultToArray(queriedElements)
        ).toThrowError(
            new Error("elementToHTMLElement: element is not an HTMLElement")
        );
    });
});

describe("elementToHTMLElement()", () => {
    test("should return the element if it is an HTMLElement", () => {
        const element = document.createElement("div");

        expect(elementToHTMLElement(element)).toStrictEqual(element);
    });

    test("should not throw an error return the element from a query if it is an HTMLElement", () => {
        const element = document.createElement("div");
        element.className = "test";
        document.body.appendChild(element);
        const queriedElements = Array.from(document.querySelectorAll(".test"));

        expect(() => elementToHTMLElement(queriedElements[0])).not.toThrow();
        expect(elementToHTMLElement(queriedElements[0])).toStrictEqual(element);
    });

    test("should throw an error if the element is not an HTMLElement", () => {
        const element = undefined;

        expect(() => elementToHTMLElement(element)).toThrow(
            new Error("elementToHTMLElement: element is not an HTMLElement")
        );
    });
});
