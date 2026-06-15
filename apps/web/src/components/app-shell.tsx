"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { useEffect, useState, type ReactNode } from "react";

import { api, clearToken, getToken } from "@/lib/api";

export function AppShell({ children }: { children: ReactNode }) {
  const pathname = usePathname();
  const router = useRouter();
  const [user, setUser] = useState<{ name: string; email: string } | null>(null);

  useEffect(() => {
    if (!getToken()) {
      router.replace("/login");
      return;
    }
    api.me().then(setUser).catch(() => {
      clearToken();
      router.replace("/login");
    });
  }, [router]);

  const links = [
    { href: "/dashboard", label: "Visão geral", icon: "◫" },
    { href: "/campaigns", label: "Campanhas", icon: "▤" },
    { href: "/campaigns/new", label: "Nova campanha", icon: "+" },
  ];

  return (
    <div className="min-h-screen bg-[#f6f7fb] md:grid md:grid-cols-[248px_1fr]">
      <aside className="border-b border-[#e4e7ec] bg-[#17152f] px-4 py-5 text-white md:min-h-screen md:border-b-0">
        <Link href="/dashboard" className="flex items-center gap-3 px-2">
          <span className="grid h-10 w-10 place-items-center rounded-xl bg-[#6f61ff] text-lg font-black">
            I
          </span>
          <span>
            <strong className="block text-sm">INNOVA</strong>
            <span className="text-xs text-[#a9a3d9]">Content Agent</span>
          </span>
        </Link>
        <nav className="mt-7 flex gap-2 overflow-x-auto md:grid">
          {links.map((link) => {
            const active =
              pathname === link.href ||
              (link.href === "/campaigns" &&
                pathname.startsWith("/campaigns/") &&
                pathname !== "/campaigns/new");
            return (
              <Link
                key={link.href}
                href={link.href}
                className={`flex min-w-max items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium ${
                  active
                    ? "bg-[#2c2854] text-white"
                    : "text-[#b9b5d6] hover:bg-[#242143] hover:text-white"
                }`}
              >
                <span className="w-5 text-center text-base">{link.icon}</span>
                {link.label}
              </Link>
            );
          })}
        </nav>
        <div className="mt-8 hidden border-t border-[#302c54] pt-5 md:block">
          <p className="truncate px-2 text-sm font-semibold">{user?.name ?? "Carregando..."}</p>
          <p className="truncate px-2 text-xs text-[#918bad]">{user?.email}</p>
          <button
            className="mt-3 w-full rounded-lg px-3 py-2 text-left text-sm text-[#b9b5d6] hover:bg-[#242143] hover:text-white"
            onClick={() => {
              clearToken();
              router.replace("/login");
            }}
          >
            Sair
          </button>
        </div>
      </aside>
      <main className="min-w-0">
        <header className="flex h-16 items-center justify-between border-b border-[#e4e7ec] bg-white px-5 md:px-8">
          <p className="text-sm text-[#667085]">Produção de conteúdo com IA</p>
          <Link
            href="/campaigns/new"
            className="rounded-lg bg-[#5b4bf5] px-4 py-2 text-sm font-semibold text-white hover:bg-[#4738d4]"
          >
            + Nova campanha
          </Link>
        </header>
        <div className="mx-auto max-w-[1440px] p-5 md:p-8">{children}</div>
      </main>
    </div>
  );
}
