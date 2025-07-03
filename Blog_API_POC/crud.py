from models import blogs_db
from schemas import BlogCreate, Blog

def get_all_blogs():
    return blogs_db

def get_blog(blog_id: int):
    for blog in blogs_db:
        if blog["id"] == blog_id:
            return blog
    return None

def create_blog(blog: BlogCreate):
    blog_id = len(blogs_db) + 1
    new_blog = blog.dict()
    new_blog["id"] = blog_id
    blogs_db.append(new_blog)
    return new_blog

def update_blog(blog_id: int, blog_data: BlogCreate):
    for index, blog in enumerate(blogs_db):
        if blog["id"] == blog_id:
            blogs_db[index].update(blog_data.dict())
            return blogs_db[index]
    return None

def delete_blog(blog_id: int):
    for index, blog in enumerate(blogs_db):
        if blog["id"] == blog_id:
            return blogs_db.pop(index)
    return None
