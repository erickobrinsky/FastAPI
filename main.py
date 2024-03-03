from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import Optional
import json

app = FastAPI()

class Person(BaseModel):
    id: Optional[int]=None
    name:str
    age:int
    gender:str

with open('people.json', 'r') as f:
    people = json.load(f)['people']

print(people)

@app.get('/people/{p_id}')
def get_person(p_id: int):
    person = [p for p in people if p['id'] == p_id]
    return person[0] if len(people) > 0 else {}


@app.get('/search', status_code=200)
def search_person(age: Optional[int]=Query(None, title='Age', description='The age to filter for'),
                  name:Optional[str]=Query(None, title='Name', description = 'The name to filter for')):
    person1 = [p for p in people if p['age'] == age]

    if name is None:
        if age is None:
            return people
        else:
            return person1
    else:
        people2 = [p for p in people if name.lower() in p['name'].lower()]
        if age is None:
            return people2
        else:
            combined = [p for p in person1 if p in people2]
            return combined


@app.post('/addPerson', status_code=201)
def add_person(person: Person):
    p_id = max([p['id'] for p in people ] )+1
    new_person = {
        "id": p_id,
        "name": person.name,
        "age": person.age,
        "gender": person.gender
        
    }

    people.append(new_person)

    with open('people.json', 'w') as f:
        json.dump(people, f)
    return new_person

# @app.get('/')
# def hello():
#     return {"Hello":"World"}


# @app.post('/')
# def hello_post():
#     return {"Sucess:" "you posted!"}


# @app.get('/something')
# def something():
#     return {"Data":"Something"}