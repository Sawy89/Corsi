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