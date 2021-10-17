import json
from fastapi import FastAPI,HTTPException
with open("menu.json", "r+") as read_file:
    data = json.load(read_file)

app = FastAPI()

@app.get('/menu/{item_id}')
async def read_menu(item_id: int):
    for menu_item in data['menu']:
        if menu_item['id'] == item_id:
            return menu_item
    raise HTTPException(status_code=404, detail=f'Item not found')

@app.post('/menu/{item_name}')
async def add_menu(item_name: str):
    newItemId = data["menu"][-1]["id"]+1 if len(data["menu"]) > 0 else 1
    data["menu"].append({
        "id": newItemId,
        "name": item_name
    })
    with open ("menu.json", "w") as edit_file:       
        json.dump(data, edit_file, indent=4)
    return (data)

@app.delete('/menu/{item_id}')
async def del_menu(item_id: int):
    for idx, menu in enumerate(data["menu"]):
        if (menu["id"] == item_id):
            del data["menu"][idx]
    
    with open ("menu.json", "w") as edit_file:       
        json.dump(data, edit_file, indent=4)
    return (data)

@app.put('/menu/{item_id}')
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