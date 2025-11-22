# AI Text Assistant

A powerful web-based NLP application that provides grammar correction, spell checking, paraphrasing, text humanization, summarization, and multi-language translation capabilities.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0+-green.svg)
![React](https://img.shields.io/badge/React-18+-61DAFB.svg)
![TypeScript](https://img.shields.io/badge/TypeScript-5+-3178C6.svg)

## ✨ Features

- **📝 Grammar & Spell Correction**: Advanced grammar and spelling correction using TextBlob and LanguageTool
- **🔄 Paraphrasing**: Intelligent text paraphrasing using T5 transformer models
- **🤖 Text Humanization**: Make AI-generated text sound more natural and human-like
- **📚 Summarization**: High-quality text summarization using BART-large-CNN
- **🌐 Translation**: Support for 7 languages (French, Spanish, German, Italian, Russian, Chinese, Hindi)
- **🌓 Dark Mode**: Beautiful dark/light theme toggle
- **📱 Responsive Design**: Works seamlessly on desktop and mobile devices

## 🚀 Tech Stack

### Backend
- **Flask**: Web framework
- **TextBlob**: Spell correction
- **LanguageTool**: Grammar checking
- **Transformers**: NLP models (T5, BART, MarianMT)
- **PyTorch**: Deep learning framework

### Frontend
- **React 18**: UI framework
- **TypeScript**: Type-safe JavaScript
- **Vite**: Build tool
- **TailwindCSS**: Styling
- **TanStack Query**: Data fetching

## 📋 Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- npm or yarn

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd Grammar-and-Spell-Checker-App-using-machine-learning-NLP-main
```

### 2. Backend Setup

```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Frontend Setup

```bash
cd frontend
npm install
npm run build
cd ..
```

## 🎯 Usage

### Development Mode

#### Start Backend Server
```bash
# Make sure virtual environment is activated
source .venv/bin/activate
python3 app.py
```

The backend will run on `http://localhost:5001`

#### Start Frontend Dev Server (Optional)
```bash
cd frontend
npm run dev
```

The frontend dev server will run on `http://localhost:5173`

### Production Mode

```bash
# Build frontend
cd frontend
npm run build
cd ..

# Run backend (serves built frontend)
source .venv/bin/activate
python3 app.py
```

Visit `http://localhost:5001` to use the application.

## 📦 Model Information

The application uses the following pre-trained models:

| Feature | Model | Size | First Download |
|---------|-------|------|----------------|
| Paraphrasing | Vamsi/T5_Paraphrase_Paws | 220MB | ~30s |
| Humanization | Vamsi/T5_Paraphrase_Paws | 220MB | Shared with paraphrase |
| Summarization | facebook/bart-large-cnn | 1.63GB | ~2-3 min |
| Translation | Helsinki-NLP/opus-mt-en-XX | ~300MB each | Per language |

**Note**: Models are downloaded automatically on first use and cached locally.

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory (optional):

```env
# Flask Configuration
PORT=5001
FLASK_DEBUG=True

# LanguageTool Configuration
DISABLE_LOCAL_LT=1
START_LOCAL_LT_BACKGROUND=0
# LT_SERVER_URL=http://localhost:8081  # Optional: Use remote LanguageTool server
```

## 📁 Project Structure

```
.
├── app.py                 # Flask backend application
├── Model.py              # Legacy NLP model class
├── requirements.txt      # Python dependencies
├── .gitignore           # Git ignore rules
├── README.md            # This file
└── frontend/            # React frontend
    ├── src/
    │   ├── components/  # React components
    │   ├── types/       # TypeScript types
    │   ├── App.tsx      # Main app component
    │   └── main.tsx     # Entry point
    ├── dist/            # Built frontend (generated)
    ├── package.json     # Node dependencies
    └── vite.config.ts   # Vite configuration
```

## 🌍 Supported Languages for Translation

- 🇫🇷 French
- 🇪🇸 Spanish
- 🇩🇪 German
- 🇮🇹 Italian
- 🇷🇺 Russian
- 🇨🇳 Chinese
- 🇮🇳 Hindi

## 🎨 Features in Detail

### Grammar & Spell Correction
- Detects and corrects spelling mistakes
- Identifies grammatical errors
- Provides both spell-corrected and grammar-corrected versions

### Paraphrasing
- Rewrites text while preserving meaning
- Uses advanced T5 transformer model
- Generates natural-sounding alternatives

### Text Humanization
- Makes AI-generated text sound more natural
- Adds contractions and conversational tone
- Generates multiple variations and selects the best

### Summarization
- Extracts key points from long text
- Adjusts summary length based on input
- Ensures complete sentences

### Translation
- Supports 7 major languages
- Uses state-of-the-art MarianMT models
- Maintains context and meaning

## 🐛 Troubleshooting

### Models not downloading
- Check your internet connection
- Ensure you have enough disk space (~3GB for all models)
- Check firewall settings

### LanguageTool errors
- LanguageTool is disabled by default (`DISABLE_LOCAL_LT=1`)
- To enable, set `DISABLE_LOCAL_LT=0` in `.env`
- Or use a remote LanguageTool server

### Frontend not loading
- Make sure you've run `npm run build` in the frontend directory
- Check that `frontend/dist` directory exists
- Clear browser cache

## 📝 API Endpoints

### Health Check
```
GET /health
```

### Grammar & Spell Correction
```
POST /api/correct
Content-Type: application/json

{
  "text": "Your text here"
}
```

### Paraphrase
```
POST /api/paraphrase
Content-Type: application/json

{
  "text": "Your text here"
}
```

### Humanize
```
POST /api/humanize
Content-Type: application/json

{
  "text": "Your text here"
}
```

### Summarize
```
POST /api/summarize
Content-Type: application/json

{
  "text": "Your text here"
}
```

### Translate
```
POST /api/translate
Content-Type: application/json

{
  "text": "Your text here",
  "target_lang": "French"
}
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- [Hugging Face Transformers](https://huggingface.co/transformers/) for NLP models
- [LanguageTool](https://languagetool.org/) for grammar checking
- [TextBlob](https://textblob.readthedocs.io/) for spell correction
- [React](https://react.dev/) for the frontend framework

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

---

Made with ❤️ using Flask, React, and Transformers
