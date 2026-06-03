// --- web/static/js/index-script.js (with Progressive Disclosure + Markdown Formatting) ---

document.addEventListener('DOMContentLoaded', () => {
  const chatButton = document.getElementById('open-chat');
  const chatPopup = document.getElementById('chat-popup');
  const sendBtn = document.getElementById('send-btn');
  const userInput = document.getElementById('user-input');
  const chatMessages = document.getElementById('chat-messages');
  const endChatBtn = document.getElementById('end-chat');

  let conversationId = generateConversationId();
  let userId = null;
  let lastRemaining = null;

  chatButton.addEventListener('click', () => {
    chatPopup.classList.toggle('open');
    if (!userId) {
      showLoginPrompt();
    }
  });

  sendBtn.addEventListener('click', sendMessage);
  userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
  });

  if (endChatBtn) {
    endChatBtn.addEventListener('click', async () => {
      if (userId && conversationId) {
        await fetch('/api/end_session', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ user_id: userId, conversation_id: conversationId })
        });
      }
      appendMessage('bot', '👋 Chat ended. Thank you!');
      userId = null;
      conversationId = generateConversationId();
    });
  }

  function generateConversationId() {
    return 'CONV_' + Math.random().toString(36).substring(2, 10);
  }

  function showLoginPrompt() {
    appendMessage('bot', '👋 Welcome! Please enter your user ID or type "guest" to continue.');
  }

  function formatBotText(text) {
    text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    text = text.replace(/\*(.*?)\*/g, '<em>$1</em>');
    return text.split(/\n+/).map(line => `<p>${line.trim()}</p>`).join('');
  }

  async function sendMessage() {
    const message = userInput.value.trim();
    if (!message) return;

    appendMessage('user', message);
    userInput.value = '';

    if (lastRemaining && ['yes', 'y', 'more', 'continue'].includes(message.toLowerCase())) {
      appendMessage('bot', lastRemaining);
      lastRemaining = null;
      return;
    }

    if (!userId) {
      if (message.toLowerCase() === 'guest') {
        userId = 'guest';
        appendMessage('bot', '✅ Welcome, Guest! You can now ask your questions.');
        return;
      } else {
        userId = { tempId: message };
        appendMessage('bot', '🔒 Please enter your password:');
        return;
      }
    } else if (typeof userId === 'object' && userId.tempId) {
      try {
        const res = await fetch('/api/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ user_id: userId.tempId, password: message })
        });
        const result = await res.json();
        if (result.success) {
          userId = result.user_id;
          appendMessage('bot', `✅ Welcome back, ${result.name}!`);
        } else {
          appendMessage('bot', `❗ ${result.message}`);
          userId = null;
        }
      } catch (error) {
        appendMessage('bot', '❗ Login error.');
        userId = null;
      }
      return;
    }

    appendMessage('bot', 'Typing...');
    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: message,
          conversation_id: conversationId,
          user_id: userId
        })
      });
      const data = await response.json();
      const lastBotMessage = chatMessages.querySelector('.bot:last-child');
      lastRemaining = null;

      if (data.short_part) {
        lastBotMessage.innerHTML = `<img src="../static/images/Oncana_Submark_Forest.png" class="bot-icon"> ${formatBotText(data.short_part)}`;
        if (data.remaining) {
          lastRemaining = formatBotText(data.remaining);
          appendMessage('bot', 'Would you like me to provide more details? (Y/N)');
        }
      } else {
        lastBotMessage.innerHTML = `<img src="../static/images/Oncana_Submark_Forest.png" class="bot-icon"> ❗ Sorry, something went wrong.`;
      }
    } catch (error) {
      const lastBotMessage = chatMessages.querySelector('.bot:last-child');
      lastBotMessage.innerHTML = `<img src="../static/images/Oncana_Submark_Forest.png" class="bot-icon"> ❗ Error reaching the server.`;
    }
  }

  function appendMessage(sender, text) {
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', sender);

    if (sender === 'user') {
      messageElement.innerHTML = `${text} <span class="user-icon">👤</span> `;
    } else {
      const formatted = formatBotText(text);
      messageElement.innerHTML = `<img src="../static/images/Oncana_Submark_Forest.png" class="bot-icon"> ${formatted}`;
    }

    chatMessages.appendChild(messageElement);
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }
});
