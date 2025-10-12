from fastapi import APIRouter
# from app.routes.health_route import router as HealthRouter
from app.routes.product_route import router as ProductRouter
from app.routes.auth_route import router as AuthRouter
from app.routes.user_route import router as UserRouter
from app.routes.upload_route import router as UploadRouter

api_router = APIRouter()

# api_router.include_router(HealthRouter)
api_router.include_router(AuthRouter)
api_router.include_router(UserRouter)
api_router.include_router(ProductRouter)
api_router.include_router(UploadRouter)