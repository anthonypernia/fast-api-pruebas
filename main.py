#Python
from typing import Optional
from enum import Enum
#Pydantic
from pydantic import BaseModel
from pydantic import Field , HttpUrl

#FastAPI
from fastapi import FastAPI
from fastapi import Body, Query, Path, Header

app = FastAPI()

#Models

class UrlModel(BaseModel):
    url: HttpUrl


class HairColor(str, Enum):
    white = "white"
    blonde = "blonde"
    brown = "brown"
    black = "black"
    red = "red"

class Location(BaseModel):
    city: str = Field(..., title="City", description="Person's city", example="New York")
    state: str = Field(..., title="State", description="Person's state", example="NY")
    country: str = Field(..., title="Country", description="Person's country", example="USA")

class Person(BaseModel):
    firts_name: str = Field(..., 
                                min_length=1, 
                                max_length=50,
                                title="First Name",
                                example="Anthony",
                                )
    last_name: str = Field(...,
                            min_length=1,
                            max_length=50,
                            title="Last Name",
                            example="Herrera",
                            )
    age: int = Field(...,
                    gt=0,
                    le=115,
                    title="Age",
                    example=30,
                    )
    hair_color: Optional[HairColor] = Field(None, title="Hair Color", example="brown")
    is_married: Optional[bool] = Field(default=None, title="Married", example=False)
    password: str = Field(..., min_length=8, max_length=50, title="Password", example="12345678")
    
class PersonOut(BaseModel):
    firts_name: str = Field(..., 
                                min_length=1, 
                                max_length=50,
                                title="First Name",
                                example="Anthony",
                                )
    last_name: str = Field(...,
                            min_length=1,
                            max_length=50,
                            title="Last Name",
                            example="Herrera",
                            )
    age: int = Field(...,
                    gt=0,
                    le=115,
                    title="Age",
                    example=30,
                    )
    hair_color: Optional[HairColor] = Field(None, title="Hair Color", example="brown")
    is_married: Optional[bool] = Field(default=None, title="Married", example=False)
    
    # class Config:
    #     schema_extra = {
    #         "example": {
    #             "firts_name": "Anthony",
    #             "last_name": "Pernia",
    #             "age": 30,
    #             "hair_color": "black",
    #             "is_married": False
    #         }
    #     }
    


@app.get("/")
def home():
    return {"message": "Hello World"}

##rquest and response body

@app.post('/person/new', response_model=PersonOut, response_model_exclude_unset=True)
def create_person(person: Person = Body(...)): #El triple punto indica que es oblicatorio el body
    return person

#Validation query paramns
@app.get("/person/detail/" )
def show_person(name: Optional[str] = Query(
                default=None, 
                min_length=1, 
                max_length=50,
                title="person name",
                description= "this is the person name, between 1 and 50 characters",
                example="Santiago",
                ), ##Asi cuando es opcional, y le colocas un valor por defecto
                age: str = Query(
                            ..., 
                            title="Person age",
                            description="this is the person age",
                            example="30",
                            )): ##Se coloca asi cuando quieres que sea obligatorio, los tres puntos
    return {name, age}


##NOTA: se va a tomar este path, porque python lee de arriba hacia abajo, por ende se va a quedar con el ultimo path que se haya definido
#validation path parameters
@app.get("/person/detail/{person_id}")
def show_person(person_id: int = Path(
                                    ..., 
                                    gt=0,
                                    title="person id",
                                    description="this is the person id, greater than 0",
                                    example=23,
                                    )): ##Obligatorio
    return {"person_id": person_id}

#Validations body
@app.put("/person/{person_id}")
def update_person(
    person_id: int = Path(
        ..., 
        title="person_id",
        description="this is the person id",
        gt=0,
        example=24,
        ),
    person: Person = Body(
        ..., 
        title="person",
        description="this is the person",
        ),
    # location: Location = Body(
    #     ...,
    #     title="location",
    #     description="this is the location",
    # )
):
    # results = person.dict()
    # results.update(location.dict())
    return person