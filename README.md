# Nobel Prize Search API

This is a FastAPI-based application that provides a RESTful API for searching
Nobel Prize winners by name, category, or description (motivation).
The data is ingested from the Nobel Prize API and stored in MongoDB for fast 
search operations, including fuzzy matching for name searches.

## Features

- **Search by Name**: Supports partial and fuzzy name matches.
- **Search by Category**: Find laureates by prize categories (e.g., Physics, Chemistry).
- **Search by Description**: Search laureates based on the reason for their prize.
- **Data Ingestion**: Automatically fetches Nobel Prize data from an external API and stores it in MongoDB.
- **Tests**: Unit tests for ingestion and API search functionalities.

## Requirements

Make sure you have the following installed:

- **Docker** and **Docker Compose**: To run the application and MongoDB.
- **Python 3.x** (locally for development, if needed).

### Getting Started

## Clone the repository

```bash
git clone https://github.com/TimothyBenger/nobel_search.git
cd nobel_search
```

### Environment Configuration

Make sure you have a `.env` file to provide necessary environment variables. A sample `.env` might look like:

```bash
MONGO_URI=mongodb://mongodb:27017/nobel_db
NOBEL_API_URL=https://api.nobelprize.org/v1/prize.json
```

### Build and Run the Application

The application runs inside Docker containers, managed by Docker Compose. To build and run the application, use the following commands:

```bash
docker-compose up --build
```

This will start:

    MongoDB on port 27017.
    FastAPI on port 8000.

Once the app is running, you can access the API documentation at http://localhost:8000/docs to interact with the API through the automatically generated Swagger UI.

### Running the Tests

To run the tests inside the Docker environment, use the following command:

```bash
docker-compose up test
```

This will spin up the test container and run the suite of unit tests, including:

    Data ingestion tests: Ensures data is ingested correctly into MongoDB.
    Search API tests: Verifies the search functionalities (name, category, description) are working as expected.

## API Endpoints

    Search by Name:
        Endpoint: /search/name/?name={name}
        Example: http://localhost:8000/search/name/?name=Albert
    Search by Category:
        Endpoint: /search/category/?category={category}
        Example: http://localhost:8000/search/category/?category=physics
    Search by Description:
        Endpoint: /search/description/?description={description}
        Example: http://localhost:8000/search/description/?description=photoelectric effect

Notes

    Fuzzy Name Search: The API uses FuzzyWuzzy to allow partial name matches, so searches like "Albret Enstein" will return "Albert Einstein" as a match.
    MongoDB Persistence: MongoDB uses anonymous volumes, so data will persist across container restarts, but will not be accessible directly from the host filesystem.
