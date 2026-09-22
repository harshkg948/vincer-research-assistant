import structlog
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agents import VincerAgents
from xai_module import ExplainabilityModule
from auth_handler import OAuthHandler, PermissionRequestModel

logger = structlog.get_logger()

app = FastAPI(
    title="VINCER AI Research Assistant API",
    description="Enterprise-grade multi-agent research command center powered by Google AI SDK & Cloud Run",
    version="2.0.0"
)

# Enable CORS for frontend dashboard connection (Muse-like UI integration)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

vincer_agents = VincerAgents()

class ResearchQueryPayload(BaseModel):
    query: str
    user_id: str

@app.post("/api/v1/research/execute", status_code=status.HTTP_200_OK)
async def execute_research_workflow(payload: ResearchQueryPayload):
    logger.info("Initiating research pipeline", query=payload.query, user=payload.user_id)
    try:
        # Step 1: Coordinator Agent Plans
        coord_output = await vincer_agents.coordinator_agent(payload.query)
        coord_xai = ExplainabilityModule.explain_output("Coordinator Agent", str(coord_output))

        # Step 2: Data Analysis Agent Synthesizes
        analysis_text = await vincer_agents.data_analysis_agent(coord_output["milestones"])
        analysis_xai = ExplainabilityModule.explain_output("Data Analysis Agent", analysis_text)

        # Step 3: Verification Agent Validates
        verification_output = await vincer_agents.verification_agent(analysis_text)
        verification_xai = ExplainabilityModule.explain_output("Verification Agent", verification_output["validation_report"])

        return {
            "status": "success",
            "query": payload.query,
            "workflow_execution": {
                "coordination": {
                    "result": coord_output,
                    "xai": coord_xai
                },
                "data_analysis": {
                    "result": analysis_text,
                    "xai": analysis_xai
                },
                "verification": {
                    "result": verification_output,
                    "xai": verification_xai
                }
            }
        }
    except Exception as e:
        logger.error("Research workflow execution failed", error=str(e))
        raise HTTPException(status_code=500, detail=f"Internal agent execution error: {str(e)}")

@app.post("/api/v1/permissions/request-access", status_code=status.HTTP_201_CREATED)
def request_external_app_access(payload: PermissionRequestModel):
    """Handles secure permission requests for external professional apps like LinkedIn/Calendar."""
    return OAuthHandler.process_oauth_grant(payload)

@app.get("/health", status_code=status.HTTP_200_OK)
def health_check():
    return {
        "status": "healthy",
        "service": "VINCER Agentic Cloud Environment",
        "cloud_target": "Google Cloud Run Ready"
    }