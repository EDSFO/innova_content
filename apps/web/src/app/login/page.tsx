"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { useForm } from "react-hook-form";
import { z } from "zod";

import { Button, Input } from "@/components/ui";
import { api, setToken } from "@/lib/api";

const schema = z.object({
  email: z.email("Informe um e-mail válido"),
  password: z.string().min(8, "A senha deve ter pelo menos 8 caracteres"),
});
type FormData = z.infer<typeof schema>;

export default function LoginPage() {
  const router = useRouter();
  const [error, setError] = useState("");
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<FormData>({ resolver: zodResolver(schema) });

  async function submit(data: FormData) {
    setError("");
    try {
      const response = await api.login(data);
      setToken(response.access_token);
      router.push("/dashboard");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Falha ao entrar");
    }
  }

  return (
    <main className="grid min-h-screen bg-white lg:grid-cols-2">
      <section className="hidden bg-[#17152f] p-12 text-white lg:flex lg:flex-col lg:justify-between">
        <div className="flex items-center gap-3">
          <span className="grid h-11 w-11 place-items-center rounded-xl bg-[#6f61ff] text-xl font-black">
            I
          </span>
          <strong>INNOVA CONTENT AGENT</strong>
        </div>
        <div className="max-w-xl">
          <p className="mb-5 text-sm font-semibold uppercase tracking-[0.2em] text-[#a9a3d9]">
            Uma ideia. Múltiplos canais.
          </p>
          <h1 className="text-5xl font-semibold leading-[1.08]">
            Transforme conhecimento em conteúdo que gera negócio.
          </h1>
          <p className="mt-6 text-lg leading-8 text-[#bbb7d4]">
            Planeje, gere e revise conteúdos para LinkedIn, Instagram e YouTube em um único
            fluxo.
          </p>
        </div>
        <p className="text-sm text-[#77718f]">Innovaapps © 2026</p>
      </section>
      <section className="grid place-items-center p-6">
        <form onSubmit={handleSubmit(submit)} className="w-full max-w-md">
          <div className="mb-8 lg:hidden">
            <strong className="text-[#4738d4]">INNOVA CONTENT AGENT</strong>
          </div>
          <h2 className="text-3xl font-semibold tracking-tight text-[#101828]">
            Acesse sua conta
          </h2>
          <p className="mt-2 text-[#667085]">Continue criando conteúdo estratégico.</p>
          <div className="mt-8 grid gap-5">
            <Input
              label="E-mail"
              type="email"
              placeholder="voce@empresa.com"
              error={errors.email?.message}
              {...register("email")}
            />
            <Input
              label="Senha"
              type="password"
              placeholder="••••••••"
              error={errors.password?.message}
              {...register("password")}
            />
            {error && (
              <p className="rounded-lg bg-[#fef3f2] p-3 text-sm text-[#b42318]">{error}</p>
            )}
            <Button className="w-full" disabled={isSubmitting}>
              {isSubmitting ? "Entrando..." : "Entrar"}
            </Button>
          </div>
          <p className="mt-6 text-center text-sm text-[#667085]">
            Ainda não tem conta?{" "}
            <Link className="font-semibold text-[#5b4bf5]" href="/register">
              Criar conta
            </Link>
          </p>
        </form>
      </section>
    </main>
  );
}
