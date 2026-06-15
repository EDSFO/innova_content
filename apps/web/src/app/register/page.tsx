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
  name: z.string().min(2, "Informe seu nome"),
  email: z.email("Informe um e-mail válido"),
  password: z.string().min(8, "Use pelo menos 8 caracteres"),
});
type FormData = z.infer<typeof schema>;

export default function RegisterPage() {
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
      const response = await api.register(data);
      setToken(response.access_token);
      router.push("/dashboard");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Falha ao criar conta");
    }
  }

  return (
    <main className="grid min-h-screen place-items-center bg-[#f6f7fb] p-6">
      <form
        onSubmit={handleSubmit(submit)}
        className="w-full max-w-md rounded-2xl border border-[#e4e7ec] bg-white p-8 shadow-sm"
      >
        <p className="text-sm font-bold text-[#5b4bf5]">INNOVA CONTENT AGENT</p>
        <h1 className="mt-4 text-3xl font-semibold text-[#101828]">Crie sua conta</h1>
        <p className="mt-2 text-[#667085]">Comece a organizar sua produção multicanal.</p>
        <div className="mt-8 grid gap-5">
          <Input label="Nome" error={errors.name?.message} {...register("name")} />
          <Input
            label="E-mail"
            type="email"
            error={errors.email?.message}
            {...register("email")}
          />
          <Input
            label="Senha"
            type="password"
            error={errors.password?.message}
            {...register("password")}
          />
          {error && (
            <p className="rounded-lg bg-[#fef3f2] p-3 text-sm text-[#b42318]">{error}</p>
          )}
          <Button className="w-full" disabled={isSubmitting}>
            {isSubmitting ? "Criando..." : "Criar conta"}
          </Button>
        </div>
        <p className="mt-6 text-center text-sm text-[#667085]">
          Já possui conta?{" "}
          <Link className="font-semibold text-[#5b4bf5]" href="/login">
            Entrar
          </Link>
        </p>
      </form>
    </main>
  );
}
