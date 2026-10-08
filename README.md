# AI Text Assistant

A full-stack AI/NLP web application for improving, transforming, and understanding text. It combines a Flask backend with a React + TypeScript frontend and uses pre-trained NLP models for grammar correction, paraphrasing, humanization, summarization, and translation.

## ✨ Features

- **Grammar & Spell Correction** — combines TextBlob and LanguageTool.
- **Paraphrasing** — rewrites text while preserving its meaning with a T5 model.
- **Text Humanization** — produces more natural-sounding versions of text.
- **Summarization** — generates concise summaries with BART.
- **Translation** — supports French, Spanish, German, Italian, Russian, Chinese, and Hindi.
- **Responsive UI** — React interface with dark/light mode support.

## 🏗️ Architecture

```
React + TypeScript + Vite
            │
            │ HTTP / JSON
            ▼
       Flask REST API
            │
     ┌──────┼──────────────┐
     ▼      ▼              ▼
TextBlob  LanguageTool  Transformers
                         │
                 T5 / BART / MarianMT
```

### Tech Stack

**Frontend**
- React 18
- TypeScript
- Vite
- Tailwind CSS
- TanStack Query

**Backend**
- Python
- Flask
- TextBlob
- LanguageTool
- Hugging Face Transformers
- PyTorch

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Node.js 16+
- npm

### 1. Clone the repository

```bash
git clone https://github.com/farhan-islam-2004/Grammar-And-Spell-Checker-Full_Stack_Website.git
cd Grammar-And-Spell-Checker-Full_Stack_Website
```

### 2. Set up the backend

```bash
python3 -m venv .venv
source .venv/bin/activate       # macOS/Linux
# .venv\\Scripts\\activate     # Windows

pip install -r requirements.txt
```

### 3. Set up the frontend

```bash
cd frontend
npm install
npm run build
cd ..
```

### 4. Run the application

Start the Flask backend:

```bash
python3 app.py
```

The backend runs on:

```
http://localhost:5001
```

For frontend development, run the Vite server separately:

```bash
cd frontend
npm run dev
```

The Vite development server runs on:

```
http://localhost:5173
```

## 🔌 API

The backend exposes JSON endpoints for the main text-processing operations.

| Endpoint | Method | Purpose |
|---|---|---|
| `/health` | GET | Health check |
| `/api/correct` | POST | Grammar and spelling correction |
| `/api/paraphrase` | POST | Paraphrasing |
| `/api/humanize` | POST | Text humanization |
| `/api/summarize` | POST | Text summarization |
| `/api/translate` | POST | Translation |

Example request:

```json
{
  "text": "Your text here"
}
```

Translation requests additionally provide a `target_lang` value.

## 🤖 Model Usage

The application downloads Hugging Face models when they are first required and caches them locally.

| Capability | Model |
|---|---|
| Paraphrasing | `Vamsi/T5_Paraphrase_Paws` |
| Humanization | `Vamsi/T5_Paraphrase_Paws` |
| Summarization | `facebook/bart-large-cnn` |
| Translation | Helsinki-NLP MarianMT models |

The first model download can require significant disk space and network bandwidth.

## ⚙️ Configuration

Create a `.env` file in the project root when custom configuration is needed:

```env
PORT=5001
FLASK_DEBUG=True

DISABLE_LOCAL_LT=1
START_LOCAL_LT_BACKGROUND=0
# LT_SERVER_URL=http://localhost:8081
```

By default, local LanguageTool startup is disabled. A remote LanguageTool server can be configured when required.

## 📁 Project Structure

```
.
├── app.py
├── Model.py
├── requirements.txt
├── dev.sh
├── README.md
└── frontend/
    ├── src/
    ├── package.json
    ├── vite.config.ts
    └── ...
```

## 🛠️ Troubleshooting

**Models are not downloading**
- Check your internet connection.
- Make sure sufficient disk space is available.
- Check firewall or proxy restrictions.

**LanguageTool errors**
- Local LanguageTool is disabled by default.
- Set `DISABLE_LOCAL_LT=0` to enable local startup, or configure `LT_SERVER_URL`.

**Frontend changes are not visible**
- Run `npm run build` for the production build.
- Run `npm run dev` while developing the frontend.

## 📄 License

This project is available under the MIT License.

## 🙏 Acknowledgments

- Hugging Face Transformers
- LanguageTool
- TextBlob
- React
- Flask

---

Built with Python, Flask, React, TypeScript, and NLP models.
