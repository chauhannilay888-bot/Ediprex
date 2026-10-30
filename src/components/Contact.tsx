"use client";

import { useState, FormEvent } from "react";
import { siteConfig } from "@/content/site";

const projectTypes = [
  "YouTube Video",
  "Shorts / Reels",
  "Long-Form Editing",
  "Motion Graphics",
  "Cinematic Editing",
  "Other",
];

type Status = "idle" | "loading" | "success" | "error";

export default function Contact() {
  const [status, setStatus] = useState<Status>("idle");
  const [errorMsg, setErrorMsg] = useState("");

  async function handleSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setStatus("loading");
    setErrorMsg("");

    const form = e.currentTarget;
    const data = new FormData(form);

    // Honeypot
    if (data.get("website")) {
      setStatus("success");
      return;
    }

    const payload = {
      name: String(data.get("name") || "").trim(),
      email: String(data.get("email") || "").trim(),
      phone: String(data.get("phone") || "").trim(),
      social: String(data.get("social") || "").trim(),
      projectType: String(data.get("projectType") || "").trim(),
      message: String(data.get("message") || "").trim(),
    };

    if (!payload.name || !payload.email || !payload.message) {
      setStatus("error");
      setErrorMsg("Please fill in name, email, and message.");
      return;
    }

    try {
      const res = await fetch("/api/contact", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      const json = await res.json().catch(() => ({}));

      if (!res.ok) {
        setStatus("error");
        setErrorMsg(
          json.error ||
            "Something went wrong while sending your message. Please try again or contact me directly by email/WhatsApp."
        );
        return;
      }

      setStatus("success");
      form.reset();
    } catch {
      setStatus("error");
      setErrorMsg(
        "Something went wrong while sending your message. Please try again or contact me directly by email/WhatsApp."
      );
    }
  }

  const whatsappUrl = `https://wa.me/${siteConfig.whatsapp.replace(/\D/g, "")}?text=${encodeURIComponent(
    "Hi, I found your video editing portfolio and would like to discuss a project."
  )}`;

  return (
    <section id="contact" className="border-t border-white/5 py-20 sm:py-28">
      <div className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8">
        <div className="max-w-2xl">
          <p className="text-sm font-medium uppercase tracking-widest text-[#f5c518]">
            Contact
          </p>
          <h2 className="mt-2 text-3xl font-bold tracking-tight text-white sm:text-4xl">
            Let&apos;s talk about your next video
          </h2>
          <p className="mt-4 text-white/60">
            Tell me about your project. I usually reply within a day or two.
          </p>
        </div>

        <div className="mt-12 grid gap-12 lg:grid-cols-[1.2fr_0.8fr]">
          <form onSubmit={handleSubmit} className="space-y-5" noValidate>
            {/* Honeypot */}
            <input
              type="text"
              name="website"
              tabIndex={-1}
              autoComplete="off"
              className="absolute left-[-9999px] opacity-0"
              aria-hidden="true"
            />

            <div className="grid gap-5 sm:grid-cols-2">
              <div>
                <label htmlFor="name" className="block text-sm font-medium text-white/80">
                  Name <span className="text-[#f5c518]">*</span>
                </label>
                <input
                  id="name"
                  name="name"
                  type="text"
                  required
                  maxLength={100}
                  className="mt-1.5 w-full rounded-xl border border-white/10 bg-[#0c0c0c] px-4 py-3 text-white placeholder:text-white/30 focus:border-[#f5c518]/50 focus:outline-none"
                  placeholder="Your name"
                />
              </div>
              <div>
                <label htmlFor="email" className="block text-sm font-medium text-white/80">
                  Email <span className="text-[#f5c518]">*</span>
                </label>
                <input
                  id="email"
                  name="email"
                  type="email"
                  required
                  maxLength={150}
                  className="mt-1.5 w-full rounded-xl border border-white/10 bg-[#0c0c0c] px-4 py-3 text-white placeholder:text-white/30 focus:border-[#f5c518]/50 focus:outline-none"
                  placeholder="you@example.com"
                />
              </div>
            </div>

            <div className="grid gap-5 sm:grid-cols-2">
              <div>
                <label htmlFor="phone" className="block text-sm font-medium text-white/80">
                  WhatsApp / Phone
                </label>
                <input
                  id="phone"
                  name="phone"
                  type="tel"
                  maxLength={30}
                  className="mt-1.5 w-full rounded-xl border border-white/10 bg-[#0c0c0c] px-4 py-3 text-white placeholder:text-white/30 focus:border-[#f5c518]/50 focus:outline-none"
                  placeholder="+91 ..."
                />
              </div>
              <div>
                <label htmlFor="social" className="block text-sm font-medium text-white/80">
                  YouTube / Social Link
                </label>
                <input
                  id="social"
                  name="social"
                  type="url"
                  maxLength={200}
                  className="mt-1.5 w-full rounded-xl border border-white/10 bg-[#0c0c0c] px-4 py-3 text-white placeholder:text-white/30 focus:border-[#f5c518]/50 focus:outline-none"
                  placeholder="https://..."
                />
              </div>
            </div>

            <div>
              <label htmlFor="projectType" className="block text-sm font-medium text-white/80">
                Project Type
              </label>
              <select
                id="projectType"
                name="projectType"
                className="mt-1.5 w-full rounded-xl border border-white/10 bg-[#0c0c0c] px-4 py-3 text-white focus:border-[#f5c518]/50 focus:outline-none"
                defaultValue=""
              >
                <option value="" disabled>
                  Select a type
                </option>
                {projectTypes.map((t) => (
                  <option key={t} value={t}>
                    {t}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label htmlFor="message" className="block text-sm font-medium text-white/80">
                Message <span className="text-[#f5c518]">*</span>
              </label>
              <textarea
                id="message"
                name="message"
                required
                rows={5}
                maxLength={2000}
                className="mt-1.5 w-full resize-y rounded-xl border border-white/10 bg-[#0c0c0c] px-4 py-3 text-white placeholder:text-white/30 focus:border-[#f5c518]/50 focus:outline-none"
                placeholder="Tell me about your project, goals, and timeline..."
              />
            </div>

            {status === "success" && (
              <p className="rounded-xl border border-green-500/30 bg-green-500/10 px-4 py-3 text-sm text-green-400">
                Message received. Thanks — I&apos;ll get back to you soon.
              </p>
            )}
            {status === "error" && (
              <p className="rounded-xl border border-red-500/30 bg-red-500/10 px-4 py-3 text-sm text-red-400">
                {errorMsg}
              </p>
            )}

            <button
              type="submit"
              disabled={status === "loading"}
              className="w-full rounded-full bg-[#f5c518] px-6 py-3.5 text-sm font-semibold text-black transition hover:bg-[#ffd54f] disabled:opacity-60 sm:w-auto"
            >
              {status === "loading" ? "Sending..." : "Send Message"}
            </button>
          </form>

          <div className="space-y-6">
            <div className="rounded-2xl border border-white/8 bg-[#0c0c0c] p-6">
              <h3 className="text-sm font-medium uppercase tracking-wider text-white/50">
                Email
              </h3>
              <a
                href={`mailto:${siteConfig.email}`}
                className="mt-2 block text-lg text-white transition hover:text-[#f5c518]"
              >
                {siteConfig.email}
              </a>
            </div>

            <div className="rounded-2xl border border-white/8 bg-[#0c0c0c] p-6">
              <h3 className="text-sm font-medium uppercase tracking-wider text-white/50">
                WhatsApp
              </h3>
              <p className="mt-2 text-lg text-white">{siteConfig.whatsappDisplay}</p>
              <a
                href={whatsappUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="mt-4 inline-flex items-center gap-2 rounded-full border border-white/15 bg-white/5 px-4 py-2 text-sm font-medium text-white transition hover:bg-white/10"
              >
                Message Me on WhatsApp
              </a>
            </div>

            <div className="rounded-2xl border border-white/8 bg-[#0c0c0c] p-6">
              <h3 className="text-sm font-medium uppercase tracking-wider text-white/50">
                YouTube
              </h3>
              <a
                href={siteConfig.youtubeUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="mt-2 block text-lg text-white transition hover:text-[#f5c518]"
              >
                {siteConfig.youtubeHandle}
              </a>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
