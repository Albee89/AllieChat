// allieChat.js

// Establish a connection to the SocketIO server
var socket = io.connect('http://' + document.domain + ':' + location.port);

// Function to send a message to the server:
function sendMessage() {
    // Getting user input:
    var userInput = document.getElementById("userInput").value.trim(); // Trim to remove leading and trailing spaces

    // Checking if the user input is not empty:
    if (userInput !== "") {
        // Emitting a 'message' event with the user input:
        socket.emit('message', { user_input: userInput });

        // Logging the user's input to the console:
        console.log('User Input:', userInput);

        // Clearing the input field:
        document.getElementById("userInput").value = "";
    }
}

// Event listener for incoming messages:
socket.on('message', function(data) {
    // Checking if the bot response is empty or null:
    if (!data.bot_response) {
        console.log('Chat bot did not respond.'); // Log to the console
        return; // Exiting the function
    }

    // Logging the user's input and bot response to the console:
    console.log('User Input:', data.user_input);
    console.log('Bot Response:', data.bot_response);

    // Update the chatOutput div with user and bot messages
    document.getElementById("chatOutput").innerHTML +=
        '<div><strong>User:</strong> ' + data.user_input + '</div>' +
        '<div><strong>Bot:</strong> ' + data.bot_response + '</div>';
});
