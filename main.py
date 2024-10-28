from fastapi import FastAPI, Depends, HTTPException  
from models import (
    NoteResponse, 
    NoteInfoResponse, 
    NoteListResponse,  
    CreateNoteResponse,  
    create_new_note,  
    read_note_from_file,  
    update_note,  
    delete_note,  
    list_notes  
)

app = FastAPI()  #экземпляр приложения FastAPI

''' эндпоинты для работы с заметками'''

# создание заметки
@app.post("/notes", response_model=CreateNoteResponse)
async def create_note(note: NoteResponse):
    return create_new_note(note.text)  

#чтение заметки
@app.get("/notes/{note_id}", response_model=NoteResponse)
async def get_note(note_id: int):
    note_data = read_note_from_file(note_id)  
    return NoteResponse(id=note_id, text=note_data["text"])  

# получение информации о заметке
@app.get("/notes/{note_id}/info", response_model=NoteInfoResponse)
async def get_note_info(note_id: int):
    note_data = read_note_from_file(note_id)  
    return NoteInfoResponse(
        created_at=note_data["created_at"],  
        updated_at=note_data["updated_at"]  
    )

# обновление заметки
@app.patch("/notes/{note_id}", response_model=dict)
async def update_existing_note(note_id: int, note: NoteResponse):
    update_note(note_id, note.text)  
    return {"detail": "Note updated"}  

#удаление заметки
@app.delete("/notes/{note_id}", response_model=dict)
async def delete_existing_note(note_id: int):
    delete_note(note_id)  
    return {"detail": "Note deleted"} 

# получение списка заметок
@app.get("/notes", response_model=NoteListResponse)
async def get_notes():
    return list_notes()  
