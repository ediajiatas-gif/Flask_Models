from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Date, Float, Table, Column, ForeignKey, Integer
from datetime import date

app = Flask(__name__) 
# Main class from Flask library
# app variable becomes Flask application object
# What is Flask: tool that build/run websites / web apps using Python

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
# Tells Flask app where database is located

class Base(DeclarativeBase):
    pass
#Created our Base Class

db = SQLAlchemy(model_class = Base)
#creating connection between Flask and DB using SQLALCHEMY
#makes db "tool to talk to database and create tables"

db.init_app(app)

#Association Table
ticket_mechanics = Table(
    'ticket_mechanics',
    Base.metadata,
    Column('service_ticket_id', Integer, ForeignKey('service_tickets.id')),
    Column('mechanic_id', Integer, ForeignKey('mechanics.id'))
)

class Customers(Base):
    __tablename__ = 'customers'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(250), nullable=False)
    last_name: Mapped[str] = mapped_column(String(250), nullable=False)
    email: Mapped[str] = mapped_column(String(350), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(String(150), nullable=False)
    address: Mapped[str] = mapped_column(String(500), nullable=True)

    customer_service_ticket: Mapped['Service_tickets'] = relationship('Service_tickets', back_populates='service_ticket_customer')

class Service_tickets(Base):
    __tablename__ = 'service_tickets'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey('customers.id'))
    service_desc: Mapped[str] = mapped_column(String(500), nullable=False)
    vin: Mapped[str] = mapped_column(String(30), nullable=False)
    service_date: Mapped[date] = mapped_column(Date, nullable=False)
    price: Mapped[float] = mapped_column(Float)

    service_ticket_customer: Mapped['Customers'] = relationship('Customers', back_populates='customer_service_ticket')   
    
    service_ticket_mechanic: Mapped['Mechanics'] = relationship('Mechanics', secondary='ticket_mechanics', back_populates='mechanic_service_ticket')
    
class Mechanics(Base):
    __tablename__ = 'mechanics'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(250), nullable=False)
    last_name: Mapped[str] = mapped_column(String(250), nullable=False)
    email: Mapped[str] = mapped_column(String(350), nullable=False, unique=True)
    address: Mapped[str] = mapped_column(String(500), nullable=True)
    salary: Mapped[float] = mapped_column(Float)
    
    mechanic_service_ticket: Mapped['Service_tickets'] = relationship('Service_tickets', secondary='ticket_mechanics', back_populates='service_ticket_mechanic')
    
with app.app_context():
    db.create_all()
#creates all our tables 
    
app.run()
#Runs our Flask app