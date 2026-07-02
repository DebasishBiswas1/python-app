from fastapi import FastAPI

# Initialize the FastAPI application
app = FastAPI()

# Define a route for the root URL "/"
@app.get("/")
def read_root():
    return {"message": "Hello World! Our API is up and running."}

# Define a second route at "/health"
@app.get("/health")
def health_check():
    return {"status": "healthy"}