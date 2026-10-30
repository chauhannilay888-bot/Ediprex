import { siteConfig } from "@/content/site";

export default function Footer() {
  return (
    <footer className="border-t border-white/5 bg-black py-12">
      <div className="mx-auto flex max-w-6xl flex-col items-center justify-between gap-6 px-4 sm:flex-row sm:px-6 lg:px-8">
        <div>
          <p className="text-lg font-semibold text-white">
            Edit<span className="text-[#f5c518]">Forge</span>
          </p>
          <p className="mt-1 text-sm text-white/50">
            {siteConfig.name} · Video Editor
          </p>
        </div>

        <div className="flex flex-wrap items-center justify-center gap-6 text-sm text-white/60">
          <a href="#work" className="hover:text-white">
            Work
          </a>
          <a href="#about" className="hover:text-white">
            About
          </a>
          <a href="#services" className="hover:text-white">
            Services
          </a>
          <a href="#contact" className="hover:text-white">
            Contact
          </a>
          <a
            href={siteConfig.youtubeUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="hover:text-[#f5c518]"
          >
            YouTube
          </a>
        </div>

        <a
          href="#contact"
          className="rounded-full bg-[#f5c518] px-5 py-2.5 text-sm font-semibold text-black transition hover:bg-[#ffd54f]"
        >
          Start a Project
        </a>
      </div>
      <p className="mt-8 text-center text-xs text-white/30">
        © {new Date().getFullYear()} {siteConfig.name}. All rights reserved.
      </p>
    </footer>
  );
}
