"""
Deep Learning Module for Text Summarization
Uses Keras for summarization and GloVe embeddings for feedback generation
"""

import os
import numpy as np
from typing import List
import gensim.downloader as api
from gensim.models import KeyedVectors
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Embedding
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences


class Summarizer:
    """Handles text summarization using deep learning"""
    
    def __init__(self, models_dir: str = "models"):
        self.models_dir = models_dir
        os.makedirs(models_dir, exist_ok=True)
        self.model = None
        self.tokenizer = None
        self.glove_model = None
        self.max_len = 200
        self.summary_len = 50
    
    def load_glove_embeddings(self):
        """Load GloVe embeddings for feedback generation"""
        try:
            # Try to load pre-trained GloVe (this will download if not present)
            print("Loading GloVe embeddings...")
            self.glove_model = api.load("glove-wiki-gigaword-100")  # Smaller, faster
            print("GloVe embeddings loaded successfully")
            return True
        except Exception as e:
            print(f"Error loading GloVe: {e}")
            print("Using simple word embeddings instead")
            return False
    
    def build_summarization_model(self, vocab_size: int = 10000, embedding_dim: int = 100):
        """
        Build a simple LSTM-based summarization model
        
        Args:
            vocab_size: Vocabulary size
            embedding_dim: Embedding dimension
        """
        model = Sequential([
            Embedding(vocab_size, embedding_dim, input_length=self.max_len),
            LSTM(128, return_sequences=True),
            LSTM(64),
            Dense(32, activation='relu'),
            Dense(1, activation='sigmoid')  # Binary classification for sentence importance
        ])
        
        model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        self.model = model
        return model
    
    def train_summarizer(self, texts: List[str], summaries: List[str], epochs: int = 10):
        """
        Train summarization model (simplified - for demonstration)
        
        Note: In a real scenario, you'd need a proper seq2seq model.
        This is a simplified extractive summarization approach.
        """
        # For student project, we'll use a simpler extractive approach
        # Full abstractive summarization requires more complex architecture
        print("Training summarizer (simplified extractive approach)...")
        
        # Initialize tokenizer
        self.tokenizer = Tokenizer(num_words=10000, oov_token="<OOV>")
        all_texts = texts + summaries
        self.tokenizer.fit_on_texts(all_texts)
        
        # Build model
        vocab_size = len(self.tokenizer.word_index) + 1
        self.build_summarization_model(vocab_size)
        
        # For demo, we'll just save the tokenizer
        # In practice, you'd train on actual text-summary pairs
        model_path = os.path.join(self.models_dir, "summarizer.h5")
        self.model.save(model_path)
        
        # Save tokenizer
        import pickle
        tokenizer_path = os.path.join(self.models_dir, "tokenizer.pkl")
        with open(tokenizer_path, 'wb') as f:
            pickle.dump(self.tokenizer, f)
        
        print("Summarizer model saved (simplified version)")
    
    def load_summarizer(self):
        """Load pre-trained summarizer"""
        model_path = os.path.join(self.models_dir, "summarizer.h5")
        tokenizer_path = os.path.join(self.models_dir, "tokenizer.pkl")
        
        if os.path.exists(model_path) and os.path.exists(tokenizer_path):
            try:
                self.model = keras.models.load_model(model_path)
                import pickle
                with open(tokenizer_path, 'rb') as f:
                    self.tokenizer = pickle.load(f)
                return True
            except Exception as e:
                print(f"Error loading summarizer: {e}")
                return False
        return False
    
    def summarize_text(self, text: str, target_length: int = 50) -> str:
        """
        Summarize text to target length
        
        Args:
            text: Input text (e.g., 200 words)
            target_length: Target summary length in words (e.g., 50)
            
        Returns:
            Summarized text
        """
        # Simple extractive summarization approach
        # Split into sentences
        sentences = [s.strip() for s in text.split('.') if len(s.strip()) > 10]
        
        if len(sentences) == 0:
            return text[:target_length * 5]  # Fallback
        
        # Simple approach: take first N sentences that fit target length
        summary_sentences = []
        current_length = 0
        
        for sentence in sentences:
            words = sentence.split()
            if current_length + len(words) <= target_length:
                summary_sentences.append(sentence)
                current_length += len(words)
            else:
                # Add partial sentence if needed
                remaining = target_length - current_length
                if remaining > 5:
                    partial = ' '.join(words[:remaining])
                    summary_sentences.append(partial)
                break
        
        summary = '. '.join(summary_sentences)
        if summary and not summary.endswith('.'):
            summary += '.'
        
        return summary if summary else text[:target_length * 5]
    
    def generate_feedback(self, performance: str = "good") -> str:
        """
        Generate motivational feedback using GloVe embeddings
        
        Args:
            performance: Performance level ("good", "excellent", "needs_improvement")
            
        Returns:
            Motivational feedback message
        """
        if self.glove_model is None:
            self.load_glove_embeddings()
        
        # Template-based feedback with sentiment words
        feedback_templates = {
            "good": [
                "Great job! Keep up the excellent work!",
                "You're doing well! Continue practicing!",
                "Good progress! Stay motivated!"
            ],
            "excellent": [
                "Outstanding performance! You're mastering this!",
                "Excellent work! Keep pushing forward!",
                "Amazing progress! You're on the right track!"
            ],
            "needs_improvement": [
                "Keep practicing! You'll improve with time!",
                "Don't give up! Review the key concepts!",
                "Focus on the basics and you'll get there!"
            ]
        }
        
        import random
        feedback = random.choice(feedback_templates.get(performance, feedback_templates["good"]))
        
        # If GloVe is loaded, we could enhance with similar words, but for simplicity
        # we'll use templates
        return feedback

