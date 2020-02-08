document.addEventListener('DOMContentLoaded', () => {

    // By default, submit button is disabled
    document.querySelector('button').disabled = true;

    // Enable button only if there is text in the input field
    document.querySelector('#form-name').onkeyup = () => {
        if (document.querySelector('#form-name').value.length > 0)
            document.querySelector('button').disabled = false;
        else
            document.querySelector('button').disabled = true;
    };

    // At the click of the button, save the name and redirect to index
    document.querySelector('button').onclick = () => {
        // Get the name and save it
        const user_name = document.querySelector('#form-name').value;
        localStorage.setItem('user_name', user_name);
    
        // Redirect to 
        // window.location.href = $SCRIPT_ROOT + "\index";
    
        // Stop form from submitting
        // return false;
    };
});



