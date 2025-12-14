# Weather API

## Overview
The Weather API is a robust and scalable application designed to provide weather data and forecasts. It utilizes a PostgreSQL database to store weather information and offers a RESTful interface for easy access to this data.

## Features
- **Weather Data Retrieval**: Access current weather conditions and forecasts.
- **User Authentication**: Secure access to user-specific data.
- **Historical Data**: Retrieve past weather data for analysis.

## Technologies Used
- **Python**: The primary programming language for the application.
- **Flask**: A lightweight WSGI web application framework for building the API.
- **PostgreSQL**: A powerful, open-source object-relational database system.
- **Docker**: For containerization and easy deployment.

## Getting Started
To get started with the Weather API, follow these steps:

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd weather-api
   ```

2. **Set Up Environment Variables**:
   Create a `.env` file in the root directory and define the necessary environment variables, including database connection details.

3. **Build and Run the Application**:
   Use Docker to build and run the application:
   ```bash
   docker-compose up --build
   ```

4. **Access the API**:
   The API will be available at `http://localhost:5000`.

## Documentation
For detailed documentation, visit [Weather API Documentation](https://weatherapi.lat).

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
