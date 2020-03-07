document.addEventListener('DOMContentLoaded', () => {
    
    // Add hide & show
    document.querySelectorAll('.dish-category').forEach(element => showHide(element));

});


function showHide(element) {
    element.querySelector(".dish-list").style.visibility = 'hidden'; 
    element.querySelector("button").onclick = function () {
        // alert("Hello World!");
        if (this.innerText == 'Hide') {
            this.parentElement.parentElement.querySelector(".dish-list").style.visibility = 'hidden'; 
            this.innerText = 'Show';
        } else {
            this.parentElement.parentElement.querySelector(".dish-list").style.visibility = 'visible';
            this.innerText = 'Hide';
        }
    };
};

function showElement(element) { 
    // element = document.querySelector('.DishCat'); 
    element.style.visibility = 'visible'; 
};

function hideElement(element) { 
    // elementelement = document.querySelector('.DishCat'); 
    element.style.visibility = 'hidden'; 
};