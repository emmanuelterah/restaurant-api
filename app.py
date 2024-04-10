# from flask import Flask
# from flask_migrate import Migrate
# from routes import create_app
# from models.dbconfig import db

# # Create the Flask app instance
# app = create_app()

# # Configure database URI and track modifications
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pizza.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# # Initialize Flask-Migrate with the Flask app and SQLAlchemy db instance
# migrate = Migrate(app, db)

# if __name__ == '__main__':
#     app.run(debug=True, port=5000)

from flask import Flask
from flask_cors import CORS
from models.dbconfig import db
from routes import create_app
from flask_migrate import Migrate

app = create_app()
app.config.from_object('config.Config')
CORS(app)
db.init_app(app)
migrate = Migrate(app, db)


@app.cli.command("seed_db")
def seed_db_command():
    """Seeds the database with initial data."""
    from seed import seed_data
    seed_data()
    print("Database seeded.")
    
if __name__ == '__main__':
    app.run(debug=True, port=5000)