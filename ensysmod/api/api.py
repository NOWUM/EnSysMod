from fastapi import APIRouter

from .endpoints import (
    authentication,
    capacity_fix,
    capacity_max,
    capacity_min,
    datasets,
    datasets_permissions,
    energy_commodities,
    energy_conversions,
    energy_models,
    energy_sinks,
    energy_sources,
    energy_storages,
    energy_transmissions,
    operation_rate_fix,
    operation_rate_max,
    regions,
    transmission_distances,
    transmission_losses,
    users,
    yearly_full_load_hours_max,
    yearly_full_load_hours_min,
)

api_router = APIRouter()
api_router.include_router(authentication.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(datasets.router, prefix="/datasets", tags=["Datasets"])
api_router.include_router(datasets_permissions.router, prefix="/datasets/permissions", tags=["Dataset Permissions"])
api_router.include_router(regions.router, prefix="/regions", tags=["Regions"])
api_router.include_router(energy_commodities.router, prefix="/commodities", tags=["Commodities"])
api_router.include_router(energy_conversions.router, prefix="/conversions", tags=["Energy Conversions"])
api_router.include_router(energy_sinks.router, prefix="/sinks", tags=["Energy Sinks"])
api_router.include_router(energy_sources.router, prefix="/sources", tags=["Energy Sources"])
api_router.include_router(energy_storages.router, prefix="/storages", tags=["Energy Storages"])
api_router.include_router(energy_transmissions.router, prefix="/transmissions", tags=["Energy Transmissions"])
api_router.include_router(transmission_distances.router, prefix="/transmission-distances", tags=["Transmission Distances"])
api_router.include_router(transmission_losses.router, prefix="/transmission-losses", tags=["Transmission Losses"])
api_router.include_router(energy_models.router, prefix="/models", tags=["Energy Models"])

api_router.include_router(capacity_fix.router, prefix="/fix-capacities", tags=["Fix Capacities"])
api_router.include_router(capacity_max.router, prefix="/max-capacities", tags=["Max Capacities"])
api_router.include_router(capacity_min.router, prefix="/min-capacities", tags=["Min Capacities"])
api_router.include_router(operation_rate_fix.router, prefix="/fix-operation-rates", tags=["Fix Operation Rates"])
api_router.include_router(operation_rate_max.router, prefix="/max-operation-rates", tags=["Max Operation Rates"])
api_router.include_router(yearly_full_load_hours_max.router, prefix="/max-yearly-full-load-hours", tags=["Max Yearly Full Load Hours"])
api_router.include_router(yearly_full_load_hours_min.router, prefix="/min-yearly-full-load-hours", tags=["Min Yearly Full Load Hours"])
