import { siteConfig } from "@/content/site";
import Image from "next/image";

export default function Hero() {
  return (
    <section className="relative min-h-[90vh] overflow-hidden pt-20">
      {/* Banner background */}
      <div className="absolute inset-0">
        <Image
          src={siteConfig.banner}
          alt="EditForge cinematic editing studio"
          fill
          priority
          className="object-cover object-center opacity-40"
          sizes="100vw"
        />
        <div className="absolute inset-0 bg-gradient-to-b from-black/70 via-black/50 to-[#050505]" />
      </div>

      <div className="relative mx-auto flex max-w-6xl flex-col items-start justify-center px-4 py-24 sm:px-6 lg:px-8">
        <p className="mb-3 text-sm font-medium uppercase tracking-widest text-[#f5c518]">
          {siteConfig.role}
        </p>
        <h1 className="max-w-3xl text-4xl font-bold leading-tight tracking-tight text-white sm:text-5xl lg:text-6xl">
          {siteConfig.tagline}
        </h1>
        <p className="mt-6 max-w-xl text-lg text-white/70">
          I&apos;m {siteConfig.name} — an independent video editor focused on pacing,
          storytelling, and edits that keep viewers watching.
        </p>

        <div className="mt-10 flex flex-wrap gap-4">
          <a
            href="#work"
            className="rounded-full bg-[#f5c518] px-6 py-3 text-sm font-semibold text-black transition hover:bg-[#ffd54f]"
          >
            View My Work
          </a>
          <a
            href="#contact"
            className="rounded-full border border-white/20 bg-white/5 px-6 py-3 text-sm font-semibold text-white backdrop-blur transition hover:bg-white/10"
          >
            Work With Me
          </a>
        </div>

        <a
          href={siteConfig.youtubeUrl}
          target="_blank"
          rel="noopener noreferrer"
          className="mt-8 inline-flex items-center gap-2 text-sm text-white/60 transition hover:text-[#f5c518]"
        >
          <svg className="h-5 w-5" viewBox="0 0 24 24" fill="currentColor">
            <path d="M23.5 6.2a3 3 0 0 0-2.1-2.1C19.5 3.5 12 3.5 12 3.5s-7.5 0-9.4.6A3 3 0 0 0 .5 6.2 31.5 31.5 0 0 0 0 12a31.5 31.5 0 0 0 .5 5.8 3 3 0 0 0 2.1 2.1c1.9.6 9.4.6 9.4.6s7.5 0 9.4-.6a3 3 0 0 0 2.1-2.1A31.5 31.5 0 0 0 24 12a31.5 31.5 0 0 0-.5-5.8zM9.8 15.5v-7l6.2 3.5-6.2 3.5z" />
          </svg>
          Watch My Edits → {siteConfig.youtubeHandle}
        </a>
      </div>
    </section>
  );
}
