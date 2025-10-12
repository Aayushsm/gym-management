import google.generativeai as genai
import json
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

class WorkoutPlanner:
    def __init__(self):
        self.model = genai.GenerativeModel('models/gemini-2.5-flash')
    
    def generate_plan(self, user_data):
        goal = user_data.get('goal', 'general_fitness')
        experience = user_data.get('experience', 'beginner')
        days = int(user_data.get('days_per_week', 3))
        duration = user_data.get('duration', '45')
        equipment = user_data.get('equipment', 'bodyweight')
        age = user_data.get('age', 25)
        weight = user_data.get('weight', 70)
        height = user_data.get('height', 170)
        health = user_data.get('health_conditions', 'None')
        
        # Simpler prompt for more concise output
        prompt = f"""Create a {days}-day workout plan in JSON format.

Goal: {goal}
Experience: {experience}
Equipment: {equipment}

Return ONLY this JSON structure:
{{
  "plan_overview": "One brief sentence about this plan",
  "weekly_schedule": [
    {{
      "day": "Day 1",
      "focus": "Cardio & Strength",
      "exercises": [
        {{"name": "Jumping Jacks", "sets": 3, "reps": "25", "rest": "30s", "notes": "Keep pace steady"}},
        {{"name": "Push-ups", "sets": 3, "reps": "15", "rest": "45s", "notes": "Proper form"}},
        {{"name": "Squats", "sets": 3, "reps": "20", "rest": "45s", "notes": "Full depth"}},
        {{"name": "Plank", "sets": 3, "reps": "30s", "rest": "30s", "notes": "Stay tight"}},
        {{"name": "Burpees", "sets": 3, "reps": "10", "rest": "60s", "notes": "Full range"}}
      ]
    }}
  ],
  "nutrition_tips": "Brief nutrition advice",
  "progress_tracking": "How to track progress"
}}

Create exactly {days} days. Each day needs 5 exercises.
Keep descriptions SHORT. Return valid JSON only."""

        try:
            # Increase max tokens to 4000
            response = self.model.generate_content(
                prompt,
                generation_config=genai.GenerationConfig(
                    temperature=0.5,
                    max_output_tokens=4000,
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
