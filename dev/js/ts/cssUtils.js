export function getElementStylesAsNumberSum(...a){return a.reduce((a,b)=>a+pxToNumber(b),0)}export function pxToNumber(a){return Number(a.replace("px",""))}export function toPx(a){return a+"px"}