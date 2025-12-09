# app/main.py
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware

from app.routes.employee_routes import router as employee_router
from app.routes.policy_routes import router as policy_router
from app.utils.logger import logger

app = FastAPI(
    title="Employee Policy Management API",
    description="API to manage employees, policies, and assignments.",
    version="1.0.0",
)

# CORS (optional, but useful)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Global Error Handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"Validation error: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={"detail": "Validation error", "errors": exc.errors()},
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )


# Routers
app.include_router(employee_router, prefix="/employees", tags=["Employees"])
app.include_router(policy_router, prefix="/policies", tags=["Policies"])


@app.get("/", tags=["Health"])
async def root():
    return {"message": "Employee Policy Management API is running"}
