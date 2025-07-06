from fastapi import FastAPI, Path, HTTPException, Query 
import json

app = FastAPI()

def load_data():
    with open('patients.json', 'r') as f:
        data = json.load(f)

    return data

@app.get("/")  # defining route with the endpoint location / for HTTP get method  and it's the home url

def hello():

    return {'message':'Patient Managemnet System API'}

@app.get("/about")

def about():   

    return {'message':'A fully functional API to manage your patient records'}

@app.get("/view")

def view():

    data = load_data()

    return data





# Path Parameter: Path Parameters are dynamic segments of a URL path used to indentify a specific resource
# Path function: Path() function in FastAPI is used to provide metadata, validation rules, and documentation hints 
# for Path Parameter(Path Params) in your API endpoints


@app.get("/patient/{patient_id}")  # patient_id is the dynamic segment of the URL
def view_patient(patient_id: str=Path(..., description='ID of the Patient in DB', example='P001')):   # ... means patient_id is required 
    # http://127.0.0.1:8000/patient/P005

    # load all the patients data 
    data = load_data()

    if patient_id in data:
        return data[patient_id]
    
    # return{'error' : 'Patient\'s data is NOT FOUND, please check the patient ID'}
    raise HTTPException(status_code=404, detail='Patient not found') # using HTTPException for status code # 404 means not found



# Query Parameters: Are optional key-value pairs appended to the end of a URL used to pass 
# additional data to the server via HTTP request. They are typically employed for operations like
# filtering, sorting, searching, and pagination, without altering the endpoint path itself.

@app.get('/sort')
def sort_patient(sort_by: str=Query(..., description="Sort on the basis of Height, Weight or BMI"), order: str=Query('asc', description= "Sort in asc or desc order")):  # here sort_by is required by putting ... and order is optional 
    # http://127.0.0.1:8000/sort?sort_by=bmi&order=desc

    valid_fields = ['height','weight', 'bmi']
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f'Invalid field, please select from {valid_fields}')
    
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400,detail='Invalid order, please select between asc or desc') # using HTTPException with status code # 404 means Bad Request
    

    data = load_data()


    sort_order = True if order == 'desc' else False


    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by,0), reverse=sort_order)

    return sorted_data