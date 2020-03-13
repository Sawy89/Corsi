document.addEventListener('DOMContentLoaded', () => {

    // Update cart icon
    updateCartIcon();

});


// Function to update the Cart ICON
function updateCartIcon() {
    cart = JSON.parse(localStorage.getItem('cart-list'));
    if (cart !== null && cart.length > 0)
        document.querySelector('#cart-element-number').innerHTML = cart.length;    
    else
        document.querySelector('#cart-element-number').innerHTML = '';
};