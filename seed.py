from models import MenuItem, db
from sqlalchemy.orm import Session

session = Session(db)

items = [
    # Marguerita
    MenuItem("Marguerita", "pizza", "pequena", 28, True),
    MenuItem("Marguerita", "pizza", "média", 42, True),
    MenuItem("Marguerita", "pizza", "grande", 56, True),
    MenuItem("Marguerita", "pizza", "família", 70, True),

    # Calabresa
    MenuItem("Calabresa", "pizza", "pequena", 30, True),
    MenuItem("Calabresa", "pizza", "média", 45, True),
    MenuItem("Calabresa", "pizza", "grande", 60, True),
    MenuItem("Calabresa", "pizza", "família", 75, True),

    # Portuguesa
    MenuItem("Portuguesa", "pizza", "pequena", 32, True),
    MenuItem("Portuguesa", "pizza", "média", 48, True),
    MenuItem("Portuguesa", "pizza", "grande", 64, True),
    MenuItem("Portuguesa", "pizza", "família", 80, True),

    # Quatro Queijos
    MenuItem("Quatro Queijos", "pizza", "pequena", 34, True),
    MenuItem("Quatro Queijos", "pizza", "média", 51, True),
    MenuItem("Quatro Queijos", "pizza", "grande", 68, True),
    MenuItem("Quatro Queijos", "pizza", "família", 85, True),

    # Frango com Catupiry
    MenuItem("Frango com Catupiry", "pizza", "pequena", 35, True),
    MenuItem("Frango com Catupiry", "pizza", "média", 52, True),
    MenuItem("Frango com Catupiry", "pizza", "grande", 69, True),
    MenuItem("Frango com Catupiry", "pizza", "família", 87, True),

    # Bebidas
    MenuItem("Coca-Cola", "bebida", "2L", 10, True),
    MenuItem("Guaraná", "bebida", "2L", 10, True),
]

session.add_all(items)
session.commit()

print("Cardápio criado com sucesso!")
