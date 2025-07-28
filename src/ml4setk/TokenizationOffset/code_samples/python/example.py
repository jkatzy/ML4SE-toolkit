import os

class DataProcessor:
    def __init__(self, data):
        self.data = data # Initialize data

    def calculate_average(self):
        """This function calculates the average."""
        if not self.data:
            return 0
        total_sum = sum(self.data)
        return total_sum / len(self.data)

def main_function(file_path: str):
    processor = DataProcessor([10, 20, 30, 40, 50])
    avg = processor.calculate_average()
    print(f"The average is: {avg}")