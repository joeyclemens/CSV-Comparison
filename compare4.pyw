import tkinter as tk
from tkinter import ttk, messagebox
import csv
from tkinter.filedialog import askopenfilename, asksaveasfilename
import os


# Create the main window
root = tk.Tk()
root.geometry("500x400")
root.title("CSV File Comparator")
# Create a style object
style = ttk.Style()
# Set the background color of the window
root.configure(bg="#d4d4d4")
# Set the theme to 'clam'
style.theme_use('classic')



# Create the function to select the input CSV files
def select_input_file(label):
    file_path = askopenfilename(filetypes=[('CSV Files', '*.csv')])
    if file_path == '':
        return ''
    label.config(text=os.path.basename(file_path))
    return os.path.abspath(file_path)

# Create the function to select the output CSV file
def select_output_file():
    file_path = asksaveasfilename(defaultextension=".csv", filetypes=[('CSV Files', '*.csv')])
    if file_path == '':
        return ''
    return file_path

# Create the label and entry for the first CSV file
file1_frame = tk.Frame(root, bg="#d4d4d4")
file1_frame.pack(pady=10)

file1_label = tk.Label(file1_frame, text="Select the first CSV file:", bg="#d4d4d4")
file1_label.pack(side=tk.LEFT, padx=(0, 10))

file1_entry = ttk.Entry(file1_frame)
file1_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

file1_button = tk.Button(file1_frame, text="Browse", command=lambda: file1_entry.insert(tk.END, select_input_file(file1_name_label)))
file1_button.pack(side=tk.LEFT)
# Create the label and entry for the second CSV file
file2_frame = tk.Frame(root, bg="#d4d4d4")
file2_frame.pack(pady=10)

file2_label = tk.Label(file2_frame, text="Select the second CSV file:", bg="#d4d4d4")
file2_label.pack(side=tk.LEFT, padx=(0, 10))

file2_entry = ttk.Entry(file2_frame)
file2_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

file2_button = tk.Button(file2_frame, text="Browse", command=lambda: file2_entry.insert(tk.END, select_input_file(file2_name_label)))
file2_button.pack(side=tk.LEFT)

# Create the label and drop-down menu for the matching columns
match_frame = tk.Frame(root, bg="#d4d4d4")
match_frame.pack(pady=10)

#match_label = tk.Label(match_frame, text="Select the column or columns to match on:", bg="#d4d4d4")
#match_label.pack(side=tk.LEFT, padx=(0, 10))

match_listbox = tk.Listbox(match_frame, selectmode=tk.MULTIPLE)
match_listbox.pack(side=tk.LEFT)

# Create the function to update the matching column options
def update_match_options(event=None):
    file1_path = file1_entry.get()
    file2_path = file2_entry.get()

    if file1_path and file2_path:
        headers1 = get_headers(file1_path)
        headers2 = get_headers(file2_path)
        all_headers = list(set(headers1 + headers2)) # combine headers from both files and remove duplicates
        all_headers.sort() # sort the headers alphabetically
        match_listbox.delete(0, tk.END)
        for col in all_headers:
            match_listbox.insert(tk.END, col)
                
# Create the Refresh button
refresh_button = tk.Button(match_frame, text="Select the column or columns to match on", command=update_match_options)
refresh_button.pack(side=tk.LEFT, padx=(10, 0))
                

file1_entry.bind("<FocusOut>", update_match_options)
file2_entry.bind("<FocusOut>", update_match_options)


# Create the label and entry for the output file
output_frame = tk.Frame(root, bg="#d4d4d4")
output_frame.pack(pady=10)

output_label = tk.Label(output_frame, text="Select the output file:", bg="#d4d4d4")
output_label.pack(side=tk.LEFT, padx=(0, 10))

output_entry = ttk.Entry(output_frame)
output_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

output_button = tk.Button(output_frame, text="Browse", command=lambda: output_entry.insert(tk.END, select_output_file()))
output_button.pack(side=tk.LEFT)


# Create the function to get the headers of a CSV file
def get_headers(file_path):
    with open(file_path, 'r', encoding='iso-8859-1') as file:
        reader = csv.reader(file)
        headers = next(reader)
        return headers


# Create the function to compare the CSV files
def compare_csv():
    file1_path = file1_entry.get()
    file2_path = file2_entry.get()
    output_path = output_entry.get()
    matching_cols = match_listbox.curselection()
    if not file1_path or not file2_path or not output_path or not matching_cols:
        messagebox.showerror("Error", "Please select both CSV files, the output file, and the matching columns.")
        return
    matching_cols = [match_listbox.get(idx) for idx in matching_cols]

    headers1 = get_headers(file1_path)
    headers2 = get_headers(file2_path)
    all_headers = headers1 + headers2

    if not all(col in all_headers for col in matching_cols):
        messagebox.showerror("Error", "One or more matching columns not found in the input CSV files.")
        return

# Load the CSV files into lists of dictionaries
    with open(file1_path, 'r', encoding='iso-8859-1') as file1:
        reader = csv.DictReader(file1)
        df1 = [row for row in reader]
    with open(file2_path, 'r', encoding='iso-8859-1') as file2:
        reader = csv.DictReader(file2)
        df2 = [row for row in reader]

    # Find the matching rows and non-matching rows
    matching_rows = []
    non_matching_rows1 = []
    non_matching_rows2 = []
    for row1 in df1:
        match_found = False
        for row2 in df2:
            if all(row1[col] == row2[col] for col in matching_cols):
                matching_row = {**row1, **row2}
                matching_rows.append(matching_row)
                match_found = True
                break
        if not match_found:
            non_matching_rows1.append(row1)
    for row2 in df2:
        match_found = False
        for row1 in df1:
            if all(row1[col] == row2[col] for col in matching_cols):
                match_found = True
                break
        if not match_found:
            non_matching_rows2.append(row2)

    # Write the output to a new CSV file
    with open(output_path, 'w', newline='', encoding='iso-8859-1') as output_file:
        writer = csv.writer(output_file)
        writer.writerow(all_headers)

        # Write the matching rows to the output
        for matching_row in matching_rows:
            output_row = []
            for header in all_headers:
                output_row.append(matching_row.get(header, ''))
            writer.writerow(output_row)

        # Write the non-matching rows from file 1 to the output
        for non_matching_row in non_matching_rows1:
            output_row = []
            for header in all_headers:
                output_row.append(non_matching_row.get(header, ''))
            output_row[len(headers1):] = [''] * len(headers2)
            writer.writerow(output_row)

        # Write the non-matching rows from file 2 to the output
        for non_matching_row in non_matching_rows2:
            output_row = [''] * len(headers1)
            for header in headers2:
                output_row.append(non_matching_row.get(header, ''))
            writer.writerow(output_row)

    # Show a message box to let the user know the script has finished running
    messagebox.showinfo("Success", "The new CSV file has been created.")
    
# Create the frame for displaying the selected file names
file_frame = tk.Frame(root, bg="#d4d4d4")
file_frame.pack(side=tk.BOTTOM, pady=10)    

# Create the label for the first file name
file1_name_label = tk.Label(file_frame, text="", bg="#d4d4d4")
file1_name_label.pack(side=tk.LEFT, padx=(0, 10))

# Create the label for the second file name
file2_name_label = tk.Label(file_frame, text="", bg="#d4d4d4")
file2_name_label.pack(side=tk.LEFT)

# Create the button to compare the CSV files
compare_button = tk.Button(root, text="Compare CSV Files", command=compare_csv)
compare_button.pack(pady=10)

# Run the main loop
root.mainloop()    