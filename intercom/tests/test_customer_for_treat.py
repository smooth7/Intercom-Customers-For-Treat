import json
import unittest
from unittest.mock import patch, call

from intercom.customers_for_treat import CustomersEligibleForTreat


class TestPrintCustomersEligible(unittest.TestCase):

    CUS_1 = \
        '{"latitude": 52.886375, "user_id": 22, "name": "John Oshea", "longitude": -6.3701}'.encode()
    CUS_2 = \
        '{"latitude": 53.986375, "user_id": 12, "name": "Holland Peter", "longitude": -6.19999}'.encode()
    CUS_NOT_JSON_FORMAT = \
        '{"latitude": 32.986375, "user_id": 18: "name": "Christian Chuks", "longitude": -16.043701}'.encode()
    CUS_MISSING_FIELD = \
        '{"latitude": 32.986375, "user_id": 18, "full_name": "Christian Chuks", "longitude": -16.043701}'.encode()

    @patch.object(CustomersEligibleForTreat, "_parse_customer_record")
    @patch('intercom.customers_for_treat.calculate_distance_km')
    @patch('builtins.print')
    @patch('intercom.customers_for_treat.request.urlopen')
    def test_print_pass_output_ordered_by_id(self, mock_cus_list, mock_print, calc_dis, parse_line):
        cus_json = json.loads(self.CUS_1), json.loads(self.CUS_2)
        calc_dis.side_effect = [50, 10]
        parse_line.side_effect = [(True, cus_json[0]), (True, cus_json[1])]
        cus_list = [self.CUS_1, self.CUS_2]
        mock_cus_list.return_value.__enter__.return_value = cus_list
        CustomersEligibleForTreat().print_all_eligible()
        self.assertTrue([call('\nName: Holland Peter, User ID: 12'),
                        call('\nName: John Oshea, User ID: 22')] in mock_print.call_args_list)
        mock_print.assert_has_calls([call('\nName: Holland Peter, User ID: 12'),
                                          call('\nName: John Oshea, User ID: 22')])

    @patch.object(CustomersEligibleForTreat, "_parse_customer_record")
    @patch('intercom.customers_for_treat.calculate_distance_km')
    @patch('builtins.print')
    @patch('intercom.customers_for_treat.request.urlopen')
    def test_print_fail_output_not_ordered_by_id(self, mock_cus_list, mock_print, calc_dis, parse_line):
        cus_json = json.loads(self.CUS_1), json.loads(self.CUS_2)
        calc_dis.side_effect = [50, 10]
        parse_line.side_effect = [(True, cus_json[0]), (True, cus_json[1])]
        cus_list = [self.CUS_1, self.CUS_2]
        mock_cus_list.return_value.__enter__.return_value = cus_list
        CustomersEligibleForTreat().print_all_eligible()
        with self.assertRaises(AssertionError):
            mock_print.assert_has_calls([call('\nName: John Oshea, User ID: 22'),
                                         call('\nName: Holland Peter, User ID: 12')])

    @patch.object(CustomersEligibleForTreat, "_parse_customer_record")
    @patch('intercom.customers_for_treat.calculate_distance_km')
    @patch('builtins.print')
    @patch('intercom.customers_for_treat.request.urlopen')
    def test_print_cus_distance_too_far(self, mock_cus_list, mock_print, calc_dis, parse_line):
        cus_json = json.loads(self.CUS_1), json.loads(self.CUS_2)
        calc_dis.side_effect = [500, 1000]
        parse_line.side_effect = [(True, cus_json[0]), (True, cus_json[1])]
        cus_list = [self.CUS_1, self.CUS_2]
        mock_cus_list.return_value.__enter__.return_value = cus_list
        CustomersEligibleForTreat().print_all_eligible()
        self.assertTrue([call('\nName: Holland Peter, User ID: 12'),
                         call('\nName: John Oshea, User ID: 22')] not in mock_print.call_args_list)

    @patch.object(CustomersEligibleForTreat, "_parse_customer_record")
    @patch('intercom.customers_for_treat.calculate_distance_km')
    @patch('builtins.print')
    @patch('intercom.customers_for_treat.request.urlopen')
    def test_print_some_cus_distance_too_far(self, mock_cus_list, mock_print, calc_dis, parse_line):
        cus_json = json.loads(self.CUS_1), json.loads(self.CUS_2)
        calc_dis.side_effect = [1000, 10]
        parse_line.side_effect = [(True, cus_json[0]), (True, cus_json[1])]
        cus_list = [self.CUS_1, self.CUS_2]
        mock_cus_list.return_value.__enter__.return_value = cus_list
        CustomersEligibleForTreat().print_all_eligible()
        self.assertTrue([call('\nName: Holland Peter, User ID: 12')] in mock_print.call_args_list)
        self.assertTrue([call('\nName: John Oshea, User ID: 22')] not in mock_print.call_args_list)

    @patch.object(CustomersEligibleForTreat, "_parse_customer_record")
    @patch('intercom.customers_for_treat.calculate_distance_km')
    @patch('builtins.print')
    @patch('intercom.customers_for_treat.request.urlopen')
    def test_print_parse_unsuccessful(self, mock_cus_list, mock_print, calc_dis, parse_line):
        cus_json = json.loads(self.CUS_1), json.loads(self.CUS_2)
        calc_dis.side_effect = [100, 10]
        parse_line.side_effect = [(False, cus_json[0]), (False, cus_json[1])]
        cus_list = [self.CUS_1, self.CUS_2]
        mock_cus_list.return_value.__enter__.return_value = cus_list
        CustomersEligibleForTreat().print_all_eligible()
        self.assertTrue([call('\nName: Holland Peter, User ID: 12'),
                         call('\nName: John Oshea, User ID: 22')] not in mock_print.call_args_list)

    @patch.object(CustomersEligibleForTreat, "_parse_customer_record")
    @patch('intercom.customers_for_treat.calculate_distance_km')
    @patch('builtins.print')
    @patch('intercom.customers_for_treat.request.urlopen')
    def test_print_some_parse_unsuccessful(self, mock_cus_list, mock_print, calc_dis, parse_line):
        cus_json = json.loads(self.CUS_1), json.loads(self.CUS_2)
        calc_dis.side_effect = [100, 10]
        parse_line.side_effect = [(False, cus_json[0]), (True, cus_json[1])]
        cus_list = [self.CUS_1, self.CUS_2]
        mock_cus_list.return_value.__enter__.return_value = cus_list
        CustomersEligibleForTreat().print_all_eligible()
        self.assertTrue([call('\nName: Holland Peter, User ID: 12')] in mock_print.call_args_list)
        self.assertTrue([call('\nName: John Oshea, User ID: 22')] not in mock_print.call_args_list)


if __name__ == '__main__':
    unittest.main()
