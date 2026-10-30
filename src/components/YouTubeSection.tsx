import { siteConfig } from "@/content/site";

export default function YouTubeSection() {
  return (
    <section className="border-t border-white/5 py-20 sm:py-28">
      <div className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8">
        <div className="rounded-3xl border border-white/8 bg-gradient-to-br from-[#111] to-[#0a0a0a] px-6 py-12 text-center sm:px-12">
          <p className="text-sm font-medium uppercase tracking-widest text-[#f5c518]">
            YouTube
          </p>
          <h2 className="mt-3 text-3xl font-bold tracking-tight text-white sm:text-4xl">
            See more of my editing work
          </h2>
          <p className="mx-auto mt-4 max-w-xl text-white/60">
            The channel{" "}
            <span className="text-white">{siteConfig.youtubeHandle}</span>{" "}
            showcases examples of my edits — pacing, structure, and the kind of
            cuts I build for creators.
          </p>
          <a
            href={siteConfig.youtubeUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="mt-8 inline-flex items-center gap-2 rounded-full bg-[#f5c518] px-6 py-3 text-sm font-semibold text-black transition hover:bg-[#ffd54f]"
          >
            <svg className="h-5 w-5" viewBox="0 0 24 24" fill="currentColor">
              <path d="M23.5 6.2a3 3 0 0 0-2.1-2.1C19.5 3.5 12 3.5 12 3.5s-7.5 0-9.4.6A3 3 0 0 0 .5 6.2 31.5 31.5 0 0 0 0 12a31.5 31.5 0 0 0 .5 5.8 3 3 0 0 0 2.1 2.1c1.9.6 9.4.6 9.4.6s7.5 0 9.4-.6a3 3 0 0 0 2.1-2.1A31.5 31.5 0 0 0 24 12a31.5 31.5 0 0 0-.5-5.8zM9.8 15.5v-7l6.2 3.5-6.2 3.5z" />
            </svg>
            See More of My Work
          </a>
        </div>
      </div>
    </section>
  );
}
