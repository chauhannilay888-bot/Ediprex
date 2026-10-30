import { whyWorkWithMe } from "@/content/site";

export default function WhyWork() {
  return (
    <section className="border-t border-white/5 bg-[#0a0a0a] py-20 sm:py-28">
      <div className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8">
        <div className="max-w-2xl">
          <p className="text-sm font-medium uppercase tracking-widest text-[#f5c518]">
            Why work with me
          </p>
          <h2 className="mt-2 text-3xl font-bold tracking-tight text-white sm:text-4xl">
            Direct. Focused. Real.
          </h2>
        </div>

        <div className="mt-12 grid gap-6 sm:grid-cols-2">
          {whyWorkWithMe.map((item) => (
            <div
              key={item.title}
              className="rounded-2xl border border-white/8 bg-[#0c0c0c] p-6"
            >
              <h3 className="text-lg font-semibold text-white">{item.title}</h3>
              <p className="mt-2 text-sm leading-relaxed text-white/60">
                {item.description}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
