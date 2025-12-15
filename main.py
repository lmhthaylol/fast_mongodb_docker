from bson import ObjectId
from fastapi import FastAPI, HTTPException, Body, Depends
from fastapi.security import APIKeyHeader

from h11 import Response
from pymongo import ReturnDocument
from starlette import status

from config.security import get_api_key
from model.book import Book, UpdateBook
from config.connection import book_collection
from schema.schema import BookCollection

from fastapi import FastAPI
from dotenv import load_dotenv
import os


try:
    load_dotenv()
except Exception as e:
    print(f"Warning: Could not load .env file: {e}")


MASTER_KEY = os.getenv("SECRET_API_KEY_MASTER")


if not MASTER_KEY:
    raise EnvironmentError(
        "Lỗi: Biến môi trường 'SECRET_API_KEY_MASTER' chưa được thiết lập."
    )


app = FastAPI(
    title="Book API"
)


@app.get("/")
async def root():
    return {"status": "ok", "message": "Service is running"}


# Endpoint READ ALL
@app.get("/books")
async def get_all_books(api_key: str = Depends(get_api_key)):
    return BookCollection(books=await book_collection.find().to_list(100))


# Endpoint READ
@app.get("/books/{book_id}", response_model=Book)
async def get_book(book_id):
    if (
            book := await book_collection.find_one({"_id": ObjectId(book_id)})
    ) is not None:
        return book
    raise HTTPException(status_code=404, detail=f"book {book_id} not found")


# Endpoint post
@app.post('/book', response_description="Add new book", response_model=Book, response_model_by_alias=False)
async def create_book(book: Book = Body(...), api_key: str = Depends(get_api_key)):
    newbook = await book_collection.insert_one(
        book.model_dump(by_alias=True, exclude=['id'])
    )
    create_book1 = await book_collection.find_one(
        {"_id": newbook.inserted_id}
    )
    return create_book1


# Endpoint put
@app.put(
    '/book/{id}',
    response_description="Update book",
    response_model=Book,
    response_model_by_alias=False
)
async def update_book(id: str, book: UpdateBook = Body(...)):
    book = {
        k: v for k, v in book.model_dump(by_alias=True).items() if v is not None
    }
    if len(book) >= 1:
        update_result = await book_collection.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": book},
            return_document=ReturnDocument.AFTER,
        )
        if update_result is not None:
            return update_result
        else:
            raise HTTPException(status_code=404, detail=f"book {id} not found")

    if (existing_book := await book_collection.find_one({"_id": id})) is not None:
        return existing_book

    raise HTTPException(status_code=404, detail=f"book {id} not found")


# Endpoint delete
@app.delete(
    '/book/{id}',
    response_description="Delete a book"
)
async def delete_book(id: str):
    delete_result = await book_collection.delete_one({"_id": ObjectId(id)})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"book {id} not found")



