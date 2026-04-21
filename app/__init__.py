import os
import sqlite3
from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
    app.config['DATABASE'] = os.path.join(app.instance_path, 'database.db')

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Register blueprints (imported here to avoid circular imports)
    from app.routes.main import main_bp
    from app.routes.auth import auth_bp
    from app.routes.event import event_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(event_bp)

    return app

def init_db():
    app = create_app()
    with app.app_context():
        db_path = app.config['DATABASE']
        schema_path = os.path.join(os.path.dirname(__file__), '..', 'database', 'schema.sql')
        
        # Connect to DB
        conn = sqlite3.connect(db_path)
        with open(schema_path, 'r', encoding='utf-8') as f:
            conn.executescript(f.read())
        conn.commit()
        conn.close()
        print("Database initialized successfully.")
