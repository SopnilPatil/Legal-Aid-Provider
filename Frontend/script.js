const TOPICS = {
  consumer: {
    label: '🛒 Consumer rights',
    focus: `Focus exclusively on CONSUMER RIGHTS:
- Consumer Protection Act 2019
- District/State/National Consumer Commissions
- Product liability, defective goods, deficient services
- Unfair trade practices, misleading advertisements
- E-commerce consumer rights, refunds, replacements`
  },
  property: {
    label: '🏠 Property & rent',
    focus: `Focus exclusively on PROPERTY & RENT:
- Transfer of Property Act 1882
- State-specific Rent Control Acts
- RERA 2016
- Landlord-tenant rights, security deposit recovery
- Eviction procedures and notice periods`
  },
  employment: {
    label: '💼 Employment & labour',
    focus: `Focus exclusively on EMPLOYMENT & LABOUR:
- Industrial Disputes Act 1947
- Payment of Wages Act, Minimum Wages Act
- Wrongful termination, retrenchment
- Gratuity, Provident Fund, ESI
- POSH Act 2013, Maternity Benefit Act`
  },
  family: {
    label: '👨‍👩‍👧 Family & marriage',
    focus: `Focus exclusively on FAMILY & MARRIAGE:
- Hindu Marriage Act 1955, Special Marriage Act 1954
- Muslim Personal Law, Christian Marriage Act
- Grounds for divorce, judicial separation
- Maintenance — Section 125 CrPC
- PWDVA 2005, child custody, adoption`
  },
  criminal: {
    label: '🚔 Criminal & FIR',
    focus: `Focus exclusively on CRIMINAL & FIR:
- IPC 1860, Bharatiya Nyaya Sanhita (BNS) 2023
- CrPC / BNSS 2023
- How to file FIR — Section 154 CrPC, Zero FIR
- Bail, anticipatory bail, rights of accused
- Cybercrime, cheating, fraud`
  },
  rti: {
    label: '📄 RTI & govt services',
    focus: `Focus exclusively on RTI & GOVT SERVICES:
- RTI Act 2005
- Filing RTI online (rtionline.gov.in) and offline
- PIO obligations, 30-day deadline
- First appeal, second appeal to CIC/SIC
- Section 8 exemptions`
  }
};

const BASE_SYSTEM_PROMPT = `You are Legal Aid Provider, a knowledgeable and empathetic Indian legal assistant chatbot. You help ordinary Indian citizens understand their legal rights and available options under Indian law. Be warm, clear, and practical.

Always follow this response structure:
1. Brief empathetic acknowledgment
2. Identify relevant law(s) — wrap every law/act/section in [LAW: ...] tags e.g. [LAW: Consumer Protection Act 2019]
3. Explain rights in simple, jargon-free language
4. Give 2-4 concrete next steps
5. Mention the appropriate forum or authority
6. Short disclaimer to consult a licensed advocate`;

const LANG_INSTRUCTIONS = {
  en: 'Respond in English.',
  hi: 'Respond in Hindi (हिंदी में उत्तर दें).',
  ta: 'Respond in Tamil (தமிழில் பதிலளிக்கவும்).',
  te: 'Respond in Telugu (తెలుగులో సమాధానం ఇవ్వండి).',
  bn: 'Respond in Bengali (বাংলায় উত্তর দিন).',
  mr: 'Respond in Marathi (मराठीत उत्तर द्या).',
  gu: 'Respond in Gujarati (ગુજરાતીમાં જવાબ આપો).',
  kn: 'Respond in Kannada (ಕನ್ನಡದಲ್ಲಿ ಉತ್ತರಿಸಿ).'
};

let history     = [];
let loading     = false;
let activeTopic = null;
let activeLang  = 'en';

function getSystemPrompt() {
  let prompt = BASE_SYSTEM_PROMPT;
  if (activeTopic && TOPICS[activeTopic]) {
    prompt += '\n\nSPECIAL INSTRUCTION — ' + TOPICS[activeTopic].focus;
  }
  prompt += '\n\n' + (LANG_INSTRUCTIONS[activeLang] || LANG_INSTRUCTIONS.en);
  return prompt;
}

function setLang(btn, lang) {
  activeLang = lang;
  document.querySelectorAll('.lang-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  if (recognition) {
    const map = { en:'en-IN', hi:'hi-IN', ta:'ta-IN', te:'te-IN', bn:'bn-IN', mr:'mr-IN', gu:'gu-IN', kn:'kn-IN' };
    recognition.lang = map[lang] || 'en-IN';
  }
}

function setTopic(btn, topicKey) {
  activeTopic = topicKey;
  document.querySelectorAll('.chip').forEach(c => c.classList.remove('active'));
  btn.classList.add('active');
  document.getElementById('topic-indicator').style.display = 'flex';
  document.getElementById('topic-label').textContent = `Focused on: ${TOPICS[topicKey].label}`;
  history = [];
  const welcomes = {
    consumer:   'I am now focused on Consumer Rights. Describe your consumer issue — defective product, refund, bad service, or anything else.',
    property:   'I am now focused on Property & Rent. Describe your issue — landlord dispute, deposit, eviction notice, or anything else.',
    employment: 'I am now focused on Employment. Describe your issue — wrongful termination, unpaid wages, harassment, or anything else.',
    family:     'I am now focused on Family & Marriage. Describe your situation — divorce, maintenance, domestic violence, custody, or anything else.',
    criminal:   'I am now focused on Criminal & FIR. Describe your situation — how to file an FIR, bail, police complaint, or anything else.',
    rti:        'I am now focused on RTI. Describe what information you need from the government and I will guide you through the process.'
  };
  addMessage('bot', welcomes[topicKey]);
}

function clearTopic() {
  activeTopic = null;
  history = [];
  document.querySelectorAll('.chip').forEach(c => c.classList.remove('active'));
  document.getElementById('topic-indicator').style.display = 'none';
  addMessage('bot', 'Topic cleared. You can now ask about any area of Indian law.');
}

function resize(el) {
  el.style.height = 'auto';
  el.style.height = Math.min(el.scrollHeight, 120) + 'px';
}

function handleKey(e) {
  if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendMessage(); }
}

function formatBotText(text) {
  return text
    .replace(/\n/g, '<br>')
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
    .replace(/\[LAW:\s*(.*?)\]/g, '<span class="law-tag">$1</span>');
}

function addMessage(role, text) {
  const msgs = document.getElementById('messages');
  const div  = document.createElement('div');
  div.className = 'msg ' + role;

  const av = document.createElement('div');
  av.className = 'avatar ' + (role === 'bot' ? 'bot-avatar' : 'user-avatar');
  av.textContent = role === 'bot' ? 'LA' : 'You';

  const group = document.createElement('div');
  group.className = 'msg-group';

  const bub = document.createElement('div');
  bub.className = 'bubble';
  bub.innerHTML = role === 'bot' ? formatBotText(text) : text.replace(/\n/g, '<br>');
  group.appendChild(bub);

  if (role === 'bot') {
    const actions = document.createElement('div');
    actions.className = 'msg-actions';
    const copyBtn = document.createElement('button');
    copyBtn.className = 'copy-btn';
    copyBtn.textContent = 'Copy';
    copyBtn.onclick = () => {
      navigator.clipboard.writeText(text);
      copyBtn.textContent = 'Copied!';
      setTimeout(() => copyBtn.textContent = 'Copy', 1800);
    };
    actions.appendChild(copyBtn);
    group.appendChild(actions);
  }

  div.appendChild(av);
  div.appendChild(group);
  msgs.appendChild(div);
  msgs.scrollTop = msgs.scrollHeight;
}

function showTyping() {
  const msgs = document.getElementById('messages');
  const div  = document.createElement('div');
  div.className = 'msg bot';
  div.id = 'typing';
  div.innerHTML = `<div class="avatar bot-avatar">LA</div><div class="typing-bubble"><div class="dot"></div><div class="dot"></div><div class="dot"></div></div>`;
  msgs.appendChild(div);
  msgs.scrollTop = msgs.scrollHeight;
}

function hideTyping() {
  const t = document.getElementById('typing');
  if (t) t.remove();
}

function clearChat() {
  if (!confirm('Clear the entire conversation?')) return;
  history = [];
  document.getElementById('messages').innerHTML = '';
  addMessage('bot', 'Chat cleared. How can I help you?');
}

async function sendMessage() {
  if (loading) return;
  const input   = document.getElementById('input');
  const sendBtn = document.getElementById('send');
  const text    = input.value.trim();
  if (!text) return;

  input.value = '';
  input.style.height = 'auto';
  addMessage('user', text);
  history.push({ role: 'user', content: text });
  if (history.length > 20) history = history.slice(-20);

  loading = true;
  sendBtn.disabled = true;
  showTyping();

  try {
    const API_BASE = window.API_BASE_URL || localStorage.getItem('api_base_url') || 'http://localhost:8000/api';
    const response = await fetch(`${API_BASE}/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ messages: history, system: getSystemPrompt() })
    });
    const data  = await response.json();
    const reply = data.reply || 'Sorry, I could not process that. Please try again.';

    history.push({ role: 'assistant', content: reply });
    hideTyping();
    addMessage('bot', reply);
    if (typeof autoSave === 'function') autoSave();

  } catch (error) {
    hideTyping();
    addMessage('bot', '⚠️ Network error — make sure your backend is running on localhost:8000');
    console.error('Error:', error);
  }

  loading = false;
  sendBtn.disabled = false;
}

// ── Voice ──
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
let recognition  = null;
let isRecording  = false;
let voiceMode    = false;

if (SpeechRecognition) {
  recognition = new SpeechRecognition();
  recognition.continuous     = false;
  recognition.interimResults = true;
  recognition.lang           = 'en-IN';

  recognition.onresult = (e) => {
    const transcript = Array.from(e.results).map(r => r[0].transcript).join('');
    document.getElementById('input').value = transcript;
    resize(document.getElementById('input'));
  };

  recognition.onend = () => {
    isRecording = false;
    document.getElementById('voice-btn').classList.remove('recording');
    document.getElementById('voice-status').textContent = '';
    const text = document.getElementById('input').value.trim();
    if (text) sendMessage();
  };

  recognition.onerror = (e) => {
    isRecording = false;
    document.getElementById('voice-btn').classList.remove('recording');
    document.getElementById('voice-status').textContent =
      e.error === 'not-allowed' ? '⚠️ Microphone access denied' : '⚠️ Voice error: ' + e.error;
  };
}

function toggleVoice() {
  if (!recognition) return;
  if (isRecording) {
    recognition.stop(); voiceMode = false;
  } else {
    voiceMode = true; isRecording = true;
    document.getElementById('voice-btn').classList.add('recording');
    document.getElementById('voice-status').textContent = '🎤 Listening… speak your question';
    recognition.start();
  }
}

function speakReply(text) {
  if (!window.speechSynthesis) return;
  const clean = text.replace(/\[LAW:\s*(.*?)\]/g, '$1').replace(/\*\*(.*?)\*\*/g, '$1').replace(/\*(.*?)\*/g, '$1');
  const map = { en:'en-IN', hi:'hi-IN', ta:'ta-IN', te:'te-IN', bn:'bn-IN', mr:'mr-IN', gu:'gu-IN', kn:'kn-IN' };
  const utterance = new SpeechSynthesisUtterance(clean);
  utterance.lang = map[activeLang] || 'en-IN';
  utterance.rate = 0.92;
  window.speechSynthesis.cancel();
  window.speechSynthesis.speak(utterance);
}