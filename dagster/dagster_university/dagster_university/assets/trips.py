import requests
import dagster as dg
from dagster import asset, AssetExecutionContext
import os
from . import constants
from dagster_duckdb import DuckDBResource
from dagster._utils.backoff import backoff
from ..partitions import monthly_partition



@dg.asset(
        partitions_def=monthly_partition
)
def taxi_trips_file(context: dg.AssetExecutionContext) -> None:
    #get the partiton key using the context, which holds info about how dagster is running and materialzing the assests
    partition_date_str = context.partition_key
    """
      The raw parquet files for the taxi trips dataset. Sourced from the NYC Open Data portal.
    """
    #month_to_fetch = '2023-03'
    month_to_fetch = partition_date_str[:-3] #to match the string format of the source
    raw_trips = requests.get(
        f"https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{month_to_fetch}.parquet"
    )

    with open(constants.TAXI_TRIPS_TEMPLATE_FILE_PATH.format(month_to_fetch), "wb") as output_file:
        output_file.write(raw_trips.content)


@dg.asset
def taxi_zones_file() -> None:
    """
      The CSV file for the distiinct taxi zones. Sourced from the NYC Open Data portal, NYC Taxi Zones.
    """
    raw_taxi_zones = requests.get(
        f"https://community-engineering-artifacts.s3.us-west-2.amazonaws.com/dagster-university/data/taxi_zones.csv"
    )

    with open(constants.TAXI_ZONES_FILE_PATH, "wb") as output_file:
        output_file.write(raw_taxi_zones.content)

#taxi zones table 
@dg.asset(
    deps=["taxi_zones_file"]
)
def taxi_zones(database: DuckDBResource) -> None:
    """
      The raw taxi zones dataset, loaded into a DuckDB database
    """
    query = """
        create or replace table zones as (
          select
            LocationID as zone_id,
            zone,
            borough,
            the_geom as geometry
          from 'data/raw/taxi_zones.csv'
        );
    """

    with database.get_connection() as conn:
        conn.execute(query)        





@dg.asset(
    deps=["taxi_trips_file"],
    partitions_def=monthly_partition,
)
def taxi_trips(context: dg.AssetExecutionContext,database: DuckDBResource) -> None:
    """
      The raw taxi trips dataset, loaded into a DuckDB database
    """
    partition_date_str = context.partition_key
    month_to_fetch = partition_date_str[:-3]
    #first step, creting the table with the partition column
    #deleting old data with the same partition date to prevent duplicates
    #insert new data
    query = f"""
    CREATE TABLE IF NOT EXISTS trips (
        vendor_id integer,
        pickup_zone_id integer,
        dropoff_zone_id integer,
        rate_code_id double,
        payment_type integer,
        dropoff_datetime timestamp,
        pickup_datetime timestamp,
        trip_distance double,
        passenger_count double,
        total_amount double,
        partition_date varchar
    );

    DELETE FROM trips WHERE partition_date = '{month_to_fetch}';

    INSERT INTO trips
    SELECT
        VendorID,
        PULocationID,
        DOLocationID,
        RatecodeID,
        payment_type,
        tpep_dropoff_datetime,
        tpep_pickup_datetime,
        trip_distance,
        passenger_count,
        total_amount,
        '{month_to_fetch}' AS partition_date
    FROM '{constants.TAXI_TRIPS_TEMPLATE_FILE_PATH.format(month_to_fetch)}';
  """



    with database.get_connection() as conn:
        conn.execute(query)       





