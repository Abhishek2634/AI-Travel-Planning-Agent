import re
import asyncio
from textwrap import dedent
from datetime import datetime, timedelta, date
import os
import streamlit as st
from dotenv import load_dotenv
from icalendar import Calendar, Event

# --- Import Agno Components ---
from agno.agent import Agent
from agno.run.agent import RunOutput
from agno.tools.mcp import MultiMCPTools
from agno.models.openai import OpenAIChat
from agno.tools.tavily import TavilyTools  # Add this

# Load environment variables
load_dotenv()


def generate_ics_content(plan_text: str, start_date: datetime = None) -> bytes:
    """Generate an ICS calendar file from a travel itinerary text."""
    cal = Calendar()
    cal.add('prodid', '-//AI Travel Planner//github.com//')
    cal.add('version', '2.0')

    if start_date is None:
        start_date = datetime.today()

    day_pattern = re.compile(r'Day (\d+)[:\s]+(.*?)(?=Day \d+|$)', re.DOTALL)
    days = day_pattern.findall(plan_text)

    if not days:
        event = Event()
        event.add('summary', "Travel Itinerary")
        event.add('description', plan_text)
        event.add('dtstart', start_date.date())
        event.add('dtend', start_date.date())
        event.add("dtstamp", datetime.now())
        cal.add_component(event)
    else:
        for day_num, day_content in days:
            day_num = int(day_num)
            current_date = start_date + timedelta(days=day_num - 1)
            event = Event()
            event.add('summary', f"Day {day_num} Itinerary")
            event.add('description', day_content.strip())
            event.add('dtstart', current_date.date())
            event.add('dtend', current_date.date())
            event.add("dtstamp", datetime.now())
            cal.add_component(event)

    return cal.to_ical()

async def run_mcp_travel_planner(source: str, destination: str, start_date_str: str, end_date_str: str,
                                   num_days: int, preferences: str, budget: int, accommodation: str, 
                                   transportation: str, dietary: str, openai_key: str, google_maps_key: str, 
                                   accuweather_key: str, google_client_id: str, 
                                   google_client_secret: str, google_refresh_token: str):
    """Run the MCP-based travel planner agent."""

    try:
        env = {
            **os.environ,
            "GOOGLE_MAPS_API_KEY": google_maps_key,
            "OPENAI_API_KEY": openai_key,
            "ACCUWEATHER_API_KEY": accuweather_key or "",
            "GOOGLE_CLIENT_ID": google_client_id or "",
            "GOOGLE_CLIENT_SECRET": google_client_secret or "",
            "GOOGLE_REFRESH_TOKEN": google_refresh_token or "",
        }

        mcp_tools = MultiMCPTools(
            [
                "npx -y @openbnb/mcp-server-airbnb --ignore-robots-txt",
                "npx -y @modelcontextprotocol/server-google-maps",
                "npx @gongrzhe/server-travelplanner-mcp",
                "./calendar_mcp.py"
            ],      
            env=env,
            timeout_seconds=120,
        )

        await mcp_tools.connect()

        travel_planner = Agent(
            name="Travel Planner",
            role="Creates comprehensive travel itineraries",
            model=OpenAIChat(id="gpt-4o", api_key=openai_key),
            description=dedent(
                """\
                You are a professional travel consultant AI that creates detailed travel itineraries.

                You have access to:
                🏨 Airbnb listings with real availability and pricing
                🗺️ Google Maps for location services and navigation
                ☁️ Weather forecasts
                📅 Calendar management

                Create complete itineraries immediately without asking questions.
                """
            ),
            instructions=[
                "Never ask questions - always generate a complete itinerary",
                "Research destination thoroughly using all tools",
                "Find accommodations within budget using Airbnb",
                "Create detailed day-by-day itinerary with timing",
                "Use Google Maps for distances and travel times",
                "Include transportation, dining, and activity recommendations",
                "Provide weather information and packing suggestions",
                "Calculate costs and ensure within budget",
                "IMPORTANT: Always use the calendar tool to create events for the trip",
                "Create a calendar event for the departure date with all trip details",
                "Add calendar events for each major activity or day of the trip",
                "Include reminders for important bookings and check-ins",
            ],
            tools=[mcp_tools, TavilyTools()],  # Use Tavily instead
            add_datetime_to_context=True,
            markdown=True,
            debug_mode=False,
        )

        prompt = f"""
        Create a comprehensive travel itinerary:

        **Source:** {source}
        **Destination:** {destination}
        **Start Date:** {start_date_str}
        **End Date:** {end_date_str}
        **Duration:** {num_days} days
        **Budget:** ${budget} USD
        **Preferences:** {preferences}
        **Accommodation:** {accommodation}
        **Transportation:** {transportation}
        **Dietary Restrictions:** {dietary}

        IMPORTANT: The trip is from {start_date_str} to {end_date_str} ({num_days} days).
        Make sure all dates in the itinerary match these exact dates.
        Start with Day 1 on {start_date_str} and end on Day {num_days} on {end_date_str}.

        Include:
        1. Trip overview with cost breakdown
        2. 3 Airbnb accommodation options with prices
        3. Detailed day-by-day itinerary
        4. Transportation details with timing
        5. Restaurant recommendations
        6. Weather forecast and packing list
        7. Local tips and safety information

        CRITICAL: Use the create_event calendar tool to add events to Google Calendar:
        - Create a main trip event with departure date
        - Add daily events for each day of the trip
        - Include reminders for check-ins and bookings

        Use all available tools and generate the complete itinerary now.
        """

        response: RunOutput = await travel_planner.arun(prompt)
        return response.content

    finally:
        await mcp_tools.close()

def run_travel_planner(source: str, destination: str, start_date_str: str, end_date_str: str,
                       num_days: int, preferences: str, budget: int, accommodation: str, 
                       transportation: str, dietary: str, openai_key: str, google_maps_key: str, 
                       accuweather_key: str, google_client_id: str, google_client_secret: str, 
                       google_refresh_token: str):
    """Synchronous wrapper."""
    return asyncio.run(run_mcp_travel_planner(source, destination, start_date_str, end_date_str,
                                               num_days, preferences, budget, accommodation, 
                                               transportation, dietary, openai_key, google_maps_key, 
                                               accuweather_key, google_client_id, google_client_secret, 
                                               google_refresh_token))

# -------------------- Streamlit App --------------------

st.set_page_config(page_title="AI Travel Planner", page_icon="✈️", layout="wide")

if 'itinerary' not in st.session_state:
    st.session_state.itinerary = None

st.title("✈️ AI Travel Planner")
st.caption("This AI-powered travel planner helps you create personalized travel itineraries using:")

st.markdown("""
- 🗺️ Maps and navigation
- ☁️ Weather forecasts
- 🏨 Accommodation booking
- 📅 Calendar management
""")

# Load API keys from .env
openai_key = os.getenv("OPENAI_API_KEY", "")
google_maps_key = os.getenv("GOOGLE_MAPS_API_KEY", "")
accuweather_key = os.getenv("ACCUWEATHER_API_KEY", "")
google_client_id = os.getenv("GOOGLE_CLIENT_ID", "")
google_client_secret = os.getenv("GOOGLE_CLIENT_SECRET", "")
google_refresh_token = os.getenv("GOOGLE_REFRESH_TOKEN", "")

# Sidebar
with st.sidebar:
    st.header("🔑 API Keys Configuration")
    st.write("Please enter your API keys to use the travel planner.")
    
    # Auto-fill from .env but allow override
    google_maps_key = st.text_input("Google Maps API Key", value=google_maps_key, type="password")
    accuweather_key = st.text_input("AccuWeather API Key", value=accuweather_key, type="password")
    openai_key = st.text_input("OpenAI API Key", value=openai_key, type="password")
    google_client_id = st.text_input("Google Client ID", value=google_client_id, type="password")
    google_client_secret = st.text_input("Google Client Secret", value=google_client_secret, type="password")
    google_refresh_token = st.text_input("Google Refresh Token", value=google_refresh_token, type="password")
    
    # Check required keys only
    required_keys = google_maps_key and openai_key
    
    if required_keys and google_client_id and google_client_secret and google_refresh_token and accuweather_key:
        st.success("✅ All API keys are configured!")
    elif required_keys:
        st.success("✅ Required API keys configured!")
        st.info("ℹ️ Optional keys missing (AccuWeather, Calendar)")
    else:
        st.warning("⚠️ Please enter OpenAI and Google Maps API keys.")

# Main form
col1, col2 = st.columns(2)

with col1:
    source = st.text_input("Source", value="Delhi")

with col2:
    budget = st.number_input("Budget (in USD)", min_value=0, step=100, value=0)

destination = st.text_input("Destination", placeholder="Enter your destination city")

# Date inputs with proper date pickers
col1, col2 = st.columns(2)

with col1:
    start_date_input = st.date_input(
        "Start Date", 
        value=date.today(),  # CHANGED: Set default to today
        min_value=date.today(),
        key="start_date"
    )

with col2:
    # Default the end date to tomorrow so it's valid
    default_end = date.today() + timedelta(days=4) 
    
    end_date_input = st.date_input(
        "End Date", 
        value=default_end,  # CHANGED: Set default to a valid future date
        min_value=date.today(),
        key="end_date"
    )


col1, col2 = st.columns(2)

with col1:
    preferences = st.multiselect(
        "Travel Preferences",
        ["Adventure", "Relaxation", "Sightseeing", "Cultural Experiences", 
         "Beach", "Mountain", "Luxury", "Budget-Friendly", "Food & Dining",
         "Shopping", "Nightlife", "Family-Friendly"],
        default=[],
        key="preferences_multiselect"
    )

with col2:
    dietary = st.selectbox(
        "Dietary Restrictions", 
        ["Choose an option", "None", "Vegetarian", "Vegan", "Gluten-Free", "Halal"], 
        key="dietary_select"
    )

st.subheader("Additional Preferences")

col1, col2 = st.columns(2)

with col1:
    accommodation = st.selectbox(
        "Preferred Accommodation", 
        ["Any", "Hotel", "Hostel", "Airbnb", "Resort"], 
        key="accommodation_select"
    )

with col2:
    transportation = st.selectbox(
        "Preferred Transportation", 
        ["Choose an option", "Public Transport", "Rental Car", "Taxi/Uber", "Walking"], 
        key="transportation_select"
    )

# Convert preferences list to string
preferences_string = ", ".join(preferences) if preferences else "General sightseeing"

if st.button("Plan My Trip", type="primary"):
    if not destination:
        st.error("Please enter a destination")
    elif not (google_maps_key and openai_key):
        st.error("Please enter required API keys (OpenAI and Google Maps)")
    elif end_date_input < start_date_input:
        st.error("End date must be after start date")
    else:
        with st.spinner("Creating your travel plan..."):
            try:
                # Calculate number of days
                num_days = (end_date_input - start_date_input).days + 1
                
                # Format dates for display
                start_date_str = start_date_input.strftime("%B %d, %Y")
                end_date_str = end_date_input.strftime("%B %d, %Y")
                
                result = run_travel_planner(
                    source=source,
                    destination=destination,
                    start_date_str=start_date_str,
                    end_date_str=end_date_str,
                    num_days=num_days,
                    preferences=preferences_string,
                    budget=budget,
                    accommodation=accommodation,
                    transportation=transportation,
                    dietary=dietary,
                    openai_key=openai_key,
                    google_maps_key=google_maps_key,
                    accuweather_key=accuweather_key,
                    google_client_id=google_client_id,
                    google_client_secret=google_client_secret,
                    google_refresh_token=google_refresh_token
                )
                
                st.session_state.itinerary = result
                st.session_state.trip_start_date = start_date_input  # ← Different key name
                st.success("✅ Your itinerary is ready!")

                
            except Exception as e:
                st.error(f"Error: {str(e)}")

if st.session_state.itinerary:
    st.header("📋 Your Travel Itinerary")
    st.markdown(st.session_state.itinerary)
    
    # Download calendar button
    if 'trip_start_date' in st.session_state:  # ← Use new key name
        ics_content = generate_ics_content(
            st.session_state.itinerary, 
            datetime.combine(st.session_state.trip_start_date, datetime.min.time())
        )
        st.download_button(
            label="📅 Download Calendar File",
            data=ics_content,
            file_name="travel_itinerary.ics",
            mime="text/calendar"
        )
