"use client";

import Link from "next/link";
import { useCallback, useEffect, useState } from "react";

import { AppShell } from "@/components/app-shell";
import { StatusBadge } from "@/components/status-badge";
import { Button, Card } from "@/components/ui";
import { api } from "@/lib/api";
import type { Campaign } from "@/types/campaign";

export default function CampaignsPage() {
  const [campaigns, setCampaigns] = useState<Campaign[]>([]);
  const [query, setQuery] = useState("");
  const [error, setError] = useState("");
  const load = useCallback(() => {
    api.campaigns().then(setCampaigns).catch((err) => setError(err.message));
  }, []);

  useEffect(load, [load]);
  const filtered = campaigns.filter((item) =>
    `${item.title} ${item.theme} ${item.objective}`.toLowerCase().includes(query.toLowerCase()),
  );

  return (
    <AppShell>
      <p className="text-sm font-semibold text-[#5b4bf5]">HISTÓRICO</p>
      <h1 className="mt-1 text-3xl font-semibold text-[#101828]">Campanhas</h1>
      <p className="mt-2 text-[#667085]">Encontre, duplique ou retome conteúdos anteriores.</p>
      <Card className="mt-7 overflow-hidden">
        <div className="border-b border-[#e4e7ec] p-4">
          <input
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            placeholder="Buscar por título, tema ou objetivo..."
            className="h-11 w-full max-w-lg rounded-lg border border-[#d0d5dd] px-3.5 outline-none focus:border-[#7f73f7] focus:ring-4 focus:ring-[#eeecff]"
          />
        </div>
        {error && (
          <p className="m-4 rounded-lg bg-[#fef3f2] p-3 text-sm text-[#b42318]">{error}</p>
        )}
        <div className="overflow-x-auto">
          <table className="w-full min-w-[760px] text-left text-sm">
            <thead className="bg-[#f9fafb] text-xs uppercase tracking-wide text-[#667085]">
              <tr>
                <th className="px-5 py-3 font-semibold">Campanha</th>
                <th className="px-5 py-3 font-semibold">Objetivo</th>
                <th className="px-5 py-3 font-semibold">Status</th>
                <th className="px-5 py-3 font-semibold">Data</th>
                <th className="px-5 py-3 font-semibold">Ações</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#e4e7ec]">
              {filtered.map((campaign) => (
                <tr key={campaign.id} className="hover:bg-[#fafafa]">
                  <td className="px-5 py-4">
                    <Link
                      href={`/campaigns/${campaign.id}`}
                      className="font-semibold text-[#101828] hover:text-[#5b4bf5]"
                    >
                      {campaign.title}
                    </Link>
                    <p className="mt-1 max-w-md truncate text-[#667085]">{campaign.theme}</p>
                  </td>
                  <td className="px-5 py-4 text-[#475467]">{campaign.objective}</td>
                  <td className="px-5 py-4">
                    <StatusBadge status={campaign.status} />
                  </td>
                  <td className="px-5 py-4 text-[#667085]">
                    {new Date(campaign.created_at).toLocaleDateString("pt-BR")}
                  </td>
                  <td className="px-5 py-4">
                    <div className="flex gap-2">
                      <Button
                        variant="ghost"
                        onClick={async () => {
                          await api.duplicate(campaign.id);
                          load();
                        }}
                      >
                        Duplicar
                      </Button>
                      <Button
                        variant="ghost"
                        onClick={async () => {
                          await api.archive(campaign.id);
                          load();
                        }}
                      >
                        Arquivar
                      </Button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>
    </AppShell>
  );
}
