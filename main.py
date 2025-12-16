from bson import ObjectId
from fastapi import FastAPI, HTTPException, Body, Depends
from fastapi.security import APIKeyHeader

from h11 import Response
from pymongo import ReturnDocument
from starlette import status

from config.jwt_depen import get_current_user
from config.security import get_api_key, get_password_hash, verify_password, create_access_token
from model.book import Book, UpdateBook
from config.connection import book_collection, users_collection
from model.user import UserRegister, UserLogin, CurrentUser
from schema.schema import BookCollection

from fastapi import FastAPI



app = FastAPI(
    title="Book API key "
)


# ------------------------- AUTH ROUTES -------------------------
@app.post("/auth/register", status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserRegister):
    # find user
    if await users_collection.find_one({"username": user_data.username}):
        raise HTTPException(status_code=400, detail="Tên đăng nhập đã tồn tại")

    # hash pass
    hashed_password = get_password_hash(user_data.password)

    user_db_data = {
        "username": user_data.username,
        "email": user_data.email,
        "role": user_data.role,
        "hashed_password": hashed_password
    }

    await users_collection.insert_one(user_db_data)
    return {"message": "Đăng ký thành công", "username": user_data.username}


@app.post("/auth/login")
async def login_for_access_token(form_data: UserLogin):

    user_data = await users_collection.find_one({"username": form_data.username})

    if not user_data:
        raise HTTPException(status_code=400, detail="Thông tin đăng nhập không hợp lệ")

    if not verify_password(form_data.password, user_data["hashed_password"]):
        raise HTTPException(status_code=400, detail="Thông tin đăng nhập không hợp lệ")

    access_token = create_access_token(
        data={"sub": user_data["username"], "role": user_data["role"]}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }

# ------------------------- PROTECTED ROUTE -------------------------

@app.get("/secret-data")
async def get_secret_data(current_user: CurrentUser = Depends(get_current_user)):
    return {
        "message": f" {current_user.username}",
        "user_role": current_user.role,
        "email": current_user.email
    }

@app.get("/")
async def root():
    return {"status": "ok", "message": "Service is running"}


# Endpoint READ ALL
@app.get("/books")
async def get_all_books(api_key: str = Depends(get_api_key)):
    return BookCollection(books=await book_collection.find().to_list(100))


# Endpoint READ
@app.get("/books/{book_id}", response_model=Book)
async def get_book(book_id, str= Depends(get_current_user)):
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



