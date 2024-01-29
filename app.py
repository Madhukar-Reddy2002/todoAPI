from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from bson import ObjectId
from typing import Optional

app = FastAPI()

# Set up MongoDB connection
mongo_client = MongoClient("mongodb+srv://root:madhukar@chat.gkbwu96.mongodb.net/?retryWrites=true&w=majority")
db = mongo_client["tasks"]
todos_collection = db["todos"]

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def individual_serial(todo) ->dict :
    return {
        "id":str(todo['_id']),
        "title": todo["title"],
        "completed":todo["completed"]
    }
def todos_serial(todos):
    return [individual_serial(i) for i in todos]

# Create a new task
@app.post('/todo', tags=["tasks"])
def create_task(title: str, completed: Optional[bool] = False):
    new_task = {
        'title': title,
        'completed': completed
    }
    result = todos_collection.insert_one(new_task)
    new_task['_id'] = str(result.inserted_id)
    return {"message": "Task created successfully", "task": new_task}

# Get all tasks
@app.get('/todo', tags=["tasks"])
def get_all_tasks():
    tasks = todos_serial(todos_collection.find())
    return tasks

# Update a task
@app.put('/todo/{id}', tags=["tasks"])
def update_task(id: str, title: Optional[str] = None, completed: Optional[bool] = None):
    task = todos_collection.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": {"title": title, "completed": completed}},
        return_document=True
    )

    if task:
        return {"message": f"Task with id {id} updated successfully", "task": task}
    else:
        raise HTTPException(status_code=404, detail=f"Task with id {id} not found")

# Delete a task
@app.delete("/todo/{id}", tags=["tasks"])
def delete_task(id: str):
    result = todos_collection.delete_one({"_id": ObjectId(id)})

    if result.deleted_count > 0:
        return {"message": f"Removed task with id {id}"}
    else:
        raise HTTPException(status_code=404, detail=f"Task with id {id} not found")
