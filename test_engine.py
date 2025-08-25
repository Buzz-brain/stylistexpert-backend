import pytest
from fastapi.testclient import TestClient
from main import app, FashionExpertSystem, UserInput

client = TestClient(app)
expert_system = FashionExpertSystem()

class TestFashionExpertSystem:
    
    def test_formal_male_recommendation(self):
        """Test Sample A - Formal male should get Navy Two Piece Suit"""
        user_input = UserInput(
            gender="male",
            occasion="formal",
            weather="mild",
            body_type="athletic",
            preferred_style="classic"
        )
        
        recommendations = expert_system.forward_chain(user_input)
        assert len(recommendations) > 0
        assert recommendations[0].title == "Navy Two Piece Suit"
        assert recommendations[0].confidence >= 0.9
        assert "R1" in recommendations[0].matched_rules
    
    def test_formal_female_recommendation(self):
        """Test formal female should get Elegant Sheath Dress"""
        user_input = UserInput(
            gender="female",
            occasion="formal",
            weather="mild",
            body_type="athletic",
            preferred_style="classic",
            color_preference="neutral"
        )
        
        recommendations = expert_system.forward_chain(user_input)
        assert len(recommendations) > 0
        assert recommendations[0].title == "Elegant Sheath Dress or Blazer Suit"
        assert recommendations[0].confidence >= 0.9
        assert "R2" in recommendations[0].matched_rules
    
    def test_casual_hot_weather_combination(self):
        """Test Sample B - Casual hot weather with slim body type"""
        user_input = UserInput(
            gender="male",
            occasion="casual",
            weather="hot",
            body_type="slim",
            preferred_style="modern"
        )
        
        recommendations = expert_system.forward_chain(user_input)
        assert len(recommendations) > 0
        # Should match R3 (casual + hot) but not R8 (needs fitted style)
        top_recommendation = recommendations[0]
        assert top_recommendation.confidence > 0.8
        assert "R3" in top_recommendation.matched_rules
    
    def test_sports_rainy_combination(self):
        """Test Sample C - Sports in rainy weather"""
        user_input = UserInput(
            gender="female",
            occasion="sports",
            weather="rainy",
            preferred_style="sporty"
        )
        
        recommendations = expert_system.forward_chain(user_input)
        assert len(recommendations) >= 1
        # Should have both sports (R6) and rainy (R9) recommendations
        titles = [r.title for r in recommendations]
        assert "Performance Sportswear" in titles or "Smart Rain Ready" in titles
    
    def test_multiple_rule_matching(self):
        """Test that multiple matching rules are handled correctly"""
        user_input = UserInput(
            gender="male",
            occasion="casual",
            weather="rainy",
            body_type="slim",
            preferred_style="fitted"
        )
        
        recommendations = expert_system.forward_chain(user_input)
        assert len(recommendations) > 0
        # Should find at least rainy weather rule
        rain_found = any("R9" in r.matched_rules for r in recommendations)
        assert rain_found
    
    def test_fallback_recommendation(self):
        """Test fallback when no rules match"""
        user_input = UserInput(
            gender="male",
            occasion="nonexistent",
            weather="alien",
            body_type="robot",
            preferred_style="impossible"
        )
        
        recommendations = expert_system.forward_chain(user_input)
        assert len(recommendations) == 1
        assert recommendations[0].matched_rules == ["FALLBACK"]
        assert "Safe Classic Style" in recommendations[0].title
        assert recommendations[0].confidence == 0.7
    
    def test_plus_size_modern_specific_rule(self):
        """Test specific rule for plus-size modern style"""
        user_input = UserInput(
            gender="female",
            occasion="work",
            weather="mild",
            body_type="plus-size",
            preferred_style="modern"
        )
        
        recommendations = expert_system.forward_chain(user_input)
        assert len(recommendations) > 0
        # Should match R7
        modern_found = any("R7" in r.matched_rules for r in recommendations)
        assert modern_found

class TestAPI:
    
    def test_recommend_endpoint_success(self):
        """Test the API endpoint with valid input"""
        response = client.post("/api/recommend", json={
            "gender": "female",
            "occasion": "formal",
            "weather": "mild",
            "body_type": "athletic",
            "preferred_style": "classic",
            "color_preference": "neutral"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert "recommendations" in data
        assert len(data["recommendations"]) > 0
        assert "title" in data["recommendations"][0]
        assert "confidence" in data["recommendations"][0]
    
    def test_recommend_endpoint_minimal_input(self):
        """Test API with minimal required fields"""
        response = client.post("/api/recommend", json={
            "gender": "male",
            "occasion": "casual",
            "weather": "mild",
            "body_type": "slim",
            "preferred_style": "modern"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert len(data["recommendations"]) >= 1
    
    def test_rules_endpoint(self):
        """Test the rules endpoint"""
        response = client.get("/api/rules")
        assert response.status_code == 200
        data = response.json()
        assert "rules" in data
        assert len(data["rules"]) == 12

if __name__ == "__main__":
    pytest.main([__file__, "-v"])