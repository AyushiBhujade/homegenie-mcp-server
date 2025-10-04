#!/usr/bin/env python3
"""
HomeGenie MCP Server
Model Context Protocol Server for HomeGenie AI Assistant using FastMCP

This server provides tools for:
1. Fetching weather data from weather APIs
2. Fetching energy prices (kWh) from energy APIs
"""

import json
import logging
from typing import Dict, Any
from datetime import datetime, timedelta
import random

from pydantic import BaseModel, Field
from mcp.server.fastmcp import FastMCP

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("homegenie-mcp")

# Initialize FastMCP server
mcp = FastMCP("HomeGenie MCP Server")

# Data models for tool inputs
class WeatherRequest(BaseModel):
    location: str = Field(default="London", description="City name or location")

class EnergyRequest(BaseModel):
    region: str = Field(default="EU", description="Region code (EU, US, UK)")
    include_forecast: bool = Field(default=True, description="Include 24-hour price forecast")

# Utility functions
def get_mock_weather_data(location: str) -> Dict[str, Any]:
    """Return mock weather data for demo purposes"""
    conditions = ["clear sky", "few clouds", "scattered clouds", "light rain"]
    return {
        "name": location,
        "main": {
            "temp": round(random.uniform(15.0, 25.0), 1),
            "feels_like": round(random.uniform(14.0, 26.0), 1),
            "humidity": random.randint(40, 80),
            "pressure": random.randint(1000, 1020)
        },
        "weather": [{
            "main": random.choice(["Clear", "Clouds", "Rain"]),
            "description": random.choice(conditions),
            "icon": "01d"
        }],
        "wind": {
            "speed": round(random.uniform(1.0, 10.0), 1)
        },
        "dt": int(datetime.now().timestamp()),
        "sys": {
            "sunrise": int((datetime.now().replace(hour=6, minute=30)).timestamp()),
            "sunset": int((datetime.now().replace(hour=19, minute=45)).timestamp())
        }
    }

def get_mock_energy_prices(region: str) -> Dict[str, Any]:
    """Return mock energy price data for demo purposes"""
    hour = datetime.now().hour
    base_price = 0.25  # €0.25 per kWh base price
    
    # Peak hours pricing
    if 7 <= hour <= 9 or 17 <= hour <= 20:
        multiplier = 1.8
        period = "peak"
    elif hour >= 22 or hour <= 6:
        multiplier = 0.7
        period = "off_peak"
    else:
        multiplier = 1.0
        period = "standard"
    
    current_price = round(base_price * multiplier, 3)
    
    # Generate 24-hour forecast
    forecast = []
    base_time = datetime.now()
    
    for i in range(24):
        time = base_time + timedelta(hours=i)
        f_hour = time.hour
        
        if 7 <= f_hour <= 9 or 17 <= f_hour <= 20:
            f_multiplier = 1.8
            f_period = "peak"
        elif f_hour >= 22 or f_hour <= 6:
            f_multiplier = 0.7
            f_period = "off_peak"
        else:
            f_multiplier = 1.0
            f_period = "standard"
        
        forecast.append({
            "time": time.strftime("%H:%M"),
            "date": time.strftime("%Y-%m-%d"),
            "price_per_kwh": round(base_price * f_multiplier, 3),
            "period": f_period
        })
    
    return {
        "region": region,
        "timestamp": datetime.now().isoformat(),
        "current_price": {
            "price_per_kwh": current_price,
            "currency": "EUR",
            "period": period,
            "unit": "kWh"
        },
        "price_forecast": forecast,
        "market_info": {
            "market": "Day Ahead",
            "source": "Energy Exchange",
            "last_updated": datetime.now().isoformat()
        }
    }

# MCP Tools using FastMCP decorators
@mcp.tool()
def get_weather_data(request: WeatherRequest) -> str:
    """
    Fetch current weather data for a specified location.
    
    Returns weather information with HomeGenie automation recommendations.
    """
    logger.info(f"Fetching weather data for: {request.location}")
    
    weather_data = get_mock_weather_data(request.location)
    
    # Format the weather data for readable output
    temp = weather_data["main"]["temp"]
    description = weather_data["weather"][0]["description"]
    humidity = weather_data["main"]["humidity"]
    wind_speed = weather_data["wind"]["speed"]
    
    result = f"""🌤️ Weather Data for {weather_data['name']}:
        
📊 Current Conditions:
• Temperature: {temp}°C
• Description: {description.title()}
• Humidity: {humidity}%
• Wind Speed: {wind_speed} m/s
• Pressure: {weather_data["main"]["pressure"]} hPa

🏠 HomeGenie Impact:
• Heating recommendation: {"Increase" if temp < 18 else "Maintain" if temp < 22 else "Decrease"}
• Natural lighting: {"Low - consider increasing indoor lighting" if "cloud" in description or "rain" in description else "Good"}
• Window management: {"Close windows" if "rain" in description else "Consider ventilation"}

📱 Raw Data: {json.dumps(weather_data, indent=2)}"""
    
    return result

@mcp.tool()
def get_energy_prices(request: EnergyRequest) -> str:
    """
    Fetch current energy prices per kWh with forecast data.
    
    Returns energy price information with smart home optimization recommendations.
    """
    logger.info(f"Fetching energy prices for region: {request.region}")
    
    price_data = get_mock_energy_prices(request.region)
    current = price_data["current_price"]
    
    result = f"""⚡ Energy Prices for {request.region}:
        
💰 Current Price:
• Price: €{current['price_per_kwh']}/kWh
• Period: {current['period'].replace('_', ' ').title()}
• Currency: {current['currency']}
• Last Updated: {price_data['timestamp'][:19]}

🏠 HomeGenie Recommendations:
• Period Type: {current['period'].replace('_', ' ').title()}
• Cost Impact: {"High cost - consider energy saving" if current['price_per_kwh'] > 0.35 else "Standard cost" if current['price_per_kwh'] > 0.20 else "Low cost - good time for energy-intensive tasks"}
• Smart Actions: {"Delay washing/heating" if current['period'] == 'peak' else "Good time for appliances" if current['period'] == 'off_peak' else "Normal usage"}"""

    if request.include_forecast:
        forecast = price_data.get("price_forecast", [])[:8]  # Next 8 hours
        result += "\n\n📈 Next 8 Hours Forecast:\n"
        for hour_data in forecast:
            result += f"• {hour_data['time']}: €{hour_data['price_per_kwh']}/kWh ({hour_data['period']})\n"
    
    result += f"\n\n📱 Raw Data: {json.dumps(price_data, indent=2)}"
    
    return result

# Main execution
if __name__ == "__main__":
    import uvicorn
    
    # For testing, you can also run the server directly
    logger.info("🏠 HomeGenie MCP Server starting...")
    logger.info("Available tools: get_weather_data, get_energy_prices")
    
    try:
        # Run the FastMCP server
        mcp.run()
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {e}")
        print(f"❌ Error starting server: {e}")
        print("\n💡 Try running the test version: python test_server.py")