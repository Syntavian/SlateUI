let scrollBar = document.getElementById("scroll-bar");
let scrollHandle = document.getElementById("scroll-handle");
let isScrollBarActive = false;

function updateScrollBar() {
    if (scrollBar && scrollHandle) {
        if (!isScrollBarActive) {
            let scrollBarStyle = getComputedStyle(scrollBar);
    
            scrollHandle.style.height = Number(scrollBarStyle.height.replace("px", "")) * window.innerHeight / document.body.scrollHeight + "px";  
            scrollHandle.style.top = Number(scrollBarStyle.height.replace("px", "")) * window.scrollY / document.body.scrollHeight + "px";  
        }
    }
}

if (document.body.classList.contains("no-scrollbar")) {
    if (!scrollBar) {
        scrollBar = document.createElement("div");
        scrollBar.id = "scroll-bar";
        scrollBar.classList.add("scroll-bar");
        document.body.appendChild(scrollBar);
    }

    if (!scrollHandle) {
        scrollHandle = document.createElement("div");
        scrollHandle.id = "scroll-handle";
        scrollHandle.classList.add("scroll-handle");
        scrollBar.appendChild(scrollHandle);
    }
}

updateScrollBar();

if (scrollBar && scrollHandle) {
    window.addEventListener("resize", e => {
        updateScrollBar();
    });

    scrollHandle.addEventListener("mousedown", function (e) {
        if (e.button === 0) {
            isScrollBarActive = true;
        }
    }, {
        passive: false
    });
    
    document.addEventListener("mousemove", function (e) {
        if (isScrollBarActive) {
            e.preventDefault();
    
            let scrollBarStyle = getComputedStyle(scrollBar);
    
            let targetPosition = Number(scrollHandle.style.top.replace("px", "")) + e.movementY;
    
            let targetMax = Number(scrollBarStyle.height.replace("px", "")) * (document.body.scrollHeight - window.innerHeight) / document.body.scrollHeight;
    
            if (targetPosition < 0) {
                targetPosition = 0;
            } else if (targetPosition > targetMax) {
                targetPosition = targetMax;
            }
    
            scrollHandle.style.top = targetPosition + "px";        
    
            window.scroll({
                top: Number(scrollHandle.style.top.replace("px", "")) * document.body.scrollHeight / Number(scrollBarStyle.height.replace("px", "")),
                left: 0,
                behavior: "instant"
            });
        }
    }, {
        passive: false
    });
    
    document.addEventListener("mouseup", function (e) {
        isScrollBarActive = false;
    }, {
        passive: false
    });
    
    document.addEventListener("scroll", function (e) {
        updateScrollBar();
    }, {
        passive: false
    });

    const observer = new ResizeObserver(() => {
        updateScrollBar();
    });
    
    document.querySelectorAll('textarea').forEach((element) => {
        observer.observe(element);
    });
}
