import requests
import json
import logging

class OllamaClient:
    """Service layer client to communicate with the local Ollama API."""

    def __init__(self, base_url: str = "http://localhost:11434", model_name: str = "phi3"):
        self.base_url = base_url
        self.model_name = model_name

    def is_connected(self) -> bool:
        """Check if the local Ollama server is reachable and has the model loaded."""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=2)
            if response.status_code == 200:
                models = [m["name"] for m in response.json().get("models", [])]
                # Check if model_name is a substring of any installed model name
                return any(self.model_name in m for m in models)
        except Exception:
            pass
        return False

    def generate(self, prompt: str, system: str = None, json_mode: bool = False) -> str:
        """Send a generation request to the local Ollama instance."""
        url = f"{self.base_url}/api/generate"
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.3
            }
        }
        if system:
            payload["system"] = system
        if json_mode:
            payload["format"] = "json"
            
        try:
            # Set a generous timeout (300 seconds) for local LLM generation
            response = requests.post(url, json=payload, timeout=300)
            if response.status_code == 200:
                return response.json().get("response", "").strip()
            else:
                return f"Error: Ollama returned status code {response.status_code}"
        except requests.exceptions.ConnectionError:
            return "Error: Could not connect to local Ollama server. Please ensure Ollama is running (`ollama run phi3`)."
        except Exception as e:
            return f"Error occurred: {str(e)}"

    def screen_resume(self, resume_text: str, job_title: str, job_requirements: str) -> dict:
        """Evaluate a candidate's resume against job requirements."""
        system_prompt = (
            "You are an expert AI recruiter. You screen candidates against job descriptions. "
            "Respond ONLY with a valid JSON object containing the keys: "
            "'match_score' (an integer from 0 to 100), "
            "'extracted_skills' (a list of strings representing key skills), "
            "'summary' (a concise paragraph overview), "
            "and 'fit_notes' (a list of pros and cons bullet points). "
            "Do not include any other markdown outside the JSON."
        )
        prompt = f"""
        Job Title: {job_title}
        Job Requirements: {job_requirements}

        Candidate Resume:
        \"\"\"{resume_text}\"\"\"

        Please perform the screening analysis.
        """
        response_text = self.generate(prompt, system=system_prompt, json_mode=True)
        try:
            # Clean potential markdown wrappers
            clean_text = response_text.strip()
            if clean_text.startswith("```json"):
                clean_text = clean_text[7:]
            if clean_text.endswith("```"):
                clean_text = clean_text[:-3]
            clean_text = clean_text.strip()
            
            return json.loads(clean_text)
        except Exception:
            return {
                "match_score": 50,
                "extracted_skills": ["AI Analysis Failed"],
                "summary": f"Could not parse AI screening output. Raw Response: {response_text}",
                "fit_notes": ["Please verify that your local Ollama server is running and the phi3 model is loaded."]
            }

    def generate_interview_questions(self, candidate_name: str, job_title: str, skills: str) -> str:
        """Generate custom interview questions for a candidate."""
        prompt = f"""
        Create a list of 5 targeted technical and behavioral interview questions for a candidate named {candidate_name} applying for the {job_title} role.
        The candidate has these key skills: {skills}.
        Provide structured questions, each with a brief note explaining what to look for in the candidate's answer.
        Keep the questions and notes concise and to-the-point to optimize local processing time.
        """
        system_prompt = "You are a hiring manager. Generate concise, highly relevant interview questions."
        return self.generate(prompt, system=system_prompt)

    def generate_growth_plan(self, team_name: str, current_skills: str, target_role: str) -> str:
        """Create a learning roadmap for skill gaps."""
        prompt = f"""
        Design a structured, personal learning path and training roadmap for a member of the {team_name} team who knows: {current_skills}.
        They are aiming to level up to a {target_role} role.
        Identify the top 3 skill gaps and recommend specific, actionable courses, books, or project ideas to bridge those gaps.
        Keep the roadmap concise, clear, and direct (use short bullet points) to optimize local generation speed.
        """
        system_prompt = "You are a talent development coach. Provide professional, structured, and concise learning recommendations."
        return self.generate(prompt, system=system_prompt)

    def generate_retention_strategy(self, employee_name: str, department: str, skills: str, tenure: str, risk_level: str) -> str:
        """Generate custom retention strategies for an employee based on their flight risk details."""
        prompt = f"""
        Analyze the retention strategy for employee {employee_name} in the {department} department.
        Current tenure: {tenure}.
        Key Skills: {skills}.
        Assessed Flight Risk: {risk_level}.
        
        Provide a concise flight risk assessment explaining potential reasons for flight risk.
        Then, list 3 targeted, actionable recommendations to retain this employee (e.g. learning path, job alignment, role adjustments, or feedback channels).
        Keep the analysis and recommendations concise and direct (use short bullet points) to optimize local processing speed.
        """
        system_prompt = "You are a retention specialist and HR strategist. Provide professional, structured, and concise workforce retention strategies."
        return self.generate(prompt, system=system_prompt)
