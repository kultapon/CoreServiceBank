from fastapi import APIRouter

auth_router = APIRouter(prefix="/auth_users", tags=["auth_users"])
products_router = APIRouter(prefix="/products", tags=["products"])
categories_router = APIRouter(prefix="/categories", tags=["categories"])
admin_router = APIRouter(prefix="/admin/users", tags=["admin"])
