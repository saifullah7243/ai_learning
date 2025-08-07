from pydantic import BaseModel, Field
from typing import Optional, List

class Product(BaseModel):
    product_id:int = Field(description="This is the Unique ID of product")
    name:str = Field(description= "Name of product")
    description:str = Field(description="Description of shopify store")
    price:float = Field(description="Price of product")
    in_stock:bool = Field(description="Is product stock availible or not")
    tags:Optional[List[str]] = Field(description="Tags used in product")


## Exmaple
try:
    product_info = Product(
        product_id=1,
        name="Ice Maker",
        description="This product is used to make Ice...",
        price = 12.3,
        in_stock=True,
        tags=["Ice", "Maker", "Ice Maker for summer"]

    )

except Exception as e:
    print(f"Error occured in schema:{e}")

print(product_info.model_dump_json(indent=2))
