from fastapi import APIRouter

auth_router = APIRouter(prefix="/auth_users", tags=["auth_users"])
product_router = APIRouter(prefix="/products", tags=["auth_users"])

