
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import json
from pathlib import Path
import os
from dotenv import load_dotenv


load_dotenv()

app = FastAPI(
    title="StylistExpert API",
    description="A rule-based expert system for fashion style advice",
    version="1.0.0"
)

# Enable CORS for frontend
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",")
allowed_origins = [origin.strip() for origin in allowed_origins if origin.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class UserInput(BaseModel):
    gender: str
    age_range: Optional[str] = None
    occasion: str
    weather: str
    body_type: str
    preferred_style: str
    color_preference: Optional[str] = None
    height: Optional[str] = None

class Recommendation(BaseModel):
    title: str
    items: List[str]
    explanation: str
    images: List[str]
    confidence: float
    matched_rules: List[str]

class RecommendationResponse(BaseModel):
    recommendations: List[Recommendation]

# Knowledge Base - The exact rules from requirements
KNOWLEDGE_BASE = {
    "rules": [
        {
            "id": "R1",
            "conditions": {"occasion": "formal", "gender": "male"},
            "recommendation": {
                "title": "Navy Two Piece Suit",
                "items": ["Navy tailored suit", "White dress shirt", "Silk tie", "Oxford shoes", "Leather belt"],
                "explanation": "Classic tailored silhouette for formal occasions. Navy is versatile and flattering for most body types."
            },
            "confidence": 0.95,
            "images": ["https://source.unsplash.com/800x600/?mens,suit,navy"]
        },
        {
            "id": "R2",
            "conditions": {"occasion": "formal", "gender": "female"},
            "recommendation": {
                "title": "Elegant Sheath Dress or Blazer Suit",
                "items": ["Sheath dress or tailored blazer and trousers", "Heels or loafers", "Delicate jewelry"],
                "explanation": "A structured dress or blazer suit projects confidence and works well for formal settings."
            },
            "confidence": 0.95,
            "images": ["https://source.unsplash.com/800x600/?women,formal,dress"]
        },
        {
            "id": "R3",
            "conditions": {"occasion": "casual", "weather": "hot"},
            "recommendation": {
                "title": "Light Casual Chic",
                "items": ["Breathable T-shirt or linen shirt", "Lightweight chinos or denim shorts", "Loafers or sandals", "Sunglasses"],
                "explanation": "Breathable fabrics keep you cool while maintaining a stylish, effortless look."
            },
            "confidence": 0.9,
            "images": ["https://source.unsplash.com/800x600/?casual,outfit,summer"]
        },
        {
            "id": "R4",
            "conditions": {"occasion": "casual", "weather": "cold"},
            "recommendation": {
                "title": "Layered Casual Warmth",
                "items": ["Knitted sweater or hoodie", "Dark denim or tapered trousers", "Boots", "Scarf"],
                "explanation": "Layering provides warmth and texture which elevates casual outfits."
            },
            "confidence": 0.9,
            "images": ["https://source.unsplash.com/800x600/?sweater,outfit,winter"]
        },
        {
            "id": "R5",
            "conditions": {"occasion": "party", "preferred_style": "flashy"},
            "recommendation": {
                "title": "Showstopper Party Look",
                "items": ["Statement dress or blazer with sheen", "Bold jewellery", "Heels or stylish boots"],
                "explanation": "High impact materials and accessories create a memorable party look."
            },
            "confidence": 0.92,
            "images": ["https://source.unsplash.com/800x600/?party,outfit,glam"]
        },
        {
            "id": "R6",
            "conditions": {"occasion": "sports"},
            "recommendation": {
                "title": "Performance Sportswear",
                "items": ["Moisture wicking top", "Athletic shorts or leggings", "Performance trainers"],
                "explanation": "Function first, but choose sporty silhouettes and color pops to look intentional."
            },
            "confidence": 0.98,
            "images": ["https://source.unsplash.com/800x600/?sportswear,athlete"]
        },
        {
            "id": "R7",
            "conditions": {"body_type": "plus-size", "preferred_style": "modern"},
            "recommendation": {
                "title": "Structured Modern Silhouette",
                "items": ["Longline blazer", "High waisted trousers", "Pointed flats or low heels"],
                "explanation": "Long lines and defined waist create a balanced silhouette while remaining comfortable."
            },
            "confidence": 0.88,
            "images": ["https://source.unsplash.com/800x600/?plus-size,stylish,outfit"]
        },
        {
            "id": "R8",
            "conditions": {"body_type": "slim", "preferred_style": "fitted"},
            "recommendation": {
                "title": "Fitted and Tailored",
                "items": ["Slim fit shirt", "Tapered trousers", "Low profile sneakers"],
                "explanation": "Fitted shapes emphasize your proportions and create a sleek modern look."
            },
            "confidence": 0.85,
            "images": ["https://source.unsplash.com/800x600/?slim,men,outfit"]
        },
        {
            "id": "R9",
            "conditions": {"weather": "rainy"},
            "recommendation": {
                "title": "Smart Rain Ready",
                "items": ["Waterproof coat or trench", "Ankle boots", "Umbrella", "Quick dry fabrics"],
                "explanation": "Waterproof outerwear keeps the look polished and practical in wet conditions."
            },
            "confidence": 0.9,
            "images": ["https://source.unsplash.com/800x600/?raincoat,outfit"]
        },
        {
            "id": "R10",
            "conditions": {"occasion": "wedding", "preferred_style": "traditional"},
            "recommendation": {
                "title": "Heritage Formal",
                "items": ["Traditional attire or ceremonial dress", "Classic accessories", "Polished shoes"],
                "explanation": "Traditional pieces are respectful and often best for weddings that expect cultural attire."
            },
            "confidence": 0.93,
            "images": ["https://source.unsplash.com/800x600/?wedding,traditional,attire"]
        },
        {
            "id": "R11",
            "conditions": {"height": "short", "body_type": "pear"},
            "recommendation": {
                "title": "Proportional Balance",
                "items": ["High waist bottoms", "V neck tops", "Minimal chunky shoes"],
                "explanation": "High waisted bottoms and V necks elongate the torso and balance proportions."
            },
            "confidence": 0.82,
            "images": ["https://source.unsplash.com/800x600/?fashion,proportions"]
        },
        {
            "id": "R12",
            "conditions": {"color_preference": "dark", "preferred_style": "minimalist"},
            "recommendation": {
                "title": "Minimalist Dark Palette",
                "items": ["Monochrome top and bottom", "Textured layers", "Clean sneakers or loafers"],
                "explanation": "Monochrome palettes with textural contrast achieve a minimalist but rich outfit."
            },
            "confidence": 0.8,
            "images": ["https://source.unsplash.com/800x600/?minimalist,outfit,black"]
        }
    ]
}

class FashionExpertSystem:
    def __init__(self):
        self.rules = KNOWLEDGE_BASE["rules"]
    
    def matches_condition(self, rule_conditions: Dict, user_input: Dict) -> bool:
        """Check if user input matches all rule conditions"""
        print(f"Checking rule conditions: {rule_conditions}")
        print(f"Against user input: {user_input}")
        for key, expected_value in rule_conditions.items():
            user_value = user_input.get(key)
            print(f"  {key}: expected='{expected_value}', user='{user_value}'")
            if user_value is None or user_value != expected_value:
                print(f"  -> No match for {key}")
                return False
        print(f"  -> All conditions matched!")
        return True
    
    def calculate_match_bonus(self, rule_conditions: Dict, user_input: Dict) -> float:
        """Calculate bonus based on number of matching conditions"""
        matches = sum(1 for key, value in rule_conditions.items() 
                     if key in user_input and user_input[key] == value)
        total_conditions = len(rule_conditions)
        return (matches / total_conditions) * 0.1  # Up to 10% bonus
    
    def forward_chain(self, user_input: UserInput) -> List[Recommendation]:
        """Forward chaining inference engine"""
        user_dict = user_input.model_dump()
        # Remove None values for cleaner matching
        user_dict = {k: v for k, v in user_dict.items() if v is not None}
        
        print(f"Processing user input: {user_dict}")
        
        matched_rules = []
        recommendations_map = {}
        
        # Find matching rules
        for rule in self.rules:
            print(f"\nEvaluating rule {rule['id']}")
            if self.matches_condition(rule["conditions"], user_dict):
                print(f"Rule {rule['id']} MATCHED!")
                matched_rules.append(rule)
                
                # Group recommendations by title to merge similar ones
                title = rule["recommendation"]["title"]
                if title not in recommendations_map:
                    recommendations_map[title] = {
                        "rule": rule,
                        "matched_rules": [rule["id"]],
                        "confidence": rule["confidence"],
                        "match_bonus": self.calculate_match_bonus(rule["conditions"], user_dict)
                    }
                else:
                    # Merge with existing recommendation
                    existing = recommendations_map[title]
                    existing["matched_rules"].append(rule["id"])
                    existing["confidence"] = (existing["confidence"] + rule["confidence"]) / 2
                    existing["match_bonus"] += self.calculate_match_bonus(rule["conditions"], user_dict)
            else:
                print(f"Rule {rule['id']} did not match")
        
        print(f"\nTotal matched rules: {len(matched_rules)}")
        print(f"Recommendations map: {list(recommendations_map.keys())}")
        
        # Convert to recommendation objects
        recommendations = []
        for title, data in recommendations_map.items():
            rule = data["rule"]
            final_confidence = min(1.0, data["confidence"] + data["match_bonus"])
            
            recommendations.append(Recommendation(
                title=rule["recommendation"]["title"],
                items=rule["recommendation"]["items"],
                explanation=rule["recommendation"]["explanation"],
                images=rule["images"],
                confidence=round(final_confidence, 2),
                matched_rules=data["matched_rules"]
            ))
        
        # Sort by confidence and return top 3
        recommendations.sort(key=lambda x: x.confidence, reverse=True)
        
        # If no matches, provide fallback recommendation
        if not recommendations:
            recommendations.append(self.get_fallback_recommendation(user_input))
        
        return recommendations[:3]
    
    def get_fallback_recommendation(self, user_input: UserInput) -> Recommendation:
        """Fallback recommendation when no rules match"""
        print("Using fallback recommendation")
        if user_input.gender == "male":
            return Recommendation(
                title="Safe Classic Style",
                items=["Well-fitted jeans or chinos", "Solid color shirt or polo", "Clean sneakers or loafers"],
                explanation="When in doubt, classic basics in neutral colors work for most situations. This safe approach ensures you look put-together.",
                images=["https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=800&h=600&fit=crop&crop=face"],
                confidence=0.7,
                matched_rules=["FALLBACK"]
            )
        else:
            return Recommendation(
                title="Versatile Chic Style",
                items=["Dark jeans or tailored pants", "Blouse or fitted top", "Ballet flats or low heels", "Simple accessories"],
                explanation="A versatile outfit that works across multiple occasions. Classic pieces ensure you're appropriately dressed.",
                images=["https://images.unsplash.com/photo-1494790108755-2616c9c0e8e0?w=800&h=600&fit=crop&crop=face"],
                confidence=0.7,
                matched_rules=["FALLBACK"]
            )

# Initialize expert system
expert_system = FashionExpertSystem()

@app.get("/")
async def root():
    return {"message": "AI Fashion Stylist API", "version": "1.0.0"}

@app.post("/api/recommend", response_model=RecommendationResponse)
async def get_recommendations(user_input: UserInput):
    """Get fashion recommendations based on user preferences"""
    try:
        recommendations = expert_system.forward_chain(user_input)
        return RecommendationResponse(recommendations=recommendations)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating recommendations: {str(e)}")

@app.get("/api/rules")
async def get_rules():
    """Get all available rules for admin purposes"""
    return KNOWLEDGE_BASE