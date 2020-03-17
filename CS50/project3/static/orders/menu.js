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

    // Topping display
    document.querySelectorAll('.toppings').forEach( (item) => {
        item.addEventListener("change", () => {
            showSelectedToppings();
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


// Function to scan toppings checklist
function getSelectedTopping(to_decheck) {
    var toppings = [];
    var toppingsName = [];
    document.querySelectorAll(".toppings").forEach(element => {
        // Get checked
        if (element.checked){
            toppings.push(element.dataset.toppingid); // save topping id
            toppingsName.push(element.dataset.name); // save topping name
            if (to_decheck)
                element.checked = false;
        };
    });
    return [toppings, toppingsName];
};


// Function show selected topping
function showSelectedToppings() {
    Topp = getSelectedTopping(false);
    toppingsName = Topp[1];
    document.querySelectorAll(".topping-disp").forEach(element => {
        if (toppingsName != null && element.dataset.navailable == toppingsName.length)
            element.innerHTML = toppingsName.join(', ');
            // ToDO: it works also for <=???
        else
            element.innerHTML = '';
    });
};


// Adding to cart
function addToCart(item) {
    // Extract price and dish clicked
    var priceid = parseInt(item.dataset.priceid);
    var dishid = item.dataset.dishid;
    // Extract if addition clicked
    var addition = [];
    document.querySelectorAll(".dish-"+dishid).forEach(element => {
        // Verify selected addition
        if (element.checked){
            element.checked = false;
            addition.push(parseInt(element.dataset.additionid));
        };
    });
    // Extract if toppings selected
    var ntopping = item.dataset.ntopping;
    Topp = getSelectedTopping(true);
    toppings = Topp[0];
    // Check topping number
    if (toppings != null && toppings.length > ntopping) {
        alert("Too many toppings selected");
        return;
    }
    else if (toppings  != null && toppings.length < ntopping) {
        alert("Too few toppings!");
        return;
    }
    
    // Get local cart
    if (localStorage.getItem('cart-list'))
        cart = JSON.parse(localStorage.getItem('cart-list'));
    else
        cart = [];

    // Prepare item
    var d = new Date();
    var itemDictToAdd = {'id': d.getTime(),
                        'priceId': priceid,
                        'addition': addition,
                        'topping': toppings};

    // Save to local cart
    cart.push(itemDictToAdd);
    localStorage.setItem('cart-list', JSON.stringify(cart));

    // Update cart icon
    updateCartIcon();

    // ToDO: add alert with product name???
    // alert("Fucking yeah! Price N° "+priceid+", Dish N° "+dishid+", addition "+addition+", Topping "+toppings);
};

