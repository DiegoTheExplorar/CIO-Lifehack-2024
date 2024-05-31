import asyncio
import aiohttp
import xml.etree.ElementTree as ET
import pandas as pd
import folium

async def get_coordinates_async(osm_id):
    url = f"https://api.openstreetmap.org/api/0.6/node/{osm_id}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                text = await response.text()
                root = ET.fromstring(text)
                for node in root.findall('.//node'):
                    lat = node.attrib.get('lat')
                    lon = node.attrib.get('lon')
                    return (float(lat), float(lon))
            return None

async def process_district(index, node_ids, map_osm, target_district):
    # Only process if the district index matches the user-specified district
    if index == target_district:
        prev_coords = None
        for idx, osm_id in enumerate(node_ids):
            coords = await get_coordinates_async(osm_id)
            if coords:
                icon_color = 'red' if idx == 0 or idx == len(node_ids) - 1 else 'blue'
                popup_text = f"District {index + 1}, Node {idx + 1}: {osm_id}"
                folium.Marker(location=coords, popup=popup_text, icon=folium.Icon(color=icon_color)).add_to(map_osm)
                if prev_coords:
                    folium.PolyLine(locations=[prev_coords, coords], color='blue').add_to(map_osm)
                prev_coords = coords

async def main():
    data = pd.read_csv('open_street_map_tsp_node_data.csv', header=None)
    map_osm = folium.Map(location=[41.8781, -87.6298], zoom_start=10)

    # Get district number input from user
    try:
        district_number = int(input("Enter the district number to process: ")) - 1
        tasks = [process_district(index, eval(row[0]), map_osm, district_number) for index, row in data.iterrows()]
        await asyncio.gather(*tasks)
        map_osm.save("osm_ids_map_with_lines_async.html")
    except ValueError:
        print("Invalid input. Please enter a valid number.")

# Run the asynchronous main function
if __name__ == "__main__":
    asyncio.run(main())
