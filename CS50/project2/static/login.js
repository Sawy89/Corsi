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
        const username = document.querySelector('#form-name').value;

        // Register with BACKEND
        const request = new XMLHttpRequest();
        request.open('POST', '/register/new'); // save on backend
        request.setRequestHeader("Content-Type", "application/json");

        // callback for registration
        request.onload = () => {
            // Extract JSON data from request
            const data = JSON.parse(request.responseText);

            // Update the result div
            if (data.registered) {
                // save on frontend
                localStorage.setItem('username', username);
                // Send to index
                window.location.href = "/";
            }
            else {
                alert("The username " + username + " is already used! Try another one!");
            }
                
        }
        
        // Register with BACKEND: lauch
        var data = JSON.stringify({'username': username, "already_registered": false});
        request.send(data);

        return false;
    };
});



