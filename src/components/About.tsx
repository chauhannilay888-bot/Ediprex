import { siteConfig } from "@/content/site";

export default function About() {
  return (
    <section id="about" className="border-t border-white/5 bg-[#0a0a0a] py-20 sm:py-28">
      <div className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8">
        <div className="grid gap-12 lg:grid-cols-[1fr_1.4fr] lg:items-center">
          <div className="flex justify-center lg:justify-start">
            <div className="relative flex h-48 w-48 items-center justify-center overflow-hidden rounded-2xl border border-white/10 bg-gradient-to-br from-[#1a1a1a] to-[#0c0c0c] sm:h-56 sm:w-56">
              {siteConfig.profileImage ? (
                // eslint-disable-next-line @next/next/no-img-element
                <img
                  src={siteConfig.profileImage}
                  alt={siteConfig.name}
                  className="h-full w-full object-cover"
                />
              ) : (
                <span className="text-5xl font-bold tracking-tight text-[#f5c518]">
                  {siteConfig.name
                    .split(" ")
                    .map((n) => n[0])
                    .join("")}
                </span>
              )}
            </div>
          </div>

          <div>
            <p className="text-sm font-medium uppercase tracking-widest text-[#f5c518]">
              About
            </p>
            <h2 className="mt-2 text-3xl font-bold tracking-tight text-white sm:text-4xl">
              {siteConfig.name}
            </h2>
            <p className="mt-1 text-lg text-white/60">{siteConfig.role}</p>

            <p className="mt-6 text-base leading-relaxed text-white/75">
              {siteConfig.shortBio}
            </p>
            <p className="mt-4 text-base leading-relaxed text-white/75">
              I care about the moments that make people stay — the cut that lands,
              the beat that hits, the visual that makes a point stick. Whether
              it&apos;s a long YouTube video or a fast Short, the goal is the same:
              make the content stronger than the raw footage.
            </p>
            <p className="mt-4 text-base leading-relaxed text-white/75">
              I work directly with creators. No agency layers. Just clear
              communication, honest feedback, and edits tailored to your style
              and audience.
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}
