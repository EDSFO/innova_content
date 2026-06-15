"use client";

import { useParams, useRouter } from "next/navigation";
import { useCallback, useEffect, useMemo, useState } from "react";

import { AppShell } from "@/components/app-shell";
import { AssetEditor } from "@/components/asset-editor";
import { StatusBadge } from "@/components/status-badge";
import { Button, Card } from "@/components/ui";
import { api } from "@/lib/api";
import type { Campaign } from "@/types/campaign";

const tabs = [
  { id: "strategy", label: "Estratégia" },
  { id: "linkedin", label: "LinkedIn" },
  { id: "instagram", label: "Instagram" },
  { id: "youtube", label: "YouTube" },
  { id: "all", label: "Outros" },
  { id: "review", label: "Revisão" },
];

export default function CampaignDetailPage() {
  const { id } = useParams<{ id: string }>();
  const router = useRouter();
  const [campaign, setCampaign] = useState<Campaign | null>(null);
  const [active, setActive] = useState("strategy");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const load = useCallback(() => {
    api.campaign(id).then(setCampaign).catch((err) => setError(err.message));
  }, [id]);

  useEffect(load, [load]);
  const visibleAssets = useMemo(() => {
    if (!campaign) return [];
    if (active === "all") {
      return campaign.assets.filter((item) =>
        ["hashtags", "cta", "video_scenes"].includes(item.asset_type),
      );
    }
    return campaign.assets.filter((item) => item.channel === active);
  }, [active, campaign]);

  async function action(callback: () => Promise<Campaign>) {
    setBusy(true);
    setError("");
    try {
      setCampaign(await callback());
    } catch (err) {
      setError(err instanceof Error ? err.message : "Operação não concluída");
    } finally {
      setBusy(false);
    }
  }

  if (!campaign) {
    return (
      <AppShell>
        <p className="text-[#667085]">{error || "Carregando campanha..."}</p>
      </AppShell>
    );
  }

  return (
    <AppShell>
      <div className="flex flex-wrap items-start justify-between gap-5">
        <div>
          <div className="flex items-center gap-3">
            <StatusBadge status={campaign.status} />
            <span className="text-sm text-[#98a2b3]">
              {new Date(campaign.created_at).toLocaleDateString("pt-BR")}
            </span>
          </div>
          <h1 className="mt-3 text-3xl font-semibold text-[#101828]">{campaign.title}</h1>
          <p className="mt-2 max-w-3xl text-[#667085]">{campaign.theme}</p>
        </div>
        <div className="flex flex-wrap gap-2">
          {campaign.assets.length === 0 && (
            <Button disabled={busy} onClick={() => action(() => api.generate(id))}>
              {busy ? "Gerando..." : "Gerar conteúdo"}
            </Button>
          )}
          {campaign.assets.length > 0 && (
            <Button disabled={busy} onClick={() => action(() => api.approve(id))}>
              Aprovar campanha
            </Button>
          )}
          <Button
            variant="secondary"
            disabled={busy}
            onClick={() => action(() => api.archive(id))}
          >
            Arquivar
          </Button>
          <Button
            variant="danger"
            disabled={busy}
            onClick={async () => {
              if (!confirm("Excluir esta campanha permanentemente?")) return;
              await api.deleteCampaign(id);
              router.push("/campaigns");
            }}
          >
            Excluir
          </Button>
        </div>
      </div>
      {error && (
        <p className="mt-5 rounded-lg bg-[#fef3f2] p-3 text-sm text-[#b42318]">{error}</p>
      )}
      <div className="mt-7 flex gap-1 overflow-x-auto border-b border-[#e4e7ec]">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActive(tab.id)}
            className={`min-w-max border-b-2 px-4 py-3 text-sm font-semibold ${
              active === tab.id
                ? "border-[#5b4bf5] text-[#5b4bf5]"
                : "border-transparent text-[#667085] hover:text-[#344054]"
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>
      <div className="mt-6">
        {active === "strategy" && (
          <div className="grid gap-5 lg:grid-cols-[1fr_320px]">
            <Card className="p-6">
              <h2 className="font-semibold text-[#101828]">Estratégia narrativa</h2>
              {campaign.strategy ? (
                <dl className="mt-5 grid gap-5 sm:grid-cols-2">
                  {Object.entries(campaign.strategy).map(([key, value]) => (
                    <div key={key} className="rounded-xl bg-[#f9fafb] p-4">
                      <dt className="text-xs font-semibold uppercase tracking-wide text-[#667085]">
                        {key.replaceAll("_", " ")}
                      </dt>
                      <dd className="mt-2 text-sm leading-6 text-[#344054]">{value}</dd>
                    </div>
                  ))}
                </dl>
              ) : (
                <p className="mt-4 text-sm text-[#667085]">
                  A estratégia aparecerá após a geração.
                </p>
              )}
            </Card>
            <Card className="p-6">
              <p className="text-sm text-[#667085]">Qualidade</p>
              <p className="mt-2 text-5xl font-semibold text-[#5b4bf5]">
                {campaign.quality_score ?? "—"}
                <span className="text-xl text-[#98a2b3]">/10</span>
              </p>
              <ul className="mt-5 grid gap-2 text-sm leading-6 text-[#475467]">
                {campaign.review_notes?.map((note) => <li key={note}>✓ {note}</li>)}
              </ul>
            </Card>
          </div>
        )}
        {active === "review" && (
          <Card className="p-6">
            <h2 className="font-semibold">Checklist de revisão</h2>
            <ul className="mt-4 grid gap-3 text-sm text-[#475467]">
              <li>✓ Clareza e coerência entre os canais</li>
              <li>✓ Linguagem compatível com o tom selecionado</li>
              <li>✓ CTA presente e objetivo</li>
              <li>✓ Revisão humana antes da publicação</li>
            </ul>
          </Card>
        )}
        {!["strategy", "review"].includes(active) && (
          <div className="grid gap-5">
            {visibleAssets.map((asset) => (
              <AssetEditor
                key={`${asset.id}-${asset.updated_at}`}
                asset={asset}
                onSaved={load}
                onRegenerate={() => action(() => api.regenerate(id, asset.asset_type))}
              />
            ))}
            {visibleAssets.length === 0 && (
              <Card className="p-10 text-center text-sm text-[#667085]">
                Nenhum conteúdo disponível nesta seção.
              </Card>
            )}
          </div>
        )}
      </div>
    </AppShell>
  );
}
