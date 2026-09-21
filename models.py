from sqlalchemy import create_engine, Column, String, Integer, Boolean, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy_utils.types import ChoiceType

db = create_engine("sqlite:///database.db")

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column("id", Integer, primary_key=True, autoincrement=True) # cria a coluna no banco de dados do id, que precisa do parâmetro de primary key que diz que ele é único e o autoincrement que automaticamente preenche com um número que vai aumentando
    name = Column("name", String)
    email = Column("email", String, nullable=False)
    password = Column("password", String)
    active = Column("active", Boolean)
    admin = Column("admin", Boolean, default=False)

    def __init__(self, name, email, password, active=True, admin=False): # Isso define o que o código espera que eu passe de informação quando for criar um usuário
        self.name = name
        self.email = email
        self.password = password
        self.active = active
        self.admin = admin


class Order(Base):
    __tablename__ = "orders"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    status = Column("status", String) # pending, canceled, completed
    user_id = Column("user_id", ForeignKey("users.id"))
    price = Column("price", Float)
    items = relationship("OrderItem", cascade="all, delete")

    def __init__(self, user_id, status="PENDING", price=0):
        self.user_id = user_id
        self.status = status
        self.price = price

    def calculate_price(self):

        self.price = sum(item.unit_price * item.quantity for item in self.items) # list comprehension


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    quantity = Column("quantity", Integer)
    unit_price = Column("unit_price", Float)
    menu_item_id = Column("menu_item_id", ForeignKey("menu_items.id"))
    order_id = Column("order_id", ForeignKey("orders.id"))

    def __init__(self, quantity, unit_price, menu_item_id, order_id):
        self.quantity = quantity
        self.unit_price = unit_price
        self.menu_item_id = menu_item_id
        self.order_id = order_id


class MenuItem(Base):
    __tablename__= "menu_items"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("name", String)
    category = Column("category", String)
    size = Column("size", String)
    price = Column("price", Float)
    available = Column("available", Boolean)

    def __init__(self, name, category, size, price, available):
        self.name = name
        self.category = category
        self.size = size
        self.price = price
        self.available = available


# Base.metadata.create_all(db)

# migrate database
# create migration: alembic revision --autogenerate -m "message"
# execute migration: alembic upgrade head
