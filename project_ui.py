import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel, QTableWidget, QTableWidgetItem, QMessageBox, QScrollArea, QFormLayout
)
import psycopg2

class ProjectManagerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Comprehensive Project Manager')
        self.setGeometry(100, 100, 800, 600)

        self.initUI()
        self.initDB()

    def initUI(self):
        layout = QVBoxLayout()

        self.formLayout = QFormLayout()

        # Dynamic input fields for all project attributes
        self.fields = {}
        field_names = [
            "version_id", "version_name", "id", "role", "release_id", "created_at", "design_id", "project_status", 
            "password", "project_start_date", "project_name", "username", "stage_name", "project_id", "stage_id", 
            "project_team", "output_id", "account", "user_fullname", "department", "release_name", "output_content", 
            "updated_at", "script", "phone_num", "output_type", "design_name", "project_end_date", "project_owner"
        ]

        for field in field_names:
            label = QLabel(field.replace("_", " ").capitalize() + ":")
            input_field = QLineEdit()
            self.fields[field] = input_field
            self.formLayout.addRow(label, input_field)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        form_container = QWidget()
        form_container.setLayout(self.formLayout)
        scroll_area.setWidget(form_container)

        # Buttons
        self.addButton = QPushButton('Add Project')
        self.addButton.clicked.connect(self.addProject)
        self.viewButton = QPushButton('View Projects')
        self.viewButton.clicked.connect(self.viewProjects)

        # Table for displaying projects
        self.projectTable = QTableWidget()
        self.projectTable.setColumnCount(len(field_names))
        self.projectTable.setHorizontalHeaderLabels(field_names)

        # Add widgets to layout
        layout.addWidget(scroll_area)
        layout.addWidget(self.addButton)
        layout.addWidget(self.viewButton)
        layout.addWidget(self.projectTable)

        self.setLayout(layout)

    def initDB(self):
        try:
            self.conn = psycopg2.connect(
                host="61.79.166.214",
                database="CoDesigner_db",
                user="farmer",
                password="farmer"
            )
            self.cursor = self.conn.cursor()
        except Exception as e:
            QMessageBox.critical(self, 'Database Error', f'Failed to connect to database: {e}')
            sys.exit(1)

    def addProject(self):
        project_data = {field: self.fields[field].text() for field in self.fields}

        if not all(project_data.values()):
            QMessageBox.warning(self, 'Input Error', 'All fields are required.')
            return

        try:
            columns = ", ".join(project_data.keys())
            placeholders = ", ".join(["%s"] * len(project_data))
            query = f"INSERT INTO Project ({columns}) VALUES ({placeholders})"
            self.cursor.execute(query, tuple(project_data.values()))
            self.conn.commit()
            QMessageBox.information(self, 'Success', 'Project added successfully.')

            for field in self.fields.values():
                field.clear()
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to add project: {e}')

    def viewProjects(self):
        try:
            query = "SELECT * FROM Project"
            self.cursor.execute(query)
            rows = self.cursor.fetchall()

            self.projectTable.setRowCount(0)
            for row_idx, row_data in enumerate(rows):
                self.projectTable.insertRow(row_idx)
                for col_idx, col_data in enumerate(row_data):
                    self.projectTable.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to retrieve projects: {e}')

    def closeEvent(self, event):
        self.cursor.close()
        self.conn.close()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ProjectManagerApp()
    window.show()
    sys.exit(app.exec_())
