// allieChat.js

function sendMessage() {
    // Get user input
    var userInput = document.getElementById("userInput").value;

    // Log user input to the console for debugging
    console.log("User Input:", userInput);

    // Send a POST request to /chatbot route
    fetch('/chatbot', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: 'user_input=' + encodeURIComponent(userInput),
    })
    .then(response => response.json())
    .then(data => {
        // Log bot response to the console for debugging
        console.log("Bot Response:", data.bot_response);

        // Update the chatOutput div with user and bot messages
        document.getElementById("chatOutput").innerHTML +=
            '<div><strong>User:</strong> ' + data.user_input + '</div>' +
            '<div><strong>Bot:</strong> ' + data.bot_response + '</div>';
    })
    .catch(error => {
        // Log errors to the console for debugging
        console.error('Error:', error);
    });
}
