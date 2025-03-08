# fmt: off
import dagster as dg
from .resources import database_resource
from .assets import metrics, trips

trip_assets = dg.load_assets_from_modules([trips])
metric_assets = dg.load_assets_from_modules([metrics])

defs = dg.Definitions(
    assets=[*trip_assets, *metric_assets],
        resources={
        "database": database_resource,
    },

)
