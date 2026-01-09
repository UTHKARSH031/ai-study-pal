"""
Python & Data Setup Module
Handles data collection, cleaning, and basic EDA with Pandas and Matplotlib
"""

import os
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
from typing import List, Dict
import wikipedia


class DataProcessor:
    """Handles educational text collection and data processing"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
        self.educational_texts_path = os.path.join(data_dir, "educational_texts.csv")
        self.user_inputs_path = os.path.join(data_dir, "user_inputs.csv")
    
    def collect_educational_texts(self, topics: List[str], max_chars: int = 1000) -> pd.DataFrame:
        """
        Collect educational texts from Wikipedia
        
        Args:
            topics: List of topics to collect
            max_chars: Maximum characters per topic
            
        Returns:
            DataFrame with subject and text columns
        """
        texts = []
        for topic in topics:
            try:
                page = wikipedia.page(topic)
                content = page.content[:max_chars]
                texts.append({
                    "subject": topic,
                    "text": content.lower(),  # Lowercase as per requirements
                    "word_count": len(content.split())
                })
            except Exception as e:
                print(f"Error fetching {topic}: {e}")
                # Add placeholder
                texts.append({
                    "subject": topic,
                    "text": f"Sample text about {topic.lower()}.",
                    "word_count": 10
                })
        
        df = pd.DataFrame(texts)
        # Remove duplicates
        df = df.drop_duplicates(subset=['subject'])
        df.to_csv(self.educational_texts_path, index=False)
        return df
    
    def save_user_input(self, subject: str, study_hours: float, scenario: str = "exam_prep"):
        """
        Save user input to CSV
        
        Args:
            subject: Subject name
            study_hours: Number of study hours
            scenario: Study scenario (exam_prep, homework, etc.)
        """
        new_input = {
            "subject": subject.lower(),
            "study_hours": study_hours,
            "scenario": scenario
        }
        
        if os.path.exists(self.user_inputs_path):
            df = pd.read_csv(self.user_inputs_path)
            df = pd.concat([df, pd.DataFrame([new_input])], ignore_index=True)
        else:
            df = pd.DataFrame([new_input])
        
        # Remove duplicates
        df = df.drop_duplicates()
        df.to_csv(self.user_inputs_path, index=False)
        return df
    
    def perform_eda(self) -> Dict:
        """
        Perform Exploratory Data Analysis
        
        Returns:
            Dictionary with EDA results
        """
        results = {}
        
        # Analyze educational texts
        if os.path.exists(self.educational_texts_path):
            df_texts = pd.read_csv(self.educational_texts_path)
            results['num_subjects'] = len(df_texts)
            results['total_words'] = df_texts['word_count'].sum() if 'word_count' in df_texts.columns else 0
            results['subjects'] = df_texts['subject'].tolist()
        
        # Analyze user inputs
        if os.path.exists(self.user_inputs_path):
            df_inputs = pd.read_csv(self.user_inputs_path)
            results['num_user_inputs'] = len(df_inputs)
            results['avg_study_hours'] = df_inputs['study_hours'].mean() if len(df_inputs) > 0 else 0
            results['subject_counts'] = df_inputs['subject'].value_counts().to_dict()
        
        return results
    
    def create_subject_pie_chart(self, save_path: str = "data/subject_distribution.png"):
        """
        Create a pie chart showing subject distribution
        
        Args:
            save_path: Path to save the chart
        """
        if not os.path.exists(self.user_inputs_path):
            return None
        
        df = pd.read_csv(self.user_inputs_path)
        if len(df) == 0:
            return None
        
        subject_counts = df['subject'].value_counts()
        
        plt.figure(figsize=(8, 6))
        plt.pie(subject_counts.values, labels=subject_counts.index, autopct='%1.1f%%')
        plt.title("Subject Distribution in User Inputs")
        plt.tight_layout()
        plt.savefig(save_path)
        plt.close()
        
        return save_path

