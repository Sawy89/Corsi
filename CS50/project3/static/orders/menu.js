document.addEventListener('DOMContentLoaded', () => {
    
    // Add hide & show
    var dishNumber = 0;
    document.querySelectorAll('.dish-category').forEach(element => showHide(element));

    // Add to Cart
    document.querySelectorAll('.glyphicon-shopping-cart').forEach( (item) => {
        item.addEventListener("click", () => {
            addToCart();
        });
    });

});


function showHide(element) {
    // https://www.w3schools.com/howto/howto_js_collapsible.asp
    element.querySelector(".dish-list").style.display = 'block'; 
    // element.querySelector(".dish-list").style.overflow = 'Hide';
    element.querySelector("button").onclick = function () {
        // alert("Hello World!");
        if (this.innerText == 'Hide') {
            this.parentElement.parentElement.querySelector(".dish-list").style.display = 'none'; 
            this.innerText = 'Show';
        } else {
            this.parentElement.parentElement.querySelector(".dish-list").style.display = 'block';
            this.innerText = 'Hide';
        }
    };
};

// ToDo: javascript per aggiungere al carrello
function addToCart() {
    alert("Fucking yeah!")
};
