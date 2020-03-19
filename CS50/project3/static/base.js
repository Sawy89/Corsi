document.addEventListener('DOMContentLoaded', () => {

    // Empty shopping cart if order placed
    infoOrder = document.querySelector('#order-placed');
    if (infoOrder.dataset.status)
        localStorage.removeItem('cart-list');

    // Update cart icon
    updateCartIcon();

    // Go To shopping cart
    document.querySelector('#button-cart').addEventListener("click", () => {
        goToCart();
    });

});


// Function to update the Cart ICON
function updateCartIcon() {
    cart = JSON.parse(localStorage.getItem('cart-list'));
    if (cart !== null && cart.length > 0)
        document.querySelector('#cart-element-number').innerHTML = cart.length;    
    else
        document.querySelector('#cart-element-number').innerHTML = '';
};
// ToDo: it gives error in some pages


// Get cart list
function getCartList() {
    if (!localStorage.getItem('cart-list')) {
        alert('Attention! No item in the cart!');
        return false;
    };
    cart = JSON.parse(localStorage.getItem('cart-list'));
    message = {"cart": cart};
    messagejson = JSON.stringify(message); //.replace(/"/g, "'");

    return messagejson
};


// Function for calling the cart page with the item in the shopping cart
function goToCart() {
    // Get shopping cart
    messagejson = getCartList();

    if (messagejson) {
        document.querySelector('#button-cart-hidden').value = messagejson;

        document.querySelector("#form-cart").submit();
    };

    return;
};