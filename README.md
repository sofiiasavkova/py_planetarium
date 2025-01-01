"# py_planetarium" 
API service for planetarium management.

## Features
- JWT authenticated
- Managing tickets and reservations
- Creating Astronomy Shows with Show themes
- managing show sessions

## Technologies
- Django
- Django REST Framework
- PostgreSQL
- Docker

## Contributing
- Clone the repository:
   ```
   bash
   git clone https://github.com/sofiiasavkova/py_planetarium.git
   cd py_planetarium
  ```
- Create a virtual environment and install dependencies:
    ```
   python -m venv venv
   source venv/bin/activate  # For Linux/Mac
   venv\Scripts\activate     # For Windows
   pip install -r requirements.txt
   ```

- Set up the environment (create a .env file):
   ```
  cp .env.sample .env
   ```

- Apply migrations:
  ```
  python manage.py migrate
  ```
  
## Docker
install Docker first

docker-compose build
docker-compose up
