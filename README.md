# GATE Flow - 2027 Prediction & Practice

An AI-powered GATE 2027 preparation platform with intelligent question prediction and practice system.

## 🚀 Features

- **Smart Predictions**: AI-powered topic prediction based on 15+ years of GATE patterns
- **Practice Mode**: Cinema-focus interface for distraction-free question solving
- **Trend Analysis**: Deep dive into topic frequency and weightage over the years
- **Progress Tracking**: Track your mastery across all subjects
- **Bookmarks**: Save important questions for revision

## 🛠️ Tech Stack

- **Frontend**: React 18 + TypeScript
- **Styling**: Tailwind CSS + shadcn/ui
- **Build Tool**: Vite
- **Routing**: React Router
- **State**: React Hooks + LocalStorage

## 📦 Installation

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build
```

## 📁 Project Structure

```
focus-flow/
├── src/
│   ├── components/     # UI components
│   ├── pages/          # Route pages
│   ├── hooks/          # Custom React hooks
│   ├── data/           # GATE question data
│   └── lib/            # Utilities
├── public/             # Static assets
└── scripts/            # Python data processing scripts
```

## 🔧 Data Processing Scripts

- `gate_prediction_system.py` - Main prediction algorithm
- `generate_data_js.py` - Converts Q.json to JS format
- `fix_qjson.py` - JSON data validation and fixes

## 📊 Data Files

- `Q.json` - Master question database (1625 questions)
- `elite_predictions_2027.json` - AI predictions for GATE 2027
- `validation_report.json` - Data quality report

## 🌐 Deployment

Deployed on Vercel

## 👤 Author

Shreyash

## 📝 License

MIT License
