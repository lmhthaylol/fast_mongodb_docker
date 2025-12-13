from bson import ObjectId
from fastapi import FastAPI, HTTPException, Body

from h11 import Response
from pymongo import ReturnDocument
from starlette import status

from model.book import Book, UpdateBook
from config.connection import book_collection
from schema.schema import BookCollection

app = FastAPI(
    title="Book API mangage"
)


# Endpoint READ ALL
@app.get("/books")
async def get_all_books():
    return BookCollection(books=await book_collection.find().to_list(100))


# Endpoint READ
@app.get("/books/{book_id}",response_model=Book)
async def get_book(book_id):
    if (
            book := await book_collection.find_one({"_id": ObjectId(book_id)})
    ) is not None:
        return book
    raise HTTPException(status_code=404, detail=f"book {book_id} not found")


# Endpoint post
@app.post('/book', response_description="Add new book", response_model=Book, response_model_by_alias=False)
async def create_book(book: Book = Body(...)):
    newbook = await book_collection.insert_one(
        book.model_dump(by_alias=True,exclude=['id'])
    )
    create_book1=await book_collection.find_one(
        {"_id":newbook.inserted_id}
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