const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

// Render 무료 플랜은 15분 idle 후 슬립 — 콜드스타트 시 30~60초 소요.
// 매 시도마다 25초 타임아웃, 최대 4회 재시도로 총 ~100초까지 버팀.
const ATTEMPT_TIMEOUT_MS = 25000;
const MAX_ATTEMPTS = 4;

async function fetchJson(url, options = {}) {
  let lastError;
  for (let attempt = 1; attempt <= MAX_ATTEMPTS; attempt++) {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), ATTEMPT_TIMEOUT_MS);
    try {
      const res = await fetch(url, { ...options, signal: controller.signal });
      clearTimeout(timer);
      if (!res.ok && res.status >= 500) {
        throw new Error(`server ${res.status}`);
      }
      return res;
    } catch (err) {
      clearTimeout(timer);
      lastError = err;
      if (attempt === MAX_ATTEMPTS) break;
      await new Promise(r => setTimeout(r, 1500));
    }
  }
  throw lastError;
}

export async function fetchPosts(type) {
  const params = type ? `?type=${type}` : '';
  const res = await fetchJson(`${API_BASE}/posts/${params}`);
  return res.json();
}

export async function fetchPost(slug) {
  const res = await fetchJson(`${API_BASE}/posts/${slug}/`);
  return res.json();
}

export async function fetchFeaturedPosts() {
  const res = await fetchJson(`${API_BASE}/posts/featured/`);
  return res.json();
}

export async function fetchTags() {
  const res = await fetchJson(`${API_BASE}/tags/`);
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
