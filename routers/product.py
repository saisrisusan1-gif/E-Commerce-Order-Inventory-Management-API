from fastapi import APIRouter, Depends, HTTPException
from schemas.product import ProductRequest,ProductResponse,ProductUpdate
from database.db_connection import get_db
from models.product import Product
from models.user import User
from core.auth import require_role,get_current_user
from sqlalchemy.orm import Session

router = APIRouter()
@router.post("/products",response_model=ProductResponse)
def product_creation(products:ProductRequest,db:Session=Depends(get_db),user:User=Depends(require_role("admin"))):
    product=db.query(Product).filter(Product.name==products.name).first()
    
    if product:
        raise HTTPException(status_code=409, detail="product already exists")

    create_product=Product(name=products.name,description=products.description,price=products.price,stock=products.stock,category=products.category)
    db.add(create_product)
    db.commit()
    db.refresh(create_product)
    
    return create_product


@router.get("/products", response_model=list[ProductResponse])
def get_products(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    products = db.query(Product).all()
    return products


@router.get("/products/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return product

@router.put("/products/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_product = db.query(Product).filter(Product.id == product_id).first()

    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    update_data = product.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_product, key, value)

    db.commit()
    db.refresh(db_product)

    return db_product

@router.delete("/products/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(product)
    db.commit()

    return {"message": "Product deleted successfully"}
