class View:
    def display_records(self, records):
        if not records:
            print("No records found.")
        else:
            for record in records:
                print(record)

    def get_input(self, prompt):
        return input(prompt)

    def get_choice(self, prompt):
        return input(prompt)

    def get_table_name(self):
        return input("Enter table name: ")
    
    def get_limit(self):
        return input("Enter limit: ")

    def get_columns_and_values(self):
        columns = input("Enter columns (comma-separated): ").split(',')
        values = input("Enter values (comma-separated): ").split(',')
        return columns, values

    def get_condition(self):
        return input("Enter condition (e.g., id=1): ")

    def show_message(self, message):
        print(message)
    
    def get_number_of_rows(self):
        return input("Enter the number of rows to generate: ")
