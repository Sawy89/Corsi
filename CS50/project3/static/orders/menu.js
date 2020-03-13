document.addEventListener('DOMContentLoaded', () => {
    
    // Add hide & show
    var dishNumber = 0;
    document.querySelectorAll('.dish-category').forEach(element => showHide(element));

    // Add to Cart
    document.querySelectorAll('.add-to-chart').forEach( (item) => {
        item.addEventListener("click", (event) => {
            // prevent browser's default action
            event.preventDefault();

            addToCart(item);
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


// Adding to cart
function addToCart(item) {
    var priceid = item.dataset.priceid;

    // Save to local cart
    if (localStorage.getItem('cart-priceid-list'))
        cartPriceidList = JSON.parse(localStorage.getItem('cart-priceid-list'));
    else
        cartPriceidList = [];
    cartPriceidList.push(parseInt(priceid));
    localStorage.setItem('cart-priceid-list', JSON.stringify(cartPriceidList));

    // ToDO: add alert with product name
    alert("Fucking yeah! N° "+priceid);
};
