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
// Contact Form Validation + Backend
// ===============================


const form =
document.getElementById("contactForm");


form.addEventListener("submit",async(e)=>{


e.preventDefault();



let name =
document.getElementById("name").value.trim();


let phone =
document.getElementById("phone").value.trim();


let email =
document.getElementById("email").value.trim();


let business =
document.getElementById("businessType").value;


let message =
document.getElementById("message").value.trim();



let valid=true;




// Clear errors

document.querySelectorAll(".form-error")
.forEach(error=>{

error.innerHTML="";

});



// Name

if(name===""){


document.getElementById("nameError")
.innerHTML="Enter your name";

valid=false;


}



// Phone

if(phone.length < 10){


document.getElementById("phoneError")
.innerHTML="Enter valid phone number";


valid=false;


}



// Email

if(!email.includes("@")){


document.getElementById("emailError")
.innerHTML="Enter valid email";


valid=false;


}



// Business

if(business===""){


document.getElementById("businessTypeError")
.innerHTML="Select business type";


valid=false;


}



// Message

if(message===""){


document.getElementById("messageError")
.innerHTML="Enter message";


valid=false;


}



if(!valid){

return;

}




// Loading button

const button =
document.getElementById("submitBtn");


button.classList.add("loading");




// Send data to backend

try{


let response =
await fetch("https://dongle-enterprises.onrender.com",{


method:"POST",


headers:{

"Content-Type":"application/json"

},


body:JSON.stringify({

name:name,

phone:phone,

email:email,

businessType:business,

message:message

})


});



let data =
await response.json();





if(response.ok){



form.style.display="none";


document
.getElementById("formSuccess")
.classList.add("visible");



form.reset();



}else{


alert("Something went wrong");


}



}

catch(error){


console.log(error);


alert("Backend server is not running");


}


button.classList.remove("loading");


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

fetch("http://localhost:5000/contact",);
});
