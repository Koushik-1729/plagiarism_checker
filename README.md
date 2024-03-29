# Plagiarism Checker

This is a Python-based plagiarism checker application. It allows you to upload text documents, check them for plagiarism against existing documents in the database, and manage the documents.
## Features
- Upload documents in .txt format
- Check plagiarism against existing documents
- Display a list of documents in the database
- Delete documents from the database
- Clear the entire database

## Technologies Used
- Python
- Tkinter (for the GUI)
- SQLite (for the database)
## Installation

1. Clone the repository:

   ```shell
   git clone https://github.com/your-username/plagiarism-checker.git

Install the required dependencies:
   - pip install tkinter sqlite3 difflib

To Run the application:
   - python plagiarism_checker.py
Usage:

- Click on the "Upload Document" button to select a text file (.txt) and upload it 
  to the database.

- Click on the "Check Plagiarism" button to select a text file and check it 
  against the existing documents in the database.

- The application will display a message if plagiarism is detected or if the file 
  is unique.

- The list box shows the names of the uploaded documents. Select a document and 
  click the "Delete Document" button to remove it from the database.

- To clear the entire database, click on the "Clear Database" button.


Contributing:
- Contributions are welcome! If you find any issues or have suggestions for 
  improvements, please feel free to open an issue or submit a pull request.