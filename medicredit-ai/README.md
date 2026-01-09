# MediCredit AI - Healthcare Financing Intelligence

**Medical debt destroys lives. MediCredit AI helps patients navigate healthcare costs and helps providers optimize billing.**

[![React](https://img.shields.io/badge/React-18+-blue.svg)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0+-blue.svg)](https://www.typescriptlang.org/)
[![Python](https://img.shields.io/badge/Python-3.11+-green.svg)](https://www.python.org/)
[![Azure](https://img.shields.io/badge/Azure-Cloud-orange.svg)](https://azure.microsoft.com/)

## 🎯 Overview

MediCredit AI is an intelligent healthcare financing platform that:
- **For Patients**: Predicts bills before treatment, finds financial assistance programs, analyzes bills for errors, and warns about financial risk
- **For Providers**: Optimizes billing to reduce claim denials, speeds up reimbursements, and provides revenue analytics

## ✨ Key Features

### Patient Portal
- 💰 **Cost Estimator** - Predict out-of-pocket costs before treatment
- 📄 **Bill Analysis** - Upload and analyze medical bills for errors and overcharges
- 🆘 **Assistance Finder** - Match patients to financial assistance programs
- 📊 **Financial Risk Dashboard** - Understand your financial exposure

### Provider Dashboard
- 🎯 **Denial Risk Scorer** - Predict which claims will be denied before submission
- ✅ **Claim QA Alerts** - Get notified about potential coding issues
- 📈 **Revenue Analytics** - Track denial rates and revenue recovery
- 💡 **Coding Recommendations** - AI-powered suggestions to improve claim approval

## 🛠️ Tech Stack

### Frontend
- **React 18** + **TypeScript** - Modern, type-safe UI
- **Tailwind CSS** - Rapid styling with accessibility-first approach
- **React Hook Form** + **Zod** - Form validation and clean UX
- **Azure Static Web Apps** - Hosting and deployment

### Backend
- **Azure Functions** (Python 3.11) - Serverless API endpoints
- **Azure API Management** - API gateway, rate limiting, versioning
- **Azure Key Vault** - Secure secret management

### AI/ML Services
- **Azure Machine Learning** - Cost prediction (XGBoost) & Denial classification (Random Forest)
- **Azure Form Recognizer** - Extract structured data from medical bills
- **Azure OpenAI** - Patient-friendly bill explanations
- **Azure AI Search** - Match patients to assistance programs

### Data Layer
- **Azure SQL Database** - Structured claims and patient data
- **Azure Blob Storage** - Store bill PDFs and documents
- **Application Insights** - Monitoring and diagnostics

## 📋 Prerequisites

- **Node.js** 18+ and **npm** or **yarn**
- **Python** 3.11+
- **Azure Account** with credits (Imagine Cup provides $5,000)
- **Azure CLI** (for deployment)

## 🚀 Quick Start

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Azure Setup

1. Create Azure Resource Group
2. Deploy infrastructure using `infrastructure/` templates
3. Configure environment variables in `.env` files

## 📁 Project Structure

```
medicredit-ai/
├── frontend/                 # React + TypeScript frontend
│   ├── src/
│   │   ├── components/      # Reusable UI components
│   │   ├── pages/           # Patient Portal & Provider Dashboard
│   │   ├── services/        # API client services
│   │   └── utils/           # Utility functions
│   └── package.json
│
├── backend/                  # Azure Functions (Python)
│   ├── functions/           # Individual function apps
│   │   ├── estimate_cost/
│   │   ├── predict_denial/
│   │   ├── analyze_bill/
│   │   ├── find_assistance/
│   │   └── explain_bill/
│   ├── shared/              # Shared utilities
│   └── requirements.txt
│
├── ml-models/               # ML model training scripts
│   ├── cost_predictor/
│   ├── denial_classifier/
│   └── data/               # Synthetic training data
│
├── infrastructure/          # Azure infrastructure as code
│   ├── bicep/              # Bicep templates
│   └── scripts/            # Deployment scripts
│
└── docs/                    # Documentation
```

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/estimate-cost` | Predict patient out-of-pocket costs |
| `POST` | `/api/predict-denial` | Score claim denial risk |
| `POST` | `/api/analyze-bill` | Analyze uploaded bill for errors |
| `POST` | `/api/find-assistance` | Match patient to assistance programs |
| `POST` | `/api/explain-bill` | Generate patient-friendly bill explanation |

## 🎯 MVP Scope (8-12 weeks)

### Phase 1: Foundations (Weeks 1-2)
- ✅ Azure resource group setup
- ✅ React frontend scaffold
- ✅ Azure SQL schema
- ✅ Synthetic data generation

### Phase 2: Patient Core (Weeks 3-5)
- ✅ Cost estimator (rule-based)
- ✅ Bill upload + Form Recognizer
- ✅ Anomaly detection
- ✅ Financial risk classifier

### Phase 3: Provider Core (Weeks 6-8)
- ✅ Train denial prediction model
- ✅ Deploy Azure ML endpoint
- ✅ Provider dashboard
- ✅ Risk scoring API

### Phase 4: Polish & Demo (Weeks 9-12)
- ✅ Azure OpenAI integration
- ✅ Accessibility (WCAG 2.1 AA)
- ✅ Demo video preparation
- ✅ Pitch deck

## 📊 Expected Performance

- **Denial Prediction Accuracy**: 92% (Random Forest)
- **False Positive Rate**: < 5%
- **Cost Estimation Error**: ±15% (within confidence interval)
- **Bill Analysis Savings**: $5K-$40K per patient

## 💰 Cost Estimate

- **Development**: ~$250 over 12 weeks
- **Azure Credits**: $5,000 provided (well within budget)
- **Free Tier Services**: Most services use free tier for MVP

## 🤝 Contributing

This project is built for Microsoft Imagine Cup 2026. Contributions welcome!

## 📄 License

MIT License - See LICENSE file for details

## 🙏 Acknowledgments

- Microsoft Azure for cloud infrastructure
- Imagine Cup 2026 for platform and credits
- Healthcare providers and patients for inspiration

---

**Built with ❤️ for Imagine Cup 2026**

