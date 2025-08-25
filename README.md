# AI Fashion Stylist Backend

A robust rule-based expert system backend for fashion style advice, built with FastAPI and Python.

## Features

- **Intelligent Style Recommendations**: Rule-based expert system with forward chaining inference
- **Comprehensive API**: Accepts detailed user profiles and returns personalized recommendations
- **Test Suite**: Pytest-based tests for rules and API endpoints

## Tech Stack
- **FastAPI** - Modern, fast web framework for building APIs
- **Python 3.10+** - Core language
- **Pydantic** - Data validation using Python type annotations
- **Pytest** - Testing framework

## Setup Instructions

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the FastAPI server:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

The API will be available at `http://localhost:8000`
- Interactive API docs: `http://localhost:8000/docs`
- Alternative docs: `http://localhost:8000/redoc`

## Running Tests

Run backend tests with:
```bash
python -m pytest test_engine.py -v
```

## API Usage

### POST /api/recommend

Get personalized fashion recommendations based on user preferences.

**Request Body:**
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

**Response:**
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

### Sample cURL Request

```bash
curl -X POST "http://localhost:8000/api/recommend" \
  -H "Content-Type: application/json" \
  -d '{
    "gender": "male",
    "occasion": "casual", 
    "weather": "hot",
    "body_type": "slim",
    "preferred_style": "modern"
  }'
```

## Knowledge Base

The system uses 12 carefully crafted rules covering various fashion scenarios:

- **Formal occasions** - Professional suits and elegant dresses
- **Casual wear** - Weather-appropriate comfort styles  
- **Special events** - Party, wedding, and date night looks
- **Athletic wear** - Performance and sports styling
- **Body type considerations** - Flattering silhouettes for different shapes
- **Weather adaptations** - Hot, cold, and rainy weather styling
- **Style preferences** - Modern, classic, minimalist, flashy approaches

## Technical Architecture

- **Rules Engine**: Forward chaining, confidence scoring, rule merging, fallback system
- **API**: FastAPI endpoints for recommendations

## Project Structure

```
backend/
├── main.py         # FastAPI application and rules engine
├── test_engine.py  # Test suite
└── requirements.txt
```

## Limitations and Future Work

- Static rule base (no machine learning adaptation)
- Limited cultural/regional style variations
- Basic image sourcing from Unsplash
- No real-time fashion trend integration

### Future Enhancements
- Machine learning integration
- Advanced computer vision
- Social features
- Shopping integration
- Personalization engine
- AR/VR integration
- Seasonal adaptation

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

Built with ❤️ for fashion lovers everywhere.
