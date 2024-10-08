# IT Company Task Manager

## Overview
The IT Company Task Manager is a web application designed to help manage tasks, workers, projects, and teams within an IT company. This application is built using Django and provides a range of functionalities including user authentication, task assignment, and project management.

## Check it out!

[IT task manager deployed to Render](https://company-manager-oafg.onrender.com)

You can evaluate different functionality of this project by logining to different user entities:

Admin | Username: admin | Password: Password11

User | Username: user | Password: User11__

## Features
- User authentication and management
- Task creation, assignment, and management
- Project creation and management
- Team management
- Different permissions based on user positions (e.g., managers can add new workers)

## Technologies Used
- Python
- Django
- Django Crispy Forms
- Bootstrap
- SQLite (default, can be replaced with PostgreSQL, MySQL, etc.)

## Models
The application includes the following models:
- **TaskType**: Represents the type of tasks (e.g., Bug, Feature)
- **Position**: Represents the position of workers (e.g., Manager, Developer)
- **Tag**: Represents tags that can be associated with tasks
- **Project**: Represents projects within the company
- **Team**: Represents teams within the company
- **Worker**: Represents the workers/users of the application
- **Task**: Represents tasks assigned to workers

## Installation

### Prerequisites
- Python 3.x
- Django 3.x or higher
- pip (Python package installer)

### Steps
1. **Clone the repository:**
    ```sh
    git clone <repository-url>
    cd company-task-manager
    ```

2. **Create a virtual environment:**
    ```sh
    python -m venv venv
    ```

3. **Activate the virtual environment:**
    - On Windows:
      ```sh
      venv\Scripts\activate
      ```
    - On macOS/Linux:
      ```sh
      source venv/bin/activate
      ```

4. **Install the dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

5. **Run migrations:**
    ```sh
    python manage.py makemigrations
    python manage.py migrate
    ```

6. **Load initial data:**

    To load the initial data into your database, use the following command:

    ```sh
    python manage.py loaddata company_task_manager_db_data.json
    ```

7. **Run the development server:**

    ```sh
    python manage.py runserver
    ```

8. **Access the application:**

    Open your web browser and go to `http://127.0.0.1:8000`.

## Running Tests

To run the tests, use the following command:

```sh
python manage.py test