
class Counter:
    def __init__(self):
        self.current_num_folder: int = 0
        self.current_num_file_in_folder: int = 0
        self.total_num_file_at_all: int = 0
        self.total_num_folder_at_all: int = 0
        self.total_count_files_moved_sucessfully_in_folder: int = 0
        self.total_count_files_on_error_in_folder: int = 0
        self.total_count_files_moved_sucessfully_at_all: int = 0
        self.total_count_files_on_error_at_all: int = 0
        self.total_count_files_from_other_date_in_folder = 0
        self.total_count_files_from_other_date_at_all = 0

    def init_counter_new_folder(self):
        self.total_count_files_moved_sucessfully_in_folder = 0
        self.total_count_files_on_error_in_folder = 0
        self.current_num_file_in_folder = 0
        self.current_num_folder+= 1
        self.total_num_folder_at_all+= 1
        self.total_count_files_from_other_date_in_folder = 0

    def increment_file_moved_sucessfully(self):
        self.total_count_files_moved_sucessfully_in_folder+= 1
        self.total_count_files_moved_sucessfully_at_all+= 1

    def increment_file_from_other_date(self):
        self.total_count_files_from_other_date_in_folder+= 1
        self.total_count_files_from_other_date_at_all+= 1

    def increment_file_on_error(self):
        self.total_count_files_on_error_in_folder+= 1
        self.total_count_files_on_error_at_all+= 1

    def increment_current_file(self):
        self.current_num_file_in_folder+= 1
        self.total_num_file_at_all+= 1


    def get_id_log_file(self) -> str:
        return str(self.current_num_folder) + "." + str(self.current_num_file_in_folder)



