"""
Drug Interaction Chatbot
A chatbot that answers questions about drug interactions, side effects, and contraindications.
"""
from typing import List, Dict, Optional
from dataclasses import dataclass
import json


@dataclass
class DrugInfo:
    """Drug information"""
    name: str
    drug_class: str
    interactions: List[str]
    side_effects: List[str]
    contraindications: List[str]
    warnings: List[str]


class DrugKnowledgeBase:
    """
    Drug Knowledge Base
    
    Contains drug interaction information
    """
    
    def __init__(self):
        self.drugs: Dict[str, DrugInfo] = {}
        self._init_knowledge_base()
    
    def _init_knowledge_base(self):
        """Initialize with common drug information"""
        # This is a simplified knowledge base
        # In production, integrate with real drug databases
        
        self.drugs = {
            "aspirin": DrugInfo(
                name="Aspirin",
                drug_class="NSAID",
                interactions=[
                    "Warfarin - increased bleeding risk",
                    "Ibuprofen - reduced aspirin efficacy",
                    "Methotrexate - increased toxicity"
                ],
                side_effects=[
                    "Stomach upset",
                    "Heartburn",
                    "Easy bruising",
                    "Bleeding"
                ],
                contraindications=[
                    "Bleeding disorders",
                    "Peptic ulcer",
                    "Allergy to NSAIDs"
                ],
                warnings=[
                    "May increase bleeding risk",
                    "Avoid before surgery",
                    "Not for children with viral infections"
                ]
            ),
            "warfarin": DrugInfo(
                name="Warfarin",
                drug_class="Anticoagulant",
                interactions=[
                    "Aspirin - increased bleeding risk",
                    "Vitamin K - reduced efficacy",
                    "Antibiotics - may increase or decrease effect"
                ],
                side_effects=[
                    "Bleeding",
                    "Bruising",
                    "Stomach pain"
                ],
                contraindications=[
                    "Pregnancy",
                    "Bleeding disorders",
                    "Uncontrolled hypertension"
                ],
                warnings=[
                    "Regular INR monitoring required",
                    "Consistent vitamin K intake",
                    "Avoid sudden diet changes"
                ]
            ),
            "metformin": DrugInfo(
                name="Metformin",
                drug_class="Antidiabetic",
                interactions=[
                    "Alcohol - increased lactic acidosis risk",
                    "Contrast dyes - kidney risk",
                    "May affect vitamin B12 absorption"
                ],
                side_effects=[
                    "Nausea",
                    "Diarrhea",
                    "Stomach upset",
                    "Metallic taste"
                ],
                contraindications=[
                    "Kidney disease",
                    "Liver disease",
                    "Metabolic acidosis"
                ],
                warnings=[
                    "Monitor kidney function",
                    "Stop before contrast imaging",
                    "Report any unusual symptoms"
                ]
            ),
            "lisinopril": DrugInfo(
                name="Lisinopril",
                drug_class="ACE Inhibitor",
                interactions=[
                    "Potassium supplements - hyperkalemia",
                    "Spironolactone - increased potassium",
                    "NSAIDs - reduced effect, kidney risk"
                ],
                side_effects=[
                    "Dry cough",
                    "Dizziness",
                    "Headache",
                    "Fatigue"
                ],
                contraindications=[
                    "Pregnancy",
                    "Angioedema history",
                    "Bilateral renal artery stenosis"
                ],
                warnings=[
                    "May cause birth defects",
                    "Monitor potassium levels",
                    "Avoid potassium supplements"
                ]
            ),
            "atorvastatin": DrugInfo(
                name="Atorvastatin",
                drug_class="Statin",
                interactions=[
                    "Grapefruit juice - increased levels",
                    "Erythromycin - increased risk",
                    "Warfarin - may increase effect"
                ],
                side_effects=[
                    "Muscle pain",
                    "Headache",
                    "Joint pain",
                    "Nausea"
                ],
                contraindications=[
                    "Liver disease",
                    "Pregnancy",
                    "Breastfeeding"
                ],
                warnings=[
                    "Report muscle pain immediately",
                    "Regular liver function tests",
                    "Avoid grapefruit"
                ]
            ),
            "levothyroxine": DrugInfo(
                name="Levothyroxine",
                drug_class="Thyroid Hormone",
                interactions=[
                    "Calcium - reduced absorption",
                    "Iron - reduced absorption",
                    "Antacids - reduced absorption"
                ],
                side_effects=[
                    "Weight changes",
                    "Mood changes",
                    "Hair loss",
                    "Palpitations"
                ],
                contraindications=[
                    "Adrenal insufficiency",
                    "Thyroid cancer"
                ],
                warnings=[
                    "Take on empty stomach",
                    "Don't switch brands",
                    "Regular thyroid tests"
                ]
            )
        }
    
    def get_drug(self, name: str) -> Optional[DrugInfo]:
        """Get drug information"""
        return self.drugs.get(name.lower())
    
    def search_drugs(self, query: str) -> List[DrugInfo]:
        """Search drugs by name"""
        query = query.lower()
        return [drug for name, drug in self.drugs.items() 
                if query in name or query in drug.drug_class.lower()]


class DrugInteractionChatbot:
    """
    Drug Interaction Chatbot
    
    A chatbot for answering drug-related questions
    """
    
    def __init__(self, use_llm: bool = False, model_name: str = "gpt-3.5-turbo"):
        self.knowledge_base = DrugKnowledgeBase()
        self.use_llm = use_llm
        self.model_name = model_name
        self.conversation_history = []
        
        if use_llm:
            self._init_llm()
    
    def _init_llm(self):
        """Initialize LLM"""
        try:
            import os
            from langchain.chat_models import ChatOpenAI
            from langchain.prompts import ChatPromptTemplate
            
            api_key = os.getenv("OPENAI_API_KEY")
            if api_key:
                self.llm = ChatOpenAI(model=self.model_name, api_key=api_key)
                self.prompt_template = self._create_prompt_template()
        except ImportError:
            print("LangChain not installed. Using rule-based responses.")
            self.use_llm = False
    
    def _create_prompt_template(self):
        """Create LLM prompt template"""
        from langchain.prompts import ChatPromptTemplate
        
        return ChatPromptTemplate.from_messages([
            ("system", """You are a helpful pharmaceutical assistant. 
You provide information about drug interactions, side effects, and contraindications.
Always remind users to consult healthcare professionals for medical advice.
Use the provided drug knowledge base to answer questions."""),
            ("human", "{user_input}")
        ])
    
    def ask(self, question: str) -> str:
        """
        Ask a question about drugs
        
        Args:
            question: User's question
        
        Returns:
            Answer string
        """
        # Add to conversation history
        self.conversation_history.append(f"User: {question}")
        
        # Extract drug names from question
        drugs = self._extract_drugs(question)
        
        if not drugs:
            response = self._general_response(question)
        elif len(drugs) == 1:
            response = self._single_drug_response(drugs[0], question)
        else:
            response = self._interaction_response(drugs, question)
        
        # Add response to history
        self.conversation_history.append(f"Bot: {response}")
        
        return response
    
    def _extract_drugs(self, question: str) -> List[str]:
        """Extract drug names from question"""
        question = question.lower()
        found = []
        
        for drug_name in self.knowledge_base.drugs:
            if drug_name in question:
                found.append(drug_name)
        
        return found
    
    def _single_drug_response(self, drug_name: str, question: str) -> str:
        """Response for single drug questions"""
        drug = self.knowledge_base.get_drug(drug_name)
        
        if not drug:
            return "I don't have information about that drug."
        
        question = question.lower()
        
        if "side effect" in question or "adverse" in question:
            return self._format_side_effects(drug)
        elif "contraindication" in question or "avoid" in question:
            return self._format_contraindications(drug)
        elif "warning" in question or "precaution" in question:
            return self._format_warnings(drug)
        else:
            return self._format_drug_info(drug)
    
    def _interaction_response(self, drugs: List[str], question: str) -> str:
        """Response for drug interaction questions"""
        question = question.lower()
        
        # Check if we have interaction info
        interactions = []
        
        for drug_name in drugs:
            drug = self.knowledge_base.get_drug(drug_name)
            if drug:
                for interaction in drug.interactions:
                    for other_drug in drugs:
                        if other_drug != drug_name and other_drug in interaction.lower():
                            interactions.append(interaction)
        
        if interactions:
            return self._format_interactions(drugs, interactions)
        else:
            return self._no_interaction_found(drugs)
    
    def _format_drug_info(self, drug: DrugInfo) -> str:
        """Format drug information"""
        return f"""## {drug.name} ({drug.drug_class})

### Drug Class
{drug.drug_class}

### Common Side Effects
{chr(10).join(f"- {effect}" for effect in drug.side_effects[:5])}

### Interactions
{chr(10).join(f"- {interaction}" for interaction in drug.interactions[:3])}

### Warnings
{chr(10).join(f"- {warning}" for warning in drug.warnings[:3])}

⚠️ **Disclaimer**: Always consult a healthcare professional for medical advice."""

    def _format_side_effects(self, drug: DrugInfo) -> str:
        """Format side effects"""
        return f"""## Side Effects of {drug.name}

{chr(10).join(f"- {effect}" for effect in drug.side_effects)}

⚠️ **Note**: This is not a complete list. Consult your doctor or pharmacist."""

    def _format_contraindications(self, drug: DrugInfo) -> str:
        """Format contraindications"""
        return f"""## Contraindications for {drug.name}

**When NOT to use {drug.name}:**

{chr(10).join(f"- {contra}" for contra in drug.contraindications)}

⚠️ **Important**: Tell your doctor about all your medical conditions before taking this medication."""

    def _format_warnings(self, drug: DrugInfo) -> str:
        """Format warnings"""
        return f"""## Warnings for {drug.name}

{chr(10).join(f"- {warning}" for drug.warnings)}

⚠️ **Safety First**: Follow your doctor's instructions carefully."""

    def _format_interactions(self, drugs: List[str], interactions: List[str]) -> str:
        """Format drug interactions"""
        return f"""## Drug Interactions between {', '.join(drugs).title()}

### Known Interactions

{chr(10).join(f"- {interaction}" for interaction in interactions)}

⚠️ **Warning**: These interactions can be serious. Always consult your healthcare provider.

### Tips
- Keep a list of all your medications
- Ask your pharmacist about interactions
- Report any unusual symptoms"""

    def _no_interaction_found(self, drugs: List[str]) -> str:
        """No interaction found response"""
        return f"""## No Known Interactions Found

I don't have specific interaction data for {', '.join(drugs).title()} in my knowledge base.

### Recommendations
- Consult your pharmacist
- Check with a drug interaction database
- Always inform healthcare providers about all medications you're taking

⚠️ **Disclaimer**: This is not medical advice."""

    def _general_response(self, question: str) -> str:
        """General response for non-drug questions"""
        return """I'm a drug interaction assistant. You can ask me about:
- Drug-drug interactions
- Side effects of medications
- Contraindications
- Warnings and precautions

Just tell me which medication(s) you're interested in!"""

    def reset_conversation(self):
        """Reset conversation history"""
        self.conversation_history = []


# ============== Main ==============

if __name__ == "__main__":
    # Test
    chatbot = DrugInteractionChatbot()
    
    # Test questions
    questions = [
        "What are the side effects of aspirin?",
        "What are the interactions between aspirin and warfarin?",
        "Is it safe to take metformin with alcohol?",
        "What are the contraindications for lisinopril?"
    ]
    
    for q in questions:
        print(f"\n{'='*50}")
        print(f"Q: {q}")
        print(f"A: {chatbot.ask(q)}")
