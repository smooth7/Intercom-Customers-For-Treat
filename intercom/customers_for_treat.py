import json
from urllib import request

from intercom.distance import calculate_distance_km


class CustomersEligibleForTreat:

    # Keys (fields) expected in each Customer record
    _USER_ID_KEY = "user_id"
    _NAME_KEY = "name"
    _LATITUDE_KEY = "latitude"
    _LONGITUDE_KEY = "longitude"

    # Dictionary containing all expected fields and expected data types
    _EXPECTED_FIELDS = {_USER_ID_KEY: int, _NAME_KEY: str, _LATITUDE_KEY: float, _LONGITUDE_KEY: float}

    # Other constant class variables defined here
    _MAX_DISTANCE = 100  # Distance is in KM
    _OFFICE_LATITUDE = 53.339428  # Latitude in degrees
    _OFFICE_LONGITUDE = -6.257664  # Longitude in degrees
    _CUSTOMERS_INFO_URL = "https://s3.amazonaws.com/intercom-take-home-test/customers.txt"

    def print_all_eligible(self):
        customers_within_distance = []
        with request.urlopen(self._CUSTOMERS_INFO_URL) as customers:
            for number, line in enumerate(customers, start=1):
                parse_successful, customer_record = self._parse_customer_record(line.decode("utf-8"), number)
                if not parse_successful:
                    continue
                distance_from_office = calculate_distance_km(self._OFFICE_LATITUDE, self._OFFICE_LONGITUDE,
                                                             customer_record[self._LATITUDE_KEY],
                                                             customer_record[self._LONGITUDE_KEY])
                if distance_from_office <= self._MAX_DISTANCE:
                    customers_within_distance.append(customer_record)
        print("CUSTOMERS TO BE INVITED FOR FOOD AND DRINKS:")
        for customer in sorted(customers_within_distance, key=lambda i: i[self._USER_ID_KEY]):
            print(f"\nName: {customer[self._NAME_KEY]}, User ID: {customer[self._USER_ID_KEY]}")

    def _parse_customer_record(self, customer_string: str, line_number: int) -> (bool, dict):
        # Converts a Customer's string record (which is given in JSON format) to dict
        try:
            customer_record = json.loads(customer_string)
        except json.JSONDecodeError:
            print(f"ERROR: Parsing the Customer data on line {line_number} failed "
                  f"because it does not have the expected JSON format.")
            return False, {}
        # Cast all fields to expected type or fail where not possible
        for field in self._EXPECTED_FIELDS:
            expected_type = self._EXPECTED_FIELDS[field]
            try:
                customer_record[field] = expected_type(customer_record[field])
            except ValueError:
                print(f"ERROR: Parsing the Customer data on line {line_number} failed "
                      f"because {field} has an unexpected type.")
                return False, {}
            except KeyError:
                print(f"ERROR: Parsing the Customer data on line {line_number} failed "
                      f"because an expected field with name {field} is missing.")
                return False, {}
        # Parse is Successful
        return True, customer_record


if __name__ == "__main__":
    customers_eligible_for_treat = CustomersEligibleForTreat()
    customers_eligible_for_treat.print_all_eligible()
