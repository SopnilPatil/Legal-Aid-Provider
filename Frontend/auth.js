const API = window.API_BASE_URL || localStorage.getItem('api_base_url') || 'http://localhost:8000/api';
window.API_BASE_URL = API;

function saveAuth(token, name, email) {
  localStorage.setItem('token',      token);
  localStorage.setItem('user_name',  name);
  localStorage.setItem('user_email', email);
}

function getToken()    { return localStorage.getItem('token'); }
function getUserName() { return localStorage.getItem('user_name'); }
function isLoggedIn()  { return !!getToken(); }

function logout() {
  localStorage.removeItem('token');
  localStorage.removeItem('user_name');
  localStorage.removeItem('user_email');
  window.location.href = 'login.html';
}

async function signup(name, email, password) {
  const res  = await fetch(`${API}/auth/signup`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name, email, password })
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || 'Signup failed');
  saveAuth(data.token, data.name, data.email);
}

async function login(email, password) {
  const res  = await fetch(`${API}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password })
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || 'Login failed');
  saveAuth(data.token, data.name, data.email);
}

async function saveConversation(conversationId, title, topic, messages) {
  const res = await fetch(`${API}/history/save`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${getToken()}`
    },
    body: JSON.stringify({ conversation_id: conversationId, title, topic, messages })
  });
  const data = await res.json();
  return data.id;
}

async function loadConversations() {
  const res = await fetch(`${API}/history`, {
    headers: { 'Authorization': `Bearer ${getToken()}` }
  });
  return await res.json();
}

async function loadConversation(id) {
  const res = await fetch(`${API}/history/${id}`, {
    headers: { 'Authorization': `Bearer ${getToken()}` }
  });
  return await res.json();
}

async function deleteConversation(id) {
  await fetch(`${API}/history/${id}`, {
    method: 'DELETE',
    headers: { 'Authorization': `Bearer ${getToken()}` }
  });
}