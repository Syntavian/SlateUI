let a=Array.from(document.querySelectorAll(".active,.inactive"));function b(a){a.addEventListener("click",c=>{var b;((b=a).classList.contains("active")||b.classList.contains("inactive"))&&(b.classList.toggle("active"),b.classList.toggle("inactive"))})}for(let c of a)b(c)