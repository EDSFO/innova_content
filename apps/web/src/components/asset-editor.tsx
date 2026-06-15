"use client";

import { useState } from "react";

import { Button, Card } from "@/components/ui";
import { api } from "@/lib/api";
import type { CampaignAsset } from "@/types/campaign";

export function AssetEditor({
  asset,
  onSaved,
  onRegenerate,
}: {
  asset: CampaignAsset;
  onSaved: () => void;
  onRegenerate: () => Promise<void>;
}) {
  const [content, setContent] = useState(asset.content);
  const [busy, setBusy] = useState(false);
  const [copied, setCopied] = useState(false);

  return (
    <Card className="overflow-hidden">
      <div className="flex flex-wrap items-center justify-between gap-3 border-b border-[#e4e7ec] px-5 py-4">
        <div>
          <h2 className="font-semibold capitalize text-[#101828]">
            {asset.asset_type.replaceAll("_", " ")}
          </h2>
          <p className="mt-1 text-xs text-[#667085]">
            Editado em {new Date(asset.updated_at).toLocaleString("pt-BR")}
          </p>
        </div>
        <div className="flex gap-2">
          <Button
            variant="secondary"
            onClick={async () => {
              await navigator.clipboard.writeText(content);
              setCopied(true);
              setTimeout(() => setCopied(false), 1500);
            }}
          >
            {copied ? "Copiado" : "Copiar"}
          </Button>
          <Button
            variant="secondary"
            disabled={busy}
            onClick={async () => {
              setBusy(true);
              await onRegenerate();
              setBusy(false);
            }}
          >
            {busy ? "Regenerando..." : "Regenerar"}
          </Button>
          <Button
            disabled={busy || content === asset.content}
            onClick={async () => {
              setBusy(true);
              await api.updateAsset(asset.id, content);
              onSaved();
              setBusy(false);
            }}
          >
            Salvar
          </Button>
        </div>
      </div>
      <textarea
        value={content}
        onChange={(event) => setContent(event.target.value)}
        className="min-h-[440px] w-full resize-y p-6 text-[15px] leading-7 text-[#344054] outline-none"
      />
    </Card>
  );
}
