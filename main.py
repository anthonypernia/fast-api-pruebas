#Python
from typing import Optional
from enum import Enum
#Pydantic
from pydantic import BaseModel
from pydantic import Field , HttpUrl
from pydantic import EmailStr

#FastAPI
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import Body, Query, Path, Header, Form, Header, Cookie, File , UploadFile
from fastapi import status

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

class PersonBase(BaseModel):
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
    

class Person(PersonBase):
    password: str = Field(..., min_length=8, max_length=50, title="Password", example="12345678")
    
class PersonOut(PersonBase):
    pass
    

class LoginOut(BaseModel):
    username: str = Field(..., max_length=20, title="Username", example="anthonypernia")
    message: str = Field(default="Welcome!!! Login succesfully", title="Message", example="Welcome")


@app.get(path="/", status_code=status.HTTP_200_OK, tags=["Home"])
def home():
    return {"message": "Hello World"}

##request and response body

@app.post(path='/person/new', response_model=PersonOut, response_model_exclude_unset=True, status_code=status.HTTP_201_CREATED, tags=['Persons'])
def create_person(person: Person = Body(...)): #El triple punto indica que es oblicatorio el body
    return person

#Validation query paramns
@app.get(path="/person/detail/", status_code=status.HTTP_200_OK, tags=['Persons'])
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
persons = [1,2,3,4,5]
@app.get("/person/detail/{person_id}", status_code=status.HTTP_200_OK, tags=['Persons'])
def show_person(person_id: int = Path(
                                    ..., 
                                    gt=0,
                                    title="person id",
                                    description="this is the person id, greater than 0",
                                    example=23,
                                    )): ##Obligatorio
    if person_id not in persons:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This person not found")
    return {person_id: "Its exist!"}

#Validations body
@app.put(path="/person/{person_id}", status_code=status.HTTP_200_OK, tags=['Persons'])
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

@app.post("/login", response_model=LoginOut , status_code=status.HTTP_200_OK, tags=['Persons'])
def login(username: str = Form(...), password: str = Form(...)):
    return LoginOut(username=username)

#cookies and headers

@app.post(path="/contact", status_code=status.HTTP_200_OK, tags=['Contact'])
def contact(first_name: str = Form(..., max_length=20, min_length=1, title="Fist name", description="Person first name"),
            last_name: str = Form(..., max_length=20, min_length=1, title="last name", description="Person last name"),
            email: EmailStr = Form(...),
            message: str = Form(..., max_length=200, min_length=20, title="Message", description="Person Message"),
            user_agent: Optional[str] = Header(default=None, title="User Agent", description="Person User Agent"),
            ads: Optional[str] = Cookie(default=None, title="Ads", description="Person Ads"),
            ):
    return user_agent

@app.post(path='/post-image', tags=['Images'])
def post_image(image: UploadFile = File(...)):
    return {"filename": image.filename,
            "Format": image.content_type,
            "Size(kb)": round(len(image.file.read())/1024, ndigits=2)
            }
            
    

