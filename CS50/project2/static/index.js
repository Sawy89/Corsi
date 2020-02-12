document.addEventListener('DOMContentLoaded', () => {

    // Check if already registered
    if (!localStorage.getItem('username'))
        window.location.replace($SCRIPT_ROOT + "\login");
    else
        username = localStorage.getItem('username');

        // Create Get request
        const request = new XMLHttpRequest();
        request.open('GET', '/register/check/'+username);
        request.send(true);

        // Result of request
        request.onload = () => {
            const data = JSON.parse(request.responseText);
            if (data.registered) {
                // Update the result div
                document.querySelector('#disp-username').innerHTML = "Welcome " + localStorage.getItem('username');   // already logged in!    
            }
            else {
                // send to LOGIN
                window.location.replace($SCRIPT_ROOT + "\login");
            }
        }

});

// document.addEventListener('DOMContentLoaded', () => {

//     // Connect to websocket
//     var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

//     // When connected, configure buttons
//     socket.on('connect', () => {

//         // Each button should emit a "submit vote" event
//         document.querySelectorAll('button').forEach(button => {
//             button.onclick = () => {
//                 const selection = button.dataset.vote;
//                 socket.emit('submit vote', {'selection': selection});
//             };
//         });
//     });

//     // When a new vote is announced, add to the unordered list
//     socket.on('vote totals', data => {
//         document.querySelector('#yes').innerHTML = data.yes;
//         document.querySelector('#no').innerHTML = data.no;
//         document.querySelector('#maybe').innerHTML = data.maybe;
//     });
// });
