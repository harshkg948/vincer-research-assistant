from fastapi import HTTPException
from pydantic import BaseModel

class PermissionRequestModel(BaseModel):
    app_name: str
    scopes: list[str]
    user_id: str

class OAuthHandler:
    SUPPORTED_APPS = {
        "LinkedIn": ["r_liteprofile", "w_member_social"],
        "Google Calendar": ["https://www.googleapis.com/auth/calendar.readonly"],
        "Slack": ["channels:read", "chat:write"]
    }

    @classmethod
    def process_oauth_grant(cls, req: PermissionRequestModel):
        if req.app_name not in cls.SUPPORTED_APPS:
            raise HTTPException(
                status_code=400, 
                detail=f"Integration with '{req.app_name}' is not supported. Supported apps: {list(cls.SUPPORTED_APPS.keys())}"
            )
        
        valid_scopes = cls.SUPPORTED_APPS[req.app_name]
        granted_scopes = [s for s in req.scopes if s in valid_scopes]

        return {
            "status": "PENDING_EXPLICIT_USER_CONSENT",
            "target_app": req.app_name,
            "user_id": req.user_id,
            "approved_scopes": granted_scopes,
            "authorization_redirect_url": f"https://vincer-auth.internal/oauth/v1/authorize?app={req.app_name.lower()}&user={req.user_id}"
        }