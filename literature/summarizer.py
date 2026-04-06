"""
Literature Review Assistant
Automated summarization and information extraction from pharmaceutical papers
"""
from typing import List, Dict, Optional
from dataclasses import dataclass
import re


@dataclass
class PaperSummary:
    """Paper summary"""
    title: str
    authors: List[str]
    abstract: str
    key_findings: List[str]
    methods: List[str]
    limitations: List[str]
    citations: int


class LiteratureSummarizer:
    """
    Literature Review Summarizer
    
    Summarize and extract key information from research papers
    """
    
    def __init__(self, use_llm: bool = False):
        self.use_llm = use_llm
        
    def summarize(self, text: str, title: str = "") -> PaperSummary:
        """
        Summarize a research paper
        
        Args:
            text: Paper text (abstract or full text)
            title: Paper title
        
        Returns:
            PaperSummary object
        """
        # Extract components
        abstract = self._extract_abstract(text)
        findings = self._extract_findings(text)
        methods = self._extract_methods(text)
        limitations = self._extract_limitations(text)
        
        # Extract authors (if available)
        authors = self._extract_authors(text)
        
        # Count citations (simplified)
        citations = self._count_citations(text)
        
        return PaperSummary(
            title=title,
            authors=authors,
            abstract=abstract,
            key_findings=findings,
            methods=methods,
            limitations=limitations,
            citations=citations
        )
    
    def _extract_abstract(self, text: str) -> str:
        """Extract abstract section"""
        # Look for abstract section
        abstract_match = re.search(
            r'(?:abstract|summary)[\s\n]*(.{100,2000}?)(?:\n\n|introduction|background)',
            text,
            re.IGNORECASE | re.DOTALL
        )
        
        if abstract_match:
            return abstract_match.group(1).strip()
        
        # If no abstract found, return first 500 chars
        return text[:500] + "..."
    
    def _extract_findings(self, text: str) -> List[str]:
        """Extract key findings"""
        findings = []
        
        # Look for results/findings section
        results_match = re.search(
            r'(?:results|findings|conclusions)[\s\n]*(.{500,3000}?)(?:\n\n|references|bibliography)',
            text,
            re.IGNORECASE | re.DOTALL
        )
        
        if results_match:
            results_text = results_match.group(1)
            
            # Extract bullet points or numbered items
            bullets = re.findall(
                r'(?:^|\n)\s*(?:•|-|\d+\.)\s*([^\n]+)',
                results_text
            )
            
            findings = [b.strip() for b in bullets[:5]]
        
        # If no structured findings, extract sentences with key words
        if not findings:
            sentences = re.split(r'[.!?]\s+', text)
            findings = [
                s.strip() for s in sentences 
                if any(word in s.lower() for word in ['found', 'showed', 'demonstrated', 'observed'])
            ][:5]
        
        return findings
    
    def _extract_methods(self, text: str) -> List[str]:
        """Extract methodology"""
        methods = []
        
        # Look for methods section
        methods_match = re.search(
            r'(?:methods|materials|methodology)[\s\n]*(.{300,2000}?)(?:\n\n|results|discussion)',
            text,
            re.IGNORECASE | re.DOTALL
        )
        
        if methods_match:
            methods_text = methods_match.group(1)
            
            # Extract key methodological details
            details = re.findall(
                r'(?:used|performed|conducted|applied)\s+([^.\n]+)',
                methods_text
            )
            
            methods = [d.strip() for d in details[:5]]
        
        return methods
    
    def _extract_limitations(self, text: str) -> List[str]:
        """Extract limitations"""
        limitations = []
        
        # Look for limitations section
        limitations_match = re.search(
            r'(?:limitations|weaknesses)[\s\n]*(.{100,1000}?)(?:\n\n|conclusion|references)',
            text,
            re.IGNORECASE | re.DOTALL
        )
        
        if limitations_match:
            limitations_text = limitations_match.group(1)
            
            # Extract bullet points
            bullets = re.findall(
                r'(?:^|\n)\s*(?:•|-|\d+\.)\s*([^\n]+)',
                limitations_text
            )
            
            limitations = [b.strip() for b in bullets[:5]]
        
        return limitations
    
    def _extract_authors(self, text: str) -> List[str]:
        """Extract author names"""
        # Usually at the beginning of the paper
        # This is a simplified extraction
        authors = []
        
        # Look for author line
        author_match = re.search(
            r'([A-Z][a-z]+\s+[A-Z][a-z]+(?:\s*,\s*[A-Z][a-z]+\s+[A-Z][a-z]+)*)',
            text[:500]
        )
        
        if author_match:
            author_text = author_match.group(1)
            authors = [a.strip() for a in author_text.split(',')]
        
        return authors
    
    def _count_citations(self, text: str) -> int:
        """Count references/citations"""
        # Look for reference section
        ref_match = re.search(
            r'references[\s\n]*(.{100,})',
            text,
            re.IGNORECASE | re.DOTALL
        )
        
        if ref_match:
            ref_text = ref_match.group(1)
            # Count numbered references or bracketed citations
            refs = re.findall(r'\[\d+\]|\d+\.', ref_text)
            return len(refs)
        
        return 0
    
    def format_summary(self, summary: PaperSummary) -> str:
        """Format summary as markdown"""
        output = f"""# {summary.title}

## Authors
{', '.join(summary.authors) if summary.authors else 'Unknown'}

## Abstract
{summary.abstract}

## Key Findings
"""
        
        if summary.key_findings:
            for i, finding in enumerate(summary.key_findings, 1):
                output += f"{i}. {finding}\n"
        else:
            output += "_No specific findings extracted_\n"
        
        if summary.methods:
            output += "\n## Methods\n"
            for method in summary.methods:
                output += f"- {method}\n"
        
        if summary.limitations:
            output += "\n## Limitations\n"
            for limitation in summary.limitations:
                output += f"- {limitation}\n"
        
        output += f"\n## Citations\n_{summary.citations} references_"
        
        return output


class KeyExtractor:
    """
    Key Information Extractor
    
    Extract specific information from literature
    """
    
    @staticmethod
    def extract_drug_names(text: str) -> List[str]:
        """Extract drug names mentioned in text"""
        # Common drug name patterns
        drug_patterns = [
            r'\b(Aspirin|Warfarin|Metformin|Lisinopril|Atorvastatin)\b',
            r'\b(Ibuprofen|Naproxen|Acetaminophen|Omeprazole)\b',
            r'\b(Amoxicillin|Ciprofloxacin|Azithromycin)\b',
            r'\b(Sertraline|Fluoxetine|Escitalopram)\b',
            r'\b(Losartan|Amlodipine|Metoprolol)\b'
        ]
        
        drugs = set()
        for pattern in drug_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            drugs.update(matches)
        
        return list(drugs)
    
    @staticmethod
    def extract_conditions(text: str) -> List[str]:
        """Extract medical conditions"""
        conditions = []
        
        condition_patterns = [
            r'\b(diabetes|diabetic)\b',
            r'\b(hypertension|high blood pressure)\b',
            r'\b(depression|anxiety)\b',
            r'\b(cancer|tumor|carcinoma)\b',
            r'\b(infection|viral|bacterial)\b',
            r'\b(inflammation|inflammatory)\b'
        ]
        
        for pattern in condition_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            conditions.extend(matches)
        
        return list(set(conditions))
    
    @staticmethod
    def extract_statistics(text: str) -> Dict[str, str]:
        """Extract statistical results"""
        stats = {}
        
        # P-values
        p_values = re.findall(r'p\s*[<>=]\s*(\d+\.?\d*)', text, re.IGNORECASE)
        if p_values:
            stats['p_values'] = p_values
        
        # Confidence intervals
        ci_match = re.findall(r'(\d+\.?\d*%\s*CI[\s:]+[\[\(]\s*\d+\.?\d*[\s,\d]+\.?\d*[\]\)])', text)
        if ci_match:
            stats['confidence_intervals'] = ci_match
        
        # Sample sizes
        sample_match = re.findall(r'(n\s*[=:]\s*\d+|sample\s*size\s*[:=]\s*\d+)', text, re.IGNORECASE)
        if sample_match:
            stats['sample_sizes'] = sample_match
        
        return stats


# ============== Main ==============

if __name__ == "__main__":
    # Test with sample text
    sample_paper = """
    Abstract
    This study investigates the efficacy of metformin in treating type 2 diabetes 
    mellitus. We conducted a randomized controlled trial with 500 participants.
    
    Results
    The treatment group showed significant improvement in glycemic control.
    • Mean HbA1c reduction: 1.2%
    • Weight loss: 3.5 kg average
    • No severe adverse events were observed.
    
    Methods
    We used a double-blind placebo-controlled design. Participants received 
    either metformin 500mg twice daily or placebo for 24 weeks.
    
    Limitations
    • Single center study
    • Short follow-up period
    • Predominantly Caucasian participants
    """
    
    summarizer = LiteratureSummarizer()
    summary = summarizer.summarize(sample_paper, "Metformin Efficacy Study")
    
    print(summarizer.format_summary(summary))
