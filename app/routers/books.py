from fastapi import APIRouter

router = APIRouter(prefix="/books")


@router.post("/")
async def create_book():
    return {"message": "Book created"}


@router.get("/")
async def get_books():
    return {"message": "Books"}


@router.get("/{book_id}")
async def get_book(book_id: int):
    return {"message": f"Book {book_id}"}


@router.patch("/{book_id}")
async def update_book(book_id: int):
    return {"message": f"Book {book_id} updated"}


@router.delete("/{book_id}")
async def delete_book(book_id: int):
    return {"message": f"Book {book_id} deleted"}
