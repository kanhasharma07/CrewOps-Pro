from pydantic import BaseModel, field_validator

class car(BaseModel):
    
    #Class Fields
    brand: str
    model: str
    year: int
    
    
    #validation
    @field_validator("year")
    @classmethod
    def validate_year(cls, yr: int):
        if yr < 2000:
            raise ValueError("Invalid year. Must be 2000 or later.")
        return yr
    
    #Initialize
    def __init__(self, brand: str, model: str, year: int, **kwargs):
        super().__init__(brand=brand, model=model, year=year, **kwargs)
        print("Base Class hello", self.brand, " ", self.year)

# Corrected initialization
# maruti = car(brand="Maruti", model="Suzuki", year=2009)

class tesla09(car):
    def __init__(self):
        brand = "Testla"
        Model = "X Pryda"
        year = 2009
        super().__init__(brand=brand, model=Model, year=year)
    
    
    
me = tesla09()

print (me.year, "me bani thi meri", me.model)
print(me.model_json_schema())