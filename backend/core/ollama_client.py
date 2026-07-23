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
            elif clean_text.startswith("```"):
                clean_text = clean_text[3:]
            if clean_text.endswith("```"):
                clean_text = clean_text[:-3]
            clean_text = clean_text.strip()
            
            # Attempt to repair if raw json loads fails
            try:
                return json.loads(clean_text)
            except Exception:
                repaired = self._repair_json(clean_text)
                return json.loads(repaired)
        except Exception:
            return {
                "match_score": 50,
                "extracted_skills": ["AI Analysis Failed"],
                "summary": f"Could not parse AI screening output. Raw Response: {response_text}",
                "fit_notes": ["Please verify that your local Ollama server is running and the phi3 model is loaded."]
            }

    def _repair_json(self, json_str: str) -> str:
        """Attempt to repair common JSON syntax errors and truncations from LLM responses."""
        json_str = json_str.strip()
        if not json_str:
            return "{}"

        # Stack-based auto-closer
        in_string = False
        escape = False
        stack = []
        
        repaired_chars = []
        
        for i, char in enumerate(json_str):
            if escape:
                escape = False
                repaired_chars.append(char)
                continue
                
            if char == '\\':
                escape = True
                repaired_chars.append(char)
                continue
                
            if char == '"':
                in_string = not in_string
                repaired_chars.append(char)
                continue
                
            if not in_string:
                if char == '{':
                    stack.append('}')
                elif char == '[':
                    stack.append(']')
                elif char == '}':
                    if stack and stack[-1] == '}':
                        stack.pop()
                elif char == ']':
                    if stack and stack[-1] == ']':
                        stack.pop()
            
            repaired_chars.append(char)
            
        if in_string:
            if repaired_chars and repaired_chars[-1] == '\\':
                repaired_chars.pop()
            repaired_chars.append('"')
            
        temp_str = "".join(repaired_chars).strip()
        while temp_str and temp_str[-1] in (',', ':', ' '):
            temp_str = temp_str[:-1].strip()
            
        closing = []
        for brace in reversed(stack):
            closing.append(brace)
            
        repaired_json_str = temp_str + "".join(closing)
        
        try:
            json.loads(repaired_json_str)
            return repaired_json_str
        except Exception:
            pass
            
        # Drop trailing incomplete elements by splitting on last comma
        if stack:
            parts = temp_str.split(',')
            if len(parts) > 1:
                for j in range(len(parts) - 1, 0, -1):
                    candidate_base = ",".join(parts[:j]).strip()
                    c_stack = []
                    c_in_string = False
                    c_escape = False
                    for c_char in candidate_base:
                        if c_escape:
                            c_escape = False
                            continue
                        if c_char == '\\':
                            c_escape = True
                            continue
                        if c_char == '"':
                            c_in_string = not c_in_string
                            continue
                        if not c_in_string:
                            if c_char == '{':
                                c_stack.append('}')
                            elif c_char == '[':
                                c_stack.append(']')
                            elif c_char == '}':
                                if c_stack and c_stack[-1] == '}':
                                    c_stack.pop()
                            elif c_char == ']':
                                if c_stack and c_stack[-1] == ']':
                                    c_stack.pop()
                    if not c_in_string:
                        candidate_closing = "".join(reversed(c_stack))
                        candidate_json = candidate_base + candidate_closing
                        try:
                            json.loads(candidate_json)
                            return candidate_json
                        except Exception:
                            pass

        return repaired_json_str

    def generate_interview_questions(self, candidate_name: str, job_title: str, skills: str) -> str:
        """Generate custom interview questions for a candidate."""
        prompt = f"""
        Create a list of 5 targeted technical and behavioral interview questions for a candidate named {candidate_name} applying for the {job_title} role.
        The candidate has these key skills: {skills}.
        
        Requirements:
        - The questions MUST be directly relevant to the target role of {job_title}.
        - Do not ask questions about topics that are irrelevant to a {job_title} (e.g. if the role is a Product Designer, focus technical questions on Figma, design systems, prototyping, or UX research; do not ask software engineering/deep learning/NLP questions like React, Python, or data models unless they are explicitly applied to design workflows).
        - Provide structured questions, each with a brief note explaining what to look for in the candidate's answer.
        - Keep the questions and notes concise and to-the-point to optimize local processing time.
        """
        system_prompt = (
            "You are an expert hiring manager. Output ONLY the 5 structured interview questions and "
            "evaluation notes. Do NOT include meta-commentary, system prompt echoes, or requirement lists at the end."
        )
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

    def generate_email(self, candidate_name: str, job_title: str, email_type: str, tone: str, extra_context: str) -> str:
        """Generate a recruitment email for a candidate using specified tone and context."""
        prompt = f"""
        Draft a recruitment email to a candidate.
        
        Candidate Name: {candidate_name}
        Job Title: {job_title}
        Email Type: {email_type} (e.g. Interview Invitation, Job Offer, Rejection, Follow-up)
        Tone: {tone} (e.g. Professional, Friendly, Encouraging, Direct)
        Additional Context & Details: {extra_context}
        
        Requirements:
        - Provide the Subject line first (starting with "Subject:").
        - Then provide the Body of the email.
        - Do not include bracketed placeholder text like [Your Name] or [Insert Date]; instead, write ready-to-send content with a professional placeholder sign-off if needed.
        - Keep it clean, direct, and well-spaced.
        """
        system_prompt = "You are an expert recruitment assistant. Generate beautiful, professional, and ready-to-send emails."
        return self.generate(prompt, system=system_prompt)
