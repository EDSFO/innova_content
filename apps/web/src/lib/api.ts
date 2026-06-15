import type { Campaign, CampaignAsset } from "@/types/campaign";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000/api";
const TOKEN_KEY = "innova_access_token";

export function getToken() {
  if (typeof window === "undefined") return null;
  return localStorage.getItem(TOKEN_KEY);
}

export function setToken(token: string) {
  localStorage.setItem(TOKEN_KEY, token);
}

export function clearToken() {
  localStorage.removeItem(TOKEN_KEY);
}

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const token = getToken();
  const response = await fetch(`${API_URL}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...options.headers,
    },
  });
  if (!response.ok) {
    const body = await response.json().catch(() => null);
    const detail = body?.detail;
    const message =
      typeof detail === "string"
        ? detail
        : Array.isArray(detail)
          ? detail.map((item: { msg?: string }) => item.msg).join(", ")
          : "Não foi possível concluir a operação";
    throw new Error(message);
  }
  if (response.status === 204) return undefined as T;
  return response.json();
}

export const api = {
  register: (data: { name: string; email: string; password: string }) =>
    request<{ access_token: string }>("/auth/register", {
      method: "POST",
      body: JSON.stringify(data),
    }),
  login: (data: { email: string; password: string }) =>
    request<{ access_token: string }>("/auth/login", {
      method: "POST",
      body: JSON.stringify(data),
    }),
  me: () => request<{ id: string; name: string; email: string }>("/auth/me"),
  campaigns: () => request<Campaign[]>("/campaigns"),
  campaign: (id: string) => request<Campaign>(`/campaigns/${id}`),
  createCampaign: (data: Record<string, unknown>) =>
    request<Campaign>("/campaigns", { method: "POST", body: JSON.stringify(data) }),
  generate: (id: string) =>
    request<Campaign>(`/campaigns/${id}/generate`, { method: "POST" }),
  regenerate: (id: string, assetType: string) =>
    request<Campaign>(`/campaigns/${id}/regenerate`, {
      method: "POST",
      body: JSON.stringify({ asset_type: assetType }),
    }),
  updateAsset: (id: string, content: string) =>
    request<CampaignAsset>(`/assets/${id}`, {
      method: "PATCH",
      body: JSON.stringify({ content, status: "review" }),
    }),
  approve: (id: string) =>
    request<Campaign>(`/campaigns/${id}/approve`, { method: "POST" }),
  archive: (id: string) =>
    request<Campaign>(`/campaigns/${id}/archive`, { method: "POST" }),
  duplicate: (id: string) =>
    request<Campaign>(`/campaigns/${id}/duplicate`, { method: "POST" }),
  deleteCampaign: (id: string) =>
    request<void>(`/campaigns/${id}`, { method: "DELETE" }),
};
