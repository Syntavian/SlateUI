import { getElementStylesAsNumberSum, pxToNumber, toPx } from "./cssUtils";

describe("getElementStylesAsNumberSum()", () => {
    test("should remove all 'px' and return the sum of all numbers", () => {
        expect(getElementStylesAsNumberSum("0px", "1px", "2px")).toBe(3);
    });
    test("should remove all 'px' and return the sum of all numbers", () => {
        expect(getElementStylesAsNumberSum("", "3", "4px")).toBe(7);
    });
});

describe("pxToNumber()", () => {
    test("should remove 'px' and return the number", () => {
        expect(pxToNumber("0px")).toBe(0);
    });
    test("should remove 'px' and return the number", () => {
        expect(pxToNumber("20px")).toBe(20);
    });
    test("should remove 'px' and return the number", () => {
        expect(pxToNumber("03px")).toBe(3);
    });
    test("should remove 'px' and return the number", () => {
        expect(pxToNumber("4")).toBe(4);
    });
});

describe("toPx()", () => {
    test("should add 'px' to the end of a value", () => {
        expect(toPx(0)).toBe("0px");
    });
});