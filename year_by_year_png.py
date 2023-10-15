import sqlite3
import geopandas as gpd
import matplotlib.pyplot as plt
import os
import warnings

warnings.filterwarnings("ignore", category=FutureWarning)

def make_impact_by_year_png():

    # Connect and get data for the database
    conn = sqlite3.connect('meteorite_landings.db')

    # Get unique years from the database
    query = """
    SELECT DISTINCT year
    FROM meteorite_landings
    WHERE year IS NOT NULL
    """
    years = [result[0] for result in conn.execute(query).fetchall()]

    # Define the geographical bounds of the Americas
    americas_lat_min = -56.0
    americas_lat_max = 83.0
    americas_lon_min = -168.0
    americas_lon_max = -34.0

    # Create a directory to save the PNG files
    if not os.path.exists('meteorite_impacts_by_year'):
        os.mkdir('meteorite_impacts_by_year')

    # Loop through the years and create maps
    for year in years:
        # Modify the SQL query to select meteorite impacts for a specific year within the Americas
        query = f"""
        SELECT GeoLocation
        FROM meteorite_landings
        WHERE GeoLocation IS NOT NULL
            AND year = {year}
            AND (reclat >= {americas_lat_min} AND reclat <= {americas_lat_max})
            AND (reclong >= {americas_lon_min} AND reclong <= {americas_lon_max})
        """

        results = conn.execute(query).fetchall()

        # Extract latitude and longitude from the GeoLocation data
        coordinates = [result[0].strip('()').split(', ') for result in results]
        latitude = [float(coord[0]) for coord in coordinates]
        longitude = [float(coord[1]) for coord in coordinates]

        # Create a GeoDataFrame with Point geometries
        gdf = gpd.GeoDataFrame(geometry=gpd.points_from_xy(longitude, latitude))

        # Create a map of the Americas using geopandas
        world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
        america = world[(world['continent'] == 'North America') | (world['continent'] == 'South America')]

        # Plot meteorite landings on the map of the Americas
        ax = america.plot(figsize=(12, 6), color='white', edgecolor='black')
        gdf.plot(ax=ax, marker='o', color='red', markersize=5)
        plt.title(f'Meteorite Impacts in America ({year})')

        # Save the map as a PNG file
        filename = f'meteorite_impacts_by_year/{year}_meteorite_impacts.png'
        plt.savefig(filename, dpi=300)

        # Close the figure to avoid overlapping plots
        plt.close()

    # Close the database connection
    conn.close()


if __name__=="__main__":
    make_impact_by_year_png()