from model import Model
from view import View

class Controller:
    def __init__(self):
        self.model = Model()
        self.view = View()

    def run(self):
        while True:
            choice = self.show_menu()
            if choice == '1':
                self.view_records()
            elif choice == '2':
                self.add_record()
            elif choice == '3':
                self.update_record()
            elif choice == '4':
                self.delete_record()
            elif choice == '5':
                self.generate_random_data()
            elif choice == '6':
                self.run_custom_queries()
            elif choice == '7':
                break
            else:
                self.view.show_message("Invalid choice. Try again.")

    def show_menu(self):
        self.view.show_message("\nMenu:")
        self.view.show_message("1. View Records")
        self.view.show_message("2. Add Record")
        self.view.show_message("3. Update Record")
        self.view.show_message("4. Delete Record")
        self.view.show_message("5. Generate Random Data")
        self.view.show_message("6. Run Custom Queries")
        self.view.show_message("7. Quit")
        return input("Enter your choice: ")

    def generate_random_data(self):
        table = self.view.get_table_name()
        num_rows = self.view.get_number_of_rows()
        try:
            self.model.generate_random_data(table, num_rows)
            self.view.show_message(f"Successfully generated {num_rows} rows of random data!")
        except Exception as e:
            self.view.show_message(f"Error generating random data: {e}")

    def view_records(self):
        table = self.view.get_table_name()
        limit = self.view.get_limit()
        records = self.model.fetch(table, limit)
        self.view.display_records(records)

    def add_record(self):
        table = self.view.get_table_name()
        columns, values = self.view.get_columns_and_values()
        try:
            self.model.insert_into(table, columns, values)
            self.view.show_message("Record added successfully!")
        except Exception as e:
            self.view.show_message(f'Error adding record: {e}')
            self.model.conn.rollback()

    def update_record(self):
        table = self.view.get_table_name()
        columns, values = self.view.get_columns_and_values()
        condition = self.view.get_condition()
        try:
            self.model.update(table, columns, values, condition)
            self.view.show_message("Record updated successfully!")
        except Exception as e:
            self.view.show_message(f'Error updating record: {e}')
            self.model.conn.rollback()

    def delete_record(self):
        table = self.view.get_table_name()
        condition = self.view.get_condition()
        try:
            self.model.delete(table, condition)
            self.view.show_message("Record deleted successfully!")
        except Exception as e:
            self.view.show_message(f'Error deleting record: {e}')
            self.model.conn.rollback()
    
    def run_custom_queries(self):
        self.view.show_message("\nSelect a custom query to run:")
        self.view.show_message("1. Query 1: Filter freelancers by ID range and count tasks.")
        self.view.show_message("2. Query 2: Filter tasks by ID range and count required skills.")
        self.view.show_message("3. Query 3: Filter projects by ID range and count tasks.")
        choice = self.view.get_choice("Enter query number: ")

        if choice == '1':
            min_freelancer_id = self.view.get_input("Enter minimum freelancer ID: ")
            max_freelancer_id = self.view.get_input("Enter maximum freelancer ID: ")
            records, elapsed_time = self.model.custom_query_1(min_freelancer_id, max_freelancer_id)

        elif choice == '2':
            min_task_id = self.view.get_input("Enter minimum task ID: ")
            max_task_id = self.view.get_input("Enter maximum task ID: ")
            records, elapsed_time = self.model.custom_query_2(min_task_id, max_task_id)

        elif choice == '3':
            min_project_id = self.view.get_input("Enter minimum project ID: ")
            max_project_id = self.view.get_input("Enter maximum project ID: ")
            records, elapsed_time = self.model.custom_query_3(min_project_id, max_project_id)

        else:
            self.view.show_message("Invalid choice.")
            return

        self.view.display_records(records)
        self.view.show_message(f"Query executed in {elapsed_time:.2f} ms")
