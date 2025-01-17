import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QComboBox, QFileDialog
import psycopg2

# Constants for database connection
DB_USER = "farmer"
DB_PASSWORD = "farmer"
DB_HOST = "61.79.166.214"
DB_NAME = "CoDesignerDB"
DB_PORT = "5432"

class OutputTableApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.load_version_ids()

    def initUI(self):
        self.setWindowTitle("Output Table Input")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        # Fields for input
        self.output_type_label = QLabel("Output Type:")
        self.output_type_input = QLineEdit()
        layout.addWidget(self.output_type_label)
        layout.addWidget(self.output_type_input)

        self.output_content_label = QLabel("Output Content (File Name):")
        self.output_content_input = QLineEdit()
        layout.addWidget(self.output_content_label)
        layout.addWidget(self.output_content_input)

        self.file_button = QPushButton("Browse File")
        self.file_button.clicked.connect(self.browse_file)
        layout.addWidget(self.file_button)

        self.version_id_label = QLabel("Version ID:")
        self.version_id_input = QLineEdit()
        layout.addWidget(self.version_id_label)
        layout.addWidget(self.version_id_input)

        self.version_dropdown_label = QLabel("Select Version ID:")
        self.version_dropdown = QComboBox()
        self.version_dropdown.activated[str].connect(self.set_version_id)
        layout.addWidget(self.version_dropdown_label)
        layout.addWidget(self.version_dropdown)

        # Buttons
        self.save_button = QPushButton("Save")
        self.cancel_button = QPushButton("Cancel")

        layout.addWidget(self.save_button)
        layout.addWidget(self.cancel_button)

        self.setLayout(layout)

        # Button actions
        self.save_button.clicked.connect(self.save_to_database)
        self.cancel_button.clicked.connect(self.close)

    def load_version_ids(self):
        conn = None
        try:
            # Connect to PostgreSQL database
            conn = psycopg2.connect(
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD,
                host=DB_HOST,
                port=DB_PORT
            )
            cursor = conn.cursor()

            # Fetch version IDs from version table
            query = "SELECT version_id FROM version;"
            cursor.execute(query)
            version_ids = cursor.fetchall()

            # Populate the dropdown list
            self.version_dropdown.clear()
            for version_id in version_ids:
                self.version_dropdown.addItem(str(version_id[0]))

        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"Failed to load version IDs: {str(e)}")

        finally:
            if conn:
                cursor.close()
                conn.close()

    def browse_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Select File")
        if file_name:
            self.output_content_input.setText(file_name)
            try:
                with open(file_name, 'r') as file:
                    file_content = file.read()
                    self.output_content_input.setText(file_content)
            except Exception as e:
                QMessageBox.critical(self, "File Error", f"Failed to read file: {str(e)}")

    def set_version_id(self, version_id):
        self.version_id_input.setText(version_id)

    def save_to_database(self):
        output_type = self.output_type_input.text()
        output_content = self.output_content_input.text()
        version_id = self.version_id_input.text()

        if not output_type or not output_content or not version_id:
            QMessageBox.warning(self, "Input Error", "All fields must be filled out.")
            return

        conn = None
        try:
            # Connect to PostgreSQL database
            conn = psycopg2.connect(
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD,
                host=DB_HOST,
                port=DB_PORT
            )
            cursor = conn.cursor()

            # Insert data into the output table
            query = """
            INSERT INTO output (output_type, output_content, version_id)
            VALUES (%s, %s, %s)
            """
            cursor.execute(query, (output_type, output_content, version_id))

            # Commit the transaction
            conn.commit()

            QMessageBox.information(self, "Success", "Data inserted successfully.")

            # Clear input fields
            self.output_type_input.clear()
            self.output_content_input.clear()
            self.version_id_input.clear()

        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"Failed to insert data: {str(e)}")

        finally:
            # Close the connection
            if conn:
                cursor.close()
                conn.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = OutputTableApp()
    mainWin.show()
    sys.exit(app.exec_())
