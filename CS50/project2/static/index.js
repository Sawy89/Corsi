document.addEventListener('DOMContentLoaded', () => {

    // Login
    loginCheck();

    // Load all channel
    allChannel();

    // Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    // New Channel
    channelButton();
    document.querySelector('#new-channel').onclick = function () {
        newChannelClicked();
    };
    // Display new channel if the server emit!
    socket.on('new channel', data => {
        dispNewChannel(data);
    });

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
            if (data.registered)
                // Already registered!
                document.querySelector('#disp-username').innerHTML = "Welcome " + localStorage.getItem('username');
            else
                // Not yet registered: send to LOGIN page
                window.location.replace($SCRIPT_ROOT + "\login");
        }
}

// ALL CHANNEL
function allChannel () {
    // Create Get request
    var request = new XMLHttpRequest();
    request.open('GET', '/channel/getall');
    request.send(true);

    // Result of request
    request.onload = () => {
        const data = JSON.parse(request.responseText);
        if (request.status == 200)
            data.channels.forEach(element => dispNewChannel(element));
        else
            alert('Bad request!');
    };
};

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
    // get the channel name (input) and send it back to server
    const channel = document.querySelector('input[name="new-channel"]').value;
    const request = new XMLHttpRequest();
    request.open('GET', '/channel/new/'+channel);
    request.send(true);

    // Result of request
    request.onload = () => {
        const data = JSON.parse(request.responseText);
        if (data.already_present)
            alert("Channel "+channel+" already present! Try another name!");
        else
            alert("Channel "+channel+" created!");
    };

    // empty the input text and disable button
    document.querySelector('input[name="new-channel"]').value = '';
    document.querySelector('#new-channel').disabled = true;    
};






// ToDo: add active when clicked the channel

