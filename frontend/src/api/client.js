const API_BASE = import.meta.env.VITE_API_BASE || "";

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
    ...options,
  });
  let body = null;
  const text = await response.text();
  if (text) {
    try {
      body = JSON.parse(text);
    } catch {
      body = { detail: text };
    }
  }
  if (!response.ok) {
    const detail = body?.detail || response.statusText || "Request failed";
    const error = new Error(typeof detail === "string" ? detail : JSON.stringify(detail));
    error.status = response.status;
    error.body = body;
    throw error;
  }
  return body;
}

export const api = {
  health: () => request("/api/health"),
  config: () => request("/api/config"),
  runQrng: (payload) =>
    request("/api/qrng/run", { method: "POST", body: JSON.stringify(payload) }),
  getExperiment: (id) => request(`/api/experiments/${id}`),
  compare: (payload) =>
    request("/api/analysis/compare", { method: "POST", body: JSON.stringify(payload) }),
  totpEnroll: (payload) =>
    request("/api/auth/totp/enroll", { method: "POST", body: JSON.stringify(payload) }),
  totpVerify: (payload) =>
    request("/api/auth/totp/verify", { method: "POST", body: JSON.stringify(payload) }),
  pqcKeygen: () => request("/api/pqc/keygen", { method: "POST", body: "{}" }),
  pqcChallenge: (sessionId) =>
    request("/api/pqc/challenge", {
      method: "POST",
      body: JSON.stringify({ session_id: sessionId }),
    }),
  pqcVerify: (payload) =>
    request("/api/pqc/verify", { method: "POST", body: JSON.stringify(payload) }),
};
