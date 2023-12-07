// Importing the necessary modules:
const axios = require('axios');
const http = require('http');
const express = require('express');
const socketIO = require('socket.io');

// Creating an Express app
const app = express();
const server = http.createServer(app);

// Establish a connection to the Socket.IO server
const io = socketIO(server);

// using static files from the "static" directory
app.use(express.static('static'));

// Define a route to serve your HTML file
app.get('/', (req, res) => {
    res.sendFile(__dirname + '/templates/index.html');
});

// Event listener for incoming connections
io.on('connection', (socket) => {
    console.log('A user connected');

    // Event listener for incoming messages:
    socket.on('message', (data) => {
        // Your existing message handling logic
        console.log('User Input:', data.user_input);

        // Integrate your ChatterBot logic here to get a response
        const botResponse = getChatbotResponse(data.user_input);

        // Emitting a 'message' event with the user input and bot response:
        io.emit('message', { user_input: data.user_input, bot_response: botResponse });
    });

    // Event listener for disconnect
    socket.on('disconnect', () => {
        console.log('User disconnected');
    });
});

// Start the server
const port = 5000; // Choose a port
server.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});

// Function to get a response from your ChatterBot
function getChatbotResponse(userInput) {

    return 'Your bot response goes here';
}
