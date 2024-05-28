# UniVerse Alumni Mapping Project


## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/UniVerse_backend.git
    cd UniVerse_backend
    ```

2. Create a virtual environment:
    ```bash
    python -m venv venv
    ```
    ```or bash
    virtualenv venv    
    ```

3. Activate the virtual environment:
    - On Windows:
        ```bash
        venv\Scripts\activate
        ```
    - On Unix or MacOS:
        ```bash
        source venv/bin/activate
        ```

4. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

5. Apply migrations:
    ```bash
    python manage.py migrate
    ```

6. Create a superuser:
    ```bash
    python manage.py createsuperuser
    ```
    Then navigate to the admin panel.

7. Run the development server:
    ```bash
    python manage.py runserver
    ```

8. Open your browser and navigate to [http://127.0.0.1:8000/](http://127.0.0.1:8000/) to access the application.


