const DEFAULT_THEME = {
  icon: "📚",
  headerBg: "from-gray-500/10 to-gray-600/10",
  accentText: "text-gray-300",
  sectionTitle: "text-gray-300",
  chip: "bg-gray-500/10 text-gray-300 border-gray-500/30",
  cardBg: "bg-gray-500/10",
  border: "border-gray-500/30",
};

const THEMES = {
  project_based_learning: {
    icon: "🧩",
    headerBg: "from-orange-500/10 to-amber-500/10",
    accentText: "text-orange-400",
    sectionTitle: "text-orange-300",
    chip: "bg-orange-500/10 text-orange-300 border-orange-500/30",
    cardBg: "bg-orange-500/10",
    border: "border-orange-500/30",
  },
  inquiry_based_learning: {
    icon: "🔎",
    headerBg: "from-sky-500/10 to-blue-500/10",
    accentText: "text-sky-400",
    sectionTitle: "text-sky-300",
    chip: "bg-sky-500/10 text-sky-300 border-sky-500/30",
    cardBg: "bg-sky-500/10",
    border: "border-sky-500/30",
  },
  flipped_classroom: {
    icon: "🔁",
    headerBg: "from-fuchsia-500/10 to-purple-500/10",
    accentText: "text-fuchsia-400",
    sectionTitle: "text-fuchsia-300",
    chip: "bg-fuchsia-500/10 text-fuchsia-300 border-fuchsia-500/30",
    cardBg: "bg-fuchsia-500/10",
    border: "border-fuchsia-500/30",
  },
  socratic_questioning: {
    icon: "🧠",
    headerBg: "from-indigo-500/15 via-purple-500/15 to-pink-500/15",
    accentText: "text-indigo-300",
    sectionTitle: "text-purple-300",
    chip: "bg-gradient-to-r from-indigo-500/20 to-purple-500/20 text-indigo-200 border-indigo-400/40",
    cardBg: "bg-gradient-to-br from-indigo-500/5 to-purple-500/5",
    border: "border-indigo-400/30",
  },
  experiential_learning: {
    icon: "🧪",
    headerBg: "from-rose-500/10 to-red-500/10",
    accentText: "text-rose-400",
    sectionTitle: "text-rose-300",
    chip: "bg-rose-500/10 text-rose-300 border-rose-500/30",
    cardBg: "bg-rose-500/10",
    border: "border-rose-500/30",
  },
  case_based_learning: {
    icon: "📚",
    headerBg: "from-amber-500/10 to-yellow-500/10",
    accentText: "text-amber-400",
    sectionTitle: "text-amber-300",
    chip: "bg-amber-500/10 text-amber-300 border-amber-500/30",
    cardBg: "bg-amber-500/10",
    border: "border-amber-500/30",
  },
  game_based_learning: {
    icon: "🎮",
    headerBg: "from-indigo-500/10 to-violet-500/10",
    accentText: "text-indigo-400",
    sectionTitle: "text-indigo-300",
    chip: "bg-indigo-500/10 text-indigo-300 border-indigo-500/30",
    cardBg: "bg-indigo-500/10",
    border: "border-indigo-500/30",
  },
  microlearning: {
    icon: "⚡",
    headerBg: "from-teal-500/10 to-cyan-500/10",
    accentText: "text-teal-400",
    sectionTitle: "text-teal-300",
    chip: "bg-teal-500/10 text-teal-300 border-teal-500/30",
    cardBg: "bg-teal-500/10",
    border: "border-teal-500/30",
  },
  station_rotation: {
    icon: "🔄",
    headerBg: "from-pink-500/10 to-rose-500/10",
    accentText: "text-pink-400",
    sectionTitle: "text-pink-300",
    chip: "bg-pink-500/10 text-pink-300 border-pink-500/30",
    cardBg: "bg-pink-500/10",
    border: "border-pink-500/30",
  },
  direct_instruction: {
    icon: "🎯",
    headerBg: "from-red-500/10 to-orange-500/10",
    accentText: "text-red-400",
    sectionTitle: "text-red-300",
    chip: "bg-red-500/10 text-red-300 border-red-500/30",
    cardBg: "bg-red-500/10",
    border: "border-red-500/30",
  },
  blooms_taxonomy: {
    icon: "🎓",
    headerBg: "from-emerald-500/15 via-teal-500/15 to-cyan-500/15",
    accentText: "text-emerald-300",
    sectionTitle: "text-teal-300",
    chip: "bg-gradient-to-r from-emerald-500/20 to-teal-500/20 text-emerald-200 border-emerald-400/40",
    cardBg: "bg-gradient-to-br from-emerald-500/5 to-teal-500/5",
    border: "border-emerald-400/30",
  },
  peer_learning: {
    icon: "🤝",
    headerBg: "from-blue-500/15 via-indigo-500/15 to-purple-500/15",
    accentText: "text-blue-300",
    sectionTitle: "text-indigo-300",
    chip: "bg-gradient-to-r from-blue-500/20 to-indigo-500/20 text-blue-200 border-blue-400/40",
    cardBg: "bg-gradient-to-br from-blue-500/5 to-indigo-500/5",
    border: "border-blue-400/30",
  },
  constructivist: {
    icon: "🏗️",
    headerBg: "from-amber-500/15 via-orange-500/15 to-red-500/15",
    accentText: "text-amber-300",
    sectionTitle: "text-orange-300",
    chip: "bg-gradient-to-r from-amber-500/20 to-orange-500/20 text-amber-200 border-amber-400/40",
    cardBg: "bg-gradient-to-br from-amber-500/5 to-orange-500/5",
    border: "border-amber-400/30",
  },
  gamification: {
    icon: "🎮",
    headerBg: "from-violet-500/15 via-purple-500/15 to-pink-500/15",
    accentText: "text-violet-300",
    sectionTitle: "text-purple-300",
    chip: "bg-gradient-to-r from-violet-500/20 to-purple-500/20 text-violet-200 border-violet-400/40",
    cardBg: "bg-gradient-to-br from-violet-500/5 to-purple-500/5",
    border: "border-violet-400/30",
  },
  flipped_classroom: {
    icon: "🔁",
    headerBg: "from-fuchsia-500/15 via-purple-500/15 to-pink-500/15",
    accentText: "text-fuchsia-300",
    sectionTitle: "text-purple-300",
    chip: "bg-gradient-to-r from-fuchsia-500/20 to-purple-500/20 text-fuchsia-200 border-fuchsia-400/40",
    cardBg: "bg-gradient-to-br from-fuchsia-500/5 to-purple-500/5",
    border: "border-fuchsia-400/30",
  },
  inquiry_based_learning: {
    icon: "🔎",
    headerBg: "from-sky-500/15 via-blue-500/15 to-indigo-500/15",
    accentText: "text-sky-300",
    sectionTitle: "text-blue-300",
    chip: "bg-gradient-to-r from-sky-500/20 to-blue-500/20 text-sky-200 border-sky-400/40",
    cardBg: "bg-gradient-to-br from-sky-500/5 to-blue-500/5",
    border: "border-sky-400/30",
  },
};

function Header({ pedagogy, content, theme }) {
  const title =
    content?.title ||
    content?.driving_question ||
    content?.essential_question ||
    content?.hook ||
    pedagogy;

  return (
    <div className={`rounded-xl p-5 bg-gradient-to-br ${theme.headerBg} border ${theme.border}`}>
      <div className="flex items-start gap-3">
        <div className="text-2xl" aria-hidden>{theme.icon}</div>
        <div className="flex-1">
          <h2 className={`text-2xl font-bold ${theme.accentText}`}>{title}</h2>
          {content?.project_overview && (
            <p className="mt-2 text-sm text-gray-300">{content.project_overview}</p>
          )}
        </div>
        <span className={`px-2 py-1 text-xs rounded-lg border ${theme.chip}`}>{pedagogy}</span>
      </div>
    </div>
  );
}

function SectionCard({ title, children, theme }) {
  return (
    <div className={`rounded-xl p-4 border ${theme.border} ${theme.cardBg}`}>
      <h3 className={`text-lg font-semibold mb-2 ${theme.sectionTitle}`}>{title}</h3>
      <div className="space-y-2">{children}</div>
    </div>
  );
}

function renderValue(value) {
  if (value == null) return null;
  if (Array.isArray(value)) {
    return (
      <div className="grid gap-3 md:grid-cols-2">
        {value.map((item, index) => (
          <div key={index} className="p-3 rounded-lg bg-black/20 border border-white/5">
            {typeof item === "object" ? (
              <div className="space-y-1">
                {Object.entries(item).map(([k, v]) => (
                  <div key={k}>
                    <div className="text-sm font-medium text-gray-300">{humanize(k)}</div>
                    <div className="text-sm text-gray-200">{renderLeaf(v)}</div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-sm text-gray-200">{String(item)}</div>
            )}
          </div>
        ))}
      </div>
    );
  }
  if (typeof value === "object") {
    return (
      <div className="grid gap-3 md:grid-cols-2">
        {Object.entries(value).map(([k, v]) => (
          <div key={k} className="p-3 rounded-lg bg-black/20 border border-white/5">
            <div className="text-sm font-medium text-gray-300">{humanize(k)}</div>
            <div className="text-sm text-gray-200">{renderLeaf(v)}</div>
          </div>
        ))}
      </div>
    );
  }
  return <p className="text-sm text-gray-200 leading-6">{String(value)}</p>;
}

function renderLeaf(value) {
  if (Array.isArray(value)) {
    return (
      <ul className="list-disc pl-4 space-y-1">
        {value.map((x, i) => (
          <li key={i}>{typeof x === "object" ? JSON.stringify(x) : String(x)}</li>
        ))}
      </ul>
    );
  }
  if (typeof value === "object" && value !== null) {
    return (
      <div className="space-y-1">
        {Object.entries(value).map(([k, v]) => (
          <div key={k}>
            <span className="text-gray-400 mr-1">{humanize(k)}:</span>
            <span>{typeof v === "object" ? JSON.stringify(v) : String(v)}</span>
          </div>
        ))}
      </div>
    );
  }
  return <span>{String(value)}</span>;
}

function humanize(key) {
  return String(key)
    .replace(/_/g, " ")
    .replace(/\b\w/g, (m) => m.toUpperCase());
}

function KnownSections({ content, theme }) {
  const sections = [];

  const pushIf = (title, val) => {
    if (val == null) return;
    sections.push({ title, val });
  };

  pushIf("Driving Question", content?.driving_question);
  pushIf("Overview", content?.project_overview || content?.overview || content?.summary);
  pushIf("Learning Objectives", content?.learning_objectives || content?.objectives);
  pushIf("Phases", content?.project_phases || content?.phases);
  pushIf("Activities", content?.activities || content?.tasks || content?.stations);
  pushIf("Assessment", content?.assessment || content?.evaluation || content?.rubric);
  pushIf("Resources", content?.resources || content?.materials || content?.references);
  pushIf("Timeline", content?.timeline || content?.schedule || content?.plan);
  pushIf("Steps", content?.steps || content?.procedure);

  if (sections.length === 0) return null;

  return (
    <div className="space-y-4">
      {sections.map((s, i) => (
        <SectionCard key={i} title={s.title} theme={theme}>
          {renderValue(s.val)}
        </SectionCard>
      ))}
    </div>
  );
}

function ProjectBasedLearning({ content, theme }) {
  const phases = Array.isArray(content?.project_phases) ? content.project_phases : [];
  return (
    <div className="space-y-5">
      <Header pedagogy="project_based_learning" content={content} theme={theme} />
      {content?.learning_objectives && (
        <SectionCard title="Learning Objectives" theme={theme}>
          {renderValue(content.learning_objectives)}
        </SectionCard>
      )}
      <div className="grid gap-4 md:grid-cols-2">
        {phases.map((phase, i) => (
          <div key={i} className={`rounded-xl p-4 border ${theme.border} ${theme.cardBg}`}>
            <div className="flex items-center justify-between">
              <h4 className="font-semibold text-white">{phase?.phase_name || `Phase ${i + 1}`}</h4>
              {phase?.duration && (
                <span className={`px-2 py-1 text-xs rounded-lg border ${theme.chip}`}>{phase.duration}</span>
              )}
            </div>
            {phase?.content_description && (
              <p className="mt-2 text-sm text-gray-200">{phase.content_description}</p>
            )}
            {Array.isArray(phase?.activities) && phase.activities.length > 0 && (
              <div className="mt-3">
                <div className="text-sm font-medium text-gray-300 mb-1">Activities</div>
                <ul className="list-disc pl-5 space-y-1 text-sm">
                  {phase.activities.map((a, idx) => (
                    <li key={idx}>{typeof a === "object" ? a?.title || JSON.stringify(a) : String(a)}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        ))}
      </div>
      <KnownSections content={{
        resources: content?.resources,
        assessment: content?.assessment,
        timeline: content?.timeline,
      }} theme={theme} />
    </div>
  );
}

function GenericPedagogy({ pedagogy, content, theme }) {
  return (
    <div className="space-y-5">
      <Header pedagogy={pedagogy} content={content} theme={theme} />
      <KnownSections content={content} theme={theme} />
      <SectionCard title="Full Details" theme={theme}>
        <pre className="text-xs whitespace-pre-wrap leading-6">{JSON.stringify(content, null, 2)}</pre>
      </SectionCard>
    </div>
  );
}


function BloomsTaxonomy({ content, theme }) {
  if (!content || !content.cognitive_levels || content.cognitive_levels.length === 0) {
    return (
      <div className={`rounded-xl p-8 border ${theme.border} ${theme.cardBg} text-center`}>
        <div className="text-4xl mb-4">🎓</div>
        <h3 className={`text-xl font-semibold mb-2 ${theme.sectionTitle}`}>
          Blooms Taxonomy Content
        </h3>
        <p className="text-gray-400">
          {content?.cognitive_levels?.length === 0 
            ? "No cognitive levels generated yet. Please try again with different parameters."
            : "Content is being generated..."}
        </p>
      </div>
    );
  }

  const levels = content.cognitive_levels;
  const topic = content.topic || "Topic";
  const gradeLevel = content.grade_level || "Not specified";
  const targetLevel = content.target_level || "Not specified";

  return (
    <div className="space-y-6">
      {/* Header Section */}
      <div className={`rounded-xl p-6 border ${theme.border} ${theme.cardBg} relative overflow-hidden`}>
        <div className="absolute inset-0 opacity-5">
          <div className="absolute inset-0" style={{
            backgroundImage: `url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='1'%3E%3Cpath d='M30 30c0 16.569-13.431 30-30 30s-30-13.431-30-30 13.431-30 30-30 30 13.431 30 30z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")`,
          }}></div>
        </div>
        <div className="relative">
          <div className="flex items-center gap-3 mb-4">
            <div className="text-3xl">🎓</div>
            <div>
              <h1 className={`text-2xl font-bold ${theme.accentText}`}>
                Blooms Taxonomy: {topic}
              </h1>
              <div className="flex gap-4 mt-2 text-sm">
                <span className={`px-3 py-1 rounded-full ${theme.chip}`}>
                  Grade: {gradeLevel}
                </span>
                <span className={`px-3 py-1 rounded-full ${theme.chip}`}>
                  Level: {targetLevel}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Cognitive Levels */}
      <div className="space-y-6">
        {levels.map((level, index) => (
          <div key={index} className={`rounded-xl border ${theme.border} ${theme.cardBg} overflow-hidden`}>
            {/* Level Header */}
            <div className={`p-4 bg-gradient-to-r ${theme.headerBg} border-b ${theme.border}`}>
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className={`w-10 h-10 rounded-full flex items-center justify-center text-lg font-bold ${theme.chip}`}>
                    {index + 1}
                  </div>
                  <div>
                    <h3 className={`text-lg font-semibold ${theme.accentText}`}>
                      {level.level_name}
                    </h3>
                    <p className="text-sm text-gray-300">{level.description}</p>
                  </div>
                </div>
                <div className={`px-3 py-1 rounded-full text-xs font-medium ${theme.chip}`}>
                  Level {index + 1}
                </div>
              </div>
            </div>

            {/* Level Content */}
            <div className="p-6 space-y-6">
              {/* Content */}
              {level.content && (
                <div className="space-y-3">
                  <h4 className={`text-sm font-semibold ${theme.sectionTitle} flex items-center gap-2`}>
                    <span className="w-2 h-2 rounded-full bg-emerald-400"></span>
                    Content
                  </h4>
                  <p className="text-gray-200 leading-6">{level.content}</p>
                </div>
              )}

              {/* Learning Objectives */}
              {level.learning_objectives && level.learning_objectives.length > 0 && (
                <div className="space-y-3">
                  <h4 className={`text-sm font-semibold ${theme.sectionTitle} flex items-center gap-2`}>
                    <span className="w-2 h-2 rounded-full bg-blue-400"></span>
                    Learning Objectives
                  </h4>
                  <div className="space-y-2">
                    {level.learning_objectives.map((objective, objIndex) => (
                      <div key={objIndex} className="flex items-start gap-3 p-3 rounded-lg bg-white/5">
                        <div className="w-2 h-2 rounded-full bg-blue-400 flex-shrink-0 mt-2"></div>
                        <p className="text-sm text-gray-200">{objective}</p>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Activities */}
              {level.activities && level.activities.length > 0 && (
                <div className="space-y-3">
                  <h4 className={`text-sm font-semibold ${theme.sectionTitle} flex items-center gap-2`}>
                    <span className="w-2 h-2 rounded-full bg-purple-400"></span>
                    Activities
                  </h4>
                  <div className="space-y-2">
                    {level.activities.map((activity, actIndex) => (
                      <div key={actIndex} className="flex items-start gap-3 p-3 rounded-lg bg-white/5">
                        <div className="w-2 h-2 rounded-full bg-purple-400 flex-shrink-0 mt-2"></div>
                        <p className="text-sm text-gray-200">{activity}</p>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Assessment Questions */}
              {level.assessment_questions && level.assessment_questions.length > 0 && (
                <div className="space-y-3">
                  <h4 className={`text-sm font-semibold ${theme.sectionTitle} flex items-center gap-2`}>
                    <span className="w-2 h-2 rounded-full bg-amber-400"></span>
                    Assessment Questions
                  </h4>
                  <div className="space-y-2">
                    {level.assessment_questions.map((question, qIndex) => (
                      <div key={qIndex} className="flex items-start gap-3 p-3 rounded-lg bg-white/5">
                        <div className="w-2 h-2 rounded-full bg-amber-400 flex-shrink-0 mt-2"></div>
                        <p className="text-sm text-gray-200">{question}</p>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Real World Examples */}
              {level.real_world_examples && level.real_world_examples.length > 0 && (
                <div className="space-y-3">
                  <h4 className={`text-sm font-semibold ${theme.sectionTitle} flex items-center gap-2`}>
                    <span className="w-2 h-2 rounded-full bg-rose-400"></span>
                    Real World Examples
                  </h4>
                  <div className="space-y-2">
                    {level.real_world_examples.map((example, exIndex) => (
                      <div key={exIndex} className="flex items-start gap-3 p-3 rounded-lg bg-white/5">
                        <div className="w-2 h-2 rounded-full bg-rose-400 flex-shrink-0 mt-2"></div>
                        <p className="text-sm text-gray-200">{example}</p>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Key Concepts */}
              {level.key_concepts && level.key_concepts.length > 0 && (
                <div className="space-y-3">
                  <h4 className={`text-sm font-semibold ${theme.sectionTitle} flex items-center gap-2`}>
                    <span className="w-2 h-2 rounded-full bg-teal-400"></span>
                    Key Concepts
                  </h4>
                  <div className="flex flex-wrap gap-2">
                    {level.key_concepts.map((concept, cIndex) => (
                      <span key={cIndex} className={`px-3 py-1 rounded-full text-xs font-medium ${theme.chip}`}>
                        {concept}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        ))}
      </div>

      {/* Additional Information */}
      {(content.learning_progression || content.assessment_strategy) && (
        <div className="grid gap-4 md:grid-cols-2">
          {content.learning_progression && (
            <div className={`rounded-xl p-4 border ${theme.border} ${theme.cardBg}`}>
              <h3 className={`text-lg font-semibold mb-3 ${theme.sectionTitle}`}>
                Learning Progression
              </h3>
              <p className="text-sm text-gray-200 leading-6">{content.learning_progression}</p>
            </div>
          )}
          
          {content.assessment_strategy && (
            <div className={`rounded-xl p-4 border ${theme.border} ${theme.cardBg}`}>
              <h3 className={`text-lg font-semibold mb-3 ${theme.sectionTitle}`}>
                Assessment Strategy
              </h3>
              <p className="text-sm text-gray-200 leading-6">{content.assessment_strategy}</p>
            </div>
          )}
        </div>
      )}

      {/* Footer */}
      <div className={`rounded-xl p-6 bg-gradient-to-br from-gray-900/50 to-black/50 border border-gray-700/50 text-center`}>
        <div className="flex items-center justify-center gap-3 mb-3">
          <div className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></div>
          <span className="text-sm text-gray-400">Blooms Taxonomy Framework</span>
          <div className="w-2 h-2 rounded-full bg-teal-400 animate-pulse"></div>
        </div>
        <p className="text-xs text-gray-500">
          Progressive cognitive development from basic recall to advanced evaluation
        </p>
      </div>
    </div>
  );
}

// function PeerLearning({ content, theme }) {
//   if (!content) {
//     return (
//       <div className={`rounded-xl p-8 border ${theme.border} ${theme.cardBg} text-center`}>
//         <div className="text-4xl mb-4">🤝</div>
//         <h3 className={`text-xl font-semibold mb-2 ${theme.sectionTitle}`}>
//           Peer Learning Content
//         </h3>
//         <p className="text-gray-400">Content is being generated...</p>
//       </div>
//     );
//   }

//   const topic = content.topic || "Topic";
//   const groupSize = content.group_size || "Not specified";
//   const collaborationType = content.collaboration_type || "Not specified";
//   const skillDiversity = content.skill_diversity || "Not specified";

//   return (
//     <div className="space-y-6">
//       {/* Header Section */}
//       <div className={`rounded-xl p-6 border ${theme.border} ${theme.cardBg} relative overflow-hidden`}>
//         <div className="absolute inset-0 opacity-5">
//           <div className="absolute inset-0" style={{
//             backgroundImage: `url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='1'%3E%3Cpath d='M30 30c0 16.569-13.431 30-30 30s-30-13.431-30-30 13.431-30 30-30 30 13.431 30 30z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")`,
//           }}></div>
//         </div>
//         <div className="relative">
//           <div className="flex items-center gap-3 mb-4">
//             <div className="text-3xl">🤝</div>
//             <div>
//               <h1 className={`text-2xl font-bold ${theme.accentText}`}>
//                 Peer Learning: {topic}
//               </h1>
//               <div className="flex gap-4 mt-2 text-sm">
//                 <span className={`px-3 py-1 rounded-full ${theme.chip}`}>
//                   Group: {groupSize}
//                 </span>
//                 <span className={`px-3 py-1 rounded-full ${theme.chip}`}>
//                   Type: {collaborationType}
//                 </span>
//                 <span className={`px-3 py-1 rounded-full ${theme.chip}`}>
//                   Skills: {skillDiversity}
//                 </span>
//               </div>
//             </div>
//           </div>
//         </div>
//       </div>

//       {/* Learning Activities */}
//       {content.learning_activities && content.learning_activities.length > 0 && (
//         <div className={`rounded-xl border ${theme.border} ${theme.cardBg} overflow-hidden`}>
//           <div className={`p-4 bg-gradient-to-r ${theme.headerBg} border-b ${theme.border}`}>
//             <h3 className={`text-lg font-semibold ${theme.accentText} flex items-center gap-2`}>
//               <span className="w-2 h-2 rounded-full bg-blue-400"></span>
//               Collaborative Learning Activities
//             </h3>
//           </div>
//           <div className="p-6 space-y-4">
//             {content.learning_activities.map((activity, index) => (
//               <div key={index} className="flex items-start gap-3 p-4 rounded-lg bg-white/5 hover:bg-white/10 transition-colors">
//                 <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold ${theme.chip}`}>
//                   {index + 1}
//                 </div>
//                 <div className="flex-1">
//                   <h4 className={`font-semibold ${theme.sectionTitle} mb-2`}>
//                     {activity.title || `Activity ${index + 1}`}
//                   </h4>
//                   {activity.description && (
//                     <p className="text-gray-200 text-sm leading-6 mb-3">{activity.description}</p>
//                   )}
//                   {activity.steps && activity.steps.length > 0 && (
//                     <div className="space-y-2">
//                       <h5 className="text-xs font-medium text-gray-400 uppercase tracking-wide">Steps:</h5>
//                       <ol className="list-decimal list-inside space-y-1 text-sm text-gray-300">
//                         {activity.steps.map((step, stepIndex) => (
//                           <li key={stepIndex}>{step}</li>
//                         ))}
//                       </ol>
//                     </div>
//                   )}
//                 </div>
//               </div>
//             ))}
//           </div>
//         </div>
//       )}

//       {/* Group Formation Strategies */}
//       {content.group_formation && (
//         <div className={`rounded-xl border ${theme.border} ${theme.cardBg} overflow-hidden`}>
//           <div className={`p-4 bg-gradient-to-r ${theme.headerBg} border-b ${theme.border}`}>
//             <h3 className={`text-lg font-semibold ${theme.accentText} flex items-center gap-2`}>
//               <span className="w-2 h-2 rounded-full bg-indigo-400"></span>
//               Group Formation Strategies
//             </h3>
//           </div>
//           <div className="p-6">
//             <p className="text-gray-200 leading-6">{content.group_formation}</p>
//           </div>
//         </div>
//       )}

//       {/* Collaboration Guidelines */}
//       {content.collaboration_guidelines && (
//         <div className={`rounded-xl border ${theme.border} ${theme.cardBg} overflow-hidden`}>
//           <div className={`p-4 bg-gradient-to-r ${theme.headerBg} border-b ${theme.border}`}>
//             <h3 className={`text-lg font-semibold ${theme.accentText} flex items-center gap-2`}>
//               <span className="w-2 h-2 rounded-full bg-purple-400"></span>
//               Collaboration Guidelines
//             </h3>
//           </div>
//           <div className="p-6">
//             <p className="text-gray-200 leading-6">{content.collaboration_guidelines}</p>
//           </div>
//         </div>
//       )}

//       {/* Assessment Methods */}
//       {content.assessment_methods && content.assessment_methods.length > 0 && (
//         <div className={`rounded-xl border ${theme.border} ${theme.cardBg} overflow-hidden`}>
//           <div className={`p-4 bg-gradient-to-r ${theme.headerBg} border-b ${theme.border}`}>
//             <h3 className={`text-lg font-semibold ${theme.accentText} flex items-center gap-2`}>
//               <span className="w-2 h-2 rounded-full bg-cyan-400"></span>
//               Assessment Methods
//             </h3>
//           </div>
//           <div className="p-6 space-y-3">
//             {content.assessment_methods.map((method, index) => (
//               <div key={index} className="flex items-start gap-3 p-3 rounded-lg bg-white/5">
//                 <div className="w-2 h-2 rounded-full bg-cyan-400 flex-shrink-0 mt-2"></div>
//                 <p className="text-sm text-gray-200">{method}</p>
//               </div>
//             ))}
//           </div>
//         </div>
//       )}

//       {/* Footer */}
//       <div className={`rounded-xl p-6 bg-gradient-to-br from-gray-900/50 to-black/50 border border-gray-700/50 text-center`}>
//         <div className="flex items-center justify-center gap-3 mb-3">
//           <div className="w-2 h-2 rounded-full bg-blue-400 animate-pulse"></div>
//           <span className="text-sm text-gray-400">Collaborative Learning Framework</span>
//           <div className="w-2 h-2 rounded-full bg-indigo-400 animate-pulse"></div>
//         </div>
//         <p className="text-xs text-gray-500">
//           Learning together through structured collaboration and peer support
//         </p>
//       </div>
//     </div>
//   );
// }
function PeerLearning({ content, theme }) {
  if (!content) {
    return (
      <div
        className={`rounded-xl p-8 border ${theme.border} ${theme.cardBg} text-center`}
      >
        <div className="text-4xl mb-4">🤝</div>
        <h3 className={`text-xl font-semibold mb-2 ${theme.sectionTitle}`}>
          Peer Learning Content
        </h3>
        <p className="text-gray-400">Content is being generated...</p>
      </div>
    );
  }

  const topic = content.topic || "Topic";

  const collabStructures = content.collaboration_structures || [];
  const accountability = content.accountability_measures || [];
  const communication = content.communication_protocols || [];
  const facilitation = content.facilitation_guidelines || null;
  const groupFormation = content.group_formation_strategy || null;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div
        className={`rounded-xl p-6 border ${theme.border} ${theme.cardBg} relative`}
      >
        <div className="flex items-center gap-3 mb-2">
          <div className="text-3xl">🤝</div>
          <h1 className={`text-2xl font-bold ${theme.accentText}`}>
            Peer Learning: {topic}
          </h1>
        </div>
      </div>

      {/* Collaboration Structures */}
      {collabStructures.length > 0 && (
        <div className={`rounded-xl border ${theme.border} ${theme.cardBg}`}>
          <div
            className={`p-4 bg-gradient-to-r ${theme.headerBg} border-b ${theme.border}`}
          >
            <h3 className={`text-lg font-semibold ${theme.accentText}`}>
              Collaboration Structures
            </h3>
          </div>
          <div className="p-6 space-y-4">
            {collabStructures.map((s, i) => (
              <div
                key={i}
                className="p-4 rounded-lg bg-white/5 hover:bg-white/10 transition"
              >
                <h4 className={`font-semibold ${theme.sectionTitle}`}>
                  {s.structure_name || `Structure ${i + 1}`}
                </h4>
                {s.process_description && (
                  <p className="text-gray-200 text-sm mb-2">
                    {s.process_description}
                  </p>
                )}
                {s.detailed_content && (
                  <p className="text-gray-300 text-sm mb-2">
                    {s.detailed_content}
                  </p>
                )}
                {Array.isArray(s.roles_and_responsibilities) &&
                  s.roles_and_responsibilities.length > 0 && (
                    <div className="mt-2">
                      <h5 className="text-xs text-gray-400 uppercase mb-1">
                        Roles & Responsibilities
                      </h5>
                      <ul className="list-disc list-inside text-sm text-gray-300">
                        {s.roles_and_responsibilities.map((r, ri) => (
                          <li key={ri}>{r}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                {Array.isArray(s.step_by_step_process) &&
                  s.step_by_step_process.length > 0 && (
                    <div className="mt-2">
                      <h5 className="text-xs text-gray-400 uppercase mb-1">
                        Steps
                      </h5>
                      <ol className="list-decimal list-inside text-sm text-gray-300">
                        {s.step_by_step_process.map((st, si) => (
                          <li key={si}>{st}</li>
                        ))}
                      </ol>
                    </div>
                  )}
                {s.assessment_method && (
                  <p className="text-sm text-gray-400 mt-2">
                    Assessment: {s.assessment_method}
                  </p>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Accountability Measures */}
      {accountability.length > 0 && (
        <div className={`rounded-xl border ${theme.border} ${theme.cardBg}`}>
          <div
            className={`p-4 bg-gradient-to-r ${theme.headerBg} border-b ${theme.border}`}
          >
            <h3 className={`text-lg font-semibold ${theme.accentText}`}>
              Accountability Measures
            </h3>
          </div>
          <ul className="p-6 space-y-2 text-sm text-gray-200">
            {accountability.map((m, i) => (
              <li key={i}>• {m}</li>
            ))}
          </ul>
        </div>
      )}

      {/* Communication Protocols */}
      {communication.length > 0 && (
        <div className={`rounded-xl border ${theme.border} ${theme.cardBg}`}>
          <div
            className={`p-4 bg-gradient-to-r ${theme.headerBg} border-b ${theme.border}`}
          >
            <h3 className={`text-lg font-semibold ${theme.accentText}`}>
              Communication Protocols
            </h3>
          </div>
          <ul className="p-6 space-y-2 text-sm text-gray-200">
            {communication.map((c, i) => (
              <li key={i}>• {c}</li>
            ))}
          </ul>
        </div>
      )}

      {/* Facilitation Guidelines */}
      {facilitation && (
        <div className={`rounded-xl border ${theme.border} ${theme.cardBg}`}>
          <div
            className={`p-4 bg-gradient-to-r ${theme.headerBg} border-b ${theme.border}`}
          >
            <h3 className={`text-lg font-semibold ${theme.accentText}`}>
              Facilitation Guidelines
            </h3>
          </div>
          <div className="p-6 text-gray-200">{facilitation}</div>
        </div>
      )}

      {/* Group Formation Strategy */}
      {groupFormation && (
        <div className={`rounded-xl border ${theme.border} ${theme.cardBg}`}>
          <div
            className={`p-4 bg-gradient-to-r ${theme.headerBg} border-b ${theme.border}`}
          >
            <h3 className={`text-lg font-semibold ${theme.accentText}`}>
              Group Formation Strategy
            </h3>
          </div>
          <div className="p-6 text-gray-200">{groupFormation}</div>
        </div>
      )}

      {/* Footer */}
      <div
        className={`rounded-xl p-6 bg-gradient-to-br from-gray-900/50 to-black/50 border border-gray-700/50 text-center`}
      >
        <span className="text-sm text-gray-400">
          Collaborative Learning Framework
        </span>
      </div>
    </div>
  );
}




function Constructivist({ content, theme }) {
  if (!content) {
    return (
      <div className={`rounded-xl p-8 border ${theme.border} ${theme.cardBg} text-center`}>
        <div className="text-4xl mb-4">🏗️</div>
        <h3 className={`text-xl font-semibold mb-2 ${theme.sectionTitle}`}>
          Constructivist Learning Content
        </h3>
        <p className="text-gray-400">Content is being generated...</p>
      </div>
    );
  }

  const topic = content.topic || "Topic";

  const renderActivities = (items, title, accentDotClass) => {
    if (!Array.isArray(items) || items.length === 0) return null;
    return (
      <div className={`rounded-xl border ${theme.border} ${theme.cardBg} overflow-hidden`}>
        <div className={`p-4 bg-gradient-to-r ${theme.headerBg} border-b ${theme.border}`}>
          <h3 className={`text-lg font-semibold ${theme.accentText} flex items-center gap-2`}>
            <span className={`w-2 h-2 rounded-full ${accentDotClass}`}></span>
            {title}
          </h3>
        </div>
        <div className="p-6 space-y-4">
          {items.map((a, index) => (
            <div key={index} className="p-4 rounded-lg bg-white/5">
              <div className="flex items-center justify-between mb-2">
                <h4 className={`font-semibold ${theme.sectionTitle}`}>
                  {a.activity_name || `Activity ${index + 1}`}
                </h4>
                {a.type && (
                  <span className={`px-2 py-1 text-xs rounded-lg border ${theme.chip}`}>{a.type}</span>
                )}
              </div>
              {a.description && <p className="text-sm text-gray-200 mb-2">{a.description}</p>}
              {a.detailed_content && <p className="text-sm text-gray-300 mb-2">{a.detailed_content}</p>}
              {Array.isArray(a.step_by_step_guide) && a.step_by_step_guide.length > 0 && (
                <div className="mt-2">
                  <div className="text-xs font-medium text-gray-400 uppercase tracking-wide mb-1">Steps</div>
                  <ol className="list-decimal pl-5 space-y-1 text-sm text-gray-300">
                    {a.step_by_step_guide.map((step, i) => <li key={i}>{step}</li>)}
                  </ol>
                </div>
              )}
              {a.learning_outcome && (
                <div className="mt-2 text-sm text-gray-300">
                  <span className="text-gray-400">Outcome:</span> {a.learning_outcome}
                </div>
              )}
              {a.facilitation_notes && (
                <div className="mt-2 text-sm text-gray-300">
                  <span className="text-gray-400">Facilitation Notes:</span> {a.facilitation_notes}
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    );
  };

  return (
    <div className="space-y-6">
      <div className={`rounded-xl p-6 border ${theme.border} ${theme.cardBg} relative overflow-hidden`}>
        <div className="absolute inset-0 opacity-5">
          <div className="absolute inset-0" style={{
            backgroundImage: `url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='1'%3E%3Cpath d='M30 30c0 16.569-13.431 30-30 30s-30-13.431-30-30 13.431-30 30-30 30 13.431 30 30z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")`,
          }}></div>
        </div>
        <div className="relative">
          <div className="flex items-center gap-3 mb-4">
            <div className="text-3xl">🏗️</div>
            <div>
              <h1 className={`text-2xl font-bold ${theme.accentText}`}>
                Constructivist Learning: {topic}
              </h1>
            </div>
          </div>
        </div>
      </div>

      {renderActivities(content.prior_knowledge_activities, "Prior Knowledge Activities", "bg-amber-400")}
      {renderActivities(content.experiential_activities, "Experiential Activities", "bg-emerald-400")}
      {renderActivities(content.social_construction_activities, "Social Construction Activities", "bg-red-400")}
      {renderActivities(content.reflection_activities, "Reflection Activities", "bg-orange-400")}

      {content.assessment_approach && (
        <SectionCard title="Assessment Approach" theme={theme}>
          <p className="text-sm text-gray-200 leading-6">{content.assessment_approach}</p>
        </SectionCard>
      )}

      <div className={`rounded-xl p-6 bg-gradient-to-br from-gray-900/50 to-black/50 border border-gray-700/50 text-center`}>
        <div className="flex items-center justify-center gap-3 mb-3">
          <div className="w-2 h-2 rounded-full bg-amber-400 animate-pulse"></div>
          <span className="text-sm text-gray-400">Constructivist Learning Framework</span>
          <div className="w-2 h-2 rounded-full bg-orange-400 animate-pulse"></div>
        </div>
        <p className="text-xs text-gray-500">
          Building knowledge through active experience, reflection, and social interaction
        </p>
      </div>
    </div>
  );
}

function SocraticQuestioning({ content, theme }) {
  if (!content) {
    return (
      <div className={`rounded-xl p-8 border ${theme.border} ${theme.cardBg} text-center`}>
        <div className="text-4xl mb-4">🧠</div>
        <h3 className={`text-xl font-semibold mb-2 ${theme.sectionTitle}`}>
          Socratic Questioning Content
        </h3>
        <p className="text-gray-400">Content is being generated...</p>
      </div>
    );
  }

  const topic = content.topic || "Topic";
  const depthLevel = content.depth_level || "Not specified";
  const studentLevel = content.student_level || "Not specified";

  return (
    <div className="space-y-6">
      {/* Header Section */}
      <div className={`rounded-xl p-6 border ${theme.border} ${theme.cardBg} relative overflow-hidden`}>
        <div className="absolute inset-0 opacity-5">
          <div className="absolute inset-0" style={{
            backgroundImage: `url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='1'%3E%3Cpath d='M30 30c0 16.569-13.431 30-30 30s-30-13.431-30-30 13.431-30 30-30 30 13.431 30 30z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")`,
          }}></div>
        </div>
        <div className="relative">
          <div className="flex items-center gap-3 mb-4">
            <div className="text-3xl">🧠</div>
            <div>
              <h1 className={`text-2xl font-bold ${theme.accentText}`}>
                Socratic Questioning: {topic}
              </h1>
              <div className="flex gap-4 mt-2 text-sm">
                <span className={`px-3 py-1 rounded-full ${theme.chip}`}>
                  Depth: {depthLevel}
                </span>
                <span className={`px-3 py-1 rounded-full ${theme.chip}`}>
                  Level: {studentLevel}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Question Sequences */}
      {content.question_sequences && content.question_sequences.length > 0 && (
        <div className={`rounded-xl border ${theme.border} ${theme.cardBg} overflow-hidden`}>
          <div className={`p-4 bg-gradient-to-r ${theme.headerBg} border-b ${theme.border}`}>
            <h3 className={`text-lg font-semibold ${theme.accentText} flex items-center gap-2`}>
              <span className="w-2 h-2 rounded-full bg-indigo-400"></span>
              Strategic Question Sequences
            </h3>
          </div>
          <div className="p-6 space-y-4">
            {content.question_sequences.map((sequence, index) => (
              <div key={index} className="flex items-start gap-3 p-4 rounded-lg bg-white/5 hover:bg-white/10 transition-colors">
                <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold ${theme.chip}`}>
                  {index + 1}
                </div>
                <div className="flex-1">
                  <h4 className={`font-semibold ${theme.sectionTitle} mb-2`}>
                    {sequence.title || `Sequence ${index + 1}`}
                  </h4>
                  {sequence.description && (
                    <p className="text-gray-200 text-sm leading-6 mb-3">{sequence.description}</p>
                  )}
                  {sequence.questions && sequence.questions.length > 0 && (
                    <div className="space-y-2">
                      <h5 className="text-xs font-medium text-gray-400 uppercase tracking-wide">Questions:</h5>
                      <ol className="list-decimal list-inside space-y-1 text-sm text-gray-300">
                        {sequence.questions.map((question, qIndex) => (
                          <li key={qIndex}>{question}</li>
                        ))}
                      </ol>
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Discussion Guidelines */}
      {content.discussion_guidelines && (
        <div className={`rounded-xl border ${theme.border} ${theme.cardBg} overflow-hidden`}>
          <div className={`p-4 bg-gradient-to-r ${theme.headerBg} border-b ${theme.border}`}>
            <h3 className={`text-lg font-semibold ${theme.accentText} flex items-center gap-2`}>
              <span className="w-2 h-2 rounded-full bg-purple-400"></span>
              Discussion Guidelines
            </h3>
          </div>
          <div className="p-6">
            <p className="text-gray-200 leading-6">{content.discussion_guidelines}</p>
          </div>
        </div>
      )}

      {/* Assessment Approach */}
      {content.assessment_approach && (
        <div className={`rounded-xl border ${theme.border} ${theme.cardBg} overflow-hidden`}>
          <div className={`p-4 bg-gradient-to-r ${theme.headerBg} border-b ${theme.border}`}>
            <h3 className={`text-lg font-semibold ${theme.accentText} flex items-center gap-2`}>
              <span className="w-2 h-2 rounded-full bg-pink-400"></span>
              Assessment Approach
            </h3>
          </div>
          <div className="p-6">
            <p className="text-gray-200 leading-6">{content.assessment_approach}</p>
          </div>
        </div>
      )}

      {/* Footer */}
      <div className={`rounded-xl p-6 bg-gradient-to-br from-gray-900/50 to-black/50 border border-gray-700/50 text-center`}>
        <div className="flex items-center justify-center gap-3 mb-3">
          <div className="w-2 h-2 rounded-full bg-indigo-400 animate-pulse"></div>
          <span className="text-sm text-gray-400">Socratic Questioning Framework</span>
          <div className="w-2 h-2 rounded-full bg-purple-400 animate-pulse"></div>
        </div>
        <p className="text-xs text-gray-500">
          Guiding learning through strategic questioning and critical thinking
        </p>
      </div>
    </div>
  );
}

function Gamification({ content, theme }) {
  if (!content) {
    return (
      <div className={`rounded-xl p-8 border ${theme.border} ${theme.cardBg} text-center`}>
        <div className="text-4xl mb-4">🎮</div>
        <h3 className={`text-xl font-semibold mb-2 ${theme.sectionTitle}`}>
          Gamification Content
        </h3>
        <p className="text-gray-400">Content is being generated...</p>
      </div>
    );
  }

  const topic = content.topic || "Topic";

  return (
    <div className="space-y-6">
      <div className={`rounded-xl p-6 border ${theme.border} ${theme.cardBg} relative overflow-hidden`}>
        <div className="absolute inset-0 opacity-5">
          <div className="absolute inset-0" style={{
            backgroundImage: `url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='1'%3E%3Cpath d='M30 30c0 16.569-13.431 30-30 30s-30-13.431-30-30 13.431-30 30-30 30 13.431 30 30z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")`,
          }}></div>
        </div>
        <div className="relative">
          <div className="flex items-center gap-3 mb-4">
            <div className="text-3xl">🎮</div>
            <div>
              <h1 className={`text-2xl font-bold ${theme.accentText}`}>
                Gamification: {topic}
              </h1>
            </div>
          </div>
        </div>
      </div>

      {Array.isArray(content.game_mechanics) && content.game_mechanics.length > 0 && (
        <div className={`rounded-xl border ${theme.border} ${theme.cardBg} overflow-hidden`}>
          <div className={`p-4 bg-gradient-to-r ${theme.headerBg} border-b ${theme.border}`}>
            <h3 className={`text-lg font-semibold ${theme.accentText} flex items-center gap-2`}>
              <span className="w-2 h-2 rounded-full bg-violet-400"></span>
              Game Mechanics
            </h3>
          </div>
          <div className="p-6 space-y-4">
            {content.game_mechanics.map((mechanic, index) => (
              <div key={index} className="flex items-start gap-3 p-4 rounded-lg bg-white/5 hover:bg-white/10 transition-colors">
                <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold ${theme.chip}`}>
                  {index + 1}
                </div>
                <div className="flex-1">
                  <h4 className={`font-semibold ${theme.sectionTitle} mb-2`}>
                    {mechanic.mechanic_name || `Mechanic ${index + 1}`}
                  </h4>
                  {mechanic.description && (
                    <p className="text-gray-200 text-sm leading-6 mb-3">{mechanic.description}</p>
                  )}
                  {mechanic.detailed_implementation && (
                    <div className="space-y-2">
                      <h5 className="text-xs font-medium text-gray-400 uppercase tracking-wide">Implementation</h5>
                      <p className="text-sm text-gray-300">{mechanic.detailed_implementation}</p>
                    </div>
                  )}
                  {mechanic.learning_connection && (
                    <div className="space-y-2">
                      <h5 className="text-xs font-medium text-gray-400 uppercase tracking-wide">Learning Connection</h5>
                      <p className="text-sm text-gray-300">{mechanic.learning_connection}</p>
                    </div>
                  )}
                  {mechanic.content_integration && (
                    <div className="space-y-2">
                      <h5 className="text-xs font-medium text-gray-400 uppercase tracking-wide">Content Integration</h5>
                      <p className="text-sm text-gray-300">{mechanic.content_integration}</p>
                    </div>
                  )}
                  {mechanic.implementation_notes && (
                    <div className="space-y-2">
                      <h5 className="text-xs font-medium text-gray-400 uppercase tracking-wide">Notes</h5>
                      <p className="text-sm text-gray-300">{mechanic.implementation_notes}</p>
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {(content.progression_system || content.assessment_integration || content.motivation_strategy) && (
        <div className="grid gap-4 md:grid-cols-3">
          {content.progression_system && (
            <div className={`rounded-xl p-4 border ${theme.border} ${theme.cardBg}`}>
              <h3 className={`text-lg font-semibold mb-2 ${theme.sectionTitle}`}>Progression System</h3>
              <p className="text-sm text-gray-200 leading-6">{content.progression_system}</p>
            </div>
          )}
          {content.assessment_integration && (
            <div className={`rounded-xl p-4 border ${theme.border} ${theme.cardBg}`}>
              <h3 className={`text-lg font-semibold mb-2 ${theme.sectionTitle}`}>Assessment Integration</h3>
              <p className="text-sm text-gray-200 leading-6">{content.assessment_integration}</p>
            </div>
          )}
          {content.motivation_strategy && (
            <div className={`rounded-xl p-4 border ${theme.border} ${theme.cardBg}`}>
              <h3 className={`text-lg font-semibold mb-2 ${theme.sectionTitle}`}>Motivation Strategy</h3>
              <p className="text-sm text-gray-200 leading-6">{content.motivation_strategy}</p>
            </div>
          )}
        </div>
      )}

      {Array.isArray(content.technology_requirements) && content.technology_requirements.length > 0 && (
        <div className={`rounded-xl border ${theme.border} ${theme.cardBg} overflow-hidden`}>
          <div className={`p-4 bg-gradient-to-r ${theme.headerBg} border-b ${theme.border}`}>
            <h3 className={`text-lg font-semibold ${theme.accentText} flex items-center gap-2`}>
              <span className="w-2 h-2 rounded-full bg-purple-400"></span>
              Technology Requirements
            </h3>
          </div>
          <div className="p-6 space-y-2">
            {content.technology_requirements.map((req, index) => (
              <div key={index} className="flex items-start gap-3 p-3 rounded-lg bg-white/5">
                <div className="w-2 h-2 rounded-full bg-purple-400 flex-shrink-0 mt-2"></div>
                <p className="text-sm text-gray-200">{req}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      <div className={`rounded-xl p-6 bg-gradient-to-br from-gray-900/50 to-black/50 border border-gray-700/50 text-center`}>
        <div className="flex items-center justify-center gap-3 mb-3">
          <div className="w-2 h-2 rounded-full bg-violet-400 animate-pulse"></div>
          <span className="text-sm text-gray-400">Gamification Framework</span>
          <div className="w-2 h-2 rounded-full bg-purple-400 animate-pulse"></div>
        </div>
        <p className="text-xs text-gray-500">
          Engaging learning through game mechanics, rewards, and interactive elements
        </p>
      </div>
    </div>
  );
}

function FlippedClassroom({ content, theme }) {
  if (!content) {
    return (
      <div className={`rounded-xl p-8 border ${theme.border} ${theme.cardBg} text-center`}>
        <div className="text-4xl mb-4">🔁</div>
        <h3 className={`text-xl font-semibold mb-2 ${theme.sectionTitle}`}>Flipped Classroom</h3>
        <p className="text-gray-400">Content is being generated...</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <Header pedagogy="flipped_classroom" content={content} theme={theme} />

      {Array.isArray(content.pre_class_content) && content.pre_class_content.length > 0 && (
        <div className={`rounded-xl border ${theme.border} ${theme.cardBg} overflow-hidden`}>
          <div className={`p-4 bg-gradient-to-r ${theme.headerBg} border-b ${theme.border}`}>
            <h3 className={`text-lg font-semibold ${theme.accentText}`}>Pre-class Content</h3>
          </div>
          <div className="p-6 space-y-4">
            {content.pre_class_content.map((item, index) => (
              <div key={index} className="p-4 rounded-lg bg-white/5">
                <div className="flex items-center justify-between mb-2">
                  <h4 className={`font-semibold ${theme.sectionTitle}`}>{item.title || item.content_type || `Item ${index + 1}`}</h4>
                  {item.estimated_time && (
                    <span className={`px-2 py-1 text-xs rounded-lg border ${theme.chip}`}>{item.estimated_time}</span>
                  )}
                </div>
                {item.description && <p className="text-sm text-gray-200 mb-2">{item.description}</p>}
                {item.full_content && <p className="text-sm text-gray-300 mb-2">{item.full_content}</p>}
                {Array.isArray(item.learning_objectives) && item.learning_objectives.length > 0 && (
                  <div className="mt-2">
                    <div className="text-xs font-medium text-gray-400 uppercase tracking-wide mb-1">Learning Objectives</div>
                    <ul className="list-disc pl-5 space-y-1 text-sm text-gray-300">
                      {item.learning_objectives.map((obj, i) => <li key={i}>{obj}</li>)}
                    </ul>
                  </div>
                )}
                {Array.isArray(item.key_points) && item.key_points.length > 0 && (
                  <div className="mt-2">
                    <div className="text-xs font-medium text-gray-400 uppercase tracking-wide mb-1">Key Points</div>
                    <ul className="list-disc pl-5 space-y-1 text-sm text-gray-300">
                      {item.key_points.map((kp, i) => <li key={i}>{kp}</li>)}
                    </ul>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {Array.isArray(content.in_class_activities) && content.in_class_activities.length > 0 && (
        <div className={`rounded-xl border ${theme.border} ${theme.cardBg} overflow-hidden`}>
          <div className={`p-4 bg-gradient-to-r ${theme.headerBg} border-b ${theme.border}`}>
            <h3 className={`text-lg font-semibold ${theme.accentText}`}>In-class Activities</h3>
          </div>
          <div className="p-6 space-y-4">
            {content.in_class_activities.map((act, index) => (
              <div key={index} className="p-4 rounded-lg bg-white/5">
                <div className="flex items-center justify-between mb-2">
                  <h4 className={`font-semibold ${theme.sectionTitle}`}>{act.activity_name || `Activity ${index + 1}`}</h4>
                  {act.duration && (
                    <span className={`px-2 py-1 text-xs rounded-lg border ${theme.chip}`}>{act.duration}</span>
                  )}
                </div>
                {act.description && <p className="text-sm text-gray-200 mb-2">{act.description}</p>}
                {act.detailed_instructions && <p className="text-sm text-gray-300 mb-2">{act.detailed_instructions}</p>}
                {Array.isArray(act.materials_needed) && act.materials_needed.length > 0 && (
                  <div className="mt-2">
                    <div className="text-xs font-medium text-gray-400 uppercase tracking-wide mb-1">Materials</div>
                    <ul className="list-disc pl-5 space-y-1 text-sm text-gray-300">
                      {act.materials_needed.map((m, i) => <li key={i}>{m}</li>)}
                    </ul>
                  </div>
                )}
                {act.assessment_method && (
                  <div className="mt-2 text-sm text-gray-300">
                    <span className="text-gray-400">Assessment:</span> {act.assessment_method}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {Array.isArray(content.post_class_reinforcement) && content.post_class_reinforcement.length > 0 && (
        <SectionCard title="Post-class Reinforcement" theme={theme}>
          {renderValue(content.post_class_reinforcement)}
        </SectionCard>
      )}

      {(content.assessment_strategy || (Array.isArray(content.technology_tools) && content.technology_tools.length > 0)) && (
        <div className="grid gap-4 md:grid-cols-2">
          {content.assessment_strategy && (
            <div className={`rounded-xl p-4 border ${theme.border} ${theme.cardBg}`}>
              <h3 className={`text-lg font-semibold mb-2 ${theme.sectionTitle}`}>Assessment Strategy</h3>
              <p className="text-sm text-gray-200 leading-6">{content.assessment_strategy}</p>
            </div>
          )}
          {Array.isArray(content.technology_tools) && content.technology_tools.length > 0 && (
            <div className={`rounded-xl p-4 border ${theme.border} ${theme.cardBg}`}>
              <h3 className={`text-lg font-semibold mb-2 ${theme.sectionTitle}`}>Technology Tools</h3>
              <ul className="list-disc pl-5 space-y-1 text-sm text-gray-300">
                {content.technology_tools.map((t, i) => <li key={i}>{t}</li>)}
              </ul>
            </div>
          )}
        </div>
      )}

      <div className={`rounded-xl p-6 bg-gradient-to-br from-gray-900/50 to-black/50 border border-gray-700/50 text-center`}>
        <div className="flex items-center justify-center gap-3 mb-3">
          <div className="w-2 h-2 rounded-full bg-fuchsia-400 animate-pulse"></div>
          <span className="text-sm text-gray-400">Flipped Classroom Framework</span>
          <div className="w-2 h-2 rounded-full bg-purple-400 animate-pulse"></div>
        </div>
        <p className="text-xs text-gray-500">Learn basics at home, apply in class through active learning</p>
      </div>
    </div>
  );
}

function InquiryBasedLearning({ content, theme }) {
  if (!content) {
    return (
      <div className={`rounded-xl p-8 border ${theme.border} ${theme.cardBg} text-center`}>
        <div className="text-4xl mb-4">🔎</div>
        <h3 className={`text-xl font-semibold mb-2 ${theme.sectionTitle}`}>Inquiry Based Learning</h3>
        <p className="text-gray-400">Content is being generated...</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <Header pedagogy="inquiry_based_learning" content={content} theme={theme} />

      {Array.isArray(content.essential_questions) && content.essential_questions.length > 0 && (
        <SectionCard title="Essential Questions" theme={theme}>
          {renderValue(content.essential_questions)}
        </SectionCard>
      )}

      {Array.isArray(content.investigation_phases) && content.investigation_phases.length > 0 && (
        <div className={`rounded-xl border ${theme.border} ${theme.cardBg} overflow-hidden`}>
          <div className={`p-4 bg-gradient-to-r ${theme.headerBg} border-b ${theme.border}`}>
            <h3 className={`text-lg font-semibold ${theme.accentText}`}>Investigation Phases</h3>
          </div>
          <div className="p-6 space-y-4">
            {content.investigation_phases.map((phase, index) => (
              <div key={index} className="p-4 rounded-lg bg-white/5">
                <h4 className={`font-semibold ${theme.sectionTitle} mb-2`}>{phase.phase_name || `Phase ${index + 1}`}</h4>
                {phase.content_guide && <p className="text-sm text-gray-200 mb-2">{phase.content_guide}</p>}
                {Array.isArray(phase.objectives) && phase.objectives.length > 0 && (
                  <div className="mt-2">
                    <div className="text-xs font-medium text-gray-400 uppercase tracking-wide mb-1">Objectives</div>
                    <ul className="list-disc pl-5 space-y-1 text-sm text-gray-300">
                      {phase.objectives.map((o, i) => <li key={i}>{o}</li>)}
                    </ul>
                  </div>
                )}
                {Array.isArray(phase.activities) && phase.activities.length > 0 && (
                  <div className="mt-2">
                    <div className="text-xs font-medium text-gray-400 uppercase tracking-wide mb-1">Activities</div>
                    <ul className="list-disc pl-5 space-y-1 text-sm text-gray-300">
                      {phase.activities.map((a, i) => <li key={i}>{a}</li>)}
                    </ul>
                  </div>
                )}
                {Array.isArray(phase.research_methods) && phase.research_methods.length > 0 && (
                  <div className="mt-2">
                    <div className="text-xs font-medium text-gray-400 uppercase tracking-wide mb-1">Research Methods</div>
                    <ul className="list-disc pl-5 space-y-1 text-sm text-gray-300">
                      {phase.research_methods.map((m, i) => <li key={i}>{m}</li>)}
                    </ul>
                  </div>
                )}
                {Array.isArray(phase.support_materials) && phase.support_materials.length > 0 && (
                  <div className="mt-2">
                    <div className="text-xs font-medium text-gray-400 uppercase tracking-wide mb-1">Support Materials</div>
                    <ul className="list-disc pl-5 space-y-1 text-sm text-gray-300">
                      {phase.support_materials.map((m, i) => <li key={i}>{m}</li>)}
                    </ul>
                  </div>
                )}
                {Array.isArray(phase.example_investigations) && phase.example_investigations.length > 0 && (
                  <div className="mt-2">
                    <div className="text-xs font-medium text-gray-400 uppercase tracking-wide mb-1">Example Investigations</div>
                    <ul className="list-disc pl-5 space-y-1 text-sm text-gray-300">
                      {phase.example_investigations.map((ex, i) => <li key={i}>{ex}</li>)}
                    </ul>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {(Array.isArray(content.research_skills) && content.research_skills.length > 0) && (
        <SectionCard title="Research Skills" theme={theme}>
          {renderValue(content.research_skills)}
        </SectionCard>
      )}

      {(Array.isArray(content.presentation_formats) && content.presentation_formats.length > 0) && (
        <SectionCard title="Presentation Formats" theme={theme}>
          {renderValue(content.presentation_formats)}
        </SectionCard>
      )}

      {content.assessment_rubric && (
        <SectionCard title="Assessment Rubric" theme={theme}>
          {renderValue(content.assessment_rubric)}
        </SectionCard>
      )}

      <div className={`rounded-xl p-6 bg-gradient-to-br from-gray-900/50 to-black/50 border border-gray-700/50 text-center`}>
        <div className="flex items-center justify-center gap-3 mb-3">
          <div className="w-2 h-2 rounded-full bg-sky-400 animate-pulse"></div>
          <span className="text-sm text-gray-400">Inquiry Based Learning Framework</span>
          <div className="w-2 h-2 rounded-full bg-blue-400 animate-pulse"></div>
        </div>
        <p className="text-xs text-gray-500">Students investigate questions through research, analysis, and presentation</p>
      </div>
    </div>
  );
}



export default function OutputRenderer({ pedagogy, content }) {
  const theme = THEMES[pedagogy] || DEFAULT_THEME;

  if (!content) {
    return null;
  }

  if (pedagogy === "project_based_learning") {
    return <ProjectBasedLearning content={content} theme={theme} />;
  }

  if (pedagogy === "socratic_questioning") {
    return <SocraticQuestioning content={content} theme={theme} />;
  }

  if (pedagogy === "blooms_taxonomy") {
    return <BloomsTaxonomy content={content} theme={theme} />;
  }

  if (pedagogy === "peer_learning") {
    return <PeerLearning content={content} theme={theme} />;
  }

  if (pedagogy === "constructivist") {
    return <Constructivist content={content} theme={theme} />;
  }

  if (pedagogy === "gamification") {
    return <Gamification content={content} theme={theme} />;
  }

  if (pedagogy === "flipped_classroom") {
    return <FlippedClassroom content={content} theme={theme} />;
  }

  if (pedagogy === "inquiry_based_learning") {
    return <InquiryBasedLearning content={content} theme={theme} />;
  }

  return <GenericPedagogy pedagogy={pedagogy} content={content} theme={theme} />;
}
