"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

import { AppShell } from "@/components/app-shell";
import { StatusBadge } from "@/components/status-badge";
import { Card } from "@/components/ui";
import { api } from "@/lib/api";
import type { Campaign } from "@/types/campaign";

export default function DashboardPage() {
  const [campaigns, setCampaigns] = useState<Campaign[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.campaigns().then(setCampaigns).finally(() => setLoading(false));
  }, []);

  const metrics = [
    { label: "Total de campanhas", value: campaigns.length, color: "text-[#5b4bf5]" },
    {
      label: "Aprovadas",
      value: campaigns.filter((item) => item.status === "approved").length,
      color: "text-[#027a48]",
    },
    {
      label: "Em revisão",
      value: campaigns.filter((item) => item.status === "review").length,
      color: "text-[#c4320a]",
    },
  ];

  return (
    <AppShell>
      <p className="text-sm font-semibold text-[#5b4bf5]">DASHBOARD</p>
      <h1 className="mt-1 text-3xl font-semibold tracking-tight text-[#101828]">
        Sua central de conteúdo
      </h1>
      <p className="mt-2 text-[#667085]">
        Acompanhe campanhas e mantenha a produção em movimento.
      </p>
      <div className="mt-8 grid gap-4 sm:grid-cols-3">
        {metrics.map((metric) => (
          <Card key={metric.label} className="p-5">
            <p className="text-sm text-[#667085]">{metric.label}</p>
            <p className={`mt-3 text-4xl font-semibold ${metric.color}`}>
              {loading ? "—" : metric.value}
            </p>
          </Card>
        ))}
      </div>
      <Card className="mt-6 overflow-hidden">
        <div className="flex items-center justify-between border-b border-[#e4e7ec] px-5 py-4">
          <div>
            <h2 className="font-semibold text-[#101828]">Campanhas recentes</h2>
            <p className="mt-1 text-sm text-[#667085]">Últimos conteúdos trabalhados.</p>
          </div>
          <Link href="/campaigns" className="text-sm font-semibold text-[#5b4bf5]">
            Ver todas
          </Link>
        </div>
        {campaigns.length === 0 && !loading ? (
          <div className="grid place-items-center px-5 py-16 text-center">
            <div className="grid h-12 w-12 place-items-center rounded-full bg-[#eeecff] text-xl text-[#5b4bf5]">
              +
            </div>
            <h3 className="mt-4 font-semibold">Crie sua primeira campanha</h3>
            <p className="mt-1 max-w-sm text-sm text-[#667085]">
              Informe um tema e gere conteúdos adaptados para cada canal.
            </p>
            <Link
              href="/campaigns/new"
              className="mt-5 rounded-lg bg-[#5b4bf5] px-4 py-2 text-sm font-semibold text-white"
            >
              Nova campanha
            </Link>
          </div>
        ) : (
          <div className="divide-y divide-[#e4e7ec]">
            {campaigns.slice(0, 6).map((campaign) => (
              <Link
                key={campaign.id}
                href={`/campaigns/${campaign.id}`}
                className="grid gap-3 px-5 py-4 hover:bg-[#fafafa] sm:grid-cols-[1fr_160px_130px] sm:items-center"
              >
                <div>
                  <p className="font-medium text-[#101828]">{campaign.title}</p>
                  <p className="mt-1 line-clamp-1 text-sm text-[#667085]">{campaign.theme}</p>
                </div>
                <p className="text-sm text-[#667085]">{campaign.objective}</p>
                <StatusBadge status={campaign.status} />
              </Link>
            ))}
          </div>
        )}
      </Card>
    </AppShell>
  );
}
