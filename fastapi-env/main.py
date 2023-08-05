from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def index():
    return {'data': 'blog list'}

@app.get(f'/blog/{id}') 
def show(id):
    return {'data': id}

@app.get(f'/blog/{id}/comments')
def comments(id):
    return {'data': {'1', '2'}}