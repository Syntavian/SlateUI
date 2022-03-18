import { getElementStyleAsNumber, getElementStylesAsNumberSum } from "./utils";

describe( "getElementStyleAsNumber()", () => {
    test("should remove 'px' and return the number", () => {
        expect(getElementStyleAsNumber("0px")).toBe(0);
    });
});

describe("getElementStylesAsNumberSum()", () => {
    test("should remove all 'px' and return the sum of all numbers", () => {
        expect(getElementStylesAsNumberSum("0px", "1px", "2px")).toBe(3);
    });
});
