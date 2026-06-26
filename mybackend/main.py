from fastapi import FastAPI
from .routers import posts, users, auth, vote
from fastapi.middleware.cors import CORSMiddleware

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins  = ["https://www.google.com"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# while True:
#     try:
#         conn = psycopg2.connect(host = 'localhost', database = 'fastapi', user = 'postgres',
#                                 password = 'hrishikesh', cursor_factory=RealDictCursor)
#         curr = conn.cursor()
#         print("Database connection successfull")
#         break
#     except Exception as error:
#         print(f"Error: {error}")
#         sleep(2)

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return {"message": "Hello World"}