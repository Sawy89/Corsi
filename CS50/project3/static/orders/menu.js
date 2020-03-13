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
    // Extract data
    var priceid = parseInt(item.dataset.priceid);
    var dishid = item.dataset.dishid;
    var addition = [];
    document.querySelectorAll(".dish-"+dishid).forEach(element => {
        // Verify selected addition
        if (element.checked){
            element.checked = false;
            addition.push(parseInt(element.dataset.additionid));
        };
    });
    
    // Get local cart
    if (localStorage.getItem('cart-list'))
        cart = JSON.parse(localStorage.getItem('cart-list'));
    else
    cart = [];

    // Prepare item
    var itemDictToAdd = {'priceId': priceid,
                            'addition': addition};

    // Save to local cart
    cart.push(itemDictToAdd);
    localStorage.setItem('cart-list', JSON.stringify(cart));

    // Update cart icon
    updateCartIcon();

    // ToDO: add alert with product name
    alert("Fucking yeah! Price N° "+priceid+", Dish N° "+dishid);
};

