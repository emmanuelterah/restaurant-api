# Author Name

Author of Restaurant API is Emmanuel Nyaanga.

# Pizza Restaurant API

Welcome to the Pizza Restaurant API! This API allows you to manage pizza restaurants and their pizzas efficiently.

The Pizza Restaurant API is a robust and flexible tool designed to streamline the management of pizza restaurants and their menus. Built with Flask, SQLAlchemy, and Flask-CORS, this API offers a comprehensive set of endpoints for creating, updating, retrieving, and deleting restaurant and pizza information.


## Key Features:

- Restaurant Management: Easily manage restaurants by adding, updating, and deleting their details, including name, address, and contact information.
- Pizza Menu: Seamlessly handle pizza menus by creating, updating, and deleting pizzas associated with specific restaurants.
- Flexible Endpoints: The API provides endpoints for retrieving a list of all restaurants, details of a specific restaurant, and creating new restaurant-pizza associations.
- Error Handling: Comprehensive error handling ensures that users receive informative messages for invalid requests or server errors, enhancing the overall user experience.
- Scalability: Designed with scalability in mind, the API can accommodate future expansions and modifications to meet evolving business needs.
- Simple Setup: With clear documentation and easy setup instructions, getting started with the Pizza Restaurant API is quick and straightforward.

## Setup

- **Clone the repository:**
  - `git clone https://github.com/yourusername/pizza-restaurant-api.git`

- **Install dependencies:**
  - `pip install -r requirements.txt`

- **Set up the database:**
  - `python manage.py db init`
  - `python manage.py db migrate`
  - `python manage.py db upgrade`

- **Start the Flask server:**
  - `python app.py`

## Endpoints

### GET /restaurants

- **Method:** GET
- **Description:** Returns a list of all restaurants.

### GET /restaurants/{id}

- **Method:** GET
- **Description:** Returns details of a specific restaurant by ID.
- **Parameters:**
  - `id` (integer)

### POST /restaurant_pizzas

- **Method:** POST
- **Description:** Creates a new restaurant pizza entry.
- **Body Format:**
  ```json
  {
      "price": 12.99,
      "pizza_id": 1,
      "restaurant_id": 1
  }

### Additional Information
- **Error Handling:** The API returns appropriate error messages for invalid requests or server errors.

## License

This license belongs to Emmanuel Nyaanga.