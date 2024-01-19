// Importing the necessary modules:
const axios = require('axios');
const http = require('http');  // Add this line to import the http module
const express = require('express');
const socketIO = require('socket.io');
require('dotenv').config();

// Creating an Express app:
const app = express();
const server = http.createServer(app);

// Establishing a connection to Socket.IO server
const io = socketIO(server);

// Caching object to store weather data
const weatherCache = {};

// using static files from the "static" directory:
app.use(express.static('static'));

// Defining a route to serve  my index.html file:
app.get('/', (req, res) => {
    res.sendFile(__dirname + '/templates/index.html');
});

// Event listener for incoming connections:
io.on('connection', (socket) => {
    console.log('A user connected');

    // Event listener for incoming messages:
    socket.on('message', async (data) => {
        // Your existing message handling logic
        console.log('User Input:', data.user_input);

        // Check if weather data is cached for the given location:
        if (weatherCache[data.user_input]) {
            console.log('Using cached weather data');
            // Use cached data instead of making an API call
            const botResponse = getChatbotResponse(data.user_input, weatherCache[data.user_input]);
            io.emit('message', { user_input: data.user_input, bot_response: botResponse });
        } else {
            // If not cached, this will make API call and cache the result:
            const weatherData = await fetchWeatherData(data.user_input);
            weatherCache[data.user_input] = weatherData;
            const botResponse = getChatbotResponse(data.user_input, weatherData);
            io.emit('message', { user_input: data.user_input, bot_response: botResponse });
        }
    });

    // Event listener for disconnect
    socket.on('disconnect', () => {
        console.log('User disconnected');
    });
});

// Start the server
const port = 5000; // Choosing the usual port
server.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});

// Function to get a response from my chatbot:
function getChatbotResponse(userInput, weatherData) {
    // Sending the user input to the Flask backend, another important step I missed!
    axios.post('/chatbot', { userInput: userInput })
        .then(response => {
            const botResponse = response.data.botResponse;
            // Processing the bot response:
            console.log('Bot Response:', botResponse);

            // Updating  UI & performing actions with the bot response:
            document.getElementById("chatOutput").innerHTML +=
                `<div><strong>User:</strong> ${userInput}</div>` +
                `<div><strong>Bot:</strong> ${botResponse}</div>`;
        })
        .catch(error => {
            console.error('Error getting bot response:', error);
        });
}

async function fetchWeatherData(location) {
    // Retrieve the API key from the environment variable
    const apiKey = process.env.API_KEY;

    // Check if the API key is available
    if (!apiKey) {
        console.error('API_KEY not found in environment variables.');
        return null;
    }

    const apiUrl = `https://api.openweathermap.org/data/2.5/weather?q=${location}&appid=${apiKey}`;

    try {
        const response = await axios.get(apiUrl);
        return response.data; // Assuming the API response is JSON
    } catch (error) {
        console.error('Error fetching weather data:', error);
        return null;
    }
}
