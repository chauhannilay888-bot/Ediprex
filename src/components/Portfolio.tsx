"use client";

import { useState } from "react";
import { portfolio } from "@/content/site";

export default function Portfolio() {
  const [active, setActive] = useState<string | null>(null);

  return (
    <section id="work" className="border-t border-white/5 bg-[#0a0a0a] py-20 sm:py-28">
      <div className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8">
        <div className="max-w-2xl">
          <p className="text-sm font-medium uppercase tracking-widest text-[#f5c518]">
            Selected Work
          </p>
          <h2 className="mt-2 text-3xl font-bold tracking-tight text-white sm:text-4xl">
            Editing that speaks for itself
          </h2>
          <p className="mt-4 text-white/60">
            A few recent cuts. Watch the pacing, transitions, and how the story
            moves.
          </p>
        </div>

        <div className="mt-12 grid gap-8 md:grid-cols-2">
          {portfolio.map((item) => (
            <article
              key={item.id}
              className="group overflow-hidden rounded-2xl border border-white/8 bg-[#0c0c0c]"
            >
              <div className="relative aspect-video bg-black">
                <video
                  src={item.video}
                  poster={item.poster}
                  controls
                  preload="metadata"
                  playsInline
                  className="h-full w-full object-cover"
                  onPlay={() => setActive(item.id)}
                >
                  Your browser does not support the video tag.
                </video>
              </div>
              <div className="p-5">
                <div className="flex items-center gap-2">
                  <span className="rounded-full bg-[#f5c518]/15 px-2.5 py-0.5 text-xs font-medium text-[#f5c518]">
                    {item.category}
                  </span>
                </div>
                <h3 className="mt-3 text-lg font-semibold text-white">
                  {item.title}
                </h3>
                <p className="mt-2 text-sm leading-relaxed text-white/60">
                  {item.description}
                </p>
              </div>
            </article>
          ))}
        </div>

        <div className="mt-12 text-center">
          <a
            href="#contact"
            className="inline-flex items-center gap-2 text-sm font-medium text-[#f5c518] transition hover:text-[#ffd54f]"
          >
            Like what you see? Let&apos;s talk
            <span aria-hidden>→</span>
          </a>
        </div>
      </div>
    </section>
  );
}
