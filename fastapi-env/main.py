from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def heyy():
    return "heyy"

@app.get('/about') 
def about():
    data = {'name': 'Saketh','age':20, 'current_study': 'NBKRIST','institute_address':'Vidyanagar'}
    return data