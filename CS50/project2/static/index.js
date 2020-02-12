document.addEventListener('DOMContentLoaded', () => {

    // Login
    loginCheck();

    // New Channel
    channelButton();
    document.querySelector('#new-channel').onclick = function () {
        newChannelClicked ();
    };

});


// LOGIN
function loginCheck () {
    if (!localStorage.getItem('username'))
        // Not yet registered: send to LOGIN page
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
                // Already registered!
                document.querySelector('#disp-username').innerHTML = "Welcome " + localStorage.getItem('username');
            }
            else {
                // Not yet registered: send to LOGIN page
                window.location.replace($SCRIPT_ROOT + "\login");
            }
        }
}


// NEW CHANNEL BUTTON
function channelButton() {
    // By default, submit button is disabled
    document.querySelector('#new-channel').disabled = true;

    // Enable button only if there is text in the input field
    document.querySelector('input[name="new-channel"]').onkeyup = () => {
        if (document.querySelector('input[name="new-channel"]').value.length > 0)
            document.querySelector('#new-channel').disabled = false;
        else
            document.querySelector('#new-channel').disabled = true;
    };
};


// NEW CHANNEL
function dispNewChannel(channelName) {
    // Create a new button with the cannel name and add it
    const channel = document.createElement('button');
    channel.classList.add("btn");
    channel.classList.add("btn-secondary");
    channel.innerHTML = channelName;
    document.querySelector('#channel-list').append(channel)
};


function newChannelClicked () {
    // display the new channel
    dispNewChannel(document.querySelector('input[name="new-channel"]').value);

    // empty the input text and disable button
    document.querySelector('input[name="new-channel"]').value = '';
    document.querySelector('#new-channel').disabled = true;
};


// ToDo: add active when clicked


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
