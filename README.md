
# 🧠 StylistExpert Backend

This is the backend for **StylistExpert** 
A robust, rule-based expert system for fashion recommendations, built with FastAPI and Python.

---

## 🚩 Features

- **Intelligent Recommendations:** Rule-based expert system with forward chaining inference
- **Comprehensive API:** Accepts detailed user profiles, returns tailored advice
- **Test Suite:** Pytest-based tests for rules and API endpoints

---

## 🛠️ Tech Stack

- **FastAPI** (API framework)
- **Python 3.10+**
- **Pydantic** (data validation)
- **Pytest** (testing)

---

## 🚀 Getting Started

1. **Navigate to the backend directory:**
   ```bash
   cd backend
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Start the FastAPI server:**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

   The API will be available at [http://localhost:8000](http://localhost:8000)
   - Interactive docs: `/docs`
   - Alternative docs: `/redoc`

---

## 🧪 Running Tests

```bash
python -m pytest test_engine.py -v
```

---

## 📡 API Usage

### POST `/api/recommend`

Get personalized fashion recommendations.

**Request Example:**
```json
{
  "gender": "female",
  "occasion": "formal",
  "weather": "mild",
  "body_type": "athletic",
  "preferred_style": "classic",
  "color_preference": "neutral",
  "height": "average"
}
```

**Response Example:**
```json
{
  "recommendations": [
    {
      "title": "Elegant Sheath Dress or Blazer Suit",
      "items": ["Sheath dress or tailored blazer and trousers", "Heels or loafers", "Delicate jewelry"],
      "explanation": "A structured dress or blazer suit projects confidence and works well for formal settings.",
      "images": ["https://source.unsplash.com/800x600/?women,formal,dress"],
      "confidence": 0.95,
      "matched_rules": ["R2"]
    }
  ]
}
```

---

## 🧠 Knowledge Base

- **12+ rules** for various fashion scenarios:
  - Formal, casual, special events, athletic, body type, weather, style preferences

---

## 🏗️ Architecture

- **Rules Engine:** Forward chaining, confidence scoring, rule merging, fallback system
- **API:** FastAPI endpoints for recommendations

---

## 📁 Project Structure

```
backend/
├── main.py         # FastAPI app & rules engine
├── test_engine.py  # Test suite
└── requirements.txt
```

---

## 🚧 Limitations & Future Work

- Static rule base (no ML adaptation)
- Limited cultural/regional diversity
- Basic image sourcing from Unsplash
- No real-time trend integration

**Planned:**
- Machine learning integration
- Computer vision outfit analysis
- Social/sharing features
- Shopping integration
- Personalization engine
- AR/VR try-on

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](../LICENSE) file for details.

---

> Built with ❤️ for fashion lovers everywhere.
