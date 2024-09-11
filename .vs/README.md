# Investment Account Management API

## Project Overview

This project aims to create a Django Rest Framework (DRF) API for managing investment accounts. The API will allow multiple users to belong to an investment account and also allow a user to belong to multiple investment accounts. The project includes the following requirements:

### Requirements

1. **User Permissions**:
    - Extend the User and Django model permissions so that a user can have multiple investment accounts, each with different levels of access:
        - **Investment Account 1**: The user should only have view rights and should not be able to make transactions.
        - **Investment Account 2**: The user should have full CRUD (Create, Read, Update, Delete) permissions.
        - **Investment Account 3**: The user should only be able to post transactions, but not view them.

2. **Admin Endpoint**:
    - Create an admin endpoint that returns all of a user's transactions, along with a nested sum of the user's total balance.
    - This endpoint should include a date range filter to retrieve transactions that occurred within a specified date range.

3. **Unit Tests**:
    - Write unit tests to validate the functionality of the APIs.

### Project Structure

- **Models**: Define the `User`, `InvestmentAccount`, and `UserInvestmentAccount` models to establish the many-to-many relationship between users and investment accounts.
- **Serializers**: Create serializers for the models to handle data validation and serialization.
- **Views**: Implement views to handle CRUD operations for users and investment accounts, as well as the admin endpoint.
- **URLs**: Define URL patterns to route requests to the appropriate views.
- **Unit Tests**: Write unit tests to ensure the API functions as expected.

### Installation

1. **Clone the repository**:
    ```sh
    git clone <repository_url>
    cd <repository_directory>
    ```

2. **Create a virtual environment**:
    ```sh
    python -m venv myenv
    source myenv/bin/activate  # On Windows use `myenv\Scripts\activate`
    ```

3. **Install dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

4. **Apply migrations**:
    ```sh
    python manage.py makemigrations
    python manage.py migrate
    ```

5. **Run the server**:
    ```sh
    python manage.py runserver
    ```

### Usage

- **Register a User**:
    - Endpoint: `POST /register/`
    - Request Body:
        ```json
        {
            "email": "newuser@example.com",
            "password": "newpassword123"
        }
        ```

- **Admin Endpoint**:
    - Endpoint: `GET /admin/user-transactions/<user_id>/`
    - Query Parameters:
        - `start_date`: Start date for the date range filter.
        - `end_date`: End date for the date range filter.

### Unit Tests

- Run unit tests to validate the functionality of the APIs:
    ```sh
    python manage.py test
    ```

### Conclusion

This project provides a robust API for managing investment accounts with flexible user permissions and an admin endpoint for transaction management. The implementation includes comprehensive unit tests to ensure the reliability of the API.