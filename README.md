# 🌱 ReUse API – Sustainable Image Analysis

ReUse is an eco-friendly backend application that uses AI-powered image analysis to help users make sustainable decisions about everyday objects. By uploading an image of a used item, the system evaluates its condition and suggests whether it should be reused, repaired, donated, or recycled.

---

## 🚀 Features

* 📷 Image upload and analysis
* 🤖 AI-powered decision making
* 🌍 Sustainability-focused recommendations
* 🔄 RESTful API built with FastAPI
* ⚡ Fast and lightweight backend
* 🔐 Environment-based configuration (API keys)

---

## 🧠 How It Works

1. The user uploads an image of an object
2. The backend processes the image
3. AI analyzes:

   * Object type
   * Condition
   * Best sustainable action
4. The API returns structured recommendations

---

## 📦 Example Response

```json
{
  "objectName": "t-shirt",
  "condition": "worn, torn",
  "decision": "reuse",
  "reason": "Too damaged to wear but can be repurposed.",
  "reuseIdeas": [
    "Cut into cleaning rags",
    "Turn into a reusable bag",
    "Use for craft projects"
  ],
  "recyclingTip": "",
  "confidence": 0.95
}
```

---

## 🛠️ Tech Stack

* **Backend:** FastAPI (Python)
* **Server:** Uvicorn
* **AI Integration:** OpenAI API
* **Environment Management:** python-dotenv
* **Deployment:** Render

---

## 📁 Project Structure

```
reUse-backend/
├── main.py
├── requirements.txt
├── app/
│   ├── __init__.py
│   ├── schemas.py
│   └── ai_service.py
```

---

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/jessicayve/reUse-backend
cd reUse-backend
```

Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file in the root directory:

```env
OPENAI_API_KEY=your_api_key_here
```

---

## ▶️ Running the App

```bash
uvicorn main:app --reload
```

The API will be available at:

```
http://127.0.0.1:8000
```

Docs:

```
http://127.0.0.1:8000/docs
```

---

## 🌐 Deployment

This project is deployed using Render.


👉 [https://reuse-backend.onrender.com](https://re-use-frontend-sable.vercel.app/)

---

## 📌 Future Improvements

* 🌎 Multi-language support (EN/PT)
* 📊 Confidence explanation for decisions
* 🧠 Improved AI prompt engineering
* 📱 Mobile frontend integration (Flutter)

---

## 👩‍💻 Author

Jessica Yve
Full Stack Developer passionate about building meaningful and sustainable tech solutions.

* Portfolio: https://jessicayve.dev
* GitHub: https://github.com/jessicayve

---

## ♻️ Purpose

ReUse was created to promote conscious consumption and reduce waste by helping users make smarter decisions about their items.


