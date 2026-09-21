from sqlalchemy import create_engine, Column, String, Integer, Boolean, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy_utils.types import ChoiceType

# cria a conexão do seu banco
db = create_engine("sqlite:///database.db")

# cria a base do banco, ele permite criar uma tabela no banco e faz a tradução de uma classe do python para uma tabela no banco, por isso precisa usar ela de parâmetro ao criar as classes
Base = declarative_base()

# criar as classes/tabelas do banco

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


# Pedido
class Order(Base):
    __tablename__ = "orders"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    status = Column("status", String) # pending, canceled, completed
    user_id = Column("user_id", ForeignKey("users.id"))
    price = Column("price", Float)
    items = relationship("OrderItem", cascade="all, delete") # if you delete an order, it also deletes all order items related to that order

    def __init__(self, user_id, status="PENDING", price=0):
        self.user_id = user_id
        self.status = status
        self.price = price

    def calculate_price(self):

        # order_price = 0
        # for item in self.items:
        #     item_price = item.unit_price * item.quantity
        #     order_price += item_price

        self.price = sum(item.unit_price * item.quantity for item in self.items) # list comprehension


# ItensPedido
class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    quantity = Column("quantity", Integer)
    flavor = Column("flavor", String)
    size = Column("size", String)
    unit_price = Column("unit_price", Float)
    order = Column("order", ForeignKey("orders.id"))

    def __init__(self, quantity, flavor, size, unit_price, order):
        self.quantity = quantity
        self.flavor = flavor
        self.size = size
        self.unit_price = unit_price
        self.order = order

# executa a criação dos metadados do seu banco (cria efetivamente o banco de dados)
# Base.metadata.create_all(db)

# migrate database
# create migration: alembic revision --autogenerate -m "message"
# execute migration: alembic upgrade head
