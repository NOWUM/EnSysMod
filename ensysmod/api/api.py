from fastapi import APIRouter

from .endpoints import users, authentication, energy_sources, datasets, energy_commodities, energy_sinks, \
    energy_storages, energy_transmissions, energy_conversions

api_router = APIRouter()
api_router.include_router(authentication.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(datasets.router, prefix="/datasets", tags=["Datasets"])
api_router.include_router(energy_commodities.router, prefix="/commodities", tags=["Commodities"])
api_router.include_router(energy_conversions.router, prefix="/conversions", tags=["Energy Conversions"])
api_router.include_router(energy_sinks.router, prefix="/sinks", tags=["Energy Sinks"])
api_router.include_router(energy_sources.router, prefix="/sources", tags=["Energy Sources"])
api_router.include_router(energy_storages.router, prefix="/storages", tags=["Energy Storages"])
api_router.include_router(energy_transmissions.router, prefix="/transmissions", tags=["Energy Transmissions"])
