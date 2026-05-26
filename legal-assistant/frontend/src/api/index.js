// API 调用封装
const API_BASE = "/api";

export async function healthCheck() {
  const res = await fetch(`${API_BASE}/health`);
  return res.json();
}
