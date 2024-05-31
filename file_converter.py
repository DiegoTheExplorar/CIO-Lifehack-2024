import csv

source_filename = 'crime_hotspots.csv'
destination_filename = 'output.csv'

with open(source_filename, 'r') as source_file, open(destination_filename, 'w', newline='') as destination_file:
    # Create a CSV reader object

    csv_reader = csv.reader(source_file)
    csv_writer = csv.writer(destination_file)
    write = True

    # Iterate over each row in the input CSV file
    for row in csv_reader:
        # Get the ID from the first element of the row
        id_value = row[0]
        
        # Extract coordinates as pairs
        coordinates = [row[i:i+2] for i in range(1, len(row), 2)]
        
        # Write the ID as the first row
        csv_writer.writerow([id_value])
        
        # Write each pair of coordinates as a row
        for coord_pair in coordinates:
            csv_writer.writerow(coord_pair)