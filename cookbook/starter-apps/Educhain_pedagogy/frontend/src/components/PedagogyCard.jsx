const ICONS = {
  blooms_taxonomy: "🎓",
  socratic_questioning: "❓",
  project_based_learning: "🧩",
  flipped_classroom: "🔁",
  inquiry_based_learning: "🔎",
  constructivist: "🏗️",
  gamification: "🎮",
  peer_learning: "🤝",
};

function toTitleCase(text) {
  return String(text)
    .replace(/_/g, " ")
    .replace(/\b\w/g, (m) => m.toUpperCase());
}

export default function PedagogyCard({ name, description, onClick }) {
  const pretty = toTitleCase(name);
  const icon = ICONS[name] || "📚";

  return (
    <div
      onClick={onClick}
      className="group relative overflow-hidden cursor-pointer rounded-2xl border border-orange-500/30 bg-[#0b0b0b] p-6 shadow-lg shadow-orange-500/5 transition-transform hover:-translate-y-0.5 hover:shadow-orange-500/10"
    >
      <div className="pointer-events-none absolute inset-0 bg-gradient-to-br from-orange-500/5 to-transparent" />

      <div className="relative flex items-start gap-3">
        <div className="text-2xl" aria-hidden>
          {icon}
        </div>
        <div className="flex-1">
          <h2 className="text-lg font-semibold text-orange-200 group-hover:text-orange-100">
            {pretty}
          </h2>
          <p className="mt-1 text-sm leading-6 text-orange-200/80">{description}</p>
        </div>
      </div>

      <div className="relative mt-4 inline-flex items-center gap-1 text-xs font-medium text-orange-300/90 group-hover:text-orange-200">
        <span>Explore</span>
        <span aria-hidden>→</span>
      </div>
    </div>
  );
}
  