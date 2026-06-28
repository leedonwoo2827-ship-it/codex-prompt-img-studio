// api.js — 백엔드 호출 래퍼
async function jget(url) {
  const r = await fetch(url);
  if (!r.ok) throw await err(r);
  return r.json();
}
async function jsend(url, method, body) {
  const r = await fetch(url, {
    method,
    headers: { "Content-Type": "application/json" },
    body: body == null ? undefined : JSON.stringify(body),
  });
  if (!r.ok) throw await err(r);
  return r.json();
}
async function err(r) {
  let msg = `HTTP ${r.status}`;
  try { const j = await r.json(); if (j.detail) msg = j.detail; } catch {}
  const e = new Error(msg); e.status = r.status; return e;
}

export const api = {
  authStatus: () => jget("/api/auth/status"),
  getSettings: () => jget("/api/settings"),
  saveSettings: (patch) => jsend("/api/settings", "POST", patch),

  listProjects: () => jget("/api/projects"),
  createProject: (name) => jsend("/api/projects", "POST", { name }),
  renameProject: (id, name) => jsend(`/api/projects/${id}`, "PATCH", { name }),
  deleteProject: (id) => jsend(`/api/projects/${id}`, "DELETE"),

  listImages: (params = {}) => {
    const q = new URLSearchParams();
    if (params.project_id != null) q.set("project_id", params.project_id);
    if (params.favorite) q.set("favorite", "true");
    const s = q.toString();
    return jget("/api/images" + (s ? "?" + s : ""));
  },
  getImage: (id) => jget(`/api/images/${id}`),
  generate: (body) => jsend("/api/images/generate", "POST", body),
  edit: (id, body) => jsend(`/api/images/${id}/edit`, "POST", body),
  compose: (body) => jsend("/api/images/compose", "POST", body),
  favorite: (id) => jsend(`/api/images/${id}/favorite`, "POST"),
  move: (id, project_id) => jsend(`/api/images/${id}/move`, "POST", { project_id }),
  remove: (id) => jsend(`/api/images/${id}`, "DELETE"),
};
