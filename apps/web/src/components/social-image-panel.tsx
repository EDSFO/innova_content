"use client";

import { useEffect, useState } from "react";

import { Button, Card } from "@/components/ui";
import { api } from "@/lib/api";
import type { CampaignMedia } from "@/types/campaign";

export function SocialImagePanel({
  campaignId,
  media,
  onChanged,
}: {
  campaignId: string;
  media: CampaignMedia | undefined;
  onChanged: () => void;
}) {
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [preview, setPreview] = useState<{ mediaId: string; url: string } | null>(null);
  const previewUrl = preview && preview.mediaId === media?.id ? preview.url : null;

  useEffect(() => {
    let url: string | null = null;
    if (!media) return;
    api
      .downloadMedia(media.id)
      .then((blob) => {
        url = URL.createObjectURL(blob);
        setPreview({ mediaId: media.id, url });
      })
      .catch((err) => setError(err instanceof Error ? err.message : "Falha ao carregar imagem"));
    return () => {
      if (url) URL.revokeObjectURL(url);
    };
  }, [media]);

  async function generate() {
    setBusy(true);
    setError("");
    try {
      await api.generateSocialImage(campaignId);
      onChanged();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Falha ao gerar imagem");
    } finally {
      setBusy(false);
    }
  }

  async function download() {
    if (!media) return;
    setBusy(true);
    setError("");
    try {
      const blob = await api.downloadMedia(media.id);
      const url = URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.download = media.file_name;
      link.click();
      URL.revokeObjectURL(url);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Falha ao baixar imagem");
    } finally {
      setBusy(false);
    }
  }

  return (
    <Card className="overflow-hidden">
      <div className="flex flex-wrap items-center justify-between gap-3 border-b border-[#e4e7ec] px-5 py-4">
        <div>
          <h2 className="font-semibold text-[#101828]">Imagem social</h2>
          <p className="mt-1 text-xs text-[#667085]">
            Uma imagem compartilhada por LinkedIn e Instagram
          </p>
        </div>
        <div className="flex gap-2">
          {media && (
            <Button variant="secondary" disabled={busy} onClick={download}>
              Baixar PNG
            </Button>
          )}
          <Button disabled={busy} onClick={generate}>
            {busy ? "Gerando..." : media ? "Regenerar imagem" : "Gerar imagem"}
          </Button>
        </div>
      </div>
      <div className="grid gap-4 p-5 md:grid-cols-[280px_1fr]">
        <div className="aspect-square overflow-hidden rounded-lg border border-[#e4e7ec] bg-[#f9fafb]">
          {previewUrl ? (
            // eslint-disable-next-line @next/next/no-img-element
            <img src={previewUrl} alt="Imagem social gerada" className="h-full w-full object-cover" />
          ) : (
            <div className="flex h-full items-center justify-center px-6 text-center text-sm text-[#667085]">
              {media ? "Carregando imagem..." : "Nenhuma imagem gerada ainda."}
            </div>
          )}
        </div>
        <div className="grid content-start gap-3 text-sm text-[#475467]">
          {media ? (
            <>
              <p>
                <span className="font-semibold text-[#344054]">Arquivo:</span> {media.file_name}
              </p>
              <p>
                <span className="font-semibold text-[#344054]">Modelo:</span>{" "}
                {media.model ?? "gpt-image-2"}
              </p>
              <p>
                <span className="font-semibold text-[#344054]">Qualidade:</span>{" "}
                {String(
                  Array.isArray(media.media_metadata)
                    ? "medium"
                    : media.media_metadata?.quality ?? "medium",
                )}
              </p>
              <p className="text-xs text-[#667085]">
                Atualizada em {new Date(media.updated_at).toLocaleString("pt-BR")}
              </p>
            </>
          ) : (
            <p>
              A imagem sera criada com GPT-Image-2 em qualidade medium e ficara
              armazenada para download.
            </p>
          )}
          {error && <p className="rounded-lg bg-[#fef3f2] p-3 text-sm text-[#b42318]">{error}</p>}
        </div>
      </div>
    </Card>
  );
}
