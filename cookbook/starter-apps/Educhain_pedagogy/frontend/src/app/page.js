"use client";

import { useEffect, useRef, useState } from "react";
import { getPedagogies } from "../lib/api";
import PedagogyCard from "../components/PedagogyCard";
import { useRouter } from "next/navigation";

export default function Home() {
  const [pedagogies, setPedagogies] = useState({});
  const [topic, setTopic] = useState("");
  const [topicError, setTopicError] = useState("");
  const topicRef = useRef(null);
  const router = useRouter();

  useEffect(() => {
    getPedagogies().then(setPedagogies);
  }, []);

  return (
    <div className="relative min-h-screen bg-black text-orange-100">
      {/* Decorative background */}
      <div className="pointer-events-none absolute inset-0 [background:radial-gradient(60rem_40rem_at_20%_-10%,rgba(249,115,22,0.15),transparent),radial-gradient(60rem_40rem_at_80%_10%,rgba(234,88,12,0.12),transparent)]" />

      <div className="relative mx-auto max-w-6xl px-6 py-10">
        {/* Hero */}
        <header className="mb-10 text-center">
          <h1 className="inline-block pb-1 text-4xl md:text-6xl font-extrabold tracking-tight leading-[1.1] bg-gradient-to-r from-orange-400 via-amber-300 to-orange-500 bg-clip-text text-transparent">
            Educhain Pedagogy
          </h1>
          <p className="mt-3 text-sm md:text-base text-orange-200/80 max-w-2xl mx-auto">
            Generate tailored learning experiences across pedagogical styles. Choose a pedagogy, set your topic, and explore.
          </p>
        </header>

        {/* Topic input */}
        <div className="mb-8">
          <input
            id="topic"
            ref={topicRef}
            type="text"
            placeholder="Enter a topic (e.g., Renewable Energy)"
            value={topic}
            onChange={(e) => {
              setTopic(e.target.value);
              if (topicError) setTopicError("");
            }}
            className={`w-full p-3 rounded-lg bg-black/40 border text-orange-100 placeholder-orange-200/50 focus:outline-none focus:ring-2 ${
              topicError
                ? "border-red-500/60 focus:ring-red-500/40"
                : "border-orange-500/30 focus:ring-orange-500/40"
            }`}
          />
          {topicError ? (
            <div className="mt-2 text-xs text-red-400">{topicError}</div>
          ) : (
            <div className="mt-2 text-xs text-orange-300/70">Tip: Be specific for richer outputs (e.g., &ldquo;Photosynthesis for grade 8&rdquo;).</div>
          )}
        </div>

        {/* Section title */}
        <div className="mb-4 flex items-center gap-3">
          <div className="h-px flex-1 bg-gradient-to-r from-transparent via-orange-500/30 to-transparent" />
          <span className="text-xs uppercase tracking-widest text-orange-300/80">Choose a pedagogy</span>
          <div className="h-px flex-1 bg-gradient-to-r from-transparent via-orange-500/30 to-transparent" />
        </div>

        {/* Cards grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {Object.entries(pedagogies).map(([name, info]) => (
            <PedagogyCard
              key={name}
              name={name}
              description={info.description}
              onClick={() => {
                const trimmed = topic.trim();
                if (!trimmed) {
                  setTopicError("Topic is required.");
                  topicRef.current?.focus();
                  return;
                }
                if (trimmed.length < 3) {
                  setTopicError("Enter at least 3 characters.");
                  topicRef.current?.focus();
                  return;
                }
                router.push(`/pedagogy/${name}?topic=${encodeURIComponent(trimmed)}`);
              }}
            />
          ))}
        </div>
      </div>
    </div>
  );
}
