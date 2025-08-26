import { useRouter } from "next/router";
import dynamic from "next/dynamic";
import { useEffect, useState } from "react";
import { getPedagogies, generateContent } from "../../lib/api";
import ParamForm from "../../components/ParamForm";
import OutputRenderer from "../../components/OutputRenderer";

function toTitleCase(text) {
  return String(text || "")
    .replace(/_/g, " ")
    .replace(/\b\w/g, (m) => m.toUpperCase());
}

function PedagogyPageInner() {
  const router = useRouter();
  const { name, topic } = router.query;
  const [paramsDef, setParamsDef] = useState({});
  const [output, setOutput] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    if (name) {
      getPedagogies().then((data) => {
        setParamsDef(data[name]?.parameters || {});
      });
    }
  }, [name]);

  const handleGenerate = async (params) => {
    setError("");
    const trimmedTopic = (topic || "").trim();
    if (!trimmedTopic || trimmedTopic.length < 3) {
      setError("Please provide a valid topic (at least 3 characters) on the home page and try again.");
      return;
    }
    try {
      setLoading(true);
      console.log("Sending params:", params); // Debug log
      const result = await generateContent(trimmedTopic, name, params);
      console.log("Received result:", result); // Debug log
      setOutput(result.content);
    } catch (e) {
      const message =
        e?.response?.data?.detail ||
        e?.message ||
        "Failed to generate content. Please try again.";
      setError(String(message));
    } finally {
      setLoading(false);
    }
  };

  const displayName = toTitleCase(name);

  return (
    <div className="relative min-h-screen bg-black text-orange-100 p-6">
      <div className="pointer-events-none absolute inset-0 [background:radial-gradient(60rem_40rem_at_20%_-10%,rgba(249,115,22,0.15),transparent),radial-gradient(60rem_40rem_at_80%_10%,rgba(234,88,12,0.12),transparent)]" />
      <div className="relative mx-auto max-w-3xl text-center">
        <h1 className="inline-block pb-1 text-3xl md:text-5xl font-extrabold leading-[1.15] mb-3 bg-gradient-to-r from-orange-400 via-amber-300 to-orange-500 bg-clip-text text-transparent">
          {displayName || "Pedagogy"}
        </h1>
        <h2 className="text-sm md:text-base mb-8 text-orange-200/80">Topic: {topic}</h2>

        {!output ? (
          <div className="mx-auto max-w-xl">
            {error && (
              <div className="mb-4 rounded-lg border border-red-500/40 bg-red-500/10 p-3 text-left text-red-300">
                {error}
              </div>
            )}
            <div className="mb-6 p-4 rounded-lg border border-orange-500/30 bg-orange-500/10">
              <h3 className="text-lg font-semibold text-orange-200 mb-2">
                Configure {displayName} Parameters
              </h3>
              <p className="text-sm text-orange-200/80">
                Select the appropriate options for your learning context. All fields will use sensible defaults if not specified.
              </p>
            </div>
            <ParamForm paramsDef={paramsDef} onSubmit={handleGenerate} isSubmitting={loading} pedagogy={name} />
          </div>
        ) : (
          <div className="mx-auto max-w-3xl text-left">
            <OutputRenderer pedagogy={name} content={output} />
          </div>
        )}
      </div>
    </div>
  );
}

export default dynamic(() => Promise.resolve(PedagogyPageInner), { ssr: false });
