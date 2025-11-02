import google.generativeai as genai
import json
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

class WorkoutPlanner:
    def __init__(self):
        self.model = genai.GenerativeModel('models/gemini-2.5-flash')
    
    def generate_personalized_plan(self, member_data, preferences=None):
        """Generate a personalized workout plan based on member's profile and preferences"""
        
        # Extract member information
        member_name = member_data.get('name', 'Member')
        age = member_data.get('age', 25)
        weight = member_data.get('weight', 70)
        height = member_data.get('height', 170)
        
        # Extract preferences (if provided)
        if preferences:
            goal = preferences.get('goal', 'general_fitness')
            experience = preferences.get('experience', 'beginner')
            days = int(preferences.get('days_per_week', 3))
            duration = preferences.get('duration', '45')
            equipment = preferences.get('equipment', 'full_gym')
            health = preferences.get('health_conditions', 'None')
        else:
            # Default preferences for quick plan generation
            goal = 'general_fitness'
            experience = 'beginner'
            days = 3
            duration = '45'
            equipment = 'full_gym'
            health = 'None'
        
        # Calculate BMI for better recommendations
        height_m = height / 100  # Convert cm to meters
        bmi = weight / (height_m * height_m)
        
        # Determine BMI category
        if bmi < 18.5:
            bmi_category = "underweight"
        elif bmi < 25:
            bmi_category = "normal weight"
        elif bmi < 30:
            bmi_category = "overweight"
        else:
            bmi_category = "obese"
        
        # Create personalized prompt
        prompt = f"""Create a personalized {days}-day workout plan for {member_name}.

MEMBER PROFILE:
- Name: {member_name}
- Age: {age} years
- Weight: {weight} kg
- Height: {height} cm
- BMI: {bmi:.1f} ({bmi_category})
- Fitness Goal: {goal}
- Experience Level: {experience}
- Available Equipment: {equipment}
- Health Conditions: {health}
- Session Duration: {duration} minutes

PERSONALIZATION REQUIREMENTS:
- Address the member by name in the plan overview
- Adjust exercise intensity based on BMI and age
- Consider health conditions in exercise selection
- Provide specific recommendations based on their fitness goal
- Include progression tips suitable for their experience level

Return ONLY this JSON structure:
{{
  "plan_overview": "Personalized message for {member_name} about this plan",
  "member_stats": {{
    "name": "{member_name}",
    "bmi": {bmi:.1f},
    "bmi_category": "{bmi_category}",
    "recommended_focus": "Based on member's profile"
  }},
  "weekly_schedule": [
    {{
      "day": "Day 1",
      "focus": "Cardio & Strength",
      "exercises": [
        {{"name": "Exercise Name", "sets": 3, "reps": "15", "rest": "45s", "notes": "Personalized tip"}},
        {{"name": "Exercise Name", "sets": 3, "reps": "15", "rest": "45s", "notes": "Personalized tip"}},
        {{"name": "Exercise Name", "sets": 3, "reps": "15", "rest": "45s", "notes": "Personalized tip"}},
        {{"name": "Exercise Name", "sets": 3, "reps": "15", "rest": "45s", "notes": "Personalized tip"}},
        {{"name": "Exercise Name", "sets": 3, "reps": "15", "rest": "45s", "notes": "Personalized tip"}}
      ]
    }}
  ],
  "nutrition_tips": "Personalized nutrition advice for {member_name} based on BMI and goals",
  "progress_tracking": "Specific tracking recommendations for {member_name}",
  "personalized_notes": "Additional tips and motivation for {member_name}"
}}

Create exactly {days} days. Each day needs 5 exercises.
Make it PERSONAL for {member_name}. Use their name and stats throughout.
Keep descriptions SHORT but PERSONALIZED. Return valid JSON only."""

        try:
            # Increase max tokens for personalized content
            response = self.model.generate_content(
                prompt,
                generation_config=genai.GenerationConfig(
                    temperature=0.7,  # Slightly higher for more personalized responses
                    max_output_tokens=5000,  # More tokens for personalized content
                )
            )
            
            # Extract text
            plan_text = ""
            
            if hasattr(response, 'text'):
                try:
                    plan_text = response.text
                    print(f"✓ Got text via .text property")
                except:
                    pass
            
            if not plan_text and response.candidates:
                for part in response.candidates[0].content.parts:
                    if hasattr(part, 'text'):
                        plan_text += part.text
            
            plan_text = plan_text.strip()
            
            print(f"Response length: {len(plan_text)} chars")
            
            if not plan_text:
                raise Exception("AI returned empty response")
            
            # Clean markdown
            if '```json' in plan_text:
                parts = plan_text.split('```json')
                if len(parts) > 1:
                    plan_text = parts[1].split('```')[0]
            elif '```' in plan_text:
                parts = plan_text.split('```')
                if len(parts) > 1:
                    plan_text = parts[1]
            
            plan_text = plan_text.strip()
            
            print(f"Cleaned text length: {len(plan_text)} chars")
            print(f"First 200 chars: {plan_text[:200]}")
            print(f"Last 100 chars: {plan_text[-100:]}")
            
            # Parse JSON
            workout_plan = json.loads(plan_text)
            
            print(f"✓ Generated {len(workout_plan.get('weekly_schedule', []))} workout days")
            
            return workout_plan
            
        except json.JSONDecodeError as e:
            print(f"❌ JSON Error: {str(e)}")
            print(f"Full response text:\n{plan_text}")
            raise Exception(f"Invalid JSON: {str(e)}")
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            raise Exception(f"Error: {str(e)}")
    
    def generate_plan(self, user_data):
        """Legacy method for backward compatibility"""
        # Convert user_data to member_data format
        member_data = {
            'name': user_data.get('member_name', 'Member'),
            'age': user_data.get('age', 25),
            'weight': user_data.get('weight', 70),
            'height': user_data.get('height', 170)
        }
        
        # Extract preferences
        preferences = {
            'goal': user_data.get('goal', 'general_fitness'),
            'experience': user_data.get('experience', 'beginner'),
            'days_per_week': user_data.get('days_per_week', 3),
            'duration': user_data.get('duration', '45'),
            'equipment': user_data.get('equipment', 'full_gym'),
            'health_conditions': user_data.get('health_conditions', 'None')
        }
        
        return self.generate_personalized_plan(member_data, preferences)
