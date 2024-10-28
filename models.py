import json  
import os  
from datetime import datetime  
from pydantic import BaseModel  
from fastapi import HTTPException  #исключение для обработки HTTP-ошибок

# директория для хранения заметок
NOTES_DIR = 'notes'

# создание дир., если не существует
os.makedirs(NOTES_DIR, exist_ok=True)


'''модели для ответов'''
# информация о заметке
class NoteResponse(BaseModel):
    id: int  
    text: str  

# информациия о времени создания и обновления заметки
class NoteInfoResponse(BaseModel):
    created_at: str  
    updated_at: str  

# список id заметок
class NoteListResponse(BaseModel):
    notes: list[int] 

# создание новой заметки
class CreateNoteResponse(BaseModel):
    id: int 

# класс заметки
class Note:
    def __init__(self, id: int, text: str):
        self.id = id  
        self.text = text 
        self.created_at = datetime.now().isoformat()  
        self.updated_at = self.created_at  

    # в словарь
    def to_dict(self):
        return {
            "id": self.id,  
            "text": self.text, 
            "created_at": self.created_at,  
            "updated_at": self.updated_at 
        }

# функция создания новой заметки
def create_new_note(note_text: str) -> CreateNoteResponse:
    note_id = len(os.listdir(NOTES_DIR)) + 1  # генерируем новый id
    new_note = Note(id=note_id, text=note_text)  
    write_note_to_file(note_id, new_note.to_dict())
    return CreateNoteResponse(id=new_note.id)  

# Функция чтения заметки из файла по id
def read_note_from_file(note_id: int):
    note_file = os.path.join(NOTES_DIR, f"{note_id}.json")  # путь к файлу заметки
    if not os.path.exists(note_file):  
        raise HTTPException(status_code=404, detail="Note not found")  

    with open(note_file, 'r') as f: 
        return json.load(f)  

# Функция записи заметки в файл
def write_note_to_file(note_id: int, note_data: dict):
    with open(os.path.join(NOTES_DIR, f"{note_id}.json"), 'w') as f:  
        json.dump(note_data, f, indent=4)  

# Функция обновления существующей заметки
def update_note(note_id: int, note_text: str):
    note_data = read_note_from_file(note_id)  
    note_data["text"] = note_text  # обновляем текст заметки
    note_data["updated_at"] = datetime.now().isoformat()  
    write_note_to_file(note_id, note_data)  

# Функция удаления заметки по id
def delete_note(note_id: int):
    note_file = os.path.join(NOTES_DIR, f"{note_id}.json")  
    if os.path.exists(note_file): 
        os.remove(note_file)  # удаляем файл
    else:
        raise HTTPException(status_code=404, detail="Note not found")  # ошибка, если нет такой заметки

# Функция получения списка id всех заметок
def list_notes() -> NoteListResponse:
    note_ids = [int(filename.split('.')[0]) for filename in os.listdir(NOTES_DIR)]  # извлекаем id из файлов
    return NoteListResponse(notes=note_ids) 
