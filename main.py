import json
from fastapi import FastAPI, HTTPException, Depends, Body
from auth.auth_handler import signJWT
from auth.helpers import check_user, get_password_hash, user_exists, verify_password
from auth.auth_bearer import JWTBearer

with open("menu.json", "r+") as read_file:
    data = json.load(read_file)
with open("users.json", "r+") as data_file:
    userData = json.load(data_file)

app = FastAPI()

@app.get('/menu/{item_id}', dependencies=[Depends(JWTBearer())])
async def read_menu(item_id: int):
    for menu_item in data['menu']:
        if menu_item['id'] == item_id:
            return menu_item
    raise HTTPException(status_code=404, detail=f'Item not found')

@app.post('/menu/{item_name}', dependencies=[Depends(JWTBearer())])
async def add_menu(item_name: str):
    newItemId = data["menu"][-1]["id"]+1 if len(data["menu"]) > 0 else 1
    data["menu"].append({
        "id": newItemId,
        "name": item_name
    })
    with open ("menu.json", "w") as edit_file:       
        json.dump(data, edit_file, indent=4)
    return (data)

@app.delete('/menu/{item_id}', dependencies=[Depends(JWTBearer())])
async def del_menu(item_id: int):
    for idx, menu in enumerate(data["menu"]):
        if (menu["id"] == item_id):
            del data["menu"][idx]
    
    with open ("menu.json", "w") as edit_file:       
        json.dump(data, edit_file, indent=4)
    return (data)

@app.put('/menu/{item_id}', dependencies=[Depends(JWTBearer())])
async def update_menu(item_id: int, item_name: str):
    elementIdx = -1
    for idx, menu in enumerate(data["menu"]):
        if (menu["id"] == item_id):
            elementIdx = idx
    if (elementIdx == -1):
        raise HTTPException(status_code=404, detail=f'Item not found')

    else :
        data["menu"][elementIdx]["name"] = item_name
    with open ("menu.json", "w") as edit_file:       
        json.dump(data, edit_file, indent=4)
    return (data)

# Create Accounts
@app.post('/users')
def create_user(username: str, password: str):
    creds = {
        "username": username, 
        "password": get_password_hash(password)
    }
    if not (user_exists(userData, username)):
        userData.append(creds)
        with open ("users.json", "w") as user_file:       
            json.dump(userData, user_file, indent=4)
        return signJWT(username)
    else:
        raise HTTPException(status_code=405, detail=f'User already exists.')

# Login
@app.post('/users/login')
def login (username: str, password: str):
    creds = {
        "username": username, 
        "password": password
    }
    checkUser = check_user(userData, creds)
    print(check_user)
    if (checkUser == 200):
        return signJWT(username)
    elif (checkUser == 403):
        raise HTTPException(status_code=403, detail=f'Wrong password.')
    else:
        raise HTTPException(status_code=404, detail=f'User not found.')
        