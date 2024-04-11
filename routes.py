

from flask import Flask, jsonify, request
from sqlalchemy.exc import IntegrityError
from models.pizza import Pizza
from models.restaurant import Restaurant
from models.restaurant_pizza import RestaurantPizza
from models.dbconfig import db
from flask_cors import CORS

def create_app():
    # Create the Flask app
    app = Flask(__name__)
    # Allow CORS for all routes
    CORS(app)
    app.config.from_object('config.Config')

    @app.route("/", methods=['GET'])
    def home():
        return 'Welcome to the Pizza Restaurant API!  For a list of restaurants, visit /restaurants. For a list of pizzas, go to /pizzas'

    @app.route('/restaurants', methods=['GET'])
    def get_restaurants():
        restaurants = Restaurant.query.all()
        output = [{'id': restaurant.id, 'name': restaurant.name, 'address': restaurant.address} for restaurant in restaurants]
        return jsonify(output)

    @app.route('/restaurants/<int:id>', methods=['GET'])
    def get_restaurant(id):
        restaurant = Restaurant.query.get(id)
        if restaurant:
            return jsonify({
                "id": restaurant.id,
                "name": restaurant.name,
                "address": restaurant.address,
                "pizzas": [
                    {"id": rp.pizza.id, "name": rp.pizza.name, "ingredients": rp.pizza.ingredients}
                    for rp in restaurant.pizzas
                ]
            })
        else:
            return jsonify({"error": "Restaurant not found"}), 404

    @app.route('/restaurants/<int:id>', methods=['DELETE'])
    def delete_restaurant(id):
        restaurant = Restaurant.query.get(id)
        if restaurant:
            # Alternatively, manually delete associated RestaurantPizza entries
            for pizza in restaurant.pizzas:
                db.session.delete(pizza)
            db.session.delete(restaurant)
            db.session.commit()
            return '', 204
        else:
            return jsonify({"error": "Restaurant not found"}), 404

    @app.route('/pizzas', methods=['GET'])
    def get_pizzas():
        pizzas = Pizza.query.all()
        output = [{'id': pizza.id, 'name': pizza.name, 'ingredients': pizza.ingredients} for pizza in pizzas]
        return jsonify(output)
    
    @app.route('/restaurant_pizzas', methods=['POST'])
    def create_restaurant_pizza():
        try:
            # Get JSON data from request body
            data = request.get_json()

            # Check if data is retrieved successfully
            if not data:
                raise ValueError("Request body is empty or not in JSON format")

            # Ensure all required keys are present in the JSON data
            required_keys = ['price', 'pizza_id', 'restaurant_id']
            if not all(key in data for key in required_keys):
                missing_keys = ', '.join(key for key in required_keys if key not in data)
                raise ValueError(f"Missing required key(s) in JSON data: {missing_keys}")
            
            # Convert data types and validate input
            try:
                price = float(data['price'])
                pizza_id = int(data['pizza_id'])
                restaurant_id = int(data['restaurant_id'])
            except ValueError:
                raise ValueError("Invalid data type for price, pizza_id, or restaurant_id")

            if not (1 <= price <= 30):
                raise ValueError("Price must be between 1 and 30")

            # Check if the record already exists
            existing_entry = RestaurantPizza.query.filter_by(pizza_id=pizza_id, restaurant_id=restaurant_id).first()
            if existing_entry:
                return jsonify({"error": "A restaurant_pizza with the same pizza and restaurant already exists"}), 400

            # Check if pizza and restaurant exist
            pizza = Pizza.query.get(pizza_id)
            restaurant = Restaurant.query.get(restaurant_id)
            if not (pizza and restaurant):
                return jsonify({"error": "Pizza or Restaurant not found"}), 404

            # Create restaurant pizza object
            restaurant_pizza = RestaurantPizza(price=price, pizza_id=pizza_id, restaurant_id=restaurant_id)
            db.session.add(restaurant_pizza)
            db.session.commit()

            # Return success message
            return jsonify({"success": "Restaurant pizza created successfully"}), 201
        except ValueError as ve:
            # Provide more specific message for JSON decode error
            if "Expecting value" in str(ve):
                return jsonify({"error": "Invalid JSON data format. Please check your request body."}), 400
            else:
                return jsonify({"error": str(ve)}), 400
        except IntegrityError:
            db.session.rollback()
            return jsonify({"error": "Database integrity error"}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return app

                