document.addEventListener('DOMContentLoaded', () => {

    // Login
    loginCheck();

    // Load all channel
    allChannel();

    // Hide input messages
    document.getElementById("input-div").style.visibility = "hidden";

    // Connect to websocket
    const socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    // New Channel clicked
    disableButton(document.querySelector('#new-channel'), document.querySelector('input[name="new-channel"]'));
    document.querySelector('#new-channel').onclick = function () {
        newChannelClicked();
    };

    // New channel added
    socket.on('new channel', data => {
        dispNewChannel(data);
    });

    // Disp new message
    socket.on("new message to client", data => {
        if (data['channel'] == localStorage.getItem('currentChannel'))
            dispChannelMessage(data);
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


// ALL CHANNEL: take all channels from server
function allChannel () {
    // Create Get request
    var request = new XMLHttpRequest();
    request.open('GET', '/channel/getall');
    request.send(true);

    // Result of request
    request.onload = () => {
        const data = JSON.parse(request.responseText);
        if (request.status == 200) {
            data.channels.forEach(element => dispNewChannel(element));
        }
        else
            alert('Bad request!');
    };
};


// FUNCTION DISABLE-ENABLE button on TEXT
function disableButton(buttonE, textE) {
    // By default, submit button is disabled
    buttonE.disabled = true;

    // Enable button only if there is text in the input field
    textE.onkeyup = () => {
        if (textE.value.length > 0)
            buttonE.disabled = false;
        else
            buttonE.disabled = true;
    };
};


// NEW CHANNEL: display the new channel
function dispNewChannel(channelName) {
    // Create a new button with the cannel name and add it
    const channel = document.createElement('button');
    channel.classList.add("btn");
    channel.classList.add("btn-secondary");
    channel.classList.add("channel-button");
    channel.innerHTML = channelName;
    document.querySelector('#channel-list').append(channel)
    
    // Add event listener for click on the channel
    channel.addEventListener('click', () => {
        channelSelected(channel.innerHTML);
    });
};

// NEW CHANNEL CLICK: action when the new channel button is clicked
function newChannelClicked () {
    // get the channel name (input) and send it back to server
    const channel = document.querySelector('input[name="new-channel"]').value;
    const request = new XMLHttpRequest();
    request.open('GET', '/channel/new/'+channel);
    
    // Result of request
    request.onload = () => {
        const data = JSON.parse(request.responseText);
        if (data.already_present)
            alert("Channel "+channel+" already present! Try another name!");
        else
            alert("Channel "+channel+" created!");
    };

    request.send(true);

    // empty the input text and disable button
    document.querySelector('input[name="new-channel"]').value = '';
    document.querySelector('#new-channel').disabled = true;    
};


// CHANNEL SELECTED: what happens when a channel is selected
function channelSelected (channel) {
    console.log('yeah: '+channel);
    
    // Display channel
    document.querySelector('#channel-title').innerHTML = channel;

    // Get channel data
    const request = new XMLHttpRequest();
    request.open('GET', '/channel/'+channel+'/getmessages');

    // Result of request
    request.onload = () => {
        const data = JSON.parse(request.responseText);
        if (request.status == 200 && channel == data['name']) {
            document.querySelector('#channel-disp').innerHTML = '';
            data['messages'].forEach(element => dispChannelMessage(element));
            dispChannelMessagesInput(channel);
            localStorage.setItem('currentChannel', channel);
        }
        else
            alert("Channel "+channel+" data not found!");
    };

    request.send(true);

};

// CHANNEL MESSAGES display
function dispChannelMessage (element) {
    // display the message
    const mes = document.createElement('div');
    mes.innerHTML = element['message']
    document.querySelector('#channel-disp').append(mes);
};


// CHANNEL MESSAGES display input
function dispChannelMessagesInput (channel) {
    // Display message input block
    inputDiv = document.getElementById("input-div");
    inputDiv.style.visibility = "visible";

    // Enable & disable
    const inputMessage = inputDiv.querySelector('input');
    const inputButton = inputDiv.querySelector('button');
    disableButton(inputButton, inputMessage);

    // Onclick "Send" button
    inputButton.onclick = function () {
        const socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
        
        const data = {'channel': channel, 'message': inputMessage.value, 'username': localStorage.getItem('username')};
        socket.emit("new message to server", data);

        inputMessage.value = '';
        inputButton.disabled = true;    
    };
};


// ToDO: try to EMIT from server only to channels ?!?!
// before this, check it's working well! I am not sure!!