import msal
import httpx
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


class MicrosoftGraphClient:
    """Client for Microsoft Graph API integration"""

    GRAPH_API_ENDPOINT = "https://graph.microsoft.com/v1.0"

    def __init__(self, access_token: Optional[str] = None):
        self.access_token = access_token
        self.headers = {
            "Authorization": f"Bearer {access_token}" if access_token else "",
            "Content-Type": "application/json",
        }

    @staticmethod
    def get_auth_url(state: str) -> str:
        """Generate Microsoft OAuth2 authorization URL"""
        msal_app = msal.PublicClientApplication(
            settings.microsoft_client_id,
            authority=f"https://login.microsoftonline.com/{settings.microsoft_tenant_id}",
        )

        auth_url = msal_app.get_authorization_request_url(
            scopes=settings.microsoft_scopes_list,
            state=state,
            redirect_uri=settings.microsoft_redirect_uri,
        )
        return auth_url

    @staticmethod
    async def get_token_from_code(code: str) -> Dict[str, Any]:
        """Exchange authorization code for access token"""
        msal_app = msal.ConfidentialClientApplication(
            settings.microsoft_client_id,
            authority=f"https://login.microsoftonline.com/{settings.microsoft_tenant_id}",
            client_credential=settings.microsoft_client_secret,
        )

        result = msal_app.acquire_token_by_authorization_code(
            code,
            scopes=settings.microsoft_scopes_list,
            redirect_uri=settings.microsoft_redirect_uri,
        )

        if "error" in result:
            raise Exception(f"Failed to acquire token: {result.get('error_description')}")

        return result

    @staticmethod
    async def refresh_token(refresh_token: str) -> Dict[str, Any]:
        """Refresh access token using refresh token"""
        msal_app = msal.ConfidentialClientApplication(
            settings.microsoft_client_id,
            authority=f"https://login.microsoftonline.com/{settings.microsoft_tenant_id}",
            client_credential=settings.microsoft_client_secret,
        )

        result = msal_app.acquire_token_by_refresh_token(
            refresh_token,
            scopes=settings.microsoft_scopes_list,
        )

        if "error" in result:
            raise Exception(f"Failed to refresh token: {result.get('error_description')}")

        return result

    async def get_user_profile(self) -> Dict[str, Any]:
        """Get current user's profile"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.GRAPH_API_ENDPOINT}/me",
                headers=self.headers,
            )
            response.raise_for_status()
            return response.json()

    async def get_emails(
        self,
        folder: str = "inbox",
        since: Optional[datetime] = None,
        limit: int = 50,
    ) -> List[Dict[str, Any]]:
        """Fetch emails from Outlook"""
        url = f"{self.GRAPH_API_ENDPOINT}/me/mailFolders/{folder}/messages"

        params = {
            "$top": limit,
            "$orderby": "receivedDateTime DESC",
            "$select": "id,subject,bodyPreview,body,from,toRecipients,ccRecipients,receivedDateTime,hasAttachments,webLink",
        }

        if since:
            since_str = since.isoformat()
            params["$filter"] = f"receivedDateTime ge {since_str}"

        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()
            return data.get("value", [])

    async def get_teams_chats(
        self,
        since: Optional[datetime] = None,
        limit: int = 50,
    ) -> List[Dict[str, Any]]:
        """Fetch Teams chats"""
        url = f"{self.GRAPH_API_ENDPOINT}/me/chats"

        params = {
            "$top": limit,
            "$expand": "lastMessagePreview",
            "$orderby": "lastMessagePreview/createdDateTime DESC",
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()
            return data.get("value", [])

    async def get_chat_messages(
        self,
        chat_id: str,
        since: Optional[datetime] = None,
        limit: int = 50,
    ) -> List[Dict[str, Any]]:
        """Fetch messages from a specific Teams chat"""
        url = f"{self.GRAPH_API_ENDPOINT}/me/chats/{chat_id}/messages"

        params = {
            "$top": limit,
            "$orderby": "createdDateTime DESC",
        }

        if since:
            since_str = since.isoformat()
            params["$filter"] = f"createdDateTime ge {since_str}"

        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()
            return data.get("value", [])

    async def get_online_meetings(
        self,
        since: Optional[datetime] = None,
        limit: int = 50,
    ) -> List[Dict[str, Any]]:
        """Fetch online meetings"""
        url = f"{self.GRAPH_API_ENDPOINT}/me/onlineMeetings"

        params = {"$top": limit}

        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()
            return data.get("value", [])

    async def get_meeting_transcripts(
        self,
        meeting_id: str,
    ) -> List[Dict[str, Any]]:
        """Fetch transcripts for a specific meeting"""
        url = f"{self.GRAPH_API_ENDPOINT}/me/onlineMeetings/{meeting_id}/transcripts"

        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            return data.get("value", [])

    async def get_transcript_content(
        self,
        meeting_id: str,
        transcript_id: str,
    ) -> str:
        """Get the actual transcript content"""
        url = f"{self.GRAPH_API_ENDPOINT}/me/onlineMeetings/{meeting_id}/transcripts/{transcript_id}/content"

        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers)
            response.raise_for_status()
            return response.text

    async def search_sharepoint(
        self,
        query: str,
        limit: int = 50,
    ) -> List[Dict[str, Any]]:
        """Search SharePoint for items where user is mentioned"""
        url = f"{self.GRAPH_API_ENDPOINT}/search/query"

        body = {
            "requests": [
                {
                    "entityTypes": ["listItem", "driveItem"],
                    "query": {"queryString": query},
                    "from": 0,
                    "size": limit,
                }
            ]
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=self.headers, json=body)
            response.raise_for_status()
            data = response.json()
            hits = data.get("value", [{}])[0].get("hitsContainers", [{}])[0].get("hits", [])
            return hits

    async def get_people(self) -> List[Dict[str, Any]]:
        """Get people the user works with"""
        url = f"{self.GRAPH_API_ENDPOINT}/me/people"

        params = {"$top": 100}

        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()
            return data.get("value", [])

    async def get_organization_hierarchy(self) -> Dict[str, Any]:
        """Get user's manager and direct reports (org structure)"""
        try:
            async with httpx.AsyncClient() as client:
                # Get manager
                manager_response = await client.get(
                    f"{self.GRAPH_API_ENDPOINT}/me/manager",
                    headers=self.headers,
                )
                manager = manager_response.json() if manager_response.status_code == 200 else None

                # Get direct reports
                reports_response = await client.get(
                    f"{self.GRAPH_API_ENDPOINT}/me/directReports",
                    headers=self.headers,
                )
                direct_reports = reports_response.json().get("value", []) if reports_response.status_code == 200 else []

                # Get team memberships
                teams_response = await client.get(
                    f"{self.GRAPH_API_ENDPOINT}/me/joinedTeams",
                    headers=self.headers,
                )
                teams = teams_response.json().get("value", []) if teams_response.status_code == 200 else []

                return {
                    "manager": manager,
                    "direct_reports": direct_reports,
                    "teams": teams,
                }
        except Exception as e:
            logger.error(f"Error fetching organization hierarchy: {e}")
            return {"manager": None, "direct_reports": [], "teams": []}

    async def get_calendar_events(
        self,
        since: Optional[datetime] = None,
        until: Optional[datetime] = None,
        limit: int = 50,
    ) -> List[Dict[str, Any]]:
        """Fetch calendar events"""
        url = f"{self.GRAPH_API_ENDPOINT}/me/calendar/events"

        params = {
            "$top": limit,
            "$orderby": "start/dateTime DESC",
            "$select": "id,subject,bodyPreview,start,end,location,attendees,webLink,onlineMeeting",
        }

        filters = []
        if since:
            filters.append(f"start/dateTime ge '{since.isoformat()}'")
        if until:
            filters.append(f"start/dateTime le '{until.isoformat()}'")

        if filters:
            params["$filter"] = " and ".join(filters)

        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()
            return data.get("value", [])
