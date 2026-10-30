import { services } from "@/content/site";

export default function Services() {
  return (
    <section id="services" className="border-t border-white/5 py-20 sm:py-28">
      <div className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8">
        <div className="max-w-2xl">
          <p className="text-sm font-medium uppercase tracking-widest text-[#f5c518]">
            Services
          </p>
          <h2 className="mt-2 text-3xl font-bold tracking-tight text-white sm:text-4xl">
            What I can help you with
          </h2>
          <p className="mt-4 text-white/60">
            Practical editing support for creators who want stronger pacing,
            cleaner storytelling, and content that holds attention.
          </p>
        </div>

        <div className="mt-12 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {services.map((s) => (
            <div
              key={s.id}
              className="rounded-2xl border border-white/8 bg-[#0c0c0c] p-6 transition hover:border-[#f5c518]/30"
            >
              <h3 className="text-lg font-semibold text-white">{s.title}</h3>
              <p className="mt-3 text-sm leading-relaxed text-white/60">
                {s.description}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
