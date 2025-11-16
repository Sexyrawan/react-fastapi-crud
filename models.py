

from pydantic import BaseModel

class product(BaseModel): # we are inharited the all basemodelthing in product , and so if if ever we want to use some thing fist we import the where you want to use just inharite 
    id: int
    name: str
    description: str
    price: float
    quantity: int
"""     # constructor 
    def __init__(self,  id: int, name: str,description: str, price: float, quantity: int):
        self.id = id
        self.name = name
        self.description=description
        self.price = price
        self.quantity = quantity """
        # now by using pydantic we dont need this above code just use attribe in with data declaratiom  