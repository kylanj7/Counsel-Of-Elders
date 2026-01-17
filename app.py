import streamlit as st
import subprocess
import json
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage
from typing import List, Dict
import time
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import io


def get_available_ollama_models() -> List[str]:
    """Fetch available Ollama models from 'ollama list' command."""
    try:
        result = subprocess.run(
            ['ollama', 'list'],
            capture_output=True,
            text=True,
            check=True
        )
        lines = result.stdout.strip().split('\n')
        models = []
        for line in lines[1:]:
            if line.strip():
                model_name = line.split()[0]
                models.append(model_name)
        return models
    except subprocess.CalledProcessError as e:
        st.error(f"Error fetching Ollama models: {e}")
        return []
    except FileNotFoundError:
        st.error("Ollama is not installed or not in PATH")
        return []


class CouncilOfElders:
    """Council of 7 tech experts that debate in parallel rounds."""
    
    ELDERS = [
        {
            "name": "Elder AI/ML",
            "expertise": "AI/Machine Learning Expert",
            "system_prompt": "You are an AI/Machine Learning expert with deep knowledge of neural networks, deep learning, transformers, and modern ML frameworks. Provide insights from an AI/ML perspective."
        },
        {
            "name": "Elder Security",
            "expertise": "Cybersecurity Specialist",
            "system_prompt": "You are a Cybersecurity Specialist with expertise in threat modeling, security architecture, cryptography, and secure coding practices. Analyze from a security perspective."
        },
        {
            "name": "Elder Cloud",
            "expertise": "Cloud & Infrastructure Architect",
            "system_prompt": "You are a Cloud & Infrastructure Architect with expertise in AWS, Azure, GCP, containerization, orchestration, and scalable infrastructure design. Provide cloud architecture insights."
        },
        {
            "name": "Elder Data",
            "expertise": "Data Engineer",
            "system_prompt": "You are a Data Engineer with expertise in data pipelines, ETL processes, data warehousing, streaming architectures, and big data technologies. Analyze from a data engineering perspective."
        },
        {
            "name": "Elder DevOps",
            "expertise": "DevOps/SRE Engineer",
            "system_prompt": "You are a DevOps/SRE Engineer with expertise in CI/CD, monitoring, observability, incident response, and reliability engineering. Provide operational insights."
        },
        {
            "name": "Elder Software",
            "expertise": "Software Architecture Expert",
            "system_prompt": "You are a Software Architecture Expert with deep knowledge of design patterns, system design, microservices, monoliths, and architectural trade-offs. Analyze from a software architecture perspective."
        },
        {
            "name": "Elder Quantum",
            "expertise": "Quantum Physics PhD",
            "system_prompt": "You are a Quantum Physics PhD with expertise in quantum mechanics, quantum computing, quantum algorithms, and the intersection of quantum theory with technology. Provide insights from a quantum physics perspective."
        }
    ]
    
    def __init__(self, model_name: str):
        """Initialize the council with a specific Ollama model."""
        self.model_name = model_name
        self.llm = ChatOllama(model=model_name, temperature=0.7)
        
    def get_elder_opinion(self, elder: Dict, user_input: str, context: str = "") -> str:
        """Get a single elder's opinion on the topic."""
        messages = [
            SystemMessage(content=elder["system_prompt"]),
        ]
        
        if context:
            messages.append(SystemMessage(content=f"Previous discussion context:\n{context}"))
        
        messages.append(HumanMessage(content=user_input))
        
        response = self.llm.invoke(messages)
        return response.content
    
    def aggregate_opinions(self, opinions: Dict[str, str]) -> str:
        """Aggregate all elder opinions into a summary."""
        aggregated = "=== COUNCIL DISCUSSION SUMMARY ===\n\n"
        for elder_name, opinion in opinions.items():
            aggregated += f"{elder_name}:\n{opinion}\n\n"
        return aggregated
    
    def run_debate_round(self, user_input: str, round_num: int, previous_context: str = "") -> Dict[str, str]:
        """Run a single round of parallel debate among all elders."""
        opinions = {}
        
        st.write(f"### Round {round_num}")
        
        for elder in self.ELDERS:
            with st.expander(f"{elder['name']} - {elder['expertise']}", expanded=(round_num == 1)):
                with st.spinner(f"{elder['name']} is thinking..."):
                    opinion = self.get_elder_opinion(elder, user_input, previous_context)
                    opinions[elder['name']] = opinion
                    st.write(opinion)
        
        return opinions
    
    def merlin_synthesis(self, user_input: str, all_rounds: List[Dict[str, str]]) -> str:
        """Merlin synthesizes all debate rounds into final wisdom."""
        merlin_prompt = """You are Merlin, the mystical wizard and synthesizer of wisdom. 
You have observed a council of 7 tech elders debate a topic across multiple rounds.
Your role is to synthesize their collective wisdom into a coherent, insightful final answer.
Weave together their perspectives, resolve contradictions, and provide mystical clarity.
Speak with wisdom and gravitas befitting a legendary wizard."""
        
        context = f"Original question: {user_input}\n\n"
        context += "=== COMPLETE COUNCIL DEBATE ===\n\n"
        
        for round_num, round_opinions in enumerate(all_rounds, 1):
            context += f"--- Round {round_num} ---\n"
            for elder_name, opinion in round_opinions.items():
                context += f"\n{elder_name}:\n{opinion}\n"
            context += "\n"
        
        messages = [
            SystemMessage(content=merlin_prompt),
            HumanMessage(content=context + "\n\nNow, Merlin, synthesize the council's wisdom:")
        ]
        
        response = self.llm.invoke(messages)
        return response.content


def generate_pdf(user_input: str, all_rounds: List[Dict[str, str]], synthesis: str, model_name: str) -> bytes:
    """Generate a PDF report of the council debate."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter,
                           rightMargin=72, leftMargin=72,
                           topMargin=72, bottomMargin=18)
    
    story = []
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor='darkblue',
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor='darkgreen',
        spaceAfter=12,
        spaceBefore=12
    )
    
    elder_name_style = ParagraphStyle(
        'ElderName',
        parent=styles['Heading3'],
        fontSize=12,
        textColor='navy',
        spaceAfter=6,
        spaceBefore=6
    )
    
    normal_style = styles['BodyText']
    
    story.append(Paragraph("Council of Elders", title_style))
    story.append(Paragraph("Tech Wisdom Debate", title_style))
    story.append(Spacer(1, 0.3*inch))
    
    timestamp = datetime.now().strftime("%B %d, %Y at %I:%M %p")
    story.append(Paragraph(f"Generated: {timestamp}", styles['Normal']))
    story.append(Paragraph(f"Model: {model_name}", styles['Normal']))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("Question:", heading_style))
    story.append(Paragraph(user_input, normal_style))
    story.append(Spacer(1, 0.3*inch))
    
    for round_num, round_opinions in enumerate(all_rounds, 1):
        story.append(PageBreak())
        story.append(Paragraph(f"Round {round_num}", heading_style))
        story.append(Spacer(1, 0.2*inch))
        
        for elder_name, opinion in round_opinions.items():
            story.append(Paragraph(elder_name, elder_name_style))
            
            opinion_paragraphs = opinion.split('\n')
            for para in opinion_paragraphs:
                if para.strip():
                    story.append(Paragraph(para, normal_style))
            
            story.append(Spacer(1, 0.2*inch))
    
    story.append(PageBreak())
    story.append(Paragraph("Merlin's Synthesis", heading_style))
    story.append(Spacer(1, 0.2*inch))
    
    synthesis_paragraphs = synthesis.split('\n')
    for para in synthesis_paragraphs:
        if para.strip():
            story.append(Paragraph(para, normal_style))
    
    doc.build(story)
    
    pdf_bytes = buffer.getvalue()
    buffer.close()
    
    return pdf_bytes


def main():
    st.set_page_config(page_title="Council of Elders", page_icon="🧙", layout="wide")
    
    st.title("🧙 Council of Elders - Tech Wisdom Debate")
    st.markdown("*Seven tech experts debate your question, synthesized by Merlin the Wizard*")
    
    with st.sidebar:
        st.header("Configuration")
        
        models = get_available_ollama_models()
        
        if not models:
            st.error("No Ollama models found. Please install Ollama and pull a model.")
            st.stop()
        
        selected_model = st.selectbox(
            "Select Ollama Model",
            options=models,
            help="Choose which local Ollama model to use for the council"
        )
        
        num_iterations = st.number_input(
            "Number of Debate Rounds",
            min_value=1,
            max_value=100,
            value=2,
            help="How many rounds of debate should the council conduct?"
        )
        
        st.markdown("---")
        st.markdown("### The Council")
        st.markdown("""
        1. 🤖 AI/ML Expert
        2. 🔒 Cybersecurity Specialist
        3. ☁️ Cloud Architect
        4. 📊 Data Engineer
        5. 🔧 DevOps/SRE Engineer
        6. 🏗️ Software Architect
        7. ⚛️ Quantum Physics PhD
        
        **Merlin** 🧙 synthesizes their wisdom
        """)
    
    user_input = st.text_area(
        "Enter your question or topic for the council to debate:",
        height=100,
        placeholder="e.g., What are the key considerations for building a real-time ML inference system?"
    )
    
    if st.button("Convene the Council", type="primary"):
        if not user_input:
            st.warning("Please enter a question or topic.")
            return
        
        council = CouncilOfElders(selected_model)
        all_rounds = []
        
        st.markdown("---")
        st.header("Council Debate")
        
        previous_context = ""
        
        for round_num in range(1, num_iterations + 1):
            round_opinions = council.run_debate_round(
                user_input,
                round_num,
                previous_context
            )
            all_rounds.append(round_opinions)
            
            aggregated = council.aggregate_opinions(round_opinions)
            previous_context = aggregated
            
            if round_num < num_iterations:
                st.markdown("---")
        
        st.markdown("---")
        st.header("🧙 Merlin's Synthesis")
        
        with st.spinner("Merlin is weaving the threads of wisdom..."):
            synthesis = council.merlin_synthesis(user_input, all_rounds)
            st.markdown(f"### {synthesis}")
        
        st.success("The council has spoken!")
        
        st.markdown("---")
        st.header("📄 Export Debate")
        
        pdf_bytes = generate_pdf(user_input, all_rounds, synthesis, selected_model)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"council_debate_{timestamp}.pdf"
        
        st.download_button(
            label="📥 Download PDF Report",
            data=pdf_bytes,
            file_name=filename,
            mime="application/pdf",
            help="Download the complete council debate and synthesis as a PDF"
        )


if __name__ == "__main__":
    main()
