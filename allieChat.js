// allieChat.js

// Establish a connection to the SocketIO server
var socket = io.connect('http://' + document.domain + ':' + location.port);

// Function to send a message to the server
function sendMessage() {
    // Get user input
    var userInput = document.getElementById("userInput").value;

    // Emit a 'message' event with the user input
    socket.emit('message', { user_input: userInput });

    // Log the user's input to the console
    console.log('User Input:', userInput);
}

// Event listener for incoming messages
socket.on('message', function(data) {
    // Check if the bot response is empty or null
    if (!data.bot_response) {
        console.log('Chat bot did not respond.'); // Log to the console
        return; // Exit the function
    }

    // Log the user's input and bot response to the console
    console.log('User Input:', data.user_input);
    console.log('Bot Response:', data.bot_response);

    // Update the chatOutput div with user and bot messages
    document.getElementById("chatOutput").innerHTML +=
        '<div><strong>User:</strong> ' + data.user_input + '</div>' +
        '<div><strong>Bot:</strong> ' + data.bot_response + '</div>';
});
