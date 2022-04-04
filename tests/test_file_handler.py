
import unittest

from src.file_handler import *



class TestGetLastWorkDay(unittest.TestCase):
    """
    Unit test to covering cenaries in app.file_handler.get_last_workday(date_yyyymmdd: str)
    It has been covered many cenaries about specific days of the week
    """

    def test_get_last_workday_when_current_date_is_sunday_should_return_successfully(self):
        date_sunday = "20220306"
        result = get_last_workday(date_sunday)
        expected_date_friday = "20220304"
        self.assertEqual(expected_date_friday,result)

    def test_get_last_workday_when_current_date_is_monday_should_return_successfully(self):
        date_monday = "20220307"
        result = get_last_workday(date_monday)
        expected_date_friday = "20220304"
        self.assertEqual(expected_date_friday,result)

    def test_get_last_workday_when_current_date_is_saturday_should_return_successfully(self):
        date_saturday = "20220305"
        result = get_last_workday(date_saturday)
        expected_date_friday = "20220304"
        self.assertEqual(expected_date_friday,result)

    def test_get_last_workday_when_current_date_is_tuesday_should_return_successfully(self):
        date_tuesday = "20220308"
        result = get_last_workday(date_tuesday)
        expected_date_monday = "20220307"
        self.assertEqual(expected_date_monday,result)

    def test_get_last_workday_when_current_date_is_friday_should_return_successfully(self):
        date_friday = "20220304"
        result = get_last_workday(date_friday)
        expected_date_wednesday = "20220303"
        self.assertEqual(expected_date_wednesday,result)


class TestGetDateFromFileName(unittest.TestCase):
    """
    Unit test to covering cenaries in app.file_handler.get_date_from_file_name(file_name: str)
    It has been covered many cenaries about specific days of the week
    """

    def test_GIVEN_right_date_request_WHEN_get_date_from_file_name_SHOULD_return_obj_successfully(self):
        key_file_s3 = "folder/File_63_ANY_OTHER_INFO_20200831_211010_ANY_OTHER_INFO.EXTENSION"
        result = get_date_from_file_name(key_file_s3)
        self.assertEqual("20200831" , result)

    def test_GIVEN_right_date_request_at_the_end_WHEN_get_date_from_file_name_SHOULD_return_obj_successfully(self):
        key_file_s3 = "folder/File_63_ANY_OTHER_INFO_20210716_211010"
        result = get_date_from_file_name(key_file_s3)
        self.assertEqual("20210716" , result)

    def test_GIVEN_date_request_with_no_hour_WHEN_get_date_from_file_name_SHOULD_return_default_date(self):
        key_file_s3 = "folder/File_63_ANY_OTHER_INFO_20200831_ANY_OTHER_INFO.EXTENSION"
        result = get_date_from_file_name(key_file_s3)
        self.assertEqual("20990101" , result)

    def test_GIVEN_date_request_with_no_match_WHEN_get_date_from_file_name_SHOULD_return_default_date(self):
        key_file_s3 = "folder/File_63_ANY_OTHER_INFO_2020_08_31_211010_ANY_OTHER_INFO.EXTENSION"
        result = get_date_from_file_name(key_file_s3)
        self.assertEqual("20990101" , result)

class TestIsDateFromFileNameEqualsTo(unittest.TestCase):
    """
    Unit test to covering cenaries in app.file_handler.is_date_file_name_equal_to(file_name: str, date_yyyymmdd: str)
    """

    def test_GIVEN_right_date_in_file_name_and_same_date_to_compare_WHEN_compare_date_SHOULD_return_true(self):
        file_name = "File_63_ANY_OTHER_INFO_20200831_211010_ANY_OTHER_INFO.EXTENSION"
        date_to_found_in_name = "20200831"

        result = is_date_file_name_equal_to(file_name,date_to_found_in_name)

        self.assertTrue(result)


    def test_GIVEN_right_date_in_file_name_and_different_date_to_compare_WHEN_compare_date_SHOULD_return_false(self):
        file_name = "File_63_ANY_OTHER_INFO_20200831_211010_ANY_OTHER_INFO.EXTENSION"
        date_to_found_in_name = "20200832"
        
        result = is_date_file_name_equal_to(file_name,date_to_found_in_name)

        self.assertFalse(result)

    def test_GIVEN_wrong_date_in_file_name_and_default_date_on_wrong_date_WHEN_compare_date_SHOULD_return_true(self):
        file_name = "File_63_ANY_OTHER_INFO_2020_08_31_211010_ANY_OTHER_INFO.EXTENSION"
        default_date_when_date_is_not_found = "20990101"
        
        result = is_date_file_name_equal_to(file_name,default_date_when_date_is_not_found)

        self.assertTrue(result)

    def test_GIVEN_wrong_date_in_file_name_and_different_default_date_on_wrong_date_WHEN_compare_date_SHOULD_return_false(self):
        file_name = "File_63_ANY_OTHER_INFO_2020_08_31_211010_ANY_OTHER_INFO.EXTENSION"
        wrong_default_date_when_date_is_not_found = "20220831"
        
        result = is_date_file_name_equal_to(file_name,wrong_default_date_when_date_is_not_found)

        self.assertFalse(result)


class TestCheckIgnoreFolder(unittest.TestCase):
    """
    Unit test to covering cenaries in app.file_handler.check_to_ignore_folder(folder_path: str, list_to_be_ignored: List[str])
    """

    def test_GIVEN_list_to_be_ignored_None_WHEN_check_to_ignore_folder_SHOULD_return_false(self):
        folder_name = "any-name-folder"
        none_list_to_be_ignored: List[str] = None
        result = check_to_ignore_folder(folder_name, none_list_to_be_ignored)
        self.assertFalse(result)

    def test_GIVEN_folder_name_None_WHEN_check_to_ignore_folder_SHOULD_return_false(self):
        none_folder_name = None
        list_to_be_ignored = ["ignore-folder-item"]
        result = check_to_ignore_folder(none_folder_name, list_to_be_ignored)
        self.assertFalse(result)

    def test_GIVEN_folder_name_ignore_equals_WHEN_check_to_ignore_folder_SHOULD_return_true(self):
        folder_name_ignore_equals = "folder1"
        list_to_be_ignored = ["item1","folder1","item3"]
        result = check_to_ignore_folder(folder_name_ignore_equals, list_to_be_ignored)
        self.assertTrue(result)

    def test_GIVEN_list_to_be_ignored_with_stripped_item_WHEN_check_to_ignore_folder_SHOULD_continue_suceccfully(self):
        folder_name = "folder1"
        list_to_be_ignored = ["folder1","","      "]
        result = check_to_ignore_folder(folder_name, list_to_be_ignored)
        self.assertTrue(result)

    def test_GIVEN_folder_name_stripped_item_WHEN_check_to_ignore_folder_SHOULD_continue_suceccfully(self):
        folder_name = ""
        list_to_be_ignored = ["folder1"]
        result = check_to_ignore_folder(folder_name, list_to_be_ignored)
        self.assertFalse(result)

    def test_GIVEN_wrong_folder_name_ignore_equals_WHEN_check_to_ignore_folder_SHOULD_return_false(self):
        folder_name_ignore_equals = "folder2"
        list_to_be_ignored = ["item1","folder1","item3"]
        result = check_to_ignore_folder(folder_name_ignore_equals, list_to_be_ignored)
        self.assertFalse(result)

    def test_GIVEN_folder_name_ignore_start_with_WHEN_check_to_ignore_folder_SHOULD_return_true(self):
        folder_name_ignore_start_with = "folder1-start-with"
        list_to_be_ignored = ["item1","folder1*","item3"]
        result = check_to_ignore_folder(folder_name_ignore_start_with, list_to_be_ignored)
        self.assertTrue(result)

    def test_GIVEN_wrong_list_check_ends_with_and_folder_name_ignore_start_with_WHEN_check_to_ignore_folder_SHOULD_return_false(self):
        folder_name_ignore_start_with = "folder1-start-with"
        list_to_be_ignored = ["item1","*folder1","item3"]
        result = check_to_ignore_folder(folder_name_ignore_start_with, list_to_be_ignored)
        self.assertFalse(result)
    
    def test_GIVEN_folder_name_ignore_ends_with_WHEN_check_to_ignore_folder_SHOULD_return_true(self):
        folder_name_ignore_ends_with = "ends-with-folder1"
        list_to_be_ignored = ["item1","*folder1","item3"]
        result = check_to_ignore_folder(folder_name_ignore_ends_with, list_to_be_ignored)
        self.assertTrue(result)

    def test_GIVEN_folder_name_ignore_contains_WHEN_check_to_ignore_folder_SHOULD_return_true(self):
        folder_name_ignore_contains = "prefix-folder1-sufix"
        list_to_be_ignored = ["item1","*folder1*","item3"]
        result = check_to_ignore_folder(folder_name_ignore_contains, list_to_be_ignored)
        self.assertTrue(result)

    def test_GIVEN_list_ignore_contains_and_wrong_file_name_WHEN_check_to_ignore_folder_SHOULD_return_false(self):
        folder_name_ignore_contains = "prefix-folder2-sufix"
        list_to_be_ignored = ["item1","*folder1*","item3"]
        result = check_to_ignore_folder(folder_name_ignore_contains, list_to_be_ignored)
        self.assertFalse(result)
    

class TestNormalizePathBars(unittest.TestCase):
    """
    Unit test to covering cenaries in app.file_handler.normalize_path_bars(folder_name: str)
    """

    def test_GIVEN_cases_path_name_WHEN_normalize_path_bars_SHOULD_return_treated_all_cases(self):
        path1 = "//127.0.0.1/SMB_MOUNT\\folder\/folder//folder/"
        path2 = "\\127.0.0.1/SMB_MOUNT\\folder\/folder\\folder"
        path3 = "/127.0.0.1\/SMB_MOUNT\\folder\/folder//folder/"
        path4 = "\/127.0.0.1\\SMB_MOUNT//folder/folder//folder"

        result1 = normalize_path_bars(path1)
        result2 = normalize_path_bars(path2)
        result3 = normalize_path_bars(path3)
        result4 = normalize_path_bars(path4)

        expected = "/127.0.0.1/SMB_MOUNT/folder/folder/folder"

        self.assertEqual(expected,result1)
        self.assertEqual(expected,result2)
        self.assertEqual(expected,result3)
        self.assertEqual(expected,result4)
