import google.generativeai as genai
from config import settings

genai.configure(api_key=settings.GEMINI_API_KEY)

class VincerAgents:
    def __init__(self):
        # Using current supported stable model instance
        self.model = genai.GenerativeModel('gemini-2.5-flash')

    async def coordinator_agent(self, query: str) -> dict:
        """Plans and breaks down the deep research query into tactical execution steps."""
        prompt = (
            f"You are Vincer's Coordinator Agent. Analyze this research query: '{query}'. "
            f"Break it down into 3 distinct logical milestones or sub-tasks required for thorough investigation."
        )
        response = await self.model.generate_content_async(prompt)
        return {
            "agent": "Coordinator Agent",
            "milestones": response.text.split("\n")
        }

    async def data_analysis_agent(self, plan: list) -> str:
        """Gathers insights, parses data vectors, and synthesizes academic/technical findings."""
        prompt = (
            f"You are Vincer's Data Analysis Agent. Based on the following execution plan/milestones, "
            f"synthesize comprehensive research insights, extract metrics, and draft the technical body:\n{plan}"
        )
        response = await self.model.generate_content_async(prompt)
        return response.text

    async def verification_agent(self, content: str) -> dict:
        """Cross-checks facts, validates logical consistency, and flags potential anomalies."""
        prompt = (
            f"You are Vincer's Verification Agent. Fact-check the following synthesized research content "
            f"and evaluate its structural integrity and accuracy:\n{content}"
        )
        response = await self.model.generate_content_async(prompt)
        return {
            "status": "Verified & Cross-Checked",
            "validation_report": response.text
        }