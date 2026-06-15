export type CampaignStatus =
  | "draft"
  | "processing"
  | "generated"
  | "review"
  | "approved"
  | "archived"
  | "error";

export interface CampaignAsset {
  id: string;
  campaign_id: string;
  channel: string;
  asset_type: string;
  title: string | null;
  content: string;
  asset_metadata: Record<string, unknown> | unknown[] | null;
  status: string;
  created_at: string;
  updated_at: string;
}

export interface Campaign {
  id: string;
  title: string;
  theme: string | null;
  input_type: string;
  input_text: string | null;
  audience: string | null;
  objective: string | null;
  tone: string | null;
  cta: string | null;
  status: CampaignStatus;
  quality_score: number | null;
  review_notes: string[] | null;
  strategy: Record<string, string> | null;
  created_at: string;
  updated_at: string;
  assets: CampaignAsset[];
}
