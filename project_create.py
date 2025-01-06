import sys
import psycopg2
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel, QTextEdit, QFileDialog, QMessageBox, QDateEdit
from PyQt5.QtCore import QDate

class ProjectApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.project_id = None
        self.release_id = None
        self.design_id = None
        self.stage_id = None
        self.version_id = None

    def initUI(self):
        self.setWindowTitle('Project Management')
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        self.project_name_input = QLineEdit(self)
        self.project_name_input.setPlaceholderText('Project Name')
        layout.addWidget(QLabel('Project Name'))
        layout.addWidget(self.project_name_input)

        self.project_owner_input = QLineEdit(self)
        self.project_owner_input.setPlaceholderText('Project Owner')
        layout.addWidget(QLabel('Project Owner'))
        layout.addWidget(self.project_owner_input)

        self.project_start_date_input = QDateEdit(self)
        self.project_start_date_input.setDate(QDate.currentDate())
        layout.addWidget(QLabel('Project Start Date'))
        layout.addWidget(self.project_start_date_input)

        self.project_end_date_input = QDateEdit(self)
        self.project_end_date_input.setDate(QDate.currentDate())
        layout.addWidget(QLabel('Project End Date'))
        layout.addWidget(self.project_end_date_input)

        self.project_team_input = QLineEdit(self)
        self.project_team_input.setPlaceholderText('Project Team')
        layout.addWidget(QLabel('Project Team'))
        layout.addWidget(self.project_team_input)

        self.project_status_input = QLineEdit(self)
        self.project_status_input.setPlaceholderText('Project Status')
        layout.addWidget(QLabel('Project Status'))
        layout.addWidget(self.project_status_input)

        self.create_project_button = QPushButton('Create Project', self)
        self.create_project_button.clicked.connect(self.create_project)
        layout.addWidget(self.create_project_button)

        self.setLayout(layout)

    def get_db_connection(self):
        try:
            conn = psycopg2.connect(
                dbname="CoDesigner_db",
                user="farmer",
                password="farmer",
                host="61.79.166.214",
                port="5432"
            )
            return conn
        except Exception as e:
            QMessageBox.critical(self, "Database Error", str(e))
            return None

    def create_project(self):
        project_name = self.project_name_input.text()
        project_owner = self.project_owner_input.text()
        project_start_date = self.project_start_date_input.date().toString("yyyy-MM-dd")
        project_end_date = self.project_end_date_input.date().toString("yyyy-MM-dd")
        project_team = self.project_team_input.text()
        project_status = self.project_status_input.text()

        if not all([project_name, project_owner, project_start_date, project_team, project_status]):
            QMessageBox.warning(self, "Input Error", "All fields are required.")
            return

        conn = self.get_db_connection()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute(
                    "INSERT INTO Project (project_name, project_owner, project_start_date, project_end_date, project_team, project_status) VALUES (%s, %s, %s, %s, %s, %s) RETURNING project_id",
                    (project_name, project_owner, project_start_date, project_end_date, project_team, project_status)
                )
                self.project_id = cur.fetchone()[0]
                conn.commit()
                QMessageBox.information(self, "Success", "Project created successfully.")
                self.open_release_window()
            except Exception as e:
                QMessageBox.critical(self, "Database Error", str(e))
            finally:
                cur.close()
                conn.close()

    def open_release_window(self):
        self.release_window = QWidget()
        self.release_window.setWindowTitle('Create Release')
        self.release_window.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        self.release_name_input = QLineEdit(self.release_window)
        self.release_name_input.setPlaceholderText('Release Name')
        layout.addWidget(QLabel('Release Name'))
        layout.addWidget(self.release_name_input)

        self.create_release_button = QPushButton('Create Release', self.release_window)
        self.create_release_button.clicked.connect(self.create_release)
        layout.addWidget(self.create_release_button)

        self.release_window.setLayout(layout)
        self.release_window.show()

    def create_release(self):
        release_name = self.release_name_input.text()

        if not release_name:
            QMessageBox.warning(self.release_window, "Input Error", "Release name is required.")
            return

        conn = self.get_db_connection()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute(
                    "INSERT INTO Release (release_name, project_id) VALUES (%s, %s) RETURNING release_id",
                    (release_name, self.project_id)
                )
                self.release_id = cur.fetchone()[0]
                conn.commit()
                QMessageBox.information(self.release_window, "Success", "Release created successfully.")
                self.open_design_window()
            except Exception as e:
                QMessageBox.critical(self.release_window, "Database Error", str(e))
            finally:
                cur.close()
                conn.close()

    def open_design_window(self):
        self.design_window = QWidget()
        self.design_window.setWindowTitle('Create Design')
        self.design_window.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        self.design_name_input = QLineEdit(self.design_window)
        self.design_name_input.setPlaceholderText('Design Name')
        layout.addWidget(QLabel('Design Name'))
        layout.addWidget(self.design_name_input)

        self.create_design_button = QPushButton('Create Design', self.design_window)
        self.create_design_button.clicked.connect(self.create_design)
        layout.addWidget(self.create_design_button)

        self.design_window.setLayout(layout)
        self.design_window.show()

    def create_design(self):
        design_name = self.design_name_input.text()

        if not design_name:
            QMessageBox.warning(self.design_window, "Input Error", "Design name is required.")
            return

        conn = self.get_db_connection()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute(
                    "INSERT INTO Design (design_name, release_id) VALUES (%s, %s) RETURNING design_id",
                    (design_name, self.release_id)
                )
                self.design_id = cur.fetchone()[0]
                conn.commit()
                QMessageBox.information(self.design_window, "Success", "Design created successfully.")
                self.open_stage_window()
            except Exception as e:
                QMessageBox.critical(self.design_window, "Database Error", str(e))
            finally:
                cur.close()
                conn.close()

    def open_stage_window(self):
        self.stage_window = QWidget()
        self.stage_window.setWindowTitle('Create Stage')
        self.stage_window.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        self.stage_name_input = QLineEdit(self.stage_window)
        self.stage_name_input.setPlaceholderText('Stage Name')
        layout.addWidget(QLabel('Stage Name'))
        layout.addWidget(self.stage_name_input)

        self.create_stage_button = QPushButton('Create Stage', self.stage_window)
        self.create_stage_button.clicked.connect(self.create_stage)
        layout.addWidget(self.create_stage_button)

        self.stage_window.setLayout(layout)
        self.stage_window.show()

    def create_stage(self):
        stage_name = self.stage_name_input.text()

        if not stage_name:
            QMessageBox.warning(self.stage_window, "Input Error", "Stage name is required.")
            return

        conn = self.get_db_connection()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute(
                    "INSERT INTO Stage (stage_name, design_id) VALUES (%s, %s) RETURNING stage_id",
                    (stage_name, self.design_id)
                )
                self.stage_id = cur.fetchone()[0]
                conn.commit()
                QMessageBox.information(self.stage_window, "Success", "Stage created successfully.")
                self.open_version_window()
            except Exception as e:
                QMessageBox.critical(self.stage_window, "Database Error", str(e))
            finally:
                cur.close()
                conn.close()

    def open_version_window(self):
        self.version_window = QWidget()
        self.version_window.setWindowTitle('Create Version')
        self.version_window.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        self.version_name_input = QLineEdit(self.version_window)
        self.version_name_input.setPlaceholderText('Version Name')
        layout.addWidget(QLabel('Version Name'))
        layout.addWidget(self.version_name_input)

        self.create_version_button = QPushButton('Create Version', self.version_window)
        self.create_version_button.clicked.connect(self.create_version)
        layout.addWidget(self.create_version_button)

        self.version_window.setLayout(layout)
        self.version_window.show()

    def create_version(self):
        version_name = self.version_name_input.text()

        if not version_name:
            QMessageBox.warning(self.version_window, "Input Error", "Version name is required.")
            return

        conn = self.get_db_connection()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute(
                    "INSERT INTO Version (version_name, stage_id) VALUES (%s, %s) RETURNING version_id",
                    (version_name, self.stage_id)
                )
                self.version_id = cur.fetchone()[0]
                conn.commit()
                QMessageBox.information(self.version_window, "Success", "Version created successfully.")
                self.open_output_window()
            except Exception as e:
                QMessageBox.critical(self.version_window, "Database Error", str(e))
            finally:
                cur.close()
                conn.close()

    def open_output_window(self):
        self.output_window = QWidget()
        self.output_window.setWindowTitle('Create Output')
        self.output_window.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        self.output_type_input = QLineEdit(self.output_window)
        self.output_type_input.setPlaceholderText('Output Type')
        layout.addWidget(QLabel('Output Type'))
        layout.addWidget(self.output_type_input)

        self.output_content_input = QTextEdit(self.output_window)
        self.output_content_input.setPlaceholderText('Output Content')
        layout.addWidget(QLabel('Output Content'))
        layout.addWidget(self.output_content_input)

        self.upload_file_button = QPushButton('Upload File', self.output_window)
        self.upload_file_button.clicked.connect(self.upload_file)
        layout.addWidget(self.upload_file_button)

        self.create_output_button = QPushButton('Create Output', self.output_window)
        self.create_output_button.clicked.connect(self.create_output)
        layout.addWidget(self.create_output_button)

        self.output_window.setLayout(layout)
        self.output_window.show()

    def upload_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self.output_window, "Select File")
        if file_path:
            with open(file_path, 'r') as file:
                self.output_content_input.setText(file.read())

    def create_output(self):
        output_type = self.output_type_input.text()
        output_content = self.output_content_input.toPlainText()

        if not output_type or not output_content:
            QMessageBox.warning(self.output_window, "Input Error", "Output type and content are required.")
            return

        conn = self.get_db_connection()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute(
                    "INSERT INTO Output (output_type, output_content, version_id) VALUES (%s, %s, %s)",
                    (output_type, output_content, self.version_id)
                )
                conn.commit()
                QMessageBox.information(self.output_window, "Success", "Output created successfully.")
            except Exception as e:
                QMessageBox.critical(self.output_window, "Database Error", str(e))
            finally:
                cur.close()
                conn.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ProjectApp()
    ex.show()
    sys.exit(app.exec_())