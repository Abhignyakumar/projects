from fastapi import FastAPI, HTTPException
from schemas import BlogCreate, Blog
from typing import List
import crud

app = FastAPI(title="Blog API - POC", version="1.0")

@app.get("/", tags=["Health"])
def root():
    return {"message": "Blog API is running!"}

@app.get("/blogs", response_model=List[Blog], tags=["Blogs"])
def read_blogs():
    return crud.get_all_blogs()

@app.get("/blogs/{blog_id}", response_model=Blog, tags=["Blogs"])
def read_blog(blog_id: int):
    blog = crud.get_blog(blog_id)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog

@app.post("/blogs", response_model=Blog, tags=["Blogs"])
def create_new_blog(blog: BlogCreate):
    return crud.create_blog(blog)

@app.put("/blogs/{blog_id}", response_model=Blog, tags=["Blogs"])
def update_existing_blog(blog_id: int, blog: BlogCreate):
    updated = crud.update_blog(blog_id, blog)
    if not updated:
        raise HTTPException(status_code=404, detail="Blog not found")
    return updated

@app.delete("/blogs/{blog_id}", tags=["Blogs"])
def delete_blog(blog_id: int):
    deleted = crud.delete_blog(blog_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Blog not found")
    return {"message": "Blog deleted successfully"}
