import requests
import json
import pandas as pd
import folium
from folium import IFrame

# Define the API request
url = 'https://api.calflora.org/observations'
api_key = 'INSERT API KEY'
headers = {
    'Accept': 'application/json',
    'X-Api-Key': api_key,
    'csetId': "291"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    
    # Print the total number of records received
    total_records = len(data)
    print(f"Total number of records received: {total_records}")
    
    # Print the first few records to inspect
    print("Sample records from API response:")
    print(json.dumps(data[:5], indent=2))  # Print the first 5 records for inspection
    
    # Filter out records with null 'Latitude' or 'Longitude'
    filtered_data = [
        record for record in data
        if record.get('Latitude') and record.get('Longitude')
    ]
    
    # Print the number of filtered records
    filtered_total = len(filtered_data)
    print(f"Number of valid records: {filtered_total}")
    
    # Create a folium map centered around a default location
    map_center = (37.9331563, -122.6917638)  # Adjust based on your data
    my_map = folium.Map(location=map_center, zoom_start=14)
    
    # Add points to the map
    for record in filtered_data:
        lat = float(record.get('Latitude', 0))
        lon = float(record.get('Longitude', 0))
        Observer = record.get('Observer', 'Unknown Observer')
        Taxon = record.get('Taxon', 'Unknown Taxon')
        
        # Create a popup with bolded titles
        popup_content = f"""
        <b>Observer:</b> {Observer}<br>
        <b>Taxon:</b> {Taxon}
        """
        
        # Create an IFrame for the popup content
        iframe = IFrame(popup_content, width=200, height=100)
        popup = folium.Popup(iframe, max_width=200)
        
        # Add a marker with the popup
        folium.Marker(
            location=(lat, lon),
            popup=popup,
            icon=folium.Icon(color='blue')
        ).add_to(my_map)
    
    # Save the map to an HTML file
    my_map.save('map_with_points.html')
    print("Map has been saved to map_with_points.html")
    
    # Save filtered data to Excel and JSON files
    df = pd.DataFrame(filtered_data)
    df.to_excel('data_records.xlsx', index=False)
    print("Data has been saved to data_records.xlsx")
    
    with open('data_records.txt', 'w') as file:
        json.dump(filtered_data, file, indent=2)
    print("Data has been saved to data_records.txt")
else:
    print(f"Error: {response.status_code}")
    print(response.text)
