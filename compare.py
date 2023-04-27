import csv

# Open the sample CSV file
with open('sample.csv', 'r') as sample_file:
    sample_reader = csv.reader(sample_file)
    sample_data = list(sample_reader)

# Open the solution CSV file
with open('sol.csv', 'r') as sol_file:
    sol_reader = csv.reader(sol_file)
    sol_data = list(sol_reader)

# Find the index of the "Room ID", "Item Codes", and "Part of Union" columns
room_id_index = sample_data[0].index('Room ID')
item_codes_index = sample_data[0].index('Item Code')
part_of_union_index = sample_data[0].index('Part of Union')

# Find the index of the "Part of Union" column in the solution CSV file
sol_part_of_union_index = sol_data[0].index('Part of Union')

# Create a new CSV file for the matching and non-matching rows
with open('matching_and_non_matching_rows.csv', 'w', newline='') as matching_file:
    matching_writer = csv.writer(matching_file)

    # Write the header row
    matching_writer.writerow(['Sample Room ID'] + sample_data[0] + ['Solution Room ID'] + sol_data[0][1:])

    # Find the matching and non-matching rows and write them to the new file
    for sample_row in sample_data[1:]:
        found_match = False
        for sol_row in sol_data[1:]:
            if sample_row[room_id_index] == sol_row[room_id_index] and sample_row[item_codes_index] == sol_row[item_codes_index]:
                if sample_row[part_of_union_index] != '' and sol_row[sol_part_of_union_index] != '' and sample_row[part_of_union_index] == sol_row[sol_part_of_union_index]:
                    matching_writer.writerow([sample_row[room_id_index]] + sample_row + [sol_row[room_id_index]] + sol_row[1:])
                    found_match = True
                    break
                elif sample_row[part_of_union_index] == '' and sol_row[sol_part_of_union_index] == '':
                    matching_writer.writerow([sample_row[room_id_index]] + sample_row + [sol_row[room_id_index]] + sol_row[1:])
                    found_match = True
                    break
        if not found_match:
            matching_writer.writerow([sample_row[room_id_index]] + sample_row + [''] + [''] * len(sol_data[0]))

    for sol_row in sol_data[1:]:
        found_match = False
        for sample_row in sample_data[1:]:
            if sample_row[room_id_index] == sol_row[room_id_index] and sample_row[item_codes_index] == sol_row[item_codes_index]:
                if sample_row[part_of_union_index] != '' and sol_row[sol_part_of_union_index] != '' and sample_row[part_of_union_index] == sol_row[sol_part_of_union_index]:
                    found_match = True
                    break
                elif sample_row[part_of_union_index] == '' and sol_row[sol_part_of_union_index] == '':
                    found_match = True
                    break
        if not found_match:
            matching_writer.writerow([''] + [''] * len(sample_data[0]) + [sol_row[room_id_index]] + sol_row[1:])

# Display a message indicating the new file
print('Comparison complete :)')
