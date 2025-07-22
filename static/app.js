const chat = document.getElementById('chat');
const form = document.getElementById('chat-form');
const input = document.getElementById('user-input');
const typing = document.getElementById('typing');
const micBtn = document.getElementById('mic-btn');
const listening = document.getElementById('listening');

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

// Speech Recognition
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
if (SpeechRecognition) {
    const recognition = new SpeechRecognition();
    recognition.continuous = true;
    recognition.lang = 'en-US';
    recognition.interimResults = true;
    recognition.maxAlternatives = 1;

    let final_transcript = '';
    let recognition_timeout;

    micBtn.onclick = () => {
        if (micBtn.classList.contains('mic-listening')) {
            recognition.stop();
        } else {
            final_transcript = '';
            input.value = '';
            recognition.start();
        }
    };

    recognition.onstart = () => {
        micBtn.classList.add('mic-listening');
        listening.style.display = 'block';
        clearTimeout(recognition_timeout);
    };

    recognition.onresult = (event) => {
        let interim_transcript = '';
        for (let i = event.resultIndex; i < event.results.length; ++i) {
            if (event.results[i].isFinal) {
                final_transcript += event.results[i][0].transcript;
            } else {
                interim_transcript += event.results[i][0].transcript;
            }
        }
        input.value = final_transcript + interim_transcript;
        
        // Restart timeout
        clearTimeout(recognition_timeout);
        recognition_timeout = setTimeout(() => {
            recognition.stop();
        }, 1500); // Stop after 1.5 seconds of silence
    };

    recognition.onend = () => {
        micBtn.classList.remove('mic-listening');
        listening.style.display = 'none';
        clearTimeout(recognition_timeout);
        if (input.value.trim()) {
            form.dispatchEvent(new Event('submit'));
        }
    };

    recognition.onerror = (event) => {
        micBtn.classList.remove('mic-listening');
        listening.style.display = 'none';
        addMessage(`Sorry, I couldn't understand that. Please try again. Error: ${event.error}`, 'ai');
    };
} else {
    micBtn.style.display = 'none';
    addMessage("Sorry, your browser doesn't support speech recognition.", 'ai');
}


// Welcome message
window.onload = () => {
    setTimeout(() => {
        addMessage('Hey there! ✨ I\'m <b>Metta</b>, your delightful AI agent. Ask me anything, or just say hi! 💬', 'ai');
    }, 400);
};