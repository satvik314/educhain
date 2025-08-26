import { useState, useEffect } from "react";

export default function ParamForm({ paramsDef, onSubmit, isSubmitting = false, pedagogy }) {
  const [formData, setFormData] = useState({});

  // Set default values for all pedagogies
  useEffect(() => {
    const defaultValues = getDefaultValues(pedagogy);
    setFormData(defaultValues);
  }, [pedagogy]);

  const getDefaultValues = (pedagogyName) => {
    const defaults = {
      blooms_taxonomy: {
        grade_level: "High School",
        target_level: "Intermediate"
      },
      socratic_questioning: {
        depth_level: "Intermediate",
        student_level: "High School"
      },
      project_based_learning: {
        project_duration: "4-6 weeks",
        team_size: "3-4 students",
        industry_focus: "General"
      },
      flipped_classroom: {
        class_duration: "50 minutes",
        prep_time: "30-45 minutes",
        technology_level: "Moderate"
      },
      inquiry_based_learning: {
        inquiry_type: "Guided",
        investigation_scope: "Moderate",
        student_autonomy: "Balanced"
      },
      constructivist: {
        prior_knowledge_level: "Mixed",
        social_interaction_focus: "High",
        reflection_emphasis: "Strong"
      },
      gamification: {
        game_mechanics: "Points, badges, levels",
        competition_level: "Moderate",
        technology_platform: "Web-based"
      },
      peer_learning: {
        group_size: "3-4 students",
        collaboration_type: "Mixed",
        skill_diversity: "Moderate"
      }
    };
    return defaults[pedagogyName] || {};
  };

  const handleChange = (key, value) => {
    setFormData({ ...formData, [key]: value });
  };

  const humanize = (text) =>
    String(text)
      .replace(/_/g, " ")
      .replace(/\b\w/g, (m) => m.toUpperCase());

  const getInputType = (key, pedagogyName) => {
    // All parameters will be dropdowns for better UX
    return "select";
  };

  const getOptions = (key, pedagogyName) => {
    const options = {
      // Blooms Taxonomy
      grade_level: ["Elementary", "Middle School", "High School", "College", "University"],
      target_level: ["Beginner", "Intermediate", "Advanced", "Expert"],
      
      // Socratic Questioning
      depth_level: ["Basic", "Intermediate", "Advanced", "Expert"],
      student_level: ["Elementary", "Middle School", "High School", "College", "University"],
      
      // Project Based Learning
      project_duration: ["1-2 weeks", "2-4 weeks", "4-6 weeks", "6-8 weeks", "8+ weeks"],
      team_size: ["Individual", "2 students", "3-4 students", "5-6 students", "7+ students"],
      industry_focus: ["General", "Technology", "Healthcare", "Education", "Business", "Arts", "Science", "Engineering"],
      
      // Flipped Classroom
      class_duration: ["30 minutes", "45 minutes", "50 minutes", "60 minutes", "90 minutes", "120 minutes"],
      prep_time: ["15-20 minutes", "20-30 minutes", "30-45 minutes", "45-60 minutes", "60+ minutes"],
      technology_level: ["Basic", "Moderate", "Advanced", "Expert"],
      
      // Inquiry Based Learning
      inquiry_type: ["Structured", "Guided", "Open", "Free"],
      investigation_scope: ["Limited", "Moderate", "Extensive", "Comprehensive"],
      student_autonomy: ["Low", "Balanced", "High", "Complete"],
      
      // Constructivist
      prior_knowledge_level: ["None", "Basic", "Mixed", "Advanced", "Expert"],
      social_interaction_focus: ["Low", "Medium", "High", "Essential"],
      reflection_emphasis: ["Minimal", "Moderate", "Strong", "Critical"],
      
      // Gamification
      game_mechanics: ["Points, badges, levels", "Leaderboards", "Achievements", "Quests", "Story-based", "Competition", "Collaboration"],
      competition_level: ["None", "Low", "Moderate", "High", "Intense"],
      technology_platform: ["Web-based", "Mobile app", "Desktop software", "Mixed reality", "Board games", "Hybrid"],
      
      // Peer Learning
      group_size: ["2 students", "3-4 students", "5-6 students", "7-8 students", "9+ students"],
      collaboration_type: ["Individual", "Pairs", "Small groups", "Large groups", "Mixed"],
      skill_diversity: ["Low", "Moderate", "High", "Mixed", "Random"]
    };
    
    return options[key] || ["Option 1", "Option 2", "Option 3"];
  };

  // For all pedagogies, show the required parameters with dropdowns
  const getParametersToShow = () => {
    if (pedagogy && paramsDef) {
      return paramsDef;
    }
    // Fallback if no paramsDef provided
    return getDefaultValues(pedagogy);
  };

  const parametersToShow = getParametersToShow();

  return (
    <form
      onSubmit={(e) => {
        e.preventDefault();
        // Ensure we always send the default values for the specific pedagogy
        const finalData = { ...getDefaultValues(pedagogy), ...formData };
        onSubmit(finalData);
      }}
      className="space-y-6"
    >
      {Object.entries(parametersToShow).map(([key, desc]) => (
        <div key={key} className="space-y-2">
          <label htmlFor={key} className="block text-sm font-semibold text-orange-200">
            {humanize(key)}
          </label>
          <select
            id={key}
            value={formData[key] || ""}
            onChange={(e) => handleChange(key, e.target.value)}
            className="w-full rounded-lg border border-orange-500/30 bg-black/40 p-3 text-orange-100 focus:outline-none focus:ring-2 focus:ring-orange-500/40 focus:border-orange-500/50"
          >
            <option value="">Select {humanize(key)}</option>
            {getOptions(key, pedagogy).map((option) => (
              <option key={option} value={option} className="bg-black text-orange-100">
                {option}
              </option>
            ))}
          </select>
          {desc && (
            <p className="text-xs text-orange-200/60">{desc}</p>
          )}
        </div>
      ))}

      <button
        type="submit"
        disabled={isSubmitting}
        className={`w-full rounded-lg px-6 py-3 font-semibold text-black shadow-lg focus:outline-none focus:ring-2 transition-all duration-200 ${
          isSubmitting
            ? "bg-orange-500/60 cursor-not-allowed"
            : "bg-gradient-to-r from-orange-500 to-amber-500 hover:from-orange-600 hover:to-amber-600 focus:ring-orange-500/50 transform hover:scale-105"
        }`}
      >
        {isSubmitting ? "Generating..." : `Generate ${humanize(pedagogy)}`}
      </button>
    </form>
  );
}
