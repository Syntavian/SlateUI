import { getElementStyleAsNumber, getElementStylesAsNumberSum } from "./utils";

describe("getElementStyleAsNumber()", () => {
    test("should remove 'px' and return the number", () => {
        expect(getElementStyleAsNumber("0px")).toBe(0);
    });
    test("should remove 'px' and return the number", () => {
        expect(getElementStyleAsNumber("20px")).toBe(20);
    });
    test("should remove 'px' and return the number", () => {
        expect(getElementStyleAsNumber("03px")).toBe(3);
    });
    test("should remove 'px' and return the number", () => {
        expect(getElementStyleAsNumber("4")).toBe(4);
    });
});

describe("getElementStylesAsNumberSum()", () => {
    test("should remove all 'px' and return the sum of all numbers", () => {
        expect(getElementStylesAsNumberSum("0px", "1px", "2px")).toBe(3);
    });
    test("should remove all 'px' and return the sum of all numbers", () => {
        expect(getElementStylesAsNumberSum("", "3", "4px")).toBe(7);
    });
});
