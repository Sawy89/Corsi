document.addEventListener('DOMContentLoaded', () => {

    // Check if already registered
    if (!localStorage.getItem('user_name'))
        window.location.replace($SCRIPT_ROOT + "\login");
    else
        user_name = localStorage.getItem('user_name');

        // Create Get request
        const request = new XMLHttpRequest();
        request.open('GET', '/register/check/'+user_name);
        request.send(true);

        // Result of request
        request.onload = () => {
            const data = JSON.parse(request.responseText);
            if (data.registered) {
                // Update the result div
                document.querySelector('#disp-user-name').innerHTML = "Welcome " + localStorage.getItem('user_name');   // already logged in!    
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
