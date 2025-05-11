
document.addEventListener('DOMContentLoaded', function () {
    const chatContainer = document.getElementById('chatContainer');
    const loadingIndicator = document.getElementById('loadingIndicator');
    const chatForm = document.getElementById('chatForm');
    const userInput = document.getElementById('userInput');

    function addMessage(message, isUser, isError = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = isUser ? 'user-message' : (isError ? 'ai-message error-message' : 'ai-message');
        messageDiv.innerHTML = isUser
            ? `<strong>You:</strong> ${message}`
            : message;
        chatContainer.appendChild(messageDiv);
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    chatForm.addEventListener('submit', async function (e) {
        e.preventDefault();
        const message = userInput.value.trim();

        if (message) {
            // Add user message
            addMessage(message, true);

            // Show loading indicator
            loadingIndicator.style.display = 'block';

            // Clear input
            userInput.value = '';

            try {
                // Send message to server
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                    body: `user_input=${encodeURIComponent(message)}`
                });

                const data = await response.json();

                // Always add the AI response, regardless of status
                addMessage(data.ai_message, false, data.status === 'error');

            } catch (error) {
                console.error('Error:', error);
                // Add a friendly error message
                const errorMessage = "I'm having trouble connecting to the server. Please check your internet connection and try again.";
                addMessage(errorMessage, false, true);
            } finally {
                // Hide loading indicator
                loadingIndicator.style.display = 'none';
                // Scroll to bottom
                chatContainer.scrollTop = chatContainer.scrollHeight;
            }
        }
    });
});