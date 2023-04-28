This code opens a tkinter gui window with buttons for choosing two CSV files. Running the comparison will and compare the data in them to find matching and non-matching rows. It then writes the results to a new CSV file called 'matching_and_non_matching_rows.csv'.

The code first opens the first CSV file and reads its contents using the csv.reader() function. It then opens the other CSV file and reads its contents in the same way.

Next, the code finds the index of the "Room ID", "Item Codes", and "Part of Union" columns in the sample CSV file. It also finds the index of the "Part of Union" column in the solution CSV file.

The code then creates a new CSV file called 'matching_and_non_matching_rows.csv' using the csv.writer() function. It writes the header row to this file, which includes the column names from both the sample and solution CSV files.

The code then loops through each row in the sample CSV file and compares it to each row in the solution CSV file. If a matching row is found, the code writes it to the new CSV file. If a non-matching row is found, the code writes it to the new CSV file with an empty value for the solution room ID.

Finally, the code loops through each row in the second CSV file and checks if it has already been matched. If it has not been matched, the code writes it to the new CSV file with an empty value for the sample room ID.

The code ends by printing a message indicating that the new file has been created.

For best results, ensure the target CSV files have the comparison headers in the same place. For example, Room ID could be the first column in both files and Item Codes could be the third in both. If they are different the results wont be as anticipated. 
