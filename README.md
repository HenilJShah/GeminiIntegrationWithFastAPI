# Sample Papers API

This project is a FastAPI application that provides an API for managing sample papers. It allows users to create, retrieve, update, and delete sample papers and extract text from files. The application uses MongoDB as the database and Redis for caching.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
- [API Endpoints](#api-endpoints)
- [Models](#models)
- [Running the Application](#running-the-application)

## Features

- Create, retrieve, update, and delete sample papers.
- Upload and extract text from various file types (e.g., PDFs).
- Task management for tracking extraction processes.
- Caching of retrieved sample papers using Redis.

## Technologies Used

- **FastAPI**: A modern, fast (high-performance), web framework for building APIs with Python.
- **MongoDB**: A NoSQL database to store sample papers and task information.
- **Redis**: An in-memory data structure store, used for caching.
- **Pydantic**: Data validation and settings management using Python type annotations.
- **Motor**: An asynchronous MongoDB driver for Python.

## Project Structure

```
sample_papers_api/
│
├── main.py                # Entry point of the FastAPI application.
├── models/
│   ├── paper_model.py     # Pydantic models for request/response validation.
│   └── ...
├── routes/
│   ├── paper_routes.py    # API routes for sample papers.
│   └── ...
├── config/
│   ├── db_config.py       # Database configuration and initialization.
│   └── ...
├── helper/
│   ├── helper.py          # Helper functions and utilities.
│   └── ...
└── ai_models/
    ├── ai_api_integration/
    │   ├── geminiApi.py   # AI API integration for file processing.
    │   └── ...
```

## Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your_username/sample_papers_api.git
   cd sample_papers_api
   ```

2. **Create a Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up MongoDB and Redis**
   - Ensure that MongoDB is running on `localhost:27017`.
   - Ensure that Redis is running on `localhost:6379`.

## API Endpoints

### 1. Create Sample Paper

- **Endpoint**: `POST /paper`
- **Request Body**: 
  ```json
  {
      "title": "Sample Paper Title",
      "type": "mock",
      "time": 120,
      "marks": 100,
      "params": {
          "board": "CBSE",
          "grade": 10,
          "subject": "Mathematics"
      },
      "tags": ["math", "sample"],
      "chapters": ["Chapter 1", "Chapter 2"],
      "sections": [
          {
              "marks_per_question": 5,
              "type": "default",
              "questions": [
                  {
                      "question": "What is 2 + 2?",
                      "answer": "4",
                      "type": "short",
                      "question_slug": "what-is-2-plus-2",
                      "reference_id": "ref_1"
                  }
              ]
          }
      ]
  }
  ```
- **Response**:
  - **Status 200**: 
  ```json
  {
      "code": 200,
      "status": "success",
      "message": "Sample paper created successfully",
      "data": {
          "paper_id": "some-uuid"
      }
  }
  ```

### 2. Get Sample Paper

- **Endpoint**: `GET /papers/{p_id}`
- **Response**:
  - **Status 200**: 
  ```json
  {
      "code": 200,
      "status": "success",
      "message": "Paper retrieved",
      "data": { ... }  // Paper details
  }
  ```

### 3. Update Sample Paper

- **Endpoint**: `PUT /papers/{p_id}`
- **Request Body**: Similar structure to create paper with the fields to update.
- **Response**:
  - **Status 200**: 
  ```json
  {
      "code": 200,
      "status": "success",
      "message": "Paper updated successfully",
      "data": { ... }  // Updated paper details
  }
  ```

### 4. Delete Sample Paper

- **Endpoint**: `DELETE /papers/{p_id}`
- **Response**:
  - **Status 200**: 
  ```json
  {
      "code": 200,
      "status": "success",
      "message": "Paper deleted successfully"
  }
  ```

### 5. Extract Text from File

- **Endpoint**: `POST /extract/text`
- **Request**: Multipart file upload.
- **Response**:
  - **Status 202**: 
  ```json
  {
      "code": 202,
      "status": "processing",
      "message": "Extraction started",
      "data": {
          "task_id": "some-uuid"
      }
  }
  ```

### 6. Get Task Status

- **Endpoint**: `GET /tasks/{task_id}`
- **Response**:
  - **Status 200**: 
  ```json
  {
      "code": 200,
      "status": "success",
      "message": "Task status retrieved",
      "data": {
          "status": "completed"
      }
  }
  ```

## Running the Application

To run the application, use the following command:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Your FastAPI application will be accessible at `http://localhost:8000`.

## License

This project is licensed under the MIT License.
