// ===============================
// DONGLE ENTERPRISES JAVASCRIPT
// ===============================


// Navbar scroll effect

const navbar = document.getElementById("navbar");


window.addEventListener("scroll",()=>{

    if(window.scrollY > 50){

        navbar.classList.add("scrolled");

    }else{

        navbar.classList.remove("scrolled");

    }

});




// ===============================
// Mobile Menu Toggle
// ===============================

const navToggle = document.getElementById("navToggle");
const navLinks = document.getElementById("navLinks");


navToggle.addEventListener("click",()=>{


    navToggle.classList.toggle("open");

    navLinks.classList.toggle("open");


});




// Close menu after clicking link

document.querySelectorAll(".nav-link").forEach(link=>{


    link.addEventListener("click",()=>{

        navLinks.classList.remove("open");

        navToggle.classList.remove("open");

    });


});




// ===============================
// Active Navigation Highlight
// ===============================


const sections = document.querySelectorAll("section");

const links = document.querySelectorAll(".nav-link");


window.addEventListener("scroll",()=>{


let current="";


sections.forEach(section=>{


let top = section.offsetTop - 100;

let height = section.clientHeight;


if(scrollY >= top && scrollY < top + height){

    current = section.getAttribute("id");

}


});



links.forEach(link=>{


link.classList.remove("active");


if(link.getAttribute("href") === "#"+current){

link.classList.add("active");

}


});


});




// ===============================
// Scroll Reveal Animation
// ===============================


const revealElements =
document.querySelectorAll(".reveal");


function reveal(){


revealElements.forEach(element=>{


let position =
element.getBoundingClientRect().top;


if(position < window.innerHeight - 100){


element.classList.add("visible");


}


});


}


window.addEventListener("scroll",reveal);

reveal();




// ===============================
// Footer Year
// ===============================


document.getElementById("year").textContent =
new Date().getFullYear();




// ===============================
// Back To Top Button
// ===============================


const backBtn =
document.getElementById("backToTop");


window.addEventListener("scroll",()=>{


if(window.scrollY > 500){


backBtn.classList.add("visible");


}else{


backBtn.classList.remove("visible");


}


});



backBtn.addEventListener("click",()=>{


window.scrollTo({

top:0,

behavior:"smooth"

});


});




// ===============================
// Smooth Scroll For All Links
// ===============================


document.querySelectorAll('a[href^="#"]')
.forEach(anchor=>{


anchor.addEventListener("click",function(e){


e.preventDefault();


document
.querySelector(this.getAttribute("href"))
.scrollIntoView({

behavior:"smooth"

});


});

});
