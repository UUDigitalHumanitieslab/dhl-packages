import unittest
from csvUtils import *
from filesystem import *

class TestCsvUtils(unittest.TestCase):
    def setUp(self):
        self.file = './tests/files/test_file.csv'
        self.expected_entries = [
            {'id': '1', 'how_drunk_are_you': 'yes', 'q2': '', 'name': 'ad', 'q1': '{"lat": 1.0,"lon": 1.0}'},
            {'id': '2', 'how_drunk_are_you': 'yes', 'q2': '{"lat": 3.0,"lon": 3.0} ', 'name': 'bert', 'q1': ' '},
            {'id': '3', 'how_drunk_are_you': 'no', 'q2': '{"lat": 3.0,"lon": 3.0}', 'name': 'cem',
             'q1': '{"lat": 3.0,"lon": 3.0}'}
        ]

        self.columns_to_split_on = [
            'q1',
            'q2'
        ]

        self.expected_split = [
            {'id': '1', 'q': 'q1', 'how_drunk_are_you': 'yes', 'ans': '{"lat": 1.0,"lon": 1.0}', 'name': 'ad'},
            {'id': '1', 'q': 'q2', 'how_drunk_are_you': 'yes', 'ans': '', 'name': 'ad'},
            {'id': '2', 'q': 'q1', 'how_drunk_are_you': 'yes', 'ans': ' ', 'name': 'bert'},
            {'id': '2', 'q': 'q2', 'how_drunk_are_you': 'yes', 'ans': '{"lat": 3.0,"lon": 3.0} ', 'name': 'bert'},
            {'id': '3', 'q': 'q1', 'how_drunk_are_you': 'no', 'ans': '{"lat": 3.0,"lon": 3.0}', 'name': 'cem'},
            {'id': '3', 'q': 'q2', 'how_drunk_are_you': 'no', 'ans': '{"lat": 3.0,"lon": 3.0}', 'name': 'cem'}]
        self.expected_after_delete = [
            {'id': '1', 'q': 'q1', 'how_drunk_are_you': 'yes', 'ans': '{"lat": 1.0,"lon": 1.0}', 'name': 'ad'},
            {'id': '2', 'q': 'q2', 'how_drunk_are_you': 'yes', 'ans': '{"lat": 3.0,"lon": 3.0} ', 'name': 'bert'},
            {'id': '3', 'q': 'q1', 'how_drunk_are_you': 'no', 'ans': '{"lat": 3.0,"lon": 3.0}', 'name': 'cem'},
            {'id': '3', 'q': 'q2', 'how_drunk_are_you': 'no', 'ans': '{"lat": 3.0,"lon": 3.0}', 'name': 'cem'}
        ]

        self.expected_after_split_lon_lat = [
            {'id': '1', 'q': 'q1', 'how_drunk_are_you': 'yes', 'name': 'ad', 'ans_lon': 1.0, 'ans_lat': 1.0},
            {'id': '2', 'q': 'q2', 'how_drunk_are_you': 'yes', 'name': 'bert', 'ans_lon': 3.0, 'ans_lat': 3.0},
            {'id': '3', 'q': 'q1', 'how_drunk_are_you': 'no', 'name': 'cem', 'ans_lon': 3.0, 'ans_lat': 3.0},
            {'id': '3', 'q': 'q2', 'how_drunk_are_you': 'no', 'name': 'cem', 'ans_lon': 3.0, 'ans_lat': 3.0}]

        self.correct_answers_csv = "./tests/files/correct_answers.csv"

        self.expected_after_adding_correct_answers = [
            {'ans_lon': 1.0, 'q': 'q1', 'correct_lat': 0.0, 'ans_lat': 1.0, 'id': '1', 'correct_lon': 0.0,
             'how_drunk_are_you': 'yes', 'name': 'ad'},
            {'ans_lon': 3.0, 'q': 'q2', 'correct_lat': 1.0, 'ans_lat': 3.0, 'id': '2', 'correct_lon': 1.0,
             'how_drunk_are_you': 'yes', 'name': 'bert'},
            {'ans_lon': 3.0, 'q': 'q1', 'correct_lat': 0.0, 'ans_lat': 3.0, 'id': '3', 'correct_lon': 0.0,
             'how_drunk_are_you': 'no', 'name': 'cem'},
            {'ans_lon': 3.0, 'q': 'q2', 'correct_lat': 1.0, 'ans_lat': 3.0, 'id': '3', 'correct_lon': 1.0,
             'how_drunk_are_you': 'no', 'name': 'cem'}]

        self.expected_after_add_distance = [
            {'q': 'q1', 'name': 'ad', 'how_drunk_are_you': 'yes', 'id': '1', 'correct_lat': 0.0, 'ans_lat': 1.0,
             'euclidean_distance': 156899.56828024276, 'correct_lon': 0.0, 'ans_lon': 1.0},
            {'q': 'q2', 'name': 'bert', 'how_drunk_are_you': 'yes', 'id': '2', 'correct_lat': 1.0, 'ans_lat': 3.0,
             'euclidean_distance': 313705.44544723263, 'correct_lon': 1.0, 'ans_lon': 3.0},
            {'q': 'q1', 'name': 'cem', 'how_drunk_are_you': 'no', 'id': '3', 'correct_lat': 0.0, 'ans_lat': 3.0,
             'euclidean_distance': 470604.96963796, 'correct_lon': 0.0, 'ans_lon': 3.0},
            {'q': 'q2', 'name': 'cem', 'how_drunk_are_you': 'no', 'id': '3', 'correct_lat': 1.0, 'ans_lat': 3.0,
             'euclidean_distance': 313705.44544723263, 'correct_lon': 1.0, 'ans_lon': 3.0}]

        self.expected_after_save = [
            {'ans_lon': '1.0', 'name': 'ad', 'how_drunk_are_you': 'yes', 'q': 'q1',
             'euclidean_distance': '156899.56828024276', 'correct_lat': '0.0', 'id': '1', 'correct_lon': '0.0',
             'ans_lat': '1.0'},
            {'ans_lon': '3.0', 'name': 'bert', 'how_drunk_are_you': 'yes', 'q': 'q2',
             'euclidean_distance': '313705.44544723263', 'correct_lat': '1.0', 'id': '2',
             'correct_lon': '1.0', 'ans_lat': '3.0'},
            {'ans_lon': '3.0', 'name': 'cem', 'how_drunk_are_you': 'no', 'q': 'q1',
             'euclidean_distance': '470604.96963796', 'correct_lat': '0.0', 'id': '3', 'correct_lon': '0.0',
             'ans_lat': '3.0'},
            {'ans_lon': '3.0', 'name': 'cem', 'how_drunk_are_you': 'no', 'q': 'q2',
             'euclidean_distance': '313705.44544723263', 'correct_lat': '1.0', 'id': '3',
             'correct_lon': '1.0', 'ans_lat': '3.0'}
        ]

    def test_load_file(self):
        lines = load_csv_file_to_dicts(self.file)
        self.assertEqual(
            lines, self.expected_entries
        )

    def test_split_on_columns(self):
        result = split_on_columns(self.expected_entries, self.columns_to_split_on, 'q', 'ans')
        self.assertEqual(result, self.expected_split)

    def test_delete_empty_entries(self):
        result = delete_empty_entries(self.expected_split, 'ans')
        self.assertEqual(result, self.expected_after_delete)

    def test_split_lon_lat(self):
        result = split_lon_lat(self.expected_after_delete, 'ans')
        self.assertEqual(result, self.expected_after_split_lon_lat)

    def test_save_lines_to_file(self):
        file = "./tests/files/temp.csv"
        save_as_csv(self.expected_after_add_distance, file)
        lines = load_csv_file_to_dicts(file)
        self.assertEqual(lines, self.expected_after_save)

    def test_add_correct_answers_from_csv(self):
        lines = [
            {"x":i, '2x': 2 * i} for i in range(3)
        ] + [
            {"x": i, '2x': 2 * i} for i in range(3)
        ]
        new_lines = [
            {"x": i , "3x": 3 * i} for i in range(3)
        ]
        column_1 = "x"
        column_2 = "x"

        result = merge_on(lines, new_lines, column_1, column_2)
        self.assertEqual(
            result, [
                    {"x": i, '2x': 2 * i, '3x': 3*i} for i in range(3)
                ] + [
                    {"x": i, '2x': 2 * i, '3x': 3*i} for i in range(3)
                ]
        )