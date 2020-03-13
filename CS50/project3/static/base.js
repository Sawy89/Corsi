document.addEventListener('DOMContentLoaded', () => {

    // Update cart icon
    updateCartIcon();

});


function updateCartIcon() {
    cartPriceidList = JSON.parse(localStorage.getItem('cart-priceid-list'));
    if (cartPriceidList.length > 0)
        document.querySelector('#cart-element-number').innerHTML = cartPriceidList.length;    
    else
    document.querySelector('#cart-element-number').innerHTML = '';
};