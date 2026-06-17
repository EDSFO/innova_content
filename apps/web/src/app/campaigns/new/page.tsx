"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { useForm, useWatch } from "react-hook-form";
import { z } from "zod";

import { AppShell } from "@/components/app-shell";
import { Button, Card, Input, Textarea } from "@/components/ui";
import { api } from "@/lib/api";

const schema = z
  .object({
    title: z.string().min(3, "Informe um título"),
    input_type: z.enum(["theme", "text"]),
    theme: z.string().optional(),
    input_text: z.string().optional(),
    audience: z.string().min(2, "Informe o público"),
    objective: z.string().min(2),
    tone: z.string().min(2),
    cta: z.string().min(2, "Informe a chamada para ação"),
  })
  .refine((data) => data.theme?.trim() || data.input_text?.trim(), {
    message: "Informe um tema ou texto de entrada",
    path: ["theme"],
  });
type FormData = z.infer<typeof schema>;

const objectives = [
  "educar",
  "gerar autoridade",
  "gerar leads",
  "vender serviço",
  "anunciar novidade",
  "explicar conceito",
  "nutrir audiência",
  "provocar reflexão",
];
const tones = [
  "consultivo",
  "técnico",
  "didático",
  "provocativo",
  "institucional",
  "comercial",
  "simples e direto",
  "executivo",
];

export default function NewCampaignPage() {
  const router = useRouter();
  const [error, setError] = useState("");
  const {
    register,
    handleSubmit,
    control,
    formState: { errors, isSubmitting },
  } = useForm<FormData>({
    resolver: zodResolver(schema),
    defaultValues: {
      input_type: "theme",
      audience: "empresários e gestores",
      objective: "gerar autoridade",
      tone: "consultivo",
      cta: "Solicite um diagnóstico de automação",
    },
  });
  const inputType = useWatch({ control, name: "input_type" });

  async function submit(data: FormData, generate: boolean) {
    setError("");
    try {
      const campaign = await api.createCampaign({
        ...data,
        theme: data.theme || null,
        input_text: data.input_text || null,
      });
      if (generate) await api.generate(campaign.id);
      router.push(`/campaigns/${campaign.id}${generate ? "?tab=linkedin" : ""}`);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Falha ao criar campanha");
    }
  }

  return (
    <AppShell>
      <p className="text-sm font-semibold text-[#5b4bf5]">NOVA CAMPANHA</p>
      <h1 className="mt-1 text-3xl font-semibold text-[#101828]">
        Qual conteúdo vamos transformar?
      </h1>
      <p className="mt-2 text-[#667085]">Defina o contexto para orientar todos os canais.</p>
      <form className="mt-7 grid gap-6 xl:grid-cols-[1fr_340px]">
        <Card className="grid gap-5 p-6">
          <Input
            label="Título da campanha"
            error={errors.title?.message}
            {...register("title")}
          />
          <div className="grid gap-1.5 text-sm font-medium text-[#344054]">
            Tipo de entrada
            <div className="flex gap-2">
              {(["theme", "text"] as const).map((type) => (
                <label
                  key={type}
                  className={`flex-1 cursor-pointer rounded-lg border px-4 py-3 text-center ${
                    inputType === type
                      ? "border-[#7f73f7] bg-[#f4f3ff] text-[#4738d4]"
                      : "border-[#d0d5dd]"
                  }`}
                >
                  <input
                    className="sr-only"
                    type="radio"
                    value={type}
                    {...register("input_type")}
                  />
                  {type === "theme" ? "Tema curto" : "Texto longo"}
                </label>
              ))}
            </div>
          </div>
          {inputType === "theme" ? (
            <Textarea label="Tema" error={errors.theme?.message} {...register("theme")} />
          ) : (
            <Textarea
              label="Texto de referência"
              error={errors.input_text?.message}
              {...register("input_text")}
            />
          )}
          <Input
            label="Público-alvo"
            error={errors.audience?.message}
            {...register("audience")}
          />
          <Textarea label="CTA desejado" error={errors.cta?.message} {...register("cta")} />
          {error && (
            <p className="rounded-lg bg-[#fef3f2] p-3 text-sm text-[#b42318]">{error}</p>
          )}
        </Card>
        <div className="grid content-start gap-5">
          <Card className="grid gap-5 p-6">
            <label className="grid gap-1.5 text-sm font-medium text-[#344054]">
              Objetivo
              <select
                className="h-11 rounded-lg border border-[#d0d5dd] bg-white px-3"
                {...register("objective")}
              >
                {objectives.map((item) => (
                  <option key={item}>{item}</option>
                ))}
              </select>
            </label>
            <label className="grid gap-1.5 text-sm font-medium text-[#344054]">
              Tom de voz
              <select
                className="h-11 rounded-lg border border-[#d0d5dd] bg-white px-3"
                {...register("tone")}
              >
                {tones.map((item) => (
                  <option key={item}>{item}</option>
                ))}
              </select>
            </label>
          </Card>
          <Card className="p-5 text-sm text-[#667085]">
            <p className="font-semibold text-[#344054]">A geração inclui</p>
            <ul className="mt-3 grid gap-2">
              <li>✓ LinkedIn e Instagram</li>
              <li>✓ Imagem social para LinkedIn/Instagram</li>
              <li>✓ Roteiro, título e descrição para YouTube</li>
              <li>✓ Hashtags, CTA e sugestões de cenas</li>
            </ul>
          </Card>
          <Button
            type="button"
            disabled={isSubmitting}
            onClick={handleSubmit((data) => submit(data, true))}
          >
            {isSubmitting ? "Gerando conteúdo e imagem..." : "Gerar conteúdo e imagem"}
          </Button>
          <Button
            type="button"
            variant="secondary"
            disabled={isSubmitting}
            onClick={handleSubmit((data) => submit(data, false))}
          >
            Salvar rascunho
          </Button>
        </div>
      </form>
    </AppShell>
  );
}
