"""
NLP Module for Study Tips Generation
Uses NLTK for tokenization and keyword extraction
"""

import nltk
from rake_nltk import Rake
from typing import List, Dict
import re

# Download required NLTK data
try:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
except:
    pass

# Import stopwords after download
try:
    from nltk.corpus import stopwords
    STOPWORDS = set(stopwords.words('english'))
except:
    STOPWORDS = set(['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'])


class StudyTipsGenerator:
    """Generates study tips using NLP techniques"""
    
    def __init__(self):
        self.rake = Rake()
        self.stopwords = STOPWORDS
    
    def tokenize_text(self, text: str) -> List[str]:
        """
        Tokenize text using NLTK
        
        Args:
            text: Input text
            
        Returns:
            List of tokens
        """
        try:
            tokens = nltk.word_tokenize(text.lower())
            # Remove punctuation and short tokens
            tokens = [t for t in tokens if t.isalnum() and len(t) > 2]
            return tokens
        except:
            # Fallback simple tokenization
            return [w.lower() for w in text.split() if w.isalnum() and len(w) > 2]
    
    def extract_keywords(self, text: str, top_n: int = 10) -> List[str]:
        """
        Extract top keywords from text using RAKE algorithm
        
        Args:
            text: Input text
            top_n: Number of top keywords to return
            
        Returns:
            List of keywords
        """
        self.rake.extract_keywords_from_text(text)
        keywords = self.rake.get_ranked_phrases()[:top_n]
        return keywords
    
    def generate_study_tips(self, text: str, subject: str = "general") -> List[str]:
        """
        Generate study tips based on text content
        
        Args:
            text: Educational content
            subject: Subject name
            
        Returns:
            List of study tips
        """
        # Extract keywords
        keywords = self.extract_keywords(text, top_n=5)
        
        # Tokenize for additional processing
        tokens = self.tokenize_text(text)
        
        # Get most frequent terms (excluding stopwords)
        from collections import Counter
        word_freq = Counter([t for t in tokens if t not in self.stopwords])
        top_terms = [word for word, count in word_freq.most_common(5)]
        
        # Generate tips using templates
        tips = []
        
        if keywords:
            tip1 = f"Review key terms daily: {', '.join(keywords[:3])}"
            tips.append(tip1)
        
        if top_terms:
            tip2 = f"Focus on understanding: {', '.join(top_terms[:3])}"
            tips.append(tip2)
        
        # Subject-specific tips
        subject_tips = {
            "math": "Practice problems regularly to reinforce concepts",
            "science": "Create visual diagrams to understand complex processes",
            "programming": "Write code examples for each concept you learn",
            "general": "Break down complex topics into smaller chunks"
        }
        
        subject_lower = subject.lower()
        for key, tip in subject_tips.items():
            if key in subject_lower:
                tips.append(tip)
                break
        else:
            tips.append(subject_tips["general"])
        
        # Additional generic tips
        tips.extend([
            "Take notes while studying to improve retention",
            "Review previous material before starting new topics",
            "Practice active recall by testing yourself regularly"
        ])
        
        return tips[:5]  # Return top 5 tips
    
    def get_key_concepts(self, text: str, n: int = 5) -> List[str]:
        """
        Extract key concepts from text
        
        Args:
            text: Input text
            n: Number of concepts to extract
            
        Returns:
            List of key concepts
        """
        keywords = self.extract_keywords(text, top_n=n)
        return keywords

