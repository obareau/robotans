import random
import requests

# Predefined API sources or static lists for names based on countries
name_sources = {
    "japan": "https://randomuser.me/api/?nat=jp&gender=",
    "france": "https://randomuser.me/api/?nat=fr&gender=",
    "usa": "https://randomuser.me/api/?nat=us&gender=",
    "india": "https://randomuser.me/api/?nat=in&gender=",
    "arab": ["Ahmed", "Fatima", "Ali", "Sara", "Yousef", "Noor", "Hassan", "Layla", "Omar", "Amina"],
    "kabyle": ["Tahar", "Malika", "Lounis", "Siham", "Arezki", "Yasmina", "Rachid", "Djamila", "Slimane", "Amel"],
    "african": ["Kwame", "Amina", "Chidi", "Fatou", "Tunde", "Adama", "Zubeda", "Nia", "Omari", "Sefu"]
}

# Function to fetch names from an API
def fetch_names_from_api(country, gender):
    try:
        if country in ["japan", "france", "usa", "india"]:
            api_url = name_sources[country] + gender
            response = requests.get(api_url)
            if response.status_code == 200:
                data = response.json()
                # Extract name from API response
                return [data["results"][0]["name"]["first"].capitalize()]
            else:
                print(f"Error fetching names for {country}.")
                return []
        else:
            return name_sources[country]
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

# Function to generate Robotan names
def generate_robotan_name(country, gender):
    names = fetch_names_from_api(country, gender)
    if not names:
        print("No names available to generate Robotan names.")
        return None
    
    # Generate a random name and number
    name = random.choice(names)
    number = random.randint(1, 999)  # Generate a two-digit number
    return f"{name}-{str(number).zfill(3)}"

# Example usage
def main():
    print("Welcome to the Robotan Name Generator!")
    country = input("Enter the country for the Robotan's name (e.g., japan, france, usa, india, arab, kabyle, african): ").strip().lower()
    gender = input("Enter the gender for the Robotan (male/female): ").strip().lower()
    name = generate_robotan_name(country, gender)
    if name:
        print(f"Generated Robotan Name: {name}")

if __name__ == "__main__":
    main()