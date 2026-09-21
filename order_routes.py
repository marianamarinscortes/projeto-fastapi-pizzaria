from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import get_session, verify_token
from schemas import OrderSchema, OrderItemSchema, ResponseOrderSchema
from models import Order, User, OrderItem
from typing import List

order_router = APIRouter(prefix="/orders", tags=["orders"], dependencies=[Depends(verify_token)])

@order_router.get("/")
async def orders():
    return {"message": "You have accessed the orders route."}


@order_router.post("/create-order")
async def create_order(order_schema: OrderSchema, session: Session = Depends(get_session)):
    new_order = Order(user_id=order_schema.user_id)
    session.add(new_order)
    session.commit()
    return {"message": f"Order created successfully. Order ID: {new_order.id}"}


@order_router.post("/cancel-order/{order_id}")
async def cancel_order(order_id: int, session: Session = Depends(get_session), user: User = Depends(verify_token)):
    order = session.query(Order).filter(Order.id==order_id).first()
    if not order:
        raise HTTPException(status_code=400, detail="Order not found")
    if not user.admin and user.id != order.user_id:
        raise HTTPException(status_code=401, detail="You are not authorized to make this modification.")
    order.status = "CANCELED"
    session.commit()
    return {
        "message": f"Order number: {order.id} successfully canceled",
        "order": order
    }

@order_router.get("/list-orders")
async def list_orders(session: Session = Depends(get_session), user: User = Depends(verify_token)):
    if not user.admin:
        raise HTTPException(status_code=401, detail="You are not authorized to make this operation.")
    else:
        orders = session.query(Order).all()
        return {
            "orders": orders
        }

@order_router.post("/add-item/{order_id}")
async def add_order_item(order_id: int, order_item_schema: OrderItemSchema, session: Session = Depends(get_session), user: User = Depends(verify_token)):
    order = session.query(Order).filter(Order.id==order_id).first()
    if not order:
        raise HTTPException(status_code=400, detail="Order not found")
    if not user.admin and user.id != order.user_id:
        raise HTTPException(status_code=401, detail="You are not authorized to make this operation.")
    order_item = OrderItem(order_item_schema.quantity, order_item_schema.flavor, order_item_schema.size, order_item_schema.unit_price, order_id)
    session.add(order_item)
    order.calculate_price()
    session.commit()
    return {
        "message": "Created item successfully",
        "item_id": order_item.id,
        "order_price": order.price
    }

@order_router.post("/remove-item/{order_item_id}")
async def remove_order_item(order_item_id: int, session: Session = Depends(get_session), user: User = Depends(verify_token)):
    order_item = session.query(OrderItem).filter(OrderItem.id==order_item_id).first()
    order = session.query(Order).filter(Order.id==order_item.order).first()
    if not order_item:
        raise HTTPException(status_code=400, detail="Order item not found")
    if not user.admin and user.id != order.user_id:
        raise HTTPException(status_code=401, detail="You are not authorized to make this operation.")
    session.delete(order_item)
    order.calculate_price()
    session.commit()
    return {
        "message": "Removed item successfully",
        "order_item_quantity": len(order.items),
        "order": order
    }

@order_router.post("/complete-order/{order_id}")
async def complete_order(order_id: int, session: Session = Depends(get_session), user: User = Depends(verify_token)):
    order = session.query(Order).filter(Order.id==order_id).first()
    if not order:
        raise HTTPException(status_code=400, detail="Order not found")
    if not user.admin and user.id != order.user_id:
        raise HTTPException(status_code=401, detail="You are not authorized to make this modification.")
    order.status = "COMPLETED"
    session.commit()
    return {
        "message": f"Order number: {order.id} successfully comleted",
        "order": order
    }

@order_router.get("/view-order/{order_id}")
async def view_order(order_id: int, session: Session = Depends(get_session), user: User = Depends(verify_token)):
    order = session.query(Order).filter(Order.id==order_id).first()
    if not order:
        raise HTTPException(status_code=400, detail="Order not found")
    if not user.admin and user.id != order.user_id:
        raise HTTPException(status_code=401, detail="You are not authorized to view this order.")
    return {
        "order_item_quantity": len(order.items),
        "order": order
    }

@order_router.get("/list-user-orders", response_model=List[ResponseOrderSchema])
async def list_user_orders(session: Session = Depends(get_session), user: User = Depends(verify_token)):
    orders = session.query(Order).filter(Order.user_id==user.id).all()
    return orders