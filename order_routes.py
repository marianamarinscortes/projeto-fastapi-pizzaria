from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import get_session, verify_token
from schemas import OrderItemSchema, ResponseOrderSchema
from models import Order, User, OrderItem, MenuItem
from typing import List

order_router = APIRouter(prefix="/orders", tags=["orders"], dependencies=[Depends(verify_token)])

@order_router.post("/create-order", 
                   summary="Criar um novo pedido", 
                   description="Cria um novo pedido para o usuário autenticado.")
async def create_order(session: Session = Depends(get_session), user: User = Depends(verify_token)):
    new_order = Order(user_id=user.id)
    session.add(new_order)
    session.commit()
    return {"message": f"Pedido criado com sucesso. ID do pedido: {new_order.id}"}


@order_router.post("/cancel-order/{order_id}", 
                   summary="Cancelar um pedido", 
                   description="Cancela um pedido pertencente ao usuário autenticado ou gerenciado por um administrador.")
async def cancel_order(order_id: int, session: Session = Depends(get_session), user: User = Depends(verify_token)):
    order = session.query(Order).filter(Order.id==order_id).first()
    if not order:
        raise HTTPException(status_code=400, detail="Pedido não encontrado")
    if not user.admin and user.id != order.user_id:
        raise HTTPException(status_code=403, detail="Você não tem permissão para realizar esta alteração.")
    order.status = "CANCELED"
    session.commit()
    return {
        "message": f"Pedido número {order.id} cancelado com sucesso",
        "order": order
    }


@order_router.get("/list-orders", 
                  summary="Listar todos os pedidos", 
                  description="Retorna todos os pedidos. Esta operação é restrita a administradores.")
async def list_orders(session: Session = Depends(get_session), user: User = Depends(verify_token)):
    if not user.admin:
        raise HTTPException(status_code=403, detail="Você não tem permissão para realizar esta operação.")
    
    orders = session.query(Order).all()
    return {
        "orders": orders
    }


@order_router.post("/add-item/{order_id}", 
                   summary="Adicionar um item ao pedido", 
                   description="Adiciona um item do cardápio a um pedido usando o ID do item e a quantidade. O preço do item é obtido diretamente do cardápio.")
async def add_order_item(order_id: int, 
                         order_item_schema: OrderItemSchema, 
                         session: Session = Depends(get_session), 
                         user: User = Depends(verify_token)):
    order = session.query(Order).filter(Order.id==order_id).first()
    if not order:
        raise HTTPException(status_code=400, detail="Pedido não encontrado")
    if not user.admin and user.id != order.user_id:
        raise HTTPException(status_code=403, detail="Você não tem permissão para realizar esta operação.")

    menu_item = session.query(MenuItem).filter(MenuItem.id==order_item_schema.menu_item_id).first()
    if not menu_item:
        raise HTTPException(status_code=400, detail="Item do cardápio não encontrado")

    if not menu_item.available:
        raise HTTPException(status_code=400, detail="Item do cardápio indisponível no momento")
    
    order_item = OrderItem(order_item_schema.quantity, menu_item.price, menu_item.id, order_id)

    session.add(order_item)
    order.calculate_price()
    session.commit()
    return {
        "message": "Item adicionado com sucesso",
        "item_id": order_item.id,
        "order_price": order.price
    }


@order_router.post("/remove-item/{order_item_id}", 
                   summary="Remover um item do pedido", 
                   description="Remove um item de um pedido pertencente ao usuário autenticado ou gerenciado por um administrador.")
async def remove_order_item(order_item_id: int, session: Session = Depends(get_session), user: User = Depends(verify_token)):
    order_item = session.query(OrderItem).filter(OrderItem.id==order_item_id).first()

    if not order_item:
        raise HTTPException(status_code=400, detail="Item do pedido não encontrado")

    order = session.query(Order).filter(Order.id==order_item.order_id).first()

    if not user.admin and user.id != order.user_id:
        raise HTTPException(status_code=403, detail="Você não tem permissão para realizar esta operação.")

    session.delete(order_item)
    order.calculate_price()
    session.commit()
    return {
        "message": "Item removido com sucesso",
        "order_item_quantity": len(order.items),
        "order": order
    }


@order_router.post("/complete-order/{order_id}", 
                   summary="Concluir um pedido", 
                   description="Marca um pedido como concluído para o usuário autenticado ou um administrador.")
async def complete_order(order_id: int, session: Session = Depends(get_session), user: User = Depends(verify_token)):
    order = session.query(Order).filter(Order.id==order_id).first()
    if not order:
        raise HTTPException(status_code=400, detail="Pedido não encontrado")
    if not user.admin and user.id != order.user_id:
        raise HTTPException(status_code=403, detail="Você não tem permissão para realizar esta alteração.")
    order.status = "COMPLETED"
    session.commit()
    return {
        "message": f"Pedido número {order.id} concluído com sucesso",
        "order": order
    }


@order_router.get("/view-order/{order_id}", 
                  summary="Visualizar um pedido", 
                  description="Retorna os detalhes de um pedido pertencente ao usuário autenticado ou gerenciado por um administrador.")
async def view_order(order_id: int, session: Session = Depends(get_session), user: User = Depends(verify_token)):
    order = session.query(Order).filter(Order.id==order_id).first()
    if not order:
        raise HTTPException(status_code=400, detail="Pedido não encontrado")
    if not user.admin and user.id != order.user_id:
        raise HTTPException(status_code=403, detail="Você não tem permissão para visualizar este pedido.")
    return {
        "order_item_quantity": len(order.items),
        "order": order
    }


@order_router.get("/list-user-orders", 
                  response_model=List[ResponseOrderSchema], 
                  summary="Listar meus pedidos", 
                  description="Retorna todos os pedidos pertencentes ao usuário autenticado.")
async def list_user_orders(session: Session = Depends(get_session), user: User = Depends(verify_token)):
    orders = session.query(Order).filter(Order.user_id==user.id).all()
    return orders