from typing import Optional, Any
import json
import csv
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer


class ContentExporter:
    def export_lesson_plan_to_pdf(self, lesson_plan: Any, output_path: Optional[str] = None) -> str:
        """Export lesson plan to PDF format using ReportLab"""
        if output_path is None:
            output_path = f"lesson_plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        
        # Create PDF document
        doc = SimpleDocTemplate(output_path, pagesize=letter)
        story = []
        styles = getSampleStyleSheet()
        
        # Title
        title = getattr(lesson_plan, 'title', 'Untitled Lesson Plan')
        story.append(Paragraph(f"Lesson Plan: {title}", styles['Title']))
        story.append(Spacer(1, 12))
        
        # Subject Area
        subject = getattr(lesson_plan, 'subject', 'N/A')
        story.append(Paragraph(f"Subject Area: {subject}", styles['Heading2']))
        story.append(Spacer(1, 12))
        
        # Learning Objectives
        learning_objectives = getattr(lesson_plan, 'learning_objectives', [])
        story.append(Paragraph("Learning Objectives:", styles['Heading2']))
        for obj in learning_objectives:
            story.append(Paragraph(f"- {obj}", styles['Normal']))
        story.append(Spacer(1, 12))
        
        # Main Topics
        for topic in getattr(lesson_plan, 'main_topics', []):
            topic_title = getattr(topic, 'title', 'Untitled Topic')
            story.append(Paragraph(f"Topic: {topic_title}", styles['Heading2']))
            story.append(Spacer(1, 12))
            
            for subtopic in getattr(topic, 'subtopics', []):
                subtopic_title = getattr(subtopic, 'title', 'Untitled Subtopic')
                story.append(Paragraph(f"Subtopic: {subtopic_title}", styles['Heading3']))
                story.append(Spacer(1, 12))
                
                # Add Key Concepts, Discussion Questions, and Activities
                story.append(Paragraph(f"Key Concepts: {getattr(subtopic, 'key_concepts', 'N/A')}", styles['Normal']))
                discussion_questions = getattr(subtopic, 'discussion_questions', [])
                story.append(Paragraph(f"Discussion Questions: {', '.join(str(q) for q in discussion_questions)}", styles['Normal']))
                story.append(Paragraph(f"Activities: {getattr(subtopic, 'activities', 'N/A')}", styles['Normal']))
                story.append(Spacer(1, 12))
        
        # Build the PDF
        doc.build(story)
        print(f"PDF generated successfully: {output_path}")  # Debugging output
        return output_path

    def export_lesson_plan_to_csv(self, lesson_plan: Any, output_path: Optional[str] = None) -> str:
        """Export lesson plan to CSV format."""
        if output_path is None:
            output_path = f"lesson_plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

        with open(output_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Section', 'Content'])

            writer.writerow(['Title', getattr(lesson_plan, 'title', 'Untitled Lesson Plan')])
            writer.writerow(['Subject', getattr(lesson_plan, 'subject', 'N/A')])
            learning_objectives = getattr(lesson_plan, 'learning_objectives', [])
            writer.writerow(['Learning Objectives', '\n'.join(learning_objectives) if learning_objectives else 'N/A'])

            for topic in getattr(lesson_plan, 'main_topics', []):
                writer.writerow(['Topic', getattr(topic, 'title', 'Untitled Topic')])
                for subtopic in getattr(topic, 'subtopics', []):
                    writer.writerow(['Subtopic', getattr(subtopic, 'title', 'Untitled Subtopic')])
                    writer.writerow(['Key Concepts', getattr(subtopic, 'key_concepts', 'N/A')])
                    discussion_questions = getattr(subtopic, 'discussion_questions', [])
                    writer.writerow(['Discussion Questions', '\n'.join(str(q) for q in discussion_questions)])  # Convert to string
                    writer.writerow(['Activities', getattr(subtopic, 'activities', 'N/A')])

        return output_path

    def export_study_guide_to_pdf(self, study_guide: Any, output_path: Optional[str] = None) -> str:
        """Export study guide to PDF format using ReportLab."""
        if output_path is None:
            output_path = f"study_guide_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

        # Create PDF document
        doc = SimpleDocTemplate(output_path, pagesize=letter)
        story = []
        styles = getSampleStyleSheet()
        
        # Title
        topic = getattr(study_guide, 'topic', 'N/A')
        story.append(Paragraph(f"Study Guide: {topic}", styles['Title']))
        story.append(Spacer(1, 12))

        # Overview
        overview = getattr(study_guide, 'overview', 'N/A')
        story.append(Paragraph("Overview", styles['Heading2']))
        story.append(Paragraph(overview, styles['Normal']))
        story.append(Spacer(1, 12))

        # Key Concepts
        story.append(Paragraph("Key Concepts", styles['Heading2']))
        for concept, description in getattr(study_guide, 'key_concepts', {}).items():
            story.append(Paragraph(f"{concept}: {description}", styles['Normal']))
        
        # Practice Exercises
        story.append(Paragraph("Practice Exercises", styles['Heading2']))
        for exercise in getattr(study_guide, 'practice_exercises', []):
            title = getattr(exercise, 'title', 'N/A')
            difficulty = getattr(exercise, 'difficulty', 'N/A')
            problem = getattr(exercise, 'problem', 'N/A')
            solution = getattr(exercise, 'solution', 'N/A')
            story.append(Paragraph(f"Exercise: {title} (Difficulty: {difficulty})", styles['Normal']))
            story.append(Paragraph(f"Problem: {problem}", styles['Normal']))
            story.append(Paragraph(f"Solution: {solution}", styles['Normal']))
            story.append(Spacer(1, 12))

        # Case Studies
        story.append(Paragraph("Case Studies", styles['Heading2']))
        for case in getattr(study_guide, 'case_studies', []):
            case_title = getattr(case, 'title', 'N/A')
            scenario = getattr(case, 'scenario', 'N/A')
            challenge = getattr(case, 'challenge', 'N/A')
            story.append(Paragraph(f"Case Study: {case_title}", styles['Normal']))
            story.append(Paragraph(f"Scenario: {scenario}", styles['Normal']))
            story.append(Paragraph(f"Challenge: {challenge}", styles['Normal']))
            story.append(Spacer(1, 12))

        # Build the PDF
        doc.build(story)
        print(f"PDF generated successfully: {output_path}")  # Debugging output
        return output_path

    def export_study_guide_to_csv(self, study_guide: Any, output_path: Optional[str] = None) -> str:
        """Export study guide to CSV format."""
        if output_path is None:
            output_path = f"study_guide_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

        with open(output_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Section', 'Content'])

            writer.writerow(['Topic', getattr(study_guide, 'topic', 'N/A')])
            writer.writerow(['Overview', getattr(study_guide, 'overview', 'N/A')])

            for concept, description in getattr(study_guide, 'key_concepts', {}).items():
                writer.writerow(['Key Concept', f"{concept}: {description}"])
            for exercise in getattr(study_guide, 'practice_exercises', []):
                writer.writerow(['Practice Exercise', f"{getattr(exercise, 'title', 'N/A')}: {getattr(exercise, 'problem', 'N/A')}"])

            for case in getattr(study_guide, 'case_studies', []):
                writer.writerow(['Case Study', f"{getattr(case, 'title', 'N/A')}: {getattr(case, 'scenario', 'N/A')}"])

        return output_path

    def export_career_connections_to_pdf(self, career_connections: Any, output_path: Optional[str] = None) -> str:
        """Export career connections to PDF format using ReportLab."""
        if output_path is None:
            output_path = f"career_connections_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

        # Create PDF document
        doc = SimpleDocTemplate(output_path, pagesize=letter)
        story = []
        styles = getSampleStyleSheet()
        
        # Title
        career_field = getattr(career_connections, 'career_field', 'N/A')
        story.append(Paragraph(f"Career Connections: {career_field}", styles['Title']))
        story.append(Spacer(1, 12))

        # Description
        description = getattr(career_connections, 'description', 'N/A')
        story.append(Paragraph("Description", styles['Heading2']))
        story.append(Paragraph(description, styles['Normal']))
        story.append(Spacer(1, 12))

        # Required Skills
        story.append(Paragraph("Required Skills", styles['Heading2']))
        for skill in getattr(career_connections, 'required_skills', []):
            story.append(Paragraph(f"- {skill}", styles['Normal']))
        
        # Career Pathways
        story.append(Paragraph("Career Pathways", styles['Heading2']))
        for pathway in getattr(career_connections, 'career_pathways', []):
            pathway_name = getattr(pathway, 'name', 'N/A')
            pathway_description = getattr(pathway, 'description', 'N/A')
            story.append(Paragraph(f"Pathway: {pathway_name}", styles['Normal']))
            story.append(Paragraph(f"Description: {pathway_description}", styles['Normal']))
            story.append(Spacer(1, 12))

        # Build the PDF
        doc.build(story)
        print(f"PDF generated successfully: {output_path}")  # Debugging output
        return output_path

    def export_career_connections_to_csv(self, career_connections: Any, output_path: Optional[str] = None) -> str:
        """Export career connections to CSV format."""
        if output_path is None:
            output_path = f"career_connections_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

        with open(output_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Section', 'Content'])

            writer.writerow(['Career Field', getattr(career_connections, 'career_field', 'N/A')])
            writer.writerow(['Description', getattr(career_connections, 'description', 'N/A')])

            for skill in getattr(career_connections, 'required_skills', []):
                writer.writerow(['Required Skill', skill])
            for pathway in getattr(career_connections, 'career_pathways', []):
                writer.writerow(['Career Pathway', f"{getattr(pathway, 'name', 'N/A')}: {getattr(pathway, 'description', 'N/A')}"])

        return output_path
