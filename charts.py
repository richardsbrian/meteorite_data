import sqlite3
import pandas as pd
import matplotlib.pyplot as plt


def most_common_types():
    # Connect to database
    conn = sqlite3.connect("meteorite_landings.db")

    # SQL query 
    query = """
        SELECT recclass, COUNT(recclass) as count
        FROM meteorite_landings
        WHERE reclat >= -90 AND reclat <= 90
        AND reclong >= -180 AND reclong <= -40
        GROUP BY recclass
        ORDER BY count DESC
        LIMIT 20
    """

    # Execute the query and fetch the data
    df = pd.read_sql_query(query, conn)

    # Create bar plot
    plt.figure(figsize=(12, 6))
    ax = df.plot(kind="bar", x="recclass", y="count")
    plt.title("Top 20 Most Common Meteorite Types in North America")
    plt.xlabel("Meteorite Type")
    plt.ylabel("Count")
    plt.xticks(rotation=45, ha="right")

    # Add number of meteorites to bars
    for i, v in enumerate(df["count"]):
        ax.text(i, v + 5, str(v), ha="center", va="bottom")

    # Save the plot to a PNG file
    plt.tight_layout()
    plt.savefig("png_files\\top_20_meteorite_types_north_america.png")

    # Close the database connection
    conn.close()


def number_of_strikes_on_continents():
    # Connect to database
    conn = sqlite3.connect("meteorite_landings.db")

    # SQL query 
    query = "SELECT name, reclat, reclong FROM meteorite_landings"

    # Execute the query and fetch the data
    df = pd.read_sql_query(query, conn)

    # Define ranges for latitude and longitude for each continent
    continent_ranges = {
        "North America": (-90, 90, -180, -40),
        "South America": (-90, 0, -180, -35),
        "Africa": (-40, 35, -20, 55),
        "Europe": (35, 90, -40, 55),
        "Asia": (35, 90, 55, 180),
        "Australia": (-40, -10, 110, 180),
    }

    # determine the continent based on latitude and longitude
    def get_continent(lat, lon):
        for continent, (lat_min, lat_max, lon_min, lon_max) in continent_ranges.items():
            if lat_min <= lat <= lat_max and lon_min <= lon <= lon_max:
                return continent
        return "Unknown"

    # Apply the function to the dataframe to get the continent for each strike
    df["Continent"] = df.apply(
        lambda row: get_continent(row["reclat"], row["reclong"]), axis=1
    )

    # Count the number of strikes on each continent
    continent_counts = df["Continent"].value_counts()

    # Create a bar plot 
    plt.figure(figsize=(12, 8))  
    ax = continent_counts.plot(kind="bar")
    plt.title("Meteorite Strikes by Continent")
    plt.xlabel("Continent")
    plt.ylabel("Number of Strikes")
    plt.xticks(rotation=45)

    # Add number of strikes to bars
    for i, v in enumerate(continent_counts):
        ax.text(i, v + 10, str(v), ha="center", va="bottom")

    # Save the plot to a PNG file
    plt.tight_layout()  
    plt.savefig("png_files\continent_counts.png")

    # Close the database connection
    conn.close()


if __name__ == "__main__":
    most_common_types()
