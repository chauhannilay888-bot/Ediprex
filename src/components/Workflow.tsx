import { workflow } from "@/content/site";

export default function Workflow() {
  return (
    <section className="border-t border-white/5 bg-[#0a0a0a] py-20 sm:py-28">
      <div className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8">
        <div className="max-w-2xl">
          <p className="text-sm font-medium uppercase tracking-widest text-[#f5c518]">
            Workflow
          </p>
          <h2 className="mt-2 text-3xl font-bold tracking-tight text-white sm:text-4xl">
            How we work together
          </h2>
        </div>

        <div className="mt-12 grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
          {workflow.map((step) => (
            <div key={step.step} className="relative">
              <span className="text-4xl font-bold text-[#f5c518]/40">
                {step.step}
              </span>
              <h3 className="mt-2 text-lg font-semibold text-white">
                {step.title}
              </h3>
              <p className="mt-2 text-sm leading-relaxed text-white/60">
                {step.description}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
