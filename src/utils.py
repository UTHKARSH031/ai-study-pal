"""
Utility functions for AI Study Pal
"""

import os
from typing import List


def ensure_dir(directory: str):
    """Ensure directory exists"""
    os.makedirs(directory, exist_ok=True)


def get_sample_questions() -> List[dict]:
    """Get sample questions for training difficulty classifier"""
    return [
        {"text": "What is the capital of France?", "difficulty": "easy"},
        {"text": "Explain the concept of machine learning.", "difficulty": "medium"},
        {"text": "What is 2 + 2?", "difficulty": "easy"},
        {"text": "Describe the backpropagation algorithm in neural networks.", "difficulty": "medium"},
        {"text": "What is Python?", "difficulty": "easy"},
        {"text": "How does gradient descent optimize neural network parameters?", "difficulty": "medium"},
        {"text": "What is a variable?", "difficulty": "easy"},
        {"text": "Explain the difference between supervised and unsupervised learning.", "difficulty": "medium"},
        {"text": "What is a function?", "difficulty": "easy"},
        {"text": "Describe the architecture of a convolutional neural network.", "difficulty": "medium"},
    ]


def get_sample_educational_topics() -> List[str]:
    """Get sample educational topics for data collection"""
    return [
        "Machine Learning",
        "Python Programming",
        "Neural Networks",
        "Data Science",
        "Artificial Intelligence"
    ]

