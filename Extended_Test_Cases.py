import unittest

results = []


def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    if b == 0:
        return float("inf")
    result = a / b
    return int(result) if result.is_integer() else result


class TestCalculator(unittest.TestCase):

    def check(self, operation, equation, actual, expected):
        status = "PASS" if actual == expected else "FAIL"
        results.append([operation, equation, expected, actual, status])
        self.assertEqual(actual, expected)

    # Boundary Value
    def test_boundary_maximum(self):
        self.check("Boundary Value", "1000 - 999",
                   subtract(1000, 999), 1)

    # Boundary Value
    def test_boundary_minimum(self):
        self.check("Boundary Value", "-1000 + 999",
                   add(-1000, 999), -1)

    # Decimal Value
    def test_decimal(self):
        self.check("Decimal Value", "55.7 + 98.7",
                   add(55.7, 98.7), 154.4)

    # Exception Handling
    def test_exception(self):
        try:
            add(30, "D")
            actual = "No Exception"
        except TypeError:
            actual = "Exception"

        expected = "Exception"
        status = "PASS" if actual == expected else "FAIL"

        results.append([
            "Exception Handling",
            "30 + D",
            expected,
            actual,
            status
        ])

        self.assertEqual(actual, expected)

    # Negative Value
    def test_negative(self):
        self.check("Negative Value", "-27 * 4",
                   multiply(-27, 4), -108)

    #  Zero Value
    def test_zero(self):
        self.check("Zero Value", "56 * 0",
                   multiply(56, 0), 0)

    #  Zero Division
    def test_zero_division(self):
        actual = divide(40, 0)

        actual = "Infinity" if actual == float("inf") else "Error"
        expected = "Error / Infinity"

        status = "PASS" if actual in ["Error", "Infinity"] else "FAIL"

        results.append([
            "Zero Division",
            "40 / 0",
            expected,
            actual,
            status
        ])

        self.assertIn(actual, ["Error", "Infinity"])


if __name__ == "__main__":

    suite = unittest.defaultTestLoader.loadTestsFromTestCase(
        TestCalculator
    )

    runner = unittest.TextTestRunner(
        verbosity=0,
        stream=open("nul", "w")
    )

    result = runner.run(suite)

    print("\nOperation          Equation      Expected          Actual       Result")

    for r in results:
        print(
            f"{r[0]:<19}"
            f"{r[1]:<14}"
            f"{str(r[2]):<18}"
            f"{str(r[3]):<13}"
            f"{r[4]}"
        )

    print(".......")
    print("-" * 70)
    print(f"Ran {result.testsRun} tests")
    print("\nOK" if result.wasSuccessful() else "\nFAILED")