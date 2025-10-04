# HomeGenie MCP Server

A Model Context Protocol (MCP) server that provides HomeGenie AI with access to external APIs for weather data and energy pricing information.

## Features

### 🌤️ Weather Data Tool
- Fetches current weather conditions from OpenWeatherMap API
- Provides HomeGenie-specific recommendations based on weather
- Mock data mode for development/demo purposes
- Includes temperature, humidity, wind speed, and weather conditions

### ⚡ Energy Prices Tool  
- Fetches current energy prices per kWh
- Provides 24-hour price forecasting
- Peak/off-peak period detection
- HomeGenie energy optimization recommendations
- Mock data with realistic European pricing patterns

## Installation

1. **Install Dependencies:**
   ```bash
   cd mcp-server
   pip install -r requirements.txt
   ```

2. **Configure API Keys (Optional):**
   Create `.env` file:
   ```bash
   OPENWEATHER_API_KEY=your_api_key_here
   ENERGY_API_KEY=your_energy_api_key_here
   ```

## Usage

### Running the MCP Server
```bash
python genie_mcp_server.py
```

### Available Tools

#### 1. `get_weather_data`
```json
{
  "location": "London"
}
```
Returns current weather with HomeGenie automation recommendations.

#### 2. `get_energy_prices`  
```json
{
  "region": "EU",
  "include_forecast": true
}
```
Returns current energy prices and 24-hour forecast with smart home recommendations.

## Integration with HomeGenie

The MCP server provides context-aware data that helps HomeGenie make intelligent automation decisions:

- **Weather Integration**: Adjusts heating/cooling based on weather conditions
- **Energy Optimization**: Schedules energy-intensive tasks during low-price periods
- **Smart Recommendations**: Provides actionable insights for home automation

## Demo Mode

Without API keys, the server runs in demo mode with realistic mock data:
- Weather data simulates various conditions
- Energy prices follow European market patterns with peak/off-peak pricing
- Fully functional for development and testing

## Architecture

```
MCP Server
├── WeatherAPI class     # Weather data fetching & processing
├── EnergyPriceAPI class # Energy price data & forecasting  
├── Tool handlers        # MCP protocol implementation
└── Mock data providers  # Demo/development data
```

## Example Output

### Weather Data Response:
```
🌤️ Weather Data for London:
📊 Current Conditions:
• Temperature: 22.1°C
• Description: Clear Sky
• Humidity: 65%
• Wind Speed: 3.2 m/s

🏠 HomeGenie Impact:
• Heating recommendation: Maintain
• Natural lighting: Good
• Window management: Consider ventilation
```

### Energy Prices Response:
```
⚡ Energy Prices for EU:
💰 Current Price:
• Price: €0.45/kWh
• Period: Peak
• Cost Impact: High cost - consider energy saving

📈 Next 8 Hours Forecast:
• 18:00: €0.45/kWh (peak)
• 19:00: €0.45/kWh (peak) 
• 20:00: €0.25/kWh (standard)
```

This MCP server enables HomeGenie to make data-driven automation decisions based on real-time weather and energy market conditions.