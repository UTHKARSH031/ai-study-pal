"""
AI Study Pal - Flask Web Application
Main application file integrating all components
"""

from flask import Flask, render_template, request, jsonify, send_file, session
import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.data_processor import DataProcessor
from src.ml_quiz import QuizGenerator
from src.dl_summarizer import Summarizer
from src.nlp_tips import StudyTipsGenerator
from src.study_planner import StudyPlanner
from src.utils import get_sample_questions, get_sample_educational_topics

app = Flask(__name__)
app.secret_key = 'ai-study-pal-secret-key-2024'  # Change in production

# Initialize components
data_processor = DataProcessor()
quiz_generator = QuizGenerator()
summarizer = Summarizer()
tips_generator = StudyTipsGenerator()
study_planner = StudyPlanner()

# Initialize models on startup
def initialize_models():
    """Initialize and train models if needed"""
    print("Initializing AI Study Pal...")
    
    # Collect sample educational texts
    topics = get_sample_educational_topics()
    data_processor.collect_educational_texts(topics)
    
    # Train quiz difficulty classifier
    sample_questions = get_sample_questions()
    if not quiz_generator.load_difficulty_classifier():
        print("Training quiz difficulty classifier...")
        quiz_generator.train_difficulty_classifier(sample_questions)
    
    # Load summarizer
    if not summarizer.load_summarizer():
        print("Initializing summarizer...")
        # For demo, we'll use the simple extractive approach
        # In production, you'd train on actual data
        pass
    
    # Load GloVe embeddings (optional, may take time)
    try:
        summarizer.load_glove_embeddings()
    except:
        print("GloVe embeddings will load on first use")
    
    print("Initialization complete!")

# Initialize on startup
initialize_models()

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/api/generate_plan', methods=['POST'])
def generate_plan():
    """Generate study plan"""
    try:
        data = request.json
        subject = data.get('subject', '').strip()
        study_hours = float(data.get('study_hours', 10))
        scenario = data.get('scenario', 'exam_prep')
        
        if not subject:
            return jsonify({'error': 'Subject is required'}), 400
        
        # Save user input
        data_processor.save_user_input(subject, study_hours, scenario)
        
        # Generate study plan
        plan = study_planner.generate_study_plan(subject, study_hours, scenario)
        
        return jsonify({
            'success': True,
            'plan': plan,
            'summary': study_planner.get_plan_summary(plan)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate_quiz', methods=['POST'])
def generate_quiz():
    """Generate quiz"""
    try:
        data = request.json
        content = data.get('content', '')
        subject = data.get('subject', 'general')
        num_questions = int(data.get('num_questions', 5))
        
        if not content:
            return jsonify({'error': 'Content is required'}), 400
        
        # Generate quiz
        questions = quiz_generator.generate_quiz(content, num_questions)
        
        # Get resource suggestions
        resources = quiz_generator.get_resource_suggestions(content)
        
        return jsonify({
            'success': True,
            'questions': questions,
            'resources': resources
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/summarize', methods=['POST'])
def summarize():
    """Summarize text"""
    try:
        data = request.json
        text = data.get('text', '')
        target_length = int(data.get('target_length', 50))
        
        if not text:
            return jsonify({'error': 'Text is required'}), 400
        
        # Summarize
        summary = summarizer.summarize_text(text, target_length)
        
        return jsonify({
            'success': True,
            'summary': summary,
            'original_length': len(text.split()),
            'summary_length': len(summary.split())
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate_tips', methods=['POST'])
def generate_tips():
    """Generate study tips"""
    try:
        data = request.json
        text = data.get('text', '')
        subject = data.get('subject', 'general')
        
        if not text:
            return jsonify({'error': 'Text is required'}), 400
        
        # Generate tips
        tips = tips_generator.generate_study_tips(text, subject)
        keywords = tips_generator.extract_keywords(text, top_n=5)
        
        return jsonify({
            'success': True,
            'tips': tips,
            'keywords': keywords
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate_feedback', methods=['POST'])
def generate_feedback():
    """Generate motivational feedback"""
    try:
        data = request.json
        performance = data.get('performance', 'good')
        
        feedback = summarizer.generate_feedback(performance)
        
        return jsonify({
            'success': True,
            'feedback': feedback
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/download_schedule', methods=['POST'])
def download_schedule():
    """Download study schedule as CSV"""
    try:
        data = request.json
        plan = data.get('plan')
        
        if not plan:
            return jsonify({'error': 'Plan data is required'}), 400
        
        # Create CSV
        filename = f"study_schedule_{plan.get('subject', 'study')}.csv"
        filepath = study_planner.create_csv_schedule(plan, filename)
        
        return send_file(filepath, as_attachment=True, download_name=filename)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/eda', methods=['GET'])
def get_eda():
    """Get exploratory data analysis results"""
    try:
        eda_results = data_processor.perform_eda()
        chart_path = data_processor.create_subject_pie_chart()
        
        return jsonify({
            'success': True,
            'eda': eda_results,
            'chart_path': chart_path
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Run app
    app.run(debug=True, host='0.0.0.0', port=5000)

