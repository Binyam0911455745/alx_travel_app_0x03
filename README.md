# ALX Travel App: API Development (0x01)

## Project Description
This project, `alx_travel_app_0x01`, focuses on building a robust RESTful API to manage travel listings and bookings. It's an extension of previous work, specifically implementing API views using Django REST Framework (DRF) for seamless CRUD (Create, Retrieve, Update, Delete) operations on `Listing` and `Booking` models.

## Key Features Implemented
-   **Django REST Framework Integration**: Utilizes DRF's `ModelViewSet` for efficient API development.
-   **Listings API**: Endpoints for managing travel `Listing` objects.
-   **Bookings API**: Endpoints for managing `Booking` transactions.
-   **RESTful URL Structure**: API endpoints are organized under a `/api/` prefix using DRF routers.
-   **Basic Authentication & Permissions**: Ensures secure access to API resources.
-   **API Documentation**: Integrated Swagger/OpenAPI documentation via `drf-yasg`.

## Setup and Installation

To get this project up and running locally, follow these steps:

1.  **Clone the Repository**:
    ```bash
    git clone [https://github.com/Binyam0911455745/alx_travel_app_0x01.git](https://github.com/Binyam0911455745/alx_travel_app_0x01.git)
    cd alx_travel_app_0x01/alx_travel_app # Navigate into the Django project root
    ```
    *(Note: Adjust `cd` command if your project structure is different after cloning)*

2.  **Create and Activate a Virtual Environment**:
    It's highly recommended to use a virtual environment to manage dependencies.
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Linux/macOS
    # On Windows: venv\Scripts\activate
    ```

3.  **Install Dependencies**:
    Install all required Python packages using pip.
    ```bash
    pip install django djangorestframework drf-yasg # Add other dependencies if you have them
    ```

4.  **Database Migrations**:
    Apply the database migrations to set up your database schema for `Listing` and `Booking` models.
    ```bash
    python manage.py makemigrations listings
    python manage.py migrate
    ```

5.  **Create a Superuser (Optional, for Admin Access & Testing)**:
    ```bash
    python manage.py createsuperuser
    ```

## Running the Development Server

Once set up, you can run the Django development server:

```bash
python manage.py runserver