import aiohttp
import asyncio
import xml.etree.ElementTree as ET
import pandas as pd

async def get_coordinates(osm_id):
    # Construct the URL
    url = f"https://api.openstreetmap.org/api/0.6/node/{osm_id}"

    # Send the GET request asynchronously
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                # Parse the XML response
                text = await response.text()
                root = ET.fromstring(text)

                # Extract latitude and longitude
                for node in root.findall('.//node'):
                    lat = node.attrib.get('lat')
                    lon = node.attrib.get('lon')
                    return (float(lat), float(lon))
            return None

async def process_row(node_ids):
    # Initialize a list to store coordinates for this row
    row_coordinates = []

    # Get coordinates for each node ID in the row asynchronously
    for osm_id in node_ids:
        coords = await get_coordinates(osm_id)
        if coords:
            row_coordinates.append(coords)
    return row_coordinates

async def main():
    # Load the CSV file
    input_file = 'open_street_map_tsp_node_data.csv'
    data = pd.read_csv(input_file, header=None)

    # Process each row in the CSV file asynchronously
    tasks = [process_row(eval(row[1])) for index, row in data.iterrows()]
    coordinates_list = await asyncio.gather(*tasks)

    # Save the coordinates to a new CSV file
    output_data = pd.DataFrame(coordinates_list)
    output_file = 'coordinates_async.csv'
    output_data.to_csv(output_file, index=False, header=False)

# Run the asynchronous main function
if __name__ == "__main__":
    asyncio.run(main())
