import unittest
from datetime import datetime
from calculations import calculate_apportionments

class TestSettlementCalculator(unittest.TestCase):

    def test_apportionments(self):
        # Given input values
        local_council = "Rotorua District Council"
        regional_council = "Bay of Plenty Regional Council"
        local_yearly_rates = 3801.05
        regional_yearly_rates = 599.59
        settlement_date = datetime(2025, 7, 31)  # 31 July 2025

        # Expected values
        expected_local_vendor_amount = 320.20
        expected_local_purchaser_amount = 630.06
        expected_regional_vendor_amount = 50.92
        expected_regional_purchaser_amount = 548.67

        # Call the function to calculate the apportionments
        apportionments = calculate_apportionments(
            local_council, local_yearly_rates, regional_council, regional_yearly_rates, settlement_date
        )

        # Extract the results from the apportionments
        local_vendor_amount = apportionments["local"]["vendor_amount"]
        local_purchaser_amount = apportionments["local"]["purchaser_amount"]
        regional_vendor_amount = apportionments["regional"]["vendor_amount"]
        regional_purchaser_amount = apportionments["regional"]["purchaser_amount"]

        # Check the results against the expected values
        self.assertAlmostEqual(local_vendor_amount, expected_local_vendor_amount, places=2)
        self.assertAlmostEqual(local_purchaser_amount, expected_local_purchaser_amount, places=2)
        self.assertAlmostEqual(regional_vendor_amount, expected_regional_vendor_amount, places=2)
        self.assertAlmostEqual(regional_purchaser_amount, expected_regional_purchaser_amount, places=2)

if __name__ == "__main__":
    unittest.main()
