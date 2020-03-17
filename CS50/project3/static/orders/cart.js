document.addEventListener('DOMContentLoaded', () => {

    // Place order
    document.querySelector('#button-order').addEventListener("click", () => {
        placeOrder();
    });

});


// Remove item from cart
function removeItemFromCart(itemId) {

    cart = JSON.parse(localStorage.getItem('cart-list'));
    for(var i = cart.length - 1; i >= 0; i--) {
        if(cart[i]['id'] === itemId) {
            cart.splice(i, 1);
        }
    }

    localStorage.setItem('cart-list', JSON.stringify(cart));

    goToCart();
};


// Function for calling the cart page with the item in the shopping cart
function placeOrder() {
    // Get shopping cart
    messagejson = getCartList();

    document.querySelector('#button-order-hidden').value = messagejson;

    document.querySelector("#form-place-order").submit();
};