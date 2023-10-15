import sqlite3
import geopandas as gpd
import matplotlib.pyplot as plt

import warnings

warnings.filterwarnings("ignore", category=FutureWarning)

def make_world_map():
    # Get data from the database
    conn = sqlite3.connect("meteorite_landings.db")
    query = "SELECT GeoLocation FROM meteorite_landings"
    results = conn.execute(query).fetchall()

    # Extract latitude and longitude from the GeoLocation data and filter by range
    coordinates = [
        result[0].strip("()").split(", ") for result in results if result[0] is not None
    ]
    filtered_coordinates = [
        (float(coord[0]), float(coord[1]))
        for coord in coordinates
        if (-180 <= float(coord[1]) <= 180) and (-90 <= float(coord[0]) <= 90)
    ]

    latitude, longitude = zip(*filtered_coordinates)

    # Create a GeoDataFrame with Point geometries
    gdf = gpd.GeoDataFrame(geometry=gpd.points_from_xy(longitude, latitude))

    # Load the world map dataset
    world = gpd.read_file("map_shape\\110m_cultural\\ne_110m_admin_0_countries.shp")

    # Plot meteorite landings on the map
    ax = world.plot(figsize=(12, 6), color="white", edgecolor="black")
    gdf.plot(ax=ax, marker="o", color="red", markersize=5)
    plt.title("Meteorite Landings")
    plt.savefig("png_files/world_impacts.png", dpi=300, bbox_inches="tight")

    conn.close()


def make_americas_map():
    # Get data from the database
    conn = sqlite3.connect("meteorite_landings.db")

    # SQL query to select meteorite impacts in America
    query = """
    SELECT GeoLocation
    FROM meteorite_landings
    WHERE GeoLocation IS NOT NULL
        AND (reclat >= -56.0 AND reclat <= 83.0)
        AND (reclong >= -168.0 AND reclong <= -34.0)
    """

    results = conn.execute(query).fetchall()

    # Extract latitude and longitude from the GeoLocation data
    coordinates = [result[0].strip("()").split(", ") for result in results]
    latitude = [float(coord[0]) for coord in coordinates]
    longitude = [float(coord[1]) for coord in coordinates]

    # Create a GeoDataFrame with Point geometries
    gdf = gpd.GeoDataFrame(geometry=gpd.points_from_xy(longitude, latitude))

    # Create a map of the Americas using geopandas
    world = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
    america = world[
        (world["continent"] == "North America")
        | (world["continent"] == "South America")
    ]

    # Plot meteorite landings on the map of the Americas
    ax = america.plot(figsize=(12, 6), color="white", edgecolor="black")
    gdf.plot(ax=ax, marker="o", color="red", markersize=5)
    plt.title("Meteorite Impacts in America")

    # Save the map as a PNG file
    plt.savefig("png_files\\americas_impacts.png", dpi=300)

    # Close the database connection
    conn.close()


if __name__ == "__main__":
    make_world_map()
