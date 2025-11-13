#!/usr/bin/env python
import os
import json
from datetime import datetime
from dotenv import load_dotenv
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from mcp.server.fastmcp import FastMCP

load_dotenv()

mcp = FastMCP("Google Calendar MCP")

def get_calendar_service():
    """Initialize Google Calendar service with proper error handling."""
    try:
        refresh_token = os.getenv('GOOGLE_REFRESH_TOKEN')
        client_id = os.getenv('GOOGLE_CLIENT_ID')
        client_secret = os.getenv('GOOGLE_CLIENT_SECRET')
        
        if not all([refresh_token, client_id, client_secret]):
            raise ValueError("Missing Google Calendar credentials in environment")
        
        creds = Credentials(
            token=None,
            refresh_token=refresh_token,
            token_uri='https://oauth2.googleapis.com/token',
            client_id=client_id,
            client_secret=client_secret,
            scopes=['https://www.googleapis.com/auth/calendar']
        )
        
        return build('calendar', 'v3', credentials=creds)
    except Exception as e:
        print(f"Calendar service initialization error: {str(e)}")
        raise

@mcp.tool()
async def create_event(summary: str, start_time: str, end_time: str, 
                       description: str = None, location: str = None) -> str:
    """Create a Google Calendar event."""
    try:
        service = get_calendar_service()
        event = {
            'summary': summary,
            'start': {'dateTime': start_time, 'timeZone': 'Asia/Kolkata'},
            'end': {'dateTime': end_time, 'timeZone': 'Asia/Kolkata'},
        }
        if description:
            event['description'] = description
        if location:
            event['location'] = location
        
        created = service.events().insert(calendarId='primary', body=event).execute()
        return f"✅ Calendar event created successfully: {created.get('htmlLink')}"
    except Exception as e:
        return f"❌ Failed to create calendar event: {str(e)}"

if __name__ == "__main__":
    mcp.run()
