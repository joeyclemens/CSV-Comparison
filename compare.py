import tkinter as tk
from tkinter import filedialog
import csv
import os
from tkinter import messagebox
from tkinter import ttk

# Define functions for selecting CSV files
def select_sample_file():
    global sample_file_path
    sample_file_path = filedialog.askopenfilename()

def select_solution_file():
    global solution_file_path
    solution_file_path = filedialog.askopenfilename()

# Define function for running Python script
def run_script():
    # Open the sample CSV file
    with open(sample_file_path, 'r') as sample_file:
        sample_reader = csv.reader(sample_file)
        sample_data = list(sample_reader)

    # Open the solution CSV file
    with open(solution_file_path, 'r') as sol_file:
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

    # Get the directory where the app is run from
    directory = os.getcwd()

    # Display a message indicating the new file and the directory
    message = f"The script has finished running.\n\nThe new file is located in:\n{directory}\nmatching_and_non_matching_rows.csv"
    messagebox.showinfo("All done", message)





# Create the GUI window
root = tk.Tk()
root.geometry("500x300")
# Set the title of the window
root.title("CSV Comparison")
# Set the background color of the window
root.configure(bg="#d4d4d4")


# Create a style object
style = ttk.Style()

# Set the theme to 'clam'
style.theme_use('classic')

# Add buttons to select CSV files
sample_button = ttk.Button(root, text="Select CSV File #1", command=select_sample_file)
sample_button.pack()

solution_button = ttk.Button(root, text="Select CSV File #2",command=select_solution_file)
solution_button.pack()

# Add button to run Python script
run_button = ttk.Button(root, text="Run Comparison",command=run_script)
run_button.pack()

def open_file():
    # Get the directory where the app is run from
    directory = os.getcwd()

    # Open the matching and non-matching rows CSV file
    os.startfile(os.path.join(directory, 'matching_and_non_matching_rows.csv'))

button = ttk.Button(root, text="Open the resulting match", command=open_file)
button.pack()

# Create a label with your name
name_label = ttk.Label(root, text="Created by Joey")

# Pack the label at the bottom of the window
name_label.pack(side="bottom")

# Start the GUI loop
root.mainloop()
