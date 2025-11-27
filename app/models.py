from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Date, Column, ForeignKey, Table, Integer, Float
from datetime import date

# Create a base class for our models
class Base(DeclarativeBase):
  pass
  # you could add your own configuration

db = SQLAlchemy(model_class = Base)

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
    customer_id: Mapped[int] = mapped_column(ForeignKey('customers.id')) #nullable=True for testing
    service_desc: Mapped[str] = mapped_column(String(500), nullable=False)
    vin: Mapped[str] = mapped_column(String(30), nullable=False)
    service_date: Mapped[date] = mapped_column(Date, nullable=False)
    price: Mapped[float] = mapped_column(Float)

    service_ticket_customer: Mapped['Customers'] = relationship('Customers', back_populates='customer_service_ticket')   
    
    service_ticket_mechanic: Mapped[list['Mechanics']] = relationship('Mechanics', secondary='ticket_mechanics', back_populates='mechanic_service_ticket')
    
class Mechanics(Base):
    __tablename__ = 'mechanics'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(250), nullable=False)
    last_name: Mapped[str] = mapped_column(String(250), nullable=False)
    email: Mapped[str] = mapped_column(String(350), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(250), nullable=False)
    address: Mapped[str] = mapped_column(String(500), nullable=True)
    salary: Mapped[float] = mapped_column(Float)
    
    mechanic_service_ticket: Mapped[list['Service_tickets']] = relationship('Service_tickets', secondary='ticket_mechanics', back_populates='service_ticket_mechanic')