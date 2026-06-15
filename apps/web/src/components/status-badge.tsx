import type { CampaignStatus } from "@/types/campaign";

const labels: Record<CampaignStatus, string> = {
  draft: "Rascunho",
  processing: "Processando",
  generated: "Gerado",
  review: "Em revisão",
  approved: "Aprovado",
  archived: "Arquivado",
  error: "Erro",
};

const styles: Record<CampaignStatus, string> = {
  draft: "bg-[#f2f4f7] text-[#475467]",
  processing: "bg-[#fff6ed] text-[#c4320a]",
  generated: "bg-[#eef4ff] text-[#3538cd]",
  review: "bg-[#f4f3ff] text-[#5925dc]",
  approved: "bg-[#ecfdf3] text-[#027a48]",
  archived: "bg-[#f2f4f7] text-[#667085]",
  error: "bg-[#fef3f2] text-[#b42318]",
};

export function StatusBadge({ status }: { status: CampaignStatus }) {
  return (
    <span className={`inline-flex rounded-full px-2.5 py-1 text-xs font-semibold ${styles[status]}`}>
      {labels[status]}
    </span>
  );
}
