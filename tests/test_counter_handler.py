from datetime import datetime
import unittest
from src.counter_handler import *

class TestCounterHandler(unittest.TestCase):

    def test_WHEN_init_counter_new_folder_twice_SHOULD_return_successfully_count_folders(self):
        counter = Counter()
        counter.init_counter_new_folder()
        counter.init_counter_new_folder()
        self.assertEqual(2,counter.current_num_folder)
        self.assertEqual(2,counter.total_num_folder_at_all)

    def test_WHEN_increment_current_file_and_reinit_new_folder_SHOULD_return_successfully_count_files(self):
        counter = Counter()
        counter.init_counter_new_folder()
        counter.increment_current_file()
        counter.increment_current_file()

        self.assertEqual(2,counter.current_num_file_in_folder)
        self.assertEqual(2,counter.total_num_file_at_all)

        counter.init_counter_new_folder()
        counter.increment_current_file()

        self.assertEqual(1,counter.current_num_file_in_folder)
        self.assertEqual(3,counter.total_num_file_at_all)

    def test_WHEN_increment_file_moved_sucessfully_and_reinit_new_folder_SHOULD_return_successfully_count_files(self):
        counter = Counter()
        counter.init_counter_new_folder()
        counter.increment_file_moved_sucessfully()
        counter.increment_file_moved_sucessfully()

        self.assertEqual(2,counter.total_count_files_moved_sucessfully_in_folder)
        self.assertEqual(2,counter.total_count_files_moved_sucessfully_at_all)

        counter.init_counter_new_folder()
        counter.increment_file_moved_sucessfully()

        self.assertEqual(1,counter.total_count_files_moved_sucessfully_in_folder)
        self.assertEqual(3,counter.total_count_files_moved_sucessfully_at_all)

    def test_WHEN_increment_file_from_other_date_and_reinit_new_folder_SHOULD_return_successfully_count_files(self):
        counter = Counter()
        counter.init_counter_new_folder()
        counter.increment_file_from_other_date()
        counter.increment_file_from_other_date()

        self.assertEqual(2,counter.total_count_files_from_other_date_in_folder)
        self.assertEqual(2,counter.total_count_files_from_other_date_at_all)

        counter.init_counter_new_folder()
        counter.increment_file_from_other_date()

        self.assertEqual(1,counter.total_count_files_from_other_date_in_folder)
        self.assertEqual(3,counter.total_count_files_from_other_date_at_all)

    
    def test_WHEN_increment_file_on_error_and_reinit_new_folder_SHOULD_return_successfully_count_files(self):
        counter = Counter()
        counter.init_counter_new_folder()
        counter.increment_file_on_error()
        counter.increment_file_on_error()

        self.assertEqual(2,counter.total_count_files_on_error_in_folder)
        self.assertEqual(2,counter.total_count_files_on_error_at_all)

        counter.init_counter_new_folder()
        counter.increment_file_on_error()

        self.assertEqual(1,counter.total_count_files_on_error_in_folder)
        self.assertEqual(3,counter.total_count_files_on_error_at_all)

    def test_WHEN_increment_file_on_error_and_reinit_new_folder_SHOULD_return_successfully_id_log(self):
        counter = Counter()
        counter.init_counter_new_folder()
        counter.increment_current_file()
        counter.increment_current_file()

        counter.init_counter_new_folder()
        counter.increment_current_file()

        self.assertEqual("2.1",counter.get_id_log_file())

