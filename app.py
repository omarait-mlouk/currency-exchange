import requests
import os
from dotenv import load_dotenv
import json
import sys

# Load the environment variables from the .env file
load_dotenv()

# Get the API key from the environment variables
api_key = os.getenv("API_KEY")

def make_get_request(endpoint, headers=None, timeout=5):
    """
    Make a GET request to the specified ENDPOINT using the given headers and timeout.

    Parameters:
        endpoint (str): The ENDPOINT to make the request to.
        headers (dict, optional): A dictionary of headers to include in the request.
        timeout (int, optional): The timeout value for the request in seconds.

    Returns:
        str: The text content of the response.

    Raises:
        Exception: If the request fails. The error message will describe the failure.
    """
    try:
        # Make the GET request
        response = requests.get(endpoint, headers=headers, timeout=timeout)
        # Raise an exception if the response has a status code indicating an error
        response.raise_for_status()
    except requests.exceptions.RequestException as error:
        # Raise an exception if the request failed for any reason
        raise Exception(f'Request failed with error: {error}')
    else:
        # If the request was successful, return the response content
        return response.text

def get_currencies():
    """
    Get the available currencies from the API.
    """
    # Set the headers to include the API key
    headers = {'apikey': api_key}
    # Build the ENDPOINT to get the available currencies
    endpoint = f"https://api.apilayer.com/fixer/symbols"
    try:
        # Get the response content from the API
        response_content = make_get_request(endpoint, headers, timeout=5)
        # Load the JSON data
        parsed_data = json.loads(response_content)
        # Check if the success key is true
        if parsed_data["success"]:
            # Access the symbols
            symbols = parsed_data["symbols"]
            # Iterate over the symbols and print the currency code and description
            for currency_code, description in symbols.items():
                print(f"{currency_code}: {description}")
        else:
            # If success is not true, handle the error
            print("Error while accessing symbols")
    except Exception as error:
        # Print an error message if the request failed
        print(f'Request failed with error: {error}')


def convert_currency(from_currency, to_currency, amount):
    """
    Convert a currency from one to another.

    Parameters:
        from_currency (str): The currency code to convert from.
        to_currency (str): The currency code to convert to.
        amount (str): The amount of the from currency to convert.
    """
    # Set the headers to include the API key
    headers = {'apikey': api_key}
    # Build the ENDPOINT to convert the currency
    endpoint = f"https://api.apilayer.com/fixer/convert?to={to_currency}"\
    f"&from={from_currency}&amount={amount}"
    try:
        # Get the response content from the API
        response_content = make_get_request(endpoint, headers, timeout=10)
        parsed_data = json.loads(response_content)
        # Check if the success key is true
        if parsed_data.get("success", False):
            # Access the symbols
            result = parsed_data["result"]
            query = parsed_data["query"]
            print(f"\n{query['amount']} {query['from']} ----> {result} {query['to']}")
        else:
            # If success is not true, handle the error
            error_message = parsed_data.get("message", "An unknown error occurred")
            print(f"Error while accessing symbols: {error_message}")
    except Exception as error:
        # Print an error message if the request failed
        print(f'Request failed with error: {error}')


def get_exchange_rate(base=None, symbols=None):
    """
    Retrieve the real-time exchange rate between two currencies. If either `from_currency` or `to_currency` are not specified, 
    the function returns the exchange rate of the default currency (e.g., USD) to all other currencies.

    Parameters:
        from_currency (str, optional): The code of the currency to convert from.
        to_currency (str, optional): The code of the currency to convert to.
    """
    # Set the headers to include the API key
    headers = {'apikey': api_key}
    # Define the API endpoint
    endpoint = "https://api.apilayer.com/fixer/latest"
    params = ['?']
    if symbols:
        # If symbols is provided, add it to the params list
        params.append(f"symbols={symbols}")
    # Check if the base parameter is provided
    if base:
        # If base is provided, add it to the params list
        params.append(f"base={base}")
    # Check if there are any parameters in the params list
    if params:
        # Join the parameters with an "&" and add them to the endpoint
        endpoint += "&".join(params)
    # Make the GET request to the API endpoint
    try:
        # Get the response content from the API
        response_content = make_get_request(endpoint, headers, timeout=5)
        # Load the JSON data
        parsed_data = json.loads(response_content)
        # Check if the success key is true
        if parsed_data.get("success", False):
            # Access the base
            base = parsed_data["base"]
            # Access the date
            date = parsed_data["date"]
            # Access the rates
            rates = parsed_data["rates"]
            print(f"\nBase: {base}\tDate: {date}")
            print("Rates: ")
            # Iterate over the rates and print the currency code and its rate
            for currency_code, rate in rates.items():
                print(f"{currency_code}: {rate}")
        else:
            # If success is not true, handle the error
            print("Error while accessing data")
    except Exception as error:
        # Print an error message if the request failed
        print(f'Request failed with error: {error}')


def quit_program():
    """
    Quit the program.
    """
    print("See ya!!")
    # Exit the program with a status code of 0, indicating a successful termination
    sys.exit(0)

# Dictionary of functions, where the keys are the choices 
# and the values are the functions to handle each choice
choice_handlers = {
    1: get_currencies,
    2: convert_currency,
    3: get_exchange_rate,
    4: quit_program,
}

def handle_choices(choice):
    """
    Handle the user's choice. The function retrieves the function to handle the choice from the `choice_handlers` dictionary, based on the `choice` argument.

    Parameters:
        choice (str): The choice made by the user.
    """
    try:
        # Convert the choice to int to check if it's valid
        int_value = int(choice)
    except ValueError:
        # If the choice is not a valid integer, print an error message
        print("Invalid input. Please enter a valid choice.")
    else:
        # Retrieve the function to handle the choice from the `choice_handlers` dictionary
        handler = choice_handlers.get(int_value, None)
        # If a handler was found, call the function
        if handler:
            if int_value == 2:
                # If the choice is 2 (convert currency), retrieve the from and to currency, and the amount
                from_currency = input("Enter the from currency: ")
                to_currency = input("Enter the to currency: ")
                amount = input("Enter the amount: ")
                handler(from_currency, to_currency, amount)
            elif int_value == 3:
                # If the choice is 2 (convert currency), retrieve the from and to currency, and the amount
                base = input("Enter the three-letter currency code of your preferred base currency: ")
                symbols = input("Enter a list of comma-separated currency codes to limit output currencies: ")
                handler(base, symbols)
            else:
                # If the choice is 1 (get currencies) or 3 (quit), call the handler function
                handler()
        # If no handler was found, handle the condition as a default
        else:
            # Code to handle the default condition
            print("Invalid input. Please enter a valid choice.")
    

def main():
    """
    The main function of the program. It continues to loop until the user decides to quit.
    """
    while True:
        # Ask the user to make a choice
        choice = int(input(
            "\n########### MENU #################\n"
            "## 1 - Available currencies.    ##\n"
            "## 2 - Convert a currency.      ##\n"
            "## 3 - Real-time exchange rate. ##\n"
            "## 4 - Quit.                    ##\n"
            "##################################\n"
            "Choose in the menu: "
        ))
        # Handle the user's choice
        handle_choices(choice)

if __name__ == "__main__":
    main()
