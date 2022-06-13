let a = Array.from(document.querySelectorAll(".active,.inactive"));
function b(a6) {
    a6.addEventListener("click", (c)=>{
        var b5;
        ((b5 = a6).classList.contains("active") || b5.classList.contains("inactive")) && (b5.classList.toggle("active"), b5.classList.toggle("inactive"));
    });
}
for (let c of a)b(c);
function getElementStylesAsNumberSum(...a7) {
    return a7.reduce((a8, b6)=>a8 + pxToNumber(b6), 0);
}
function pxToNumber(a9) {
    return Number(a9.replace("px", ""));
}
function toPx(a10) {
    return a10 + "px";
}
let b1 = document.querySelectorAll(".image-carousel"), e = "";
function f(n, e2, k) {
    let a11 = b1[n], g1 = 0, h = 0;
    for(let i = 0; i < a11.querySelectorAll(".image,.placeholder").length; i++){
        let l = a11.querySelectorAll(".image,.placeholder")[i];
        Number(l.style.zIndex) > g1 && (g1 = Number(l.style.zIndex), h = i);
    }
    if (a11.querySelectorAll(".image,.placeholder")[h + e2].classList.contains("placeholder")) return;
    let m = !1;
    for (let c4 of Array.from(a11.querySelectorAll(".image,.placeholder"))){
        let f2 = Number(c4.style.zIndex);
        m ? c4.style.zIndex = String(f2 + e2) : ((f2 == g1 || e2 < 0 && f2 - e2 == g1) && (m = !0), c4.style.zIndex = String(f2 - e2)), f2 < 0 ? c4.style.display = "none" : c4.style.display = "flex";
        let o = k / 2, p = f2 / g1, j = toPx(k + o * p);
        c4.style.width = j, c4.style.height = j, c4.style.minWidth = j, c4.style.minHeight = j;
    }
    a11.querySelectorAll(".image,.placeholder")[h + e2 + 1].classList.contains("placeholder") ? a11.children[a11.children.length - 1].classList.add("disabled") : a11.children[a11.children.length - 1].classList.remove("disabled"), a11.querySelectorAll(".image,.placeholder")[h + e2 - 1].classList.contains("placeholder") ? a11.children[0].classList.add("disabled") : a11.children[0].classList.remove("disabled");
}
function c1(w) {
    let a12 = b1[w], j = Math.floor(a12.children.length / 2 - .5), k = 0, l = 0, m = getComputedStyle(a12.children[0]).marginLeft;
    j > 2 && (j = 2);
    for(let v = 0; v < j; v++){
        let g2 = document.createElement("div");
        g2.classList.add("placeholder"), g2.style.marginLeft = m, g2.style.marginRight = m, a12.prepend(g2), (g2 = document.createElement("div")).classList.add("placeholder"), g2.style.marginLeft = m, g2.style.marginRight = m, a12.append(g2);
    }
    for(let s = 0; s < a12.children.length; s++){
        let n = getComputedStyle(a12.children[s]);
        Number(n.height.replace("px", "")) > k && (k = Number(n.height.replace("px", ""))), Number(n.width.replace("px", "")) > k && (k = Number(n.width.replace("px", "")));
    }
    for(let c5 = 0; c5 < a12.children.length; c5++){
        let t = -Math.abs(c5 - Math.floor(a12.children.length / 2)) + j;
        a12.children[c5].style.zIndex = t, t < 0 && (a12.children[c5].style.display = "none");
        let u = k + k / 2 * (t / j);
        l = l < u ? u : l;
        let o = toPx(u);
        a12.children[c5].style.width = o, a12.children[c5].style.height = o, a12.children[c5].style.minWidth = o, a12.children[c5].style.minHeight = o;
    }
    for(let p = 0; p < a12.children.length; p++)a12.children[p].style.marginLeft = toPx(-l / 4), a12.children[p].style.marginRight = toPx(-l / 4);
    let h = document.createElement("div"), i = document.createElement("div"), q = getComputedStyle(a12, "::before"), r = getComputedStyle(a12, "::after");
    h.textContent = q.content.slice(1, q.content.length - 1), e ? h.classList.value = e : h.classList.add("button", "fill"), h.style.fontSize = q.fontSize, h.style.fontWeight = q.fontWeight, h.style.zIndex = j + 1, i.textContent = r.content.slice(1, r.content.length - 1), e ? i.classList.value = e : i.classList.add("button", "fill"), i.style.fontSize = r.fontSize, i.style.fontWeight = r.fontWeight, i.style.zIndex = j + 1, a12.prepend(h), a12.append(i), h.addEventListener("click", (a)=>f(w, -1, k)), i.addEventListener("click", (a)=>f(w, 1, k));
}
function g(d3) {
    let a13 = b1[d3];
    for (let f3 of (e = a13.querySelectorAll(".button")[0].classList.value, a13.querySelectorAll(".placeholder,.button")))f3.parentElement.removeChild(f3);
    for (let g3 of a13.querySelectorAll(".image"))g3.style = "";
    c1(d3);
}
for(let a1 = 0; a1 < b1.length; a1++)c1(a1);
window.addEventListener("resize", (a14)=>{
    !function() {
        for(let a15 = 0; a15 < b1.length; a15++)g(a15);
    }();
});
let b2 = document.querySelectorAll(".layout-row-center-middle");
function a2() {
    for (let g4 of b2){
        let a16 = g4.children;
        a16.length % 2 == 0 && console.warn("A layout center middle component has even children");
        let e3 = Math.floor(a16.length / 2);
        for(let c6 = 0; c6 < a16.length; c6++)c6 !== e3 && (a16[c6].style.width = "", a16[c6].style.minWidth = "", a16[c6].style.maxWidth = "");
        let h = getComputedStyle(g4);
        if ("row" === h.flexDirection) {
            let i = Number(h.width.replace("px", "")), j = Number(getComputedStyle(a16[e3]).width.replace("px", "")), f4 = (i - j) / 2 / e3;
            for(let d4 = 0; d4 < a16.length; d4++)d4 !== e3 && (a16[d4].style.width = f4 + "px", a16[d4].style.minWidth = f4 + "px", a16[d4].style.maxWidth = f4 + "px");
        }
    }
}
a2(), window.addEventListener("resize", (b)=>{
    a2();
});
let a3 = document.getElementById("scroll-bar"), b3 = document.getElementById("scroll-handle"), d = !1;
function c2() {
    if (a3 && b3 && !d) {
        let c7 = getComputedStyle(a3);
        b3.style.height = Number(c7.height.replace("px", "")) * window.innerHeight / document.body.scrollHeight + "px", b3.style.top = Number(c7.height.replace("px", "")) * window.scrollY / document.body.scrollHeight + "px";
    }
}
if (document.body.classList.contains("no-scrollbar") && (a3 || ((a3 = document.createElement("div")).id = "scroll-bar", a3.classList.add("scroll-bar"), document.body.appendChild(a3)), b3 || ((b3 = document.createElement("div")).id = "scroll-handle", b3.classList.add("scroll-handle"), a3.appendChild(b3))), c2(), a3 && b3) {
    window.addEventListener("resize", (a)=>{
        c2();
    }), b3.addEventListener("mousedown", function(a17) {
        0 === a17.button && (d = !0);
    }, {
        passive: !1
    }), document.addEventListener("mousemove", function(e5) {
        if (d) {
            e5.preventDefault();
            let f5 = getComputedStyle(a3), c8 = Number(b3.style.top.replace("px", "")) + e5.movementY, g5 = Number(f5.height.replace("px", "")) * (document.body.scrollHeight - window.innerHeight) / document.body.scrollHeight;
            c8 < 0 ? c8 = 0 : c8 > g5 && (c8 = g5), b3.style.top = c8 + "px", window.scroll({
                top: Number(b3.style.top.replace("px", "")) * document.body.scrollHeight / Number(f5.height.replace("px", "")),
                left: 0,
                behavior: "instant"
            });
        }
    }, {
        passive: !1
    }), document.addEventListener("mouseup", function(a) {
        d = !1;
    }, {
        passive: !1
    }), document.addEventListener("scroll", function(a) {
        c2();
    }, {
        passive: !1
    });
    let e4 = new ResizeObserver(()=>{
        c2();
    });
    document.querySelectorAll("textarea").forEach((a18)=>{
        e4.observe(a18);
    });
}
let d1 = document.querySelectorAll(".sticky");
function a4() {
    for (let a19 of d1){
        let e6 = getComputedStyle(a19);
        if ("fixed" != e6.position) {
            if (a19.getBoundingClientRect().top < 0) {
                let f6 = document.createElement("div");
                f6.style.height = getElementStylesAsNumberSum(e6.height) + "px", f6.style.width = getElementStylesAsNumberSum(e6.width, e6.marginLeft, e6.marginRight) + "px", f6.style.display = e6.display, f6.className = "sticky-placeholder", a19.style.position = "fixed", a19.style.zIndex = 99, e6 = getComputedStyle(a19), a19.setAttribute("originalPosition", pxToNumber(e6.top)), a19.style.top = "0px", a19.parentElement.insertBefore(f6, a19);
            }
        } else {
            a19.style.top = "0px";
            let g6 = a19.parentElement.children[Array.prototype.indexOf.call(a19.parentElement.children, a19) - 1];
            g6.style.height = getElementStylesAsNumberSum(e6.height) + "px", g6.style.width = getElementStylesAsNumberSum(e6.width, e6.marginLeft, e6.marginRight) + "px", window.scrollY <= Number(a19.getAttribute("originalPosition")) && (a19.style.top = Number(a19.getAttribute("originalPosition")) - window.scrollY + "px");
        }
    }
}
a4(), document.addEventListener("scroll", function(b) {
    a4();
}, {
    passive: !1
}), window.addEventListener("resize", function(b7) {
    !function() {
        for (let b8 of d1)if (b8.removeAttribute("style"), b8.removeAttribute("originalPosition"), Array.prototype.indexOf.call(b8.parentElement.children, b8) - 1 >= 0) {
            let c9 = b8.parentElement.children[Array.prototype.indexOf.call(b8.parentElement.children, b8) - 1];
            c9.classList.contains("sticky-placeholder") && b8.parentElement.removeChild(c9);
        }
        a4();
    }();
}, {
    passive: !1
});
const a5 = "body,div,p,span,a,h1,h2,h3,h4,h5,h6,select,button,.button,.fill,.box,.inline-box,.background,.break,.link,.gradient,.gradient-hover-animation,.form-input,[class^='.shadow'],input,.image,textarea,.scroll-handle,[class^='.border'],canvas,.canvas";
let b4 = document.querySelectorAll(".theme-selector"), e1 = document.querySelectorAll(a5), f1 = "";
function c3(c10) {
    let i = document.createElement("span");
    i.textContent = getComputedStyle(c10, "::before").content.replaceAll('"', ""), c10.appendChild(i);
    let l = getComputedStyle(c10, "::after").content, g7 = document.createElement("select"), j = getComputedStyle(c10);
    for (let m of (g7.style.width = j.width, g7.style.height = j.height, l.replaceAll('\\"', "").replaceAll('"', "").replaceAll(" ", "").replaceAll("(", "").replaceAll(")", "").split(","))){
        let k = m.split(":");
        if (4 === k.length) {
            let d5 = k[0], h = document.createElement("option");
            "" === f1 && (f1 = d5), d5 = d5[0].toUpperCase() + d5.slice(1), h.textContent = d5, h.value = d5, g7.appendChild(h);
        }
    }
    for (let n of (c10.appendChild(g7), e1 = document.querySelectorAll(a5)))n.classList.add(f1);
    c10.addEventListener("mouseleave", (a)=>{
        g7.blur();
    }), g7.addEventListener("change", (b9)=>{
        !function(b10) {
            for (let c11 of e1 = document.querySelectorAll(a5))c11.classList.remove(f1), c11.classList.add(b10);
            f1 = b10;
        }(g7.value.toLowerCase());
    }), window.addEventListener("resize", (a20)=>{
        !function() {
            for (let a21 of b4){
                let c12 = getComputedStyle(a21), d6 = a21.querySelector("select");
                d6.style.width = Number(c12.width.replace("px", "")) + 18 + "px", d6.style.height = Number(c12.height.replace("px", "")) + 18 + "px";
            }
        }();
    });
}
for (let d2 of b4)c3(d2);
