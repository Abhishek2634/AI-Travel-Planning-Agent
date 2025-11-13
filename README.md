# 🌍 AI Travel Planner with MCP Integration

A sophisticated AI-powered travel planning application that creates comprehensive, personalized travel itineraries using multiple MCP (Model Context Protocol) servers. Built with Streamlit, this application uses specialized AI agents and several MCP integrations to gather real-time data for itineraries.

## ✨ Features

### 🤖 AI-Powered Travel Planning
- **Comprehensive Itineraries**: Detailed day-by-day schedules with timing, locations, and costs.
- **Multi-Agent Architecture**: Specialized AI agents for travel planning, booking, and navigation.
- **Personalized Recommendations**: Customizes itineraries based on user preferences, budget, and dietary restrictions.
- **Real-Time Data Integration**: Combines multiple data sources for accurate, up-to-date information.

### 🏨 Airbnb MCP Integration
- Real accommodation listings with current pricing and availability.
- Property details including amenities and guest capacity.
- Budget-conscious recommendations filtered by location and price range.
- Provides multiple accommodation options (e.g., 3 choices) per destination.

### 🗺️ Google Maps MCP Integration
- Precise distance calculations between itinerary locations.
- Travel time estimates for transportation planning.
- Location services for points of interest and navigation.
- Address verification for recommended places.
- Route optimization with turn-by-turn guidance.

### ☁️ Weather & Travel Planning MCP
- Weather forecasts for destination and travel dates.
- Packing recommendations based on weather conditions.
- Activity suggestions tailored to weather and season.
- Climate information and best-time-to-visit insights.

### 📅 Google Calendar Integration
- Automatic event creation for trip dates and activities.
- Calendar export (.ics file) for Google Calendar, Apple Calendar, or Outlook.
- Daily reminders for important activities and check-ins.
- Complete trip timeline with all bookings and reservations.

### 🎯 User Experience Features
- Multi-select preferences (Adventure, Relaxation, Sightseeing, etc.).
- Date range picker with automatic duration calculation.
- Budget tracking with detailed cost breakdown.
- Dietary restrictions support (Vegetarian, Vegan, Gluten-Free, Halal, etc.).
- Accommodation preferences (Hotel, Hostel, Airbnb, Resort).
- Transportation options (Public Transport, Rental Car, Taxi/Uber, Walking).
- Auto-loading API keys from environment variables.

## 🛠️ Setup

### Prerequisites

You'll need the following API keys and credentials:

1. **OpenAI API Key** (Required)
   - Get from: https://platform.openai.com/api-keys
   - Used for: AI travel planning and itinerary generation.

2. **Google Maps API Key** (Required)
   - Get from: https://console.cloud.google.com/apis/credentials
   - Used for: Location services, distance calculations, and navigation.

3. **AccuWeather API Key** (Optional)
   - Get from: https://developer.accuweather.com/
   - Free tier details: see AccuWeather for current limits.
   - Used for: Detailed weather forecasts and packing suggestions.

4. **Google Calendar OAuth** (Optional - for calendar integration)
   - Client ID and Secret from: https://console.cloud.google.com/apis/credentials
   - Refresh Token: Generated using `get_refresh_token.py`
   - Enable Google Calendar API at:
     https://console.cloud.google.com/apis/library/calendar-json.googleapis.com
   - Used for: Creating calendar events directly in your Google Calendar.

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Abhishek2634/AI-Travel-Planning-Agent.git
   cd AI-Travel-Planning-Agent
   ```

2. Create and activate a virtual environment (examples):

   Using conda:
   ```bash
   conda create -n travel python=3.11
   conda activate travel
   ```

   Or using venv:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # macOS/Linux
   .\.venv\Scripts\activate   # Windows (PowerShell)
   ```

3. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root and add your API keys and credentials:
   ```bash
   # Required API Keys
   OPENAI_API_KEY=your_openai_api_key_here
   GOOGLE_MAPS_API_KEY=your_google_maps_api_key_here

   # Optional API Keys
   ACCUWEATHER_API_KEY=your_accuweather_api_key_here

   # Optional: Google Calendar OAuth Credentials
   GOOGLE_CLIENT_ID=your_google_client_id_here
   GOOGLE_CLIENT_SECRET=your_google_client_secret_here
   GOOGLE_REFRESH_TOKEN=your_google_refresh_token_here
   ```

5. Make `calendar_mcp.py` executable (if running directly on Unix-like systems):
   ```bash
   chmod +x calendar_mcp.py
   ```

## Getting Google Calendar OAuth Credentials

If you want calendar integration:

1. Run the helper script:
   ```bash
   python get_refresh_token.py
   ```

2. Follow the prompts:
   - A browser will open for Google sign-in.
   - Sign in with the Google account you want to use.
   - Grant calendar permissions.
   - Copy the tokens displayed.

3. Add the tokens to the `.env` file as shown in the Installation section.

## 🚀 Running the App

1. Start the Streamlit app:
   ```bash
   streamlit run app.py
   ```

2. Access the app:
   - Local: http://localhost:8501
   - Network: https://abhishek2634-ai-travel-planning-agent-app-kqfyba.streamlit.app/

3. Using the app:
   - API keys auto-load from `.env` (or enter manually in the sidebar).
   - Enter your trip details (source, destination, dates, budget).
   - Select travel preferences using multi-select tags.
   - Choose dietary restrictions and accommodation preferences.
   - Click "Plan My Trip" to generate your itinerary.
   - Download calendar file (.ics) for import into your calendar app.

## 🔧 How It Works

### Multi-Agent Architecture

The app uses a multi-agent system composed of specialized agents and MCP servers.

1. Travel Planner Agent
   - Model: GPT-4o (OpenAI)
   - Role: Creates comprehensive travel itineraries.
   - Tools: Airbnb MCP, Google Maps MCP, Weather MCP, Calendar MCP, Google Search.

2. MCP Servers
   - Airbnb MCP: @openbnb/mcp-server-airbnb
   - Google Maps MCP: @modelcontextprotocol/server-google-maps
   - Weather MCP: @gongrzhe/server-travelplanner-mcp
   - Calendar MCP: Custom Python MCP server (calendar_mcp.py)

3. Flow
   User input (Streamlit UI) → AI Agent → MCP Servers → Real-time Data → GPT-4o Processing → Comprehensive Itinerary → User

## Key Features Implementation

- Date Handling: Uses proper date pickers with automatic duration calculation.
- Preferences: Multi-select tags for flexible preference selection.
- API Key Management: Auto-loads from `.env` with manual override option.
- Error Handling: Graceful fallbacks if MCP servers are unavailable.
- Calendar Export: Generates `.ics` files for universal calendar compatibility.
- Cost Tracking: Real-time budget calculations and breakdown.

## 🐛 Troubleshooting

### Common Issues & Solutions

API Key Errors
- OpenAI: Ensure you have credits and the key is valid.
- Google Maps: Enable Maps API and set up billing.
- AccuWeather: Sign up for free tier and verify usage limits.

### MCP Connection Issues

Check terminal output for messages like:
- ✅ Airbnb MCP Server running on stdio
- ✅ Google Maps MCP Server running on stdio
- ✅ Travel Planner MCP Server running on stdio
- ✅ Processing request of type ListToolsRequest

### Calendar Not Working

1. Error: "403 Forbidden - accessNotConfigured"
   - Enable Google Calendar API:
     https://console.cloud.google.com/apis/library/calendar-json.googleapis.com

2. Error: "Authentication failed"
   - Regenerate refresh token:
     ```bash
     python get_refresh_token.py
     ```
   - Make sure you're signed in with the correct Google account.

3. Calendar MCP not loading
   - Ensure `calendar_mcp.py` has execute permissions (Unix-like systems):
     ```bash
     chmod +x calendar_mcp.py
     ```
   - Verify Google OAuth credentials in `.env`.

### Date Calculation Issues
- Use the date pickers in the UI to avoid parsing errors.
- Duration is automatically calculated from start and end dates.
- Make sure the end date is after the start date.

### Network Issues
- Some corporate networks block MCP connections.
- Try using a VPN or a personal network.
- The app will continue with available tools if MCP servers fail.

## 🎯 Features in Detail

### Itinerary Generation
- Day-by-day detailed schedules.
- Specific timing for all activities.
- Transportation details between locations.
- Restaurant recommendations with cuisine types.
- Accommodation options with pricing.
- Weather forecasts and packing lists.
- Local tips and safety information.

### Budget Management
- Total estimated cost breakdown.
- Per-day budget allocation.
- Accommodation costs.
- Activity and attraction fees.
- Transportation expenses.
- Meal budgets.

### Personalization
- Adventure, Relaxation, Sightseeing, Cultural Experiences.
- Beach, Mountain, Luxury, Budget-Friendly.
- Food & Dining, Shopping, Nightlife, Family-Friendly.
- Dietary restrictions support.
- Accommodation preference customization.
- Transportation mode selection.

### 🌟 What Makes This Special
1. Real-Time Data: Uses actual Airbnb listings, not generic suggestions.
2. Precise Calculations: Google Maps MCP for accurate distances and times.
3. Calendar Integration: Automatic event creation in Google Calendar.
4. Multi-Agent System: Specialized agents for different planning aspects.
5. Comprehensive: Covers everything from booking to daily activities.
6. User-Friendly: Intuitive Streamlit interface with auto-loading API keys.
7. Flexible: Works with or without optional API keys/features.
8. Complete: Download calendar files for any calendar app.

### 🤝 Contributing
Contributions are welcome! You can:
- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

### 📄 License
This project is open source and available under the MIT License.

### 🙏 Acknowledgments
- Agno Framework: For MCP integration capabilities.
- OpenAI: GPT-4o model for AI planning.
- MCP Protocol: Standardized tool integration.
- Streamlit: Beautiful web interface.
- Airbnb, Google Maps, AccuWeather: Real-time data providers.

Built with ❤️ using AI agents and MCP servers.