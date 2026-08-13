from enum import Enum


class temperature_supported_type(Enum):
    CELSIUS = "C"
    FAHRENHEIT = "F"

class temperature_input_validator:
    def validate(self, user_input):
        if len(user_input) < 2:
            print("Invalid input. Please enter a temperature followed by 'C' or 'F'.")
            return False

        temp_value = user_input[1:]
        temp_unit = user_input[0].upper()

        supported_temp_units = [temp_type.value for temp_type in temperature_supported_type]
        if temp_unit not in supported_temp_units:
            print("Invalid temperature unit. Please use 'C' for Celsius or 'F' for Fahrenheit.")
            return False
        
        if not temp_value.isdigit():
            print("Invalid temperature value. Please enter a numeric value.")
            return False

        return True

class temperature_converter:
    
    def celsius_to_fahrenheit(self, celsius):
        return (celsius * 9/5) + 32
    
    def fahrenheit_to_celsius(self, fahrenheit):
        return (fahrenheit - 32) * 5/9 
    
    def convert(self, temperature_input):
        temp_value = int(temperature_input[1:])
        temp_unit = temperature_input[0].upper()

        if temp_unit == temperature_supported_type.CELSIUS.value:
            converted_temp = self.celsius_to_fahrenheit(temp_value)
            print(f"{temp_value}°C is equal to {converted_temp:.2f}°F")
            
        elif temp_unit == temperature_supported_type.FAHRENHEIT.value:
            converted_temp = self.fahrenheit_to_celsius(temp_value)
            print(f"{temp_value}°F is equal to {converted_temp:.2f}°C")

def init():    
    validator = temperature_input_validator()
    converter = temperature_converter()
    
    while True:
        user_input = input("Enter temperature or blank to exit: ")
        if user_input == "":
            return
        if not validator.validate(user_input):
            print("Invalid input. Please enter a temperature followed by 'C' or 'F'.")
        else:
            converter.convert(user_input)

if __name__ == "__main__":
    init()