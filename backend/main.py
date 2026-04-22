# Main entry point for the FastAPI application
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# In-memory storage for notes
notes_db = {}

class Note(BaseModel):
    id: int
    title: str
    content: str

@app.post('/notes/', response_model=Note)
async def create_note(note: Note):
    if note.id in notes_db:
        raise HTTPException(status_code=400, detail='Note with this ID already exists')
    notes_db[note.id] = note
    return note

@app.get('/notes/', response_model=List[Note])
async def get_notes():
    return list(notes_db.values())

@app.get('/notes/{note_id}', response_model=Note)
async def get_note(note_id: int):
    note = notes_db.get(note_id)
    if note is None:
        raise HTTPException(status_code=404, detail='Note not found')
    return note

@app.delete('/notes/{note_id}', response_model=Note)
async def delete_note(note_id: int):
    note = notes_db.pop(note_id, None)
    if note is None:
        raise HTTPException(status_code=404, detail='Note not found')
    return note

@app.get('/health')
async def health_check():
    return {'status': 'healthy'}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=10000)