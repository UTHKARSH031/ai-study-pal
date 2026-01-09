"""
Machine Learning Module for Quiz Generation
Uses Logistic Regression for difficulty classification and K-means for topic clustering
"""

import os
import pickle
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score
from typing import List, Dict, Tuple
import json


class QuizGenerator:
    """Generates quizzes using ML models"""
    
    def __init__(self, models_dir: str = "models"):
        self.models_dir = models_dir
        os.makedirs(models_dir, exist_ok=True)
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        self.difficulty_classifier = None
        self.topic_clusters = None
        self.resource_map = {}
        
    def prepare_question_dataset(self, questions: List[Dict]) -> Tuple[np.ndarray, np.ndarray]:
        """
        Prepare dataset for difficulty classification
        
        Args:
            questions: List of dicts with 'text' and 'difficulty' keys
            
        Returns:
            X (features), y (labels)
        """
        texts = [q['text'] for q in questions]
        labels = [1 if q['difficulty'] == 'medium' else 0 for q in questions]  # 0=easy, 1=medium
        
        X = self.vectorizer.fit_transform(texts).toarray()
        y = np.array(labels)
        
        return X, y
    
    def train_difficulty_classifier(self, questions: List[Dict], test_size: float = 0.2):
        """
        Train logistic regression model for question difficulty classification
        
        Args:
            questions: List of question dicts with 'text' and 'difficulty'
            test_size: Proportion of data for testing
        """
        X, y = self.prepare_question_dataset(questions)
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42
        )
        
        # Train logistic regression
        self.difficulty_classifier = LogisticRegression(
            max_iter=1000,
            random_state=42,
            C=1.0  # Regularization parameter
        )
        self.difficulty_classifier.fit(X_train, y_train)
        
        # Evaluate
        y_pred = self.difficulty_classifier.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        
        # Save model
        model_path = os.path.join(self.models_dir, "quiz_classifier.pkl")
        with open(model_path, 'wb') as f:
            pickle.dump({
                'classifier': self.difficulty_classifier,
                'vectorizer': self.vectorizer
            }, f)
        
        return {'accuracy': accuracy, 'f1_score': f1}
    
    def load_difficulty_classifier(self):
        """Load pre-trained difficulty classifier"""
        model_path = os.path.join(self.models_dir, "quiz_classifier.pkl")
        if os.path.exists(model_path):
            with open(model_path, 'rb') as f:
                data = pickle.load(f)
                self.difficulty_classifier = data['classifier']
                self.vectorizer = data['vectorizer']
            return True
        return False
    
    def classify_difficulty(self, question_text: str) -> str:
        """
        Classify question difficulty
        
        Args:
            question_text: Question text
            
        Returns:
            'easy' or 'medium'
        """
        if self.difficulty_classifier is None:
            if not self.load_difficulty_classifier():
                return 'easy'  # Default
        
        X = self.vectorizer.transform([question_text]).toarray()
        prediction = self.difficulty_classifier.predict(X)[0]
        return 'medium' if prediction == 1 else 'easy'
    
    def cluster_topics(self, texts: List[str], n_clusters: int = 5):
        """
        Cluster topics using K-means for resource suggestions
        
        Args:
            texts: List of text documents
            n_clusters: Number of clusters
        """
        if len(texts) < n_clusters:
            n_clusters = max(1, len(texts) // 2)
        
        # Vectorize texts
        X = self.vectorizer.fit_transform(texts).toarray()
        
        # Apply K-means
        self.topic_clusters = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        cluster_labels = self.topic_clusters.fit_predict(X)
        
        # Save model
        model_path = os.path.join(self.models_dir, "topic_clusters.pkl")
        with open(model_path, 'wb') as f:
            pickle.dump({
                'kmeans': self.topic_clusters,
                'vectorizer': self.vectorizer,
                'cluster_labels': cluster_labels
            }, f)
        
        return cluster_labels
    
    def load_topic_clusters(self):
        """Load pre-trained topic clusters"""
        model_path = os.path.join(self.models_dir, "topic_clusters.pkl")
        if os.path.exists(model_path):
            with open(model_path, 'rb') as f:
                data = pickle.load(f)
                self.topic_clusters = data['kmeans']
                self.vectorizer = data['vectorizer']
            return True
        return False
    
    def get_resource_suggestions(self, text: str, n_resources: int = 3) -> List[str]:
        """
        Get resource suggestions based on topic clustering
        
        Args:
            text: Input text
            n_resources: Number of resources to return
            
        Returns:
            List of resource URLs/links
        """
        if self.topic_clusters is None:
            if not self.load_topic_clusters():
                return self._default_resources()
        
        # Predict cluster for the text
        X = self.vectorizer.transform([text]).toarray()
        cluster_id = self.topic_clusters.predict(X)[0]
        
        # Map cluster to resources (pre-defined mapping)
        if not self.resource_map:
            self.resource_map = {
                0: ["https://www.khanacademy.org", "https://www.coursera.org"],
                1: ["https://www.edx.org", "https://www.udemy.com"],
                2: ["https://www.youtube.com/education", "https://www.ted.com"],
                3: ["https://www.wikipedia.org", "https://www.britannica.com"],
                4: ["https://www.study.com", "https://www.quizlet.com"]
            }
        
        cluster_resources = self.resource_map.get(cluster_id, self._default_resources())
        return cluster_resources[:n_resources]
    
    def _default_resources(self) -> List[str]:
        """Default resource suggestions"""
        return [
            "https://www.khanacademy.org",
            "https://www.coursera.org",
            "https://www.edx.org"
        ]
    
    def generate_quiz(self, content: str, num_questions: int = 5) -> List[Dict]:
        """
        Generate quiz questions from content
        
        Args:
            content: Educational content text
            num_questions: Number of questions to generate
            
        Returns:
            List of question dicts
        """
        # Simple template-based question generation
        sentences = [s.strip() for s in content.split('.') if len(s.strip()) > 20]
        questions = []
        
        for i, sentence in enumerate(sentences[:num_questions]):
            # Extract key terms (simple approach)
            words = sentence.split()
            key_term = words[0] if len(words) > 0 else "concept"
            
            # Generate question
            question_text = f"What is {key_term}?"
            
            # Classify difficulty
            difficulty = self.classify_difficulty(question_text)
            
            # Generate options (simple template)
            correct_answer = sentence[:50] + "..."
            options = [
                correct_answer,
                f"Option B about {key_term}",
                f"Option C related to {key_term}",
                f"Option D for {key_term}"
            ]
            
            questions.append({
                'id': i + 1,
                'question': question_text,
                'options': options,
                'correct_answer': 0,
                'difficulty': difficulty
            })
        
        return questions

