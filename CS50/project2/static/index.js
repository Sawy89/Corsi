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

    // Delete message
    socket.on("message deleted to client", data => {
        if (data['channel'] == localStorage.getItem('currentChannel'))
            deleteChannelMessage(data);
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
                document.querySelector('#disp-username').innerHTML = "Welcome <b>" + localStorage.getItem('username') + "</b>!";
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
            // Display all channels
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
    channel.classList.add("btn","btn-secondary","channel-button","mb-1");
    channel.innerHTML = channelName;
    document.querySelector('#channel-list').append(channel)
    
    // Add event listener for click on the channel
    channel.addEventListener('click', () => {
        channelSelected(channel);
    });

    // if saved, click the channel
    if (localStorage.getItem('currentChannel') == channelName)
        channel.click();
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
    channelName = channel.innerHTML;
    console.log('yeah: '+channel.inn);
    
    // Activate & Display channel
    document.querySelectorAll('.channel-button').forEach(element => element.classList.remove('active'));
    channel.classList.add('active');
    document.querySelector('#channel-title').innerHTML = channelName;

    // Get channel data
    const request = new XMLHttpRequest();
    request.open('GET', '/channel/'+channelName+'/getmessages');

    // Result of request
    request.onload = () => {
        const data = JSON.parse(request.responseText);
        if (request.status == 200 && channelName == data['name']) {
            document.querySelector('#channel-disp').innerHTML = '';
            data['messages'].forEach(element => dispChannelMessage(element)); // display all messages
            dispChannelMessagesInput(channelName);
            localStorage.setItem('currentChannel', channelName);
        }
        else
            alert("Channel "+channelName+" data not found!");
    };

    request.send(true);

};

// CHANNEL MESSAGES display
function dispChannelMessage (data) {
    // display the message
    const mesContainer = document.createElement('div');
    mesContainer.classList.add("container", "row", "mb-1");
    mesContainer.id = data["id"];
    
    // Prepare Element: Author and timestamp
    const mesAuthor = document.createElement("div");
    mesAuthor.classList.add("col-3");
    const mesAutUser = document.createElement("div");
    mesAutUser.classList.add("font-weight-bold");
    mesAutUser.innerHTML = data['username'];
    const mesAutDate = document.createElement("div");
    mesAutDate.classList.add("font-weight-light");
    mesAutDate.innerHTML = '<small>(' + data['insertdate'] + ')</small>';
    mesAuthor.append(mesAutUser);
    mesAuthor.append(mesAutDate);
    // Prepare Element: Message
    const mesMessage = document.createElement("div");
    mesMessage.classList.add("col");
    mesMessage.innerHTML = data['message'];

    // Append & display
    if (data['username'] == localStorage.getItem("username")) {
        // Prepare Element: Delete button
        const mesDelButton = document.createElement("button");
        mesDelButton.classList.add("col-1","close");
        mesDelButton.innerHTML = 'x';
        mesDelButton.onclick = function (data) {
            // Send Delete request to server
            const request = new XMLHttpRequest();
            request.open('POST', '/channel/delmessage');
            request.setRequestHeader("Content-Type", "application/json");

            // Result of request
            request.onload = () => {
                const data = JSON.parse(request.responseText);
                if (request.status == 200) 
                    alert('Message deleted!')
                else
                    alert(data['error']);
            };
            request.send(data);
        };
       
        // Concat element and display
        mesContainer.classList.add("bg-primary", "text-white");
        mesMessage.classList.add("text-right");
        mesContainer.append(mesMessage);
        mesContainer.append(mesAuthor);
        mesContainer.append(mesDelButton);
    }
    else {
        mesContainer.classList.add("bg-secondary", "text-white");
        mesContainer.append(mesAuthor);
        mesContainer.append(mesMessage);
    }
    
    document.querySelector('#channel-disp').append(mesContainer);
};



// CHANNEL MESSAGES delete
function deleteChannelMessage (data) {
    var elementToRemove = document.querySelector("#"+data['id']);
    elementToRemove.parentNode.removeChild(elementToRemove);
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


// ToDo: try to EMIT from server only to channels ?!?!
// ToDo: alert message (for channel creation) temporary!
// ToDO: work also with "Invio" and not only click