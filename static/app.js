const chat = document.getElementById('chat');
const form = document.getElementById('chat-form');
const input = document.getElementById('user-input');
const typing = document.getElementById('typing');

// Helper to add a message bubble
function addMessage(text, sender = 'user') {
    const bubble = document.createElement('div');
    bubble.className = `flex ${sender === 'user' ? 'justify-end' : 'justify-start'}`;
    bubble.innerHTML = `
    <div class="chat-bubble max-w-[75%] px-6 py-4 rounded-3xl shadow-lg transition-all duration-300
      ${sender === 'user'
            ? 'user-bubble rounded-br-none'
            : 'bg-white/90 text-indigo-900 rounded-bl-none border-2 border-pink-200 flex items-center gap-3'}
    ">
      ${sender === 'ai' ? '<span class="text-3xl">🤖</span>' : ''}
      <span class="text-lg leading-relaxed">${text.replace(/\n/g, '<br>')}</span>
    </div>
  `;
    chat.appendChild(bubble);
    chat.scrollTop = chat.scrollHeight;
}

// Show/hide typing indicator
function showTyping(show = true) {
    typing.style.display = show ? 'block' : 'none';
    chat.scrollTop = chat.scrollHeight;
}

// Handle form submit
form.onsubmit = async (e) => {
    e.preventDefault();
    const message = input.value.trim();
    if (!message) return;
    addMessage(message, 'user');
    input.value = '';
    showTyping(true);

    // Send to backend
    const res = await fetch('/ai', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message })
    });
    const data = await res.json();
    showTyping(false);

    if (data.result && Array.isArray(data.result) && data.result.length > 0 && data.result[0].title && data.result[0].url) {
        // News results
        let newsHtml = '<div class="mb-2 font-semibold text-indigo-600">Here are some news articles I found:</div>';
        newsHtml += data.result.map(a =>
            `<a href="${a.url}" target="_blank" class="block p-4 mb-2 bg-indigo-50 rounded-lg shadow hover:bg-pink-100 transition">
          <span class="font-semibold">${a.title}</span>
      </a>`
        ).join('');
        addMessage(newsHtml, 'ai');
    } else if (data.ai) {
        addMessage(data.ai, 'ai');
    } else if (data.error) {
        addMessage('Oops! ' + data.error, 'ai');
    }
};

// Welcome message
window.onload = () => {
    setTimeout(() => {
        addMessage('Hey there! ✨ I\'m <b>Metta</b>, your delightful AI agent. Ask me anything, or just say hi! 💬', 'ai');
    }, 400);
}; 