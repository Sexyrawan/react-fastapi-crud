#   liberary        class
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from models import product
from database import sessionlocal , engine
import database_models
from sqlalchemy.orm import Session 

app = FastAPI()  # object of FastAPI named "app"

#TELUSKO IS RUNNING AT PORT 3000 "CORS" PROBLEM arrive
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # frontend origin
    allow_credentials=True,
    allow_methods=["*"], # submitting somethingh server * accept all methods
    allow_headers=["*"],
)

#               Base will done the inhatirance part from data_model
database_models.Base.metadata.create_all(bind=engine)

@app.get("/")  # route decorator
def greet():
    return {"message": "Welcome to FastAPI"}


#dictonary 
products = [
           #id,name,description,price,quantity
    # product(1,"phone","budget phone" , 7000 , 12 ), # this is a constructor and we dont defined in previous models 
    product(id=1,name="phone",description="budget phone" ,price= 7000 ,quantity= 12 ),
    product(id=2,name="laptop",description="gaming laptop" ,price= 80000 ,quantity= 50 ),
    product(id=3,name="car",description="toy car" ,price= 300 ,quantity= 8 ),
    product(id=4,name="ashirwad",description="wheet flor" ,price= 1410 ,quantity= 80),  
]


def get_db(): # DEPENDENCY INJECTION
    db = sessionlocal()
    try:
        yield db 
    finally:    
        db.close()

def init_db():
    db = sessionlocal() # EVERY TIME WE ARE CREATING THE SESSION AND NOT CLOSING IT "DEPENDENCY INJ."
    count = db.query(database_models.Product).count()
    if count ==0:   
        for product in products:
            db.add(database_models.Product(**product.model_dump()))
        db.commit()
init_db()        
        
        
@app.get("/products")
def get_all_products(db: Session = Depends(get_db)): #` `INJECTED` IN METHOD 
    db_products = db.query(database_models.Product).all()
    return db_products
  
@app.get("/product/{id}") # dynamic path ** ye wala path me hamne liha hai PROCUCT NOT PRODUCTS TO GET ONE PRODUCT
def get_product_by_id(id: int , db: Session = Depends(get_db)):
    # HNN SO WHAT IF ID WAS NOT SERIAL --> IT GIVES "INTERNAL SERVER ERROR"
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id ).first()
    if db_product:
        return db_product
    return "product not found"
    
    
    # return products[id-1] # why [id-1] so this is a array if , so number start from zero , to start from one we use -1 in game . ok  AND YAHA PE PRODUCTS ?
@app.post("/products") # add new product    
def add_product(product: product , db: Session = Depends(get_db)): # reciving data
    db.add(database_models.Product(**product.model_dump()))
    db.commit()
    products.append(product) # seding the data ok , so somewere reciving the data
    return product

@app.put("/products/{id}") # update , first need to check id was present? then uopdate 
# update required two things id and update information
#                  id        information
def update_product(id: int , product: product , db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id==id).first()
    if db_product:
        db_product.name = product.name
        db_product.description = product.description
        db_product.price = product.price
        db_product.quantity = product.quantity
        db.commit()
        return "product updated sucessfully"
    else:
        return "product not found so not updated"    
    
    


@app.delete("/products/{id}")
def delete_product(id: int , db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id==id).first()
    if db_product:
        db.delete(db_product) # hnn why this is not like db_product.delete  
        db.commit()
        return "deleted"
    else:
        return "not deleted"    