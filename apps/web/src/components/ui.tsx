import type {
  ButtonHTMLAttributes,
  InputHTMLAttributes,
  ReactNode,
  TextareaHTMLAttributes,
} from "react";

export function Button({
  children,
  className = "",
  variant = "primary",
  ...props
}: ButtonHTMLAttributes<HTMLButtonElement> & {
  children: ReactNode;
  variant?: "primary" | "secondary" | "danger" | "ghost";
}) {
  const variants = {
    primary: "bg-[#5b4bf5] text-white hover:bg-[#4738d4] shadow-sm",
    secondary: "border border-[#d0d5dd] bg-white text-[#344054] hover:bg-[#f9fafb]",
    danger: "border border-[#fda29b] bg-white text-[#b42318] hover:bg-[#fff5f4]",
    ghost: "text-[#475467] hover:bg-[#f2f4f7]",
  };
  return (
    <button
      className={`inline-flex min-h-10 items-center justify-center rounded-lg px-4 py-2 text-sm font-semibold ${variants[variant]} ${className}`}
      {...props}
    >
      {children}
    </button>
  );
}

export function Input({
  label,
  error,
  ...props
}: InputHTMLAttributes<HTMLInputElement> & { label: string; error?: string }) {
  return (
    <label className="grid gap-1.5 text-sm font-medium text-[#344054]">
      {label}
      <input
        className="h-11 rounded-lg border border-[#d0d5dd] bg-white px-3.5 text-[#101828] outline-none placeholder:text-[#98a2b3] focus:border-[#7f73f7] focus:ring-4 focus:ring-[#eeecff]"
        {...props}
      />
      {error && <span className="text-xs text-[#b42318]">{error}</span>}
    </label>
  );
}

export function Textarea({
  label,
  error,
  ...props
}: TextareaHTMLAttributes<HTMLTextAreaElement> & { label: string; error?: string }) {
  return (
    <label className="grid gap-1.5 text-sm font-medium text-[#344054]">
      {label}
      <textarea
        className="min-h-32 resize-y rounded-lg border border-[#d0d5dd] bg-white px-3.5 py-3 text-[#101828] outline-none placeholder:text-[#98a2b3] focus:border-[#7f73f7] focus:ring-4 focus:ring-[#eeecff]"
        {...props}
      />
      {error && <span className="text-xs text-[#b42318]">{error}</span>}
    </label>
  );
}

export function Card({
  children,
  className = "",
}: {
  children: ReactNode;
  className?: string;
}) {
  return (
    <section
      className={`rounded-2xl border border-[#e4e7ec] bg-white shadow-[0_1px_3px_rgba(16,24,40,0.04)] ${className}`}
    >
      {children}
    </section>
  );
}
