let currentConversationId = null;

if (!isLoggedIn()) window.location.href = 'login.html';

document.getElementById('sidebar-user-name').textContent = getUserName();

function toggleSidebar() {
  const sidebar = document.getElementById('sidebar');
  const overlay = document.getElementById('sidebar-overlay');
  const isOpen  = sidebar.style.left === '0px';
  sidebar.style.left    = isOpen ? '-290px' : '0px';
  overlay.style.display = isOpen ? 'none' : 'block';
  if (!isOpen) loadHistoryList();
}

async function loadHistoryList() {
  const list = document.getElementById('history-list');
  list.innerHTML = '<p style="font-size:12px;color:var(--muted);padding:12px;">Loading...</p>';
  try {
    const conversations = await loadConversations();
    if (conversations.length === 0) {
      list.innerHTML = '<p style="font-size:12px;color:var(--muted);padding:12px;">No saved conversations yet.</p>';
      return;
    }
    list.innerHTML = conversations.map(c => `
      <div class="history-item" onclick="openConversation(${c.id})">
        <div class="history-item-title">${c.title}</div>
        <div class="history-item-meta">
          <span>${c.topic ? '● ' + c.topic : 'General'}</span>
          <span>${formatDate(c.updated_at)}</span>
        </div>
        <button class="history-item-delete" onclick="event.stopPropagation();confirmDelete(${c.id})">✕</button>
      </div>
    `).join('');
  } catch(e) {
    list.innerHTML = '<p style="font-size:12px;color:#f87171;padding:12px;">Failed to load history.</p>';
  }
}

async function openConversation(id) {
  try {
    const convo = await loadConversation(id);
    currentConversationId = convo.id;
    document.getElementById('messages').innerHTML = '';
    history = [];

    if (convo.topic && TOPICS[convo.topic]) {
      activeTopic = convo.topic;
      document.querySelectorAll('.chip').forEach(c => c.classList.remove('active'));
      document.getElementById('topic-indicator').style.display = 'flex';
      document.getElementById('topic-label').textContent = `Focused on: ${TOPICS[convo.topic].label}`;
    }

    convo.messages.forEach(m => addMessage(m.role === 'user' ? 'user' : 'bot', m.content));
    history = convo.messages.map(m => ({ role: m.role, content: m.content }));
    toggleSidebar();
  } catch(e) {
    console.error('Failed to load conversation:', e);
  }
}

function newChat() {
  currentConversationId = null;
  history = [];
  activeTopic = null;
  document.getElementById('messages').innerHTML = '';
  document.getElementById('topic-indicator').style.display = 'none';
  document.querySelectorAll('.chip').forEach(c => c.classList.remove('active'));
  addMessage('bot', 'New chat started. How can I help you today?');
  toggleSidebar();
}

async function autoSave() {
  if (history.length < 2) return;
  const firstUser = history.find(m => m.role === 'user');
  const title = firstUser
    ? firstUser.content.substring(0, 52) + (firstUser.content.length > 52 ? '…' : '')
    : 'New conversation';
  try {
    currentConversationId = await saveConversation(currentConversationId, title, activeTopic, history);
  } catch(e) {
    console.error('Auto-save failed:', e);
  }
}

async function confirmDelete(id) {
  if (!confirm('Delete this conversation?')) return;
  await deleteConversation(id);
  loadHistoryList();
}

function formatDate(isoString) {
  const date = new Date(isoString);
  const diff = Date.now() - date;
  if (diff < 60000)        return 'Just now';
  if (diff < 3600000)      return Math.floor(diff/60000) + 'm ago';
  if (diff < 86400000)     return Math.floor(diff/3600000) + 'h ago';
  if (diff < 604800000)    return Math.floor(diff/86400000) + 'd ago';
  return date.toLocaleDateString();
}