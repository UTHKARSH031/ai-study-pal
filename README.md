<div align="center">

# 📚 AI Study Pal

**Your Intelligent Study Assistant - Powered by AI, ML, DL & NLP**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3+-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.13+-orange.svg)](https://www.tensorflow.org/)

*An intelligent web application that helps students create personalized study plans, generate quizzes, summarize content, and get AI-powered study tips.*

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [API](#-api-endpoints) • [Contributing](#-contributing)

</div>

---

## ✨ Features

### 🎯 Core Capabilities

- **📅 Study Plan Generation** - Create personalized study schedules based on subject, available hours, and learning scenario
- **🎯 Quiz Generator** - Generate quizzes from educational content with ML-powered difficulty classification
- **📝 Text Summarization** - Summarize long texts using advanced extractive summarization techniques
- **💡 Study Tips** - Get AI-powered study tips and keyword extraction using NLP
- **💪 Motivational Feedback** - Receive personalized feedback based on your performance level
- **📊 Data Analysis** - Explore study patterns and subject distribution with EDA

### 🎨 Modern UI/UX

- **Dark Theme** - Beautiful gradient-based dark theme with glassmorphism effects
- **Tab Navigation** - Intuitive tab-based interface for easy feature access
- **Responsive Design** - Fully responsive design that works on all devices
- **Smooth Animations** - Polished animations and transitions throughout
- **Real-time Feedback** - Loading states and visual feedback for all operations

---

## 🛠️ Tech Stack

### Backend
- **Framework**: Flask 2.3+
- **Language**: Python 3.8+

### Machine Learning & AI
- **ML**: scikit-learn
- **Deep Learning**: TensorFlow 2.13+
- **NLP**: NLTK, Gensim, RAKE-NLTK

### Data Processing
- **Data**: pandas, numpy
- **Visualization**: matplotlib

### Frontend
- **Markup**: HTML5
- **Styling**: Modern CSS3 with CSS Variables
- **Scripting**: Vanilla JavaScript (ES6+)
- **Fonts**: Inter (Google Fonts)

---

## 📋 Prerequisites

Before you begin, ensure you have met the following requirements:

- **Python** 3.8 or higher
- **pip** (Python package manager)
- **Git** (for cloning the repository)

---

## 🚀 Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/ai-study-pal.git
cd ai-study-pal
```

### Step 2: Create Virtual Environment

**Windows:**
```powershell
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
# Upgrade pip, setuptools, and wheel first (fixes Python 3.13 compatibility)
python -m pip install --upgrade pip setuptools wheel

# Install all dependencies
pip install -r requirements.txt
```

### Step 4: Download NLTK Data

```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')"
```

---

## 🏃 Running the Application

### Start the Server

```bash
# Activate virtual environment (if not already activated)
# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate

# Run the application
python app.py
```

### Access the Application

Open your browser and navigate to:
```
http://localhost:5000
```

You should see the AI Study Pal interface! 🎉

---

## 📖 Usage

### 📅 Generate Study Plan

1. Navigate to the **Study Plan** tab
2. Enter a subject (e.g., "Machine Learning", "Mathematics", "Science")
3. Specify the number of study hours available
4. Select a scenario:
   - **Exam Preparation** - Intensive study schedule
   - **Homework** - Regular homework schedule
   - **General Learning** - Casual learning schedule
5. Click **"Generate Study Plan"**
6. Review your personalized schedule
7. Download as CSV if needed

### 🎯 Generate Quiz

1. Navigate to the **Quiz Generator** tab
2. Paste educational content in the text area
3. Specify the number of questions (1-10)
4. Click **"Generate Quiz"**
5. Review questions with difficulty levels (Easy/Medium/Hard)
6. Check resource suggestions for further learning

### 📝 Summarize Text

1. Navigate to the **Summarize** tab
2. Enter text to summarize (recommended: 200+ words)
3. Click **"Summarize"**
4. View the condensed summary with word count statistics

### 💡 Get Study Tips

1. Navigate to the **Study Tips** tab
2. Enter educational content
3. Optionally specify the subject
4. Click **"Get Study Tips"**
5. Review personalized tips and extracted keywords

### 💪 Get Motivational Feedback

1. Navigate to the **Feedback** tab
2. Select your performance level:
   - **Good** - Positive reinforcement
   - **Excellent** - Celebration and encouragement
   - **Needs Improvement** - Constructive motivation
3. Click **"Get Feedback"**
4. Receive personalized motivational message

---

## 📁 Project Structure

```
ai-study-pal/
├── app.py                    # Main Flask application
├── requirements.txt           # Python dependencies
├── README.md                 # Project documentation
├── LICENSE                   # MIT License
├── .gitignore                # Git ignore rules
│
├── data/                     # Data storage directory
│   └── (generated files)
│
├── models/                   # Trained models directory
│   └── (ML models)
│
├── src/                      # Source code modules
│   ├── __init__.py
│   ├── data_processor.py    # Data processing utilities
│   ├── ml_quiz.py           # Quiz generation with ML
│   ├── dl_summarizer.py     # Deep learning summarization
│   ├── nlp_tips.py          # NLP-based study tips
│   ├── study_planner.py     # Study plan generator
│   └── utils.py             # Utility functions
│
└── templates/                # HTML templates
    └── index.html           # Main web interface (Modern UI)
```

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/generate_plan` | Generate a personalized study plan |
| `POST` | `/api/generate_quiz` | Generate quiz questions from content |
| `POST` | `/api/summarize` | Summarize text content |
| `POST` | `/api/generate_tips` | Generate study tips and keywords |
| `POST` | `/api/generate_feedback` | Get motivational feedback |
| `POST` | `/api/download_schedule` | Download study schedule as CSV |
| `GET` | `/api/eda` | Get exploratory data analysis results |

### Example API Request

```bash
curl -X POST http://localhost:5000/api/generate_plan \
  -H "Content-Type: application/json" \
  -d '{
    "subject": "Machine Learning",
    "study_hours": 20,
    "scenario": "exam_prep"
  }'
```

---

## ⚙️ Configuration

### Secret Key (Production)

For production deployments, change the secret key in `app.py`:

```python
app.secret_key = os.environ.get('SECRET_KEY', 'your-secure-secret-key-here')
```

### Port Configuration

To change the default port, modify `app.py`:

```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Change port number
```

---

## 📦 Dependencies

### Core Dependencies

- **Flask** >= 2.3.2 - Web framework
- **pandas** >= 2.2.0 - Data manipulation
- **numpy** >= 1.26.0 - Numerical computing
- **scikit-learn** >= 1.4.0 - Machine learning
- **TensorFlow** >= 2.15.0 - Deep learning
- **NLTK** >= 3.8.1 - Natural language processing
- **Gensim** >= 4.3.1 - Topic modeling
- **matplotlib** >= 3.8.0 - Data visualization

See `requirements.txt` for the complete list.

---

## 🐛 Troubleshooting

### Virtual Environment Activation Issues (Windows)

If you encounter execution policy errors:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Python 3.13 Compatibility

If you're using Python 3.13, ensure you upgrade setuptools first:

```bash
python -m pip install --upgrade pip setuptools wheel
```

### NLTK Data Not Found

Ensure you've downloaded the required NLTK data:

```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')"
```

### Port Already in Use

If port 5000 is already in use:

1. Find the process using the port:
   ```bash
   # Windows
   netstat -ano | findstr :5000
   
   # macOS/Linux
   lsof -i :5000
   ```

2. Or change the port in `app.py`:
   ```python
   app.run(debug=True, host='0.0.0.0', port=5001)
   ```

### TensorFlow Installation Issues

If TensorFlow fails to install on Python 3.13, consider:
- Using Python 3.12 or 3.11
- Installing TensorFlow CPU version: `pip install tensorflow-cpu`

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Contribution Guidelines

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**N.uthkarsh sai**

- **Institution**: Amrita Vishwa Vidyapeetham

---

## 🙏 Acknowledgments

- Flask community for the excellent framework
- TensorFlow team for deep learning capabilities
- NLTK contributors for NLP tools
- All open-source contributors

---

## ⚠️ Disclaimer

This application is for **educational purposes**. For production use, ensure proper:
- Security measures
- Error handling
- Scalability considerations
- Data privacy compliance

---

<div align="center">


⭐ Star this repo if you find it helpful!

</div>
