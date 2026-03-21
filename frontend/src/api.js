const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

export async function fetchPosts(type) {
  const params = type ? `?type=${type}` : '';
  const res = await fetch(`${API_BASE}/posts/${params}`);
  return res.json();
}

export async function fetchPost(slug) {
  const res = await fetch(`${API_BASE}/posts/${slug}/`);
  return res.json();
}

export async function fetchFeaturedPosts() {
  const res = await fetch(`${API_BASE}/posts/featured/`);
  return res.json();
}

export async function fetchTags() {
  const res = await fetch(`${API_BASE}/tags/`);
  return res.json();
}

export async function subscribe(email) {
  const res = await fetch(`${API_BASE}/subscribe/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email }),
  });
  const data = await res.json();
  if (!res.ok) throw data;
  return data;
}
