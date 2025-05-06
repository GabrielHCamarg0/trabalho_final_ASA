from fastapi import FastAPI
from routes import auth
from dependencies.database import Base,engine


print(Base)
app = FastAPI(title="Microsserviços de autenticação",
    openapi_tags=[{"name": "auth", "description": "Operações de autenticação"}],
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
    security=[{"BearerAuth": []}])
print("Starting Auth Microservice...")
Base.metadata.create_all(bind=engine)
app.include_router(auth.router, prefix="/auth",tags= ["auth"])