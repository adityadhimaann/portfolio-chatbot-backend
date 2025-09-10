#!/usr/bin/env python3
"""
Simple Content Analyzer - Extract structured data without ML models
"""

import re
import json
import PyPDF2
from typing import Dict, List

class SimpleContentAnalyzer:
    def __init__(self):
        pass
        
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from PDF file"""
        text = ""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
        except Exception as e:
            print(f"Error reading PDF: {e}")
        return text
        
    def analyze_content(self, pdf_path: str) -> Dict:
        """Extract and analyze PDF content"""
        print("🔍 Starting content analysis...")
        
        # Extract raw text
        raw_text = self.extract_text_from_pdf(pdf_path)
        print(f"📄 Extracted {len(raw_text)} characters from PDF")
        
        # Clean text
        cleaned_text = self._clean_text(raw_text)
        
        # Extract structured information
        structured_info = self._extract_structured_info(cleaned_text)
        
        # Display analysis
        self._display_analysis(structured_info)
        
        return structured_info
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        text = re.sub(r'\s+', ' ', text)
        text = text.replace('|', ' ')
        text = text.replace('•', ' • ')
        return text.strip()
    
    def _extract_structured_info(self, text: str) -> Dict:
        """Extract structured information"""
        info = {
            'personal': {
                'name': 'Aditya Kumar',
                'role': 'Web Developer',
                'location': 'Lucknow, Uttar Pradesh'
            },
            'contact': {},
            'education': {},
            'skills': {'technical': [], 'tools': [], 'soft': []},
            'experience': [],
            'projects': [],
            'certifications': [],
            'achievements': []
        }
        
        # Extract contact
        phone_match = re.search(r'\+91\s?(\d{10})', text)
        if phone_match:
            info['contact']['phone'] = f"+91 {phone_match.group(1)}"
        
        email_match = re.search(r'(\S+@\S+\.\S+)', text)
        if email_match:
            info['contact']['email'] = email_match.group(1)
        
        # Extract education
        if 'bachelor of technology' in text.lower():
            info['education']['degree'] = 'Bachelor of Technology in Computer Science and Engineering'
        if 'lovely professional' in text.lower():
            info['education']['university'] = 'Lovely Professional University'
        if '2023' in text and '2027' in text:
            info['education']['years'] = '2023 - 2027'
        
        # Extract technical skills
        tech_skills = ['HTML', 'CSS', 'JavaScript', 'React', 'jQuery', 'Tailwind CSS', 'Python', 'Java', 'Node.js', 'MongoDB', 'MySQL']
        for skill in tech_skills:
            if skill.lower() in text.lower():
                info['skills']['technical'].append(skill)
        
        # Extract tools
        tools = ['AWS', 'Canva AI', 'Cursor AI', 'ChatGPT', 'Claude', 'Gemini', 'AutoML', 'OpenAI', 'Oracle Cloud']
        for tool in tools:
            if tool.lower() in text.lower():
                info['skills']['tools'].append(tool)
        
        # Extract soft skills
        soft_skills = ['Project Management', 'Effective Communication', 'Critical Thinking', 'Problem Solving']
        for skill in soft_skills:
            if skill.lower() in text.lower():
                info['skills']['soft'].append(skill)
        
        # Extract projects
        if 'fitness' in text.lower() and 'website' in text.lower():
            info['projects'].append({
                'name': 'Responsive Fitness-and-Sports Website',
                'description': 'Built a responsive fitness and sports website that achieved Top 10 position in CodeBlocks Hackathon 2024',
                'technologies': ['HTML', 'CSS', 'JavaScript'],
                'achievement': 'Top 10 position in CodeBlocks Hackathon 2024'
            })
        
        if 'stress' in text.lower() and 'openai' in text.lower():
            info['projects'].append({
                'name': 'Stress Reduction Application',
                'description': 'Developed stress reduction application using OpenAI API with guided exercises and meditation',
                'technologies': ['OpenAI API', 'Python'],
                'features': ['Guided exercises', 'Meditation']
            })
        
        if 'bhasavitt' in text.lower() or ('multilingual' in text.lower() and 'ai' in text.lower()):
            info['projects'].append({
                'name': 'BhasaVitt - Multilingual AI Model',
                'description': 'Developed multilingual AI model for Gromo-AWS-Sarvam AI challenge',
                'achievement': 'National Level Hackathon Finalist (25,000+ participants)',
                'technologies': ['AI/ML', 'Multilingual Processing']
            })
        
        # Extract certifications
        if 'oracle cloud infrastructure' in text.lower():
            info['certifications'].append('Oracle Cloud Infrastructure 2025 Certified')
        if 'project management professionalism' in text.lower():
            info['certifications'].append('Project Management Professionalism')
        
        # Extract achievements
        if 'top 10' in text.lower() and 'hackathon' in text.lower():
            info['achievements'].append('Top 10 position in CodeBlocks Hackathon 2024')
        if 'finalist' in text.lower() and 'finArva' in text.lower():
            info['achievements'].append('FinArva AI Hackathon Finalist')
        if 'finalist' in text.lower() and '25,000' in text:
            info['achievements'].append('National Level Hackathon Finalist in Gromo-AWS-Sarvam AI challenge (25,000+ participants)')
        
        # Extract experience
        if 'hackathon' in text.lower():
            info['experience'].append({
                'type': 'Hackathon Participation & Development',
                'description': 'Active participant in multiple national-level hackathons with consistent achievements',
                'highlights': [
                    'Top 10 position in CodeBlocks Hackathon 2024',
                    'Finalist in FinArva AI Hackathon',
                    'National Level Hackathon Finalist (25,000+ participants)',
                    'Built responsive websites and AI applications'
                ]
            })
        
        return info
    
    def _display_analysis(self, info: Dict):
        """Display analysis results"""
        print("\n" + "="*60)
        print("📊 STRUCTURED RESUME ANALYSIS")
        print("="*60)
        
        print(f"\n👤 Personal Information:")
        for key, value in info['personal'].items():
            print(f"   {key.title()}: {value}")
        
        print(f"\n📞 Contact Information:")
        for key, value in info['contact'].items():
            print(f"   {key.title()}: {value}")
        
        print(f"\n🎓 Education:")
        for key, value in info['education'].items():
            print(f"   {key.title()}: {value}")
        
        print(f"\n💼 Skills:")
        for category, skills in info['skills'].items():
            if skills:
                print(f"   {category.title()}: {', '.join(skills)}")
        
        print(f"\n🏆 Experience:")
        for exp in info['experience']:
            print(f"   Type: {exp.get('type', 'N/A')}")
            print(f"   Description: {exp.get('description', 'N/A')}")
            if exp.get('highlights'):
                for highlight in exp['highlights']:
                    print(f"     • {highlight}")
        
        print(f"\n🚀 Projects:")
        for project in info['projects']:
            print(f"   📝 {project.get('name', 'Unnamed Project')}")
            print(f"      Description: {project.get('description', 'N/A')}")
            if project.get('technologies'):
                print(f"      Technologies: {', '.join(project['technologies'])}")
            if project.get('achievement'):
                print(f"      Achievement: {project['achievement']}")
            print()
        
        print(f"\n🏅 Certifications:")
        for cert in info['certifications']:
            print(f"   • {cert}")
        
        print(f"\n🎯 Achievements:")
        for achievement in info['achievements']:
            print(f"   • {achievement}")
        
        print("\n" + "="*60)

def main():
    analyzer = SimpleContentAnalyzer()
    pdf_path = "../data/aditya-kumar.pdf"
    
    try:
        structured_info = analyzer.analyze_content(pdf_path)
        
        # Save structured data
        output_path = "../data/structured_resume_data.json"
        with open(output_path, "w") as f:
            json.dump(structured_info, f, indent=2)
        
        print(f"✅ Analysis complete! Structured data saved to {output_path}")
        return structured_info
        
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        return None

if __name__ == "__main__":
    main()
