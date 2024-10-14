# Auto Control API 🚗

## Overview 📜

The Auto Control API is the backend part of a project aimed at providing comprehensive control over automotive-related expenses, user management, and vehicle tracking.

This project is developed collaboratively by a team of four: on the backend, [Karoline Trevizani](https://github.com/KarolTrevizani/auto_control_mobile_api), on the frontend [Rolf Matela](https://github.com/roollf) and [Emanuel Vidal](https://github.com/emanuelvidall), on the design [Fernando Custódio](https://github.com/Fcsla). The frontend can be found at [Frontend Repository URL](https://github.com/roollf/auto-control-mobile).

## Technical Stack 💻

- **Framework**: Django
- **API**: Django Rest Framework (DRF)
- **Database**: Configurable

## Environment Setup 🛠️

### Prerequisites

- Python 3.8 or newer
- pip (Python package installer)

Before starting, it is recommended to use a virtual environment to isolate project dependencies. This can be done using:

```bash
# Create the venv environment
python3 -m venv venv

# Activate the venv environment
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

After activating the virtual environment, install the project dependencies.

### Requirements File

The `requirements.txt` file contains all the necessary packages to run this project. Ensure you have this file in your project root and have run the command above to install these dependencies.

```bash
# Go to the dir where the requirements.txt are
pip install -r requirements.txt
```

## Configuration 🔧

### Environment Variables

_Go to the dir where the file .env.dist is (It stays in the project dir)_

To configure your project environment, copy the `.env.dist` file to `.env` in the same directory. Update this `.env` file with your specific configurations. The `.env.dist` file serves as a template outlining all necessary environment variables.

```bash
cp .env.dist .env
# Edit .env to fill in your specific settings
```

### Django Settings

This project uses two settings files for different environments:

- `development.py` for development settings
- `production.py` for production settings

To run the project using the correct settings, specify the settings module when executing Django commands. For example:

```bash
python manage.py runserver --settings=auto_control.settings.development
```

## Running the Application 🏃

Ensure you have correctly set up your `.env` file and activated your virtual environment. To start the server with development settings, use:

```bash
python manage.py runserver --settings=auto_control.settings.development
```

## Running Migrate 🗃️

When running the server you might see a warning:

```bash
You have X unapplied migration(s)...
```

To take advantage of Django's admin, auth, authtoken, content type, and sessions along with any models previously setup in any of your apps, you need to run the migrate script:

```bash
python manage.py migrate --settings=auto_control.settings.development
```

## Seeding Tables

To make the test easier, there are some tables that should be seeded. The following: `TypeVehicle`, `TypeExpense`, and `Brand`.
To seed, run the command below:
```shell
python manage.py seed --settings=auto_control.settings.development
```

## Project Structure 🏗️

The Auto Control API is built using Django Rest Framework (DRF) and contains three main apps:

- `expenses`: Handles all operations related to managing expenses.
- `users`: Manages user authentication, registration, and profiles.
- `vehicles`: Manages vehicle-related information and operations.

## API Endpoints 🌐

## Users APP 🧑‍💼

### Register User

- **URL:** `/register-user/`
- **Method:** `POST`
- **Permissions:** AllowAny (No authentication required for registration)
- **Body:**
  - `username`: The user's username.
  - `password`: The user's chosen password.
  - `email`: The user's email address.
  - `name`: The user's full name.
  - `cnh`: The user's CNH number (optional).
  - `type`: The user type (defaults to "General" if not specified).
- **Success Response:**
  - **Code:** 201 CREATED
  - **Content:** 
  ```json
  {
      "id": 1,
      "name": "John Doe",
      "username": "john@example.com",
      "email": "john@example.com",
      "cnh": "123456789",
      "type_name": "General"
  }
  ```
- **Error Response:**
  - **Code:** 309 Custom
  - **Content:** `{ "detail": "E-mail already registered." }`

### Note:

- This endpoint is designed to allow new users to register themselves in the system. It checks if the email provided is already registered to prevent duplicate accounts.
- The `cnh` field is optional and unique if provided. It's designed to store the user's driver's license number.
- If an email is already registered, the API responds with a custom status code (309) indicating that the email is already in use.

### Authentication 🔑


- **Login**
  - **Endpoint:** `/login/`
  - **Method:** POST
  - **Parameters:**
    - `username` (string): Username (email) of the user.
    - `password` (string): Password for the user.
  - **Sample Response:**
  ```json
  {
      "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
      "user_id": 1,
      "email": "john@example.com",
      "user_name": "John Doe",
      "user_cnh": "123456789"
  }
  ```

- **Request Password Reset:**
  - **Endpoint:** `/request-reset-password/`
  - **Method:** POST
  - **Body:**
    - `email`: The email address associated with the user account.
  - **Description:** This endpoint sends a password reset email to the user if an account with the given email exists. It includes a token and instructions on how to reset their password.
  - **Sample Request:**
    ```json
    {
      "email": "john@example.com"
    }
    ```
  - **Sample Response:**
    - **Code:** 200 OK
    - **Content:** `{ "message": "If an account with this email was found, we have sent an email with instructions to reset your password." }`

- **Reset Password:**
  - **Endpoint:** `/reset-password/`
  - **Method:** POST
  - **Body:**
    - `token`: Password reset token sent via email.
    - `new_password`: New password for the account.
  - **Description:** This endpoint allows a user to reset their password using a valid reset token. The token must not be expired and should be linked to a user account.
  - **Sample Request:**
    ```json
    {
      "token": "123e4567-e89b-12d3-a456-426614174000",
      "new_password": "newpassword123"
    }
    ```
  - **Sample Response:**
    - **Code:** 200 OK
    - **Content:** `{ "message": "Your password has been reset successfully." }`
  - **Error Response:**
    - **Code:** 400 BAD REQUEST
    - **Content:** `{ "error": "Invalid or expired token." }`

- **Change Password:**
  - **Endpoint:** `/change-password/`
  - **Method:** PUT
  - **Body:**
    - `old_password`: Current password of the user.
    - `new_password`: New password to replace the old one.
  - **Description:** Allows authenticated users to change their password. The user must provide their current password for verification.
  - **Sample Request:**
    ```json
    {
      "old_password": "oldpassword123",
      "new_password": "newpassword123"
    }
    ```
  - **Sample Response:**
    - **Code:** 204 NO CONTENT
    - **Content:** `null`
  - **Error Response:**
    - **Code:** 400 BAD REQUEST
    - **Content:** `{ "old_password": ["Wrong password."] }`

## Vehicles APP 🚘

### Vehicles

#### **Create Vehicle**
- **Endpoint:** `/api/v1/app-vehicles/vehicles/`
- **Method:** POST
- **Parameters:**
  - `name` (string): Name of the vehicle.
  - `description` (string, optional): Description of the vehicle.
  - `type` (integer): ID of the vehicle type.
  - `brand` (integer): ID of the vehicle brand.
  - `owner` (integer): ID of the owner (user) of the vehicle.
  - `year` (integer, optional): Year of the vehicle.
  - `license_plate` (string, optional): License plate of the vehicle
  - `images` (A list of file, optional): Images of the vehicle.

#### **Get Vehicle**
- **Endpoint:** `/api/v1/app-vehicles/vehicles/`
- **Method:** GET
- **Sample Response:**
```json
{
    "id": 1,
    "name": "Toyota Camry",
    "owner": 1,
    "owner_name": "John Doe",
    "description": "A comfortable sedan.",
    "type": 1,
    "type_name": "Sedan",
    "brand": 1,
    "year": 1997,
    "license_plate": "SDR345-09"
    "brand_name": "Toyota",
    "images": [
        {"id": 1, "vehicle": 1, "image": "http://example.com/media/images_vehicles/toyota_camry_1.jpg"},
        {"id": 2, "vehicle": 1, "image": "http://example.com/media/images_vehicles/toyota_camry_2.jpg"}
    ],
    "expenses": [
        {
            "id": 1,
            "name": "Oil Change",
            "vehicle": 1,
            "vehicle_name": "Toyota Camry",
            "description": "Regular maintenance",
            "type": 1,
            "type_name": "Maintenance",
            "file": "http://example.com/media/expenses/oil_change_receipt.pdf",
            "created_at": "2024-04-14T12:00:00Z"
        }
    ],
    "created_at": "2024-04-14T12:00:00Z"
}
```

#### **Update/Delete Vehicle**
- **Endpoint:** `/api/v1/app-vehicles/vehicles/<vehicle_id>/`
- **Method:** PATCH/PUT/DELETE
  - Update images by including new ones in PUT/PATCH request using multipart/form-data.

### VehiclesImages 📸

- **Endpoint:** `/api/v1/app-vehicles/vehicles-images/`
- **Method:** POST
- **Parameters:**
  - `vehicle` (integer): ID of the vehicle.
  - `image` (file): File of the image.

- **List/Create VehiclesImages:** GET/POST/ `/api/v1/app-vehicles/vehicles-images/`
- **Update/Delete VehiclesImages:** PATCH/PUT/DELETE `/api/v1/app-vehicles/vehicles-images/<image_id>`

### Brands 🏷️

- **List/Create Brands:** GET/POST/PATCH/PUT `/api/v1app-vehicles/brands/`
- **Update Brands:** PATCH/PUT `/api/v1app-vehicles/brands/<brand_id>`
- **Parameters:**
  - `name` (string): Brand name.

### TypeVehicle 🏷️

- **List/Create Types:** GET/POST/PATCH/PUT `/api/v1app-vehicles/types/`
- **Update Types:** PATCH/PUT `/api/v1app-vehicles/types/<type_id>`
- **Parameters:**
  - `name` (string): Vehicle type name.


## Expenses APP 📉

### Expenses

#### **Create Expense**
- **Endpoint:** `/api/v1/app-expenses/expenses/`
- **Method:** POST
- **Parameters:**
  - `name` (string): Name of the expense.
  - `vehicle` (integer): ID of the vehicle associated with the expense.
  - `description` (string, optional): Description of the expense.
  - `type` (integer): ID of the expense type.
  - `file` (file, optional): Receipt or file related to the expense.

#### **Get Expenses**
- **Endpoint:** `/api/v1/app-expenses/expenses/`
- **Method:** GET
- **Query Parameters:**
  - `user`: User ID (integer) - optional parameter to filter results by user.
  - `/api/v1/app-expenses/expenses?user={user_id}`
- **Sample Response:**
```json
[
    {
        "id": 1,
        "name": "Multa AMC",
        "value": "0.00",
        "date": "2024-05-03",
        "vehicle": 1,
        "vehicle_name": "HRV",
        "description": "Estacionamento irregular",
        "type": 1,
        "type_name": "Multa",
        "file": "http://127.0.0.1:8000/media/integracao.pdf",
        "created_at": "2024-04-12T23:34:07.875951Z"
    },
    ...
]
```

#### **Update/Delete Expense**
- **Endpoint:** `/api/v1/app-expenses/expenses/<expense_id>/`
- **Method:** PATCH/PUT/DELETE

#### **Get Summary of Expenses**

- **Endpoint:** `/api/v1/app-expenses/summary`
- **Method:** GET
- **Description:** Provides comprehensive summaries of expenses including averages, totals, and upcoming expenses. This read-only viewset is accessible to all users and does not require authentication. It uses Django filters for filtering data based on the query parameters.
- **Query Parameters:**
  - `user`: User ID (integer) - optional parameter to filter results by user.
  - `/api/v1/app-expenses/summary?user={user_id}`
- **Sample Response:**
  ```json
  {
    "average_value_of_expenses_by_month": 200.00,
    "total_of_expense_last_six_months": 1200.00,
    "total_of_expenses": 2400.00,
    "date_of_the_next_expense": "2024-06-15",
    "future_expenses": 300.00
  }
  ```
  If there isn't any expense on the future, returns "-" and 0.00
  ```json
    {
    "average_value_of_expenses_by_month": 47.55,
    "total_of_expense_last_six_months": 570.6,
    "total_of_expenses": 570.6,
    "date_of_the_next_expense": "-",
    "future_expenses": 0.0
  }
  ```

#### **Get Summary of Expenses by Type**

- **Endpoint:** `/api/v1/app-expenses/summary-by-type`
- **Method:** GET
- **Description:** Provides a summary of expenses grouped by vehicle owner and type. This read-only viewset is accessible to all users and does not require authentication. It uses Django filters for filtering data based on the query parameters.
- **Query Parameters:**
  - `user`: User ID (integer) - optional parameter to filter results by user.
  - `/api/v1/app-expenses/summary-by-type?user={user_id}`
- **Sample Response:**
  ```json
  [
    {
      "vehicle__owner__id": 1,
      "type__name": "Abastecimento",
      "total": 1500.00
    },
    {
      "vehicle__owner__id": 2,
      "type__name": "Imposto",
      "total": 300.00
    }
  ]
  ```

## Contributing 🤝

This project is currently being developed by Karoline Trevizani, Rolf Matela, Emanuel Vidal, and Fernando Custódio. Contributions, bug reports, and feature requests are welcome.