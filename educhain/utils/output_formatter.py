# educhain/utils/output_formatter.py

from typing import Any, Optional, List, Dict
import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import json
from datetime import datetime

class OutputFormatter:
    @staticmethod
    def _convert_to_dict_list(data: Any) -> List[Dict]:
        """Convert Pydantic model data to a list of dictionaries"""
        if hasattr(data, 'questions'):
            # If it's a question list model
            return [q.dict() for q in data.questions]
        elif isinstance(data, list):
            # If it's already a list
            return [item.dict() if hasattr(item, 'dict') else item for item in data]
        else:
            # Single item
            return [data.dict() if hasattr(data, 'dict') else data]

    @staticmethod
    def to_csv(data: Any, filename: Optional[str] = None) -> str:
        """Convert data to CSV format"""
        if filename is None:
            filename = f"questions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        dict_list = OutputFormatter._convert_to_dict_list(data)
        df = pd.DataFrame(dict_list)
        
        # Handle nested structures (like options in MCQs)
        for col in df.columns:
            if isinstance(df[col].iloc[0], (list, dict)):
                df[col] = df[col].apply(json.dumps)
        
        df.to_csv(filename, index=False)
        return filename

    @staticmethod
    def _format_question(question: Dict, styles: Dict) -> List:
        """Format a single question for PDF output"""
        elements = []
        
        # Question number and text
        question_text = Paragraph(f"Q{question.get('id', '')}: {question.get('question', '')}", 
                                styles['Question'])
        elements.append(question_text)
        elements.append(Spacer(1, 12))

        # Options (if present)
        if 'options' in question:
            options = question['options']
            if isinstance(options, str):
                try:
                    options = json.loads(options)
                except:
                    options = [options]
                    
            for i, opt in enumerate(options):
                if isinstance(opt, dict):
                    opt_text = opt.get('text', '')
                    is_correct = opt.get('correct', 'false') == 'true'
                else:
                    opt_text = str(opt)
                    is_correct = False
                
                option_style = styles['CorrectOption'] if is_correct else styles['Option']
                option_text = Paragraph(f"{chr(65+i)}. {opt_text}", option_style)
                elements.append(option_text)
                elements.append(Spacer(1, 6))

        # Correct Answer (if not MCQ)
        if 'answer' in question:
            answer_text = Paragraph(f"Correct Answer: {question['answer']}", 
                                  styles['CorrectAnswer'])
            elements.append(answer_text)
            elements.append(Spacer(1, 6))

        # Explanation
        if question.get('explanation'):
            explanation_text = Paragraph(f"Explanation: {question['explanation']}", 
                                      styles['Explanation'])
            elements.append(explanation_text)
            
        elements.append(Spacer(1, 20))
        return elements

    @staticmethod
    def to_pdf(data: Any, filename: Optional[str] = None) -> str:
        """Convert data to PDF format using ReportLab"""
        if filename is None:
            filename = f"questions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

        # Create the PDF document
        doc = SimpleDocTemplate(
            filename,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )

        # Define styles
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(
            name='Question',
            parent=styles['Normal'],
            fontSize=12,
            spaceAfter=6,
            fontName='Helvetica-Bold'
        ))
        styles.add(ParagraphStyle(
            name='Option',
            parent=styles['Normal'],
            fontSize=11,
            leftIndent=20,
            fontName='Helvetica'
        ))
        styles.add(ParagraphStyle(
            name='CorrectOption',
            parent=styles['Normal'],
            fontSize=11,
            leftIndent=20,
            textColor=colors.green,
            fontName='Helvetica-Bold'
        ))
        styles.add(ParagraphStyle(
            name='CorrectAnswer',
            parent=styles['Normal'],
            fontSize=11,
            textColor=colors.green,
            fontName='Helvetica-Bold'
        ))
        styles.add(ParagraphStyle(
            name='Explanation',
            parent=styles['Normal'],
            fontSize=10,
            leftIndent=20,
            textColor=colors.gray,
            fontName='Helvetica-Oblique'
        ))

        # Build the document content
        elements = []
        
        # Add title
        title = Paragraph("Generated Questions", styles['Title'])
        elements.append(title)
        elements.append(Spacer(1, 30))

        # Process questions
        dict_list = OutputFormatter._convert_to_dict_list(data)
        for i, question in enumerate(dict_list, 1):
            question['id'] = i
            elements.extend(OutputFormatter._format_question(question, styles))

        # Generate the PDF
        doc.build(elements)
        return filename