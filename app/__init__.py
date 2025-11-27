from flask import Flask
from .models import db
from .extensions import ma, limiter, cache
from .blueprints.mechanics import mechanics_bp
from .blueprints.service_tickets import service_tickets_bp
from .blueprints.customers import customers_bp

def create_app(config_name):
  app = Flask(__name__)
  app.config.from_object(f'config.{config_name}')

  # Initialize my extension onto my Flask app
  db.init_app(app) #adding the db to the app
  ma.init_app(app)
  limiter.init_app(app)
  cache.init_app(app)

  #Register blueprints
  app.register_blueprint(mechanics_bp, url_prefix='/mechanics')
  app.register_blueprint(service_tickets_bp, url_prefix='/service_tickets')
  app.register_blueprint(customers_bp, url_prefix="/customers")


  return app