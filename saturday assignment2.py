import requests
import json
import csv
import os

class IPInfoClient:
    """
    A client for fetching IP geolocation data from the IPInfo API.
    """
    
    def __init__(self, token: str = None):
        """
        Initializes the client with an optional API token.
        
        Args:
            token (str): Optional API token for authenticated requests.
        """
        self.base_url = "https://ipinfo.io/json"
        self.token = token
    
    def fetch_data(self) -> dict:
        """
        Fetches IP geolocation data from the IPInfo API.
        
        Returns:
            dict: Parsed JSON data from the API response.
        """
        url = self.base_url
        if self.token:
            url += f"?token={self.token}"
        
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an error for bad status codes
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching data: {e}")
            return None
    
    def save_data_json(self, data: dict, filename: str = "ipinfo_data.json"):
        """
        Saves the data to a JSON file.
        
        Args:
            data (dict): The data to save.
            filename (str): Name of the file to save the JSON data.
        """
        try:
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, 'w') as json_file:
                json.dump(data, json_file, indent=4)
            print(f"Data successfully saved to {filename}")
        except IOError as e:
            print(f"Error saving JSON file: {e}")
    
    def save_data_csv(self, data: dict, filename: str = "ipinfo_data.csv"):
        """
        Saves the data to a CSV file.
        This function assumes the data is a flat dictionary.
        
        Args:
            data (dict): The data to save.
            filename (str): Name of the CSV file.
        """
        try:
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, 'w', newline='') as csv_file:
                writer = csv.writer(csv_file)
                # Write header
                writer.writerow(data.keys())
                # Write values
                writer.writerow(data.values())
            print(f"Data successfully saved to {filename}")
        except IOError as e:
            print(f"Error saving CSV file: {e}")
    
    def display_data(self, data: dict):
        """
        Displays the data in a readable format.
        
        Args:
            data (dict): The data to display.
        """
        if data:
            print("IP Information:")
            for key, value in data.items():
                print(f"{key.capitalize()}: {value}")
        else:
            print("No data to display.")

def main():
    """
    Main function to execute the IPInfo data retrieval process.
    """
    # Create an instance of IPInfoClient.
    # If you have an API token, include it as an argument: IPInfoClient(token="YOUR_TOKEN")
    client = IPInfoClient()
    
    # Fetch the data from the API.
    data = client.fetch_data()
    
    # If data is successfully fetched, display it and save it.
    if data:
        client.display_data(data)
        
        # Save data as JSON
        client.save_data_json(data)
        
        # Save data as CSV
        client.save_data_csv(data)
    else:
        print("Failed to retrieve IP data.")

if __name__ == "__main__":
    main()