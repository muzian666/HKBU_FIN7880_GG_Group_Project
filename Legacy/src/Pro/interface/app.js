const chatWindow = document.getElementById('chatWindow');
const messageInput = document.getElementById('messageInput');
const sendBtn = document.getElementById('sendBtn');
const newConversationBtn = document.getElementById('newConversationBtn');
const loading = document.getElementById('loading');
const error = document.getElementById('error');
const settingsButton = document.querySelector('#conversationHeader .settings');
const settingsModal = document.getElementById('settingsModal');
const closeModal = document.querySelector('.close');
const fontSizeInput = document.getElementById('fontSizeInput');
const themeSelect = document.getElementById('themeSelect');

let conversation = [];

function addMessageToChat(message, sender) {
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', sender);
    messageElement.textContent = message;
    chatWindow.appendChild(messageElement);
    chatWindow.scrollTop = chatWindow.scrollHeight;
}

function showLoading() {
    loading.style.display = 'block';
}

function hideLoading() {
    loading.style.display = 'none';
}

async function handleSendMessage() {
    const message = messageInput.value.trim();
    if (message) {
        addMessageToChat(message, 'user');
        conversation.push({ role: 'user', content: message });
        messageInput.value = '';
        showLoading();

        try {
            const response = await fetch('http://127.0.0.1:8000/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ messages: message })
            });

            if (response.ok) {
                const data = await response.json();
                const responseMessage = data; // Assuming the API returns the response message directly
                addMessageToChat(responseMessage, 'assistant');
                conversation.push({ role: 'assistant', content: responseMessage });
            } else {
                throw new Error('Network response was not ok.');
            }
        } catch (error) {
            console.error('Error:', error);
            addMessageToChat('An error occurred while sending the message.', 'error');
        } finally {
            hideLoading();
        }
    }
}

function startNewConversation() {
    conversation = [];
    chatWindow.innerHTML = '';
}

function openSettingsModal() {
    settingsModal.style.display = 'block';
}

function closeSettingsModal() {
    settingsModal.style.display = 'none';
}

function outsideClick(e) {
    if (e.target === settingsModal) {
        settingsModal.style.display = 'none';
    }
}

function adjustFontSize() {
    const fontSize = `${fontSizeInput.value}px`;
    chatWindow.style.fontSize = fontSize;
}

function changeTheme() {
    const theme = themeSelect.value;
    document.body.classList.toggle('dark-theme', theme === 'dark');
}

sendBtn.addEventListener('click', handleSendMessage);
messageInput.addEventListener('keydown', (event) => {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        handleSendMessage();
    }
});
newConversationBtn.addEventListener('click', startNewConversation);
settingsButton.addEventListener('click', openSettingsModal);
closeModal.addEventListener('click', closeSettingsModal);
window.addEventListener('click', outsideClick);
fontSizeInput.addEventListener('input', adjustFontSize);
themeSelect.addEventListener('change', changeTheme);
