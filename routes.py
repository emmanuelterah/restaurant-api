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
        data = request.json
        try:
            # Extract data from request
            price = float(data.get('price'))
            pizza_id = int(data.get('pizza_id'))
            restaurant_id = int(data.get('restaurant_id'))

            # Validate input (unchanged)
            if not (price and 1 <= price <= 30 and pizza_id and restaurant_id):
                return jsonify({"errors": ["Invalid input data"]}), 400

            # Check if pizza and restaurant exist (unchanged)
            pizza = Pizza.query.get(pizza_id)
            restaurant = Restaurant.query.get(restaurant_id)
            if not (pizza and restaurant):
                return jsonify({"errors": ["Pizza or Restaurant not found"]}), 404

                # Ensure valid restaurant_id before creating object (unchanged)
            if not restaurant_id:
                return jsonify({"errors": ["Restaurant ID cannot be empty"]}), 400

            # Additional validation for uniqueness (optional)
            # Check if the combination of pizza_id and restaurant_id already exists
            existing_pizza_restaurant = RestaurantPizza.query.filter_by(pizza_id=pizza_id, restaurant_id=restaurant_id).first()
            if existing_pizza_restaurant:
                return jsonify({"errors": ["This pizza already exists in the restaurant"]}), 400

            # Create restaurant pizza object (unchanged)
            restaurant_pizza = RestaurantPizza(price=price, pizza_id=pizza_id, restaurant_id=restaurant_id)
            db.session.add(restaurant_pizza)
            db.session.commit()

            # Return the created pizza details (unchanged)
            return jsonify({
                            'id': restaurant_pizza.id,
                            'price': restaurant_pizza.price,
                            'pizza_id': restaurant_pizza.pizza_id,
                            'restaurant_id': restaurant_pizza.restaurant_id
                        }), 201
        except ValueError:
            return jsonify({"errors": ["Invalid price or IDs"]}), 400
        except IntegrityError:
            db.session.rollback()
            return jsonify({"errors": ["Database integrity error"]}), 400

    return app

                