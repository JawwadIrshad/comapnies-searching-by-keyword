import http.client
import json

def fetch_people_data(api_endpoint, keyword, per_page=5):
    """
    Fetch people data from Apollo API based on the given keyword.
    Args:
        api_endpoint (str): Apollo API endpoint.
        keyword (str): Keyword to search for.
        per_page (int): Number of results per page.

    Returns:
        list: Sorted list of people with their details, including emails where available.
    """
    api_key = ""

    if not api_key:
        raise ValueError("API key not found. Ensure it's set in the .env file.")

    # JSON Payload for the API Request
    payload = json.dumps({
        "person_titles": [
            "CEO", "Founder", "Owner", "President",
            "Chief Marketing Director", "Chief Marketing Officer", "Chief Executive Director"
        ],
        "person_locations": ["United States"],
        "q_keywords": keyword,
        "company_revenue_min": 1000000,
        "per_page": per_page
    })

    # Headers for the API Request
    headers = {
        'Cache-Control': 'no-cache',
        'Content-Type': 'application/json',
        'accept': 'application/json',
        'x-api-key': api_key,
    }

    # Establish HTTPS Connection
    conn = http.client.HTTPSConnection("api.apollo.io")

    try:
        # Make the POST Request
        conn.request("POST", api_endpoint, payload, headers)
        res = conn.getresponse()
        data = res.read().decode('utf-8')

        # Parse the JSON Data
        data = json.loads(data)

        # Check if "people" key exists and has results
        if "people" in data and data["people"]:
            sorted_people = sorted(data['people'], key=lambda person: person['name'])

            # Format results to include emails
            formatted_results = [
                {
                    "name": person['name'],
                    "title": person['title'],
                    "organization": person.get('organization', {}).get('name', 'Unknown Company'),
                    "email": person.get('email', 'No Email')  # Include email if available, otherwise 'No Email'
                }
                for person in sorted_people
            ]
            return formatted_results
        else:
            print(f"No results found for keyword: {keyword}")
            return []

    except Exception as e:
        print(f"Error fetching data: {e}")
        return []

    finally:
        conn.close()


def fetch_dummy_people_data():
    """
    Returns dummy data for testing without making actual API requests.

    Returns:
        list: A list of dictionaries, each representing a person's details.
    """
    # Example dummy data
    dummy_data = [
        {"name": "John Doe", "title": "CEO", "organization": "Tech Innovations"},
        {"name": "Jane Smith", "title": "CMO", "organization": "Health Solutions"},
        {"name": "Alice Johnson", "title": "Founder", "organization": "Eco Foods"},
        {"name": "Bob Brown", "title": "President", "organization": "Auto Advancements"},
        {"name": "Carol White", "title": "Chief Executive Officer", "organization": "Future Tech"}
    ]

    return dummy_data


# Example usage
if __name__ == "__main__":
    API_ENDPOINT = "/api/v1/mixed_people/search?includedOrganizationKeywordFields%5B%5D=tags&includedOrganizationKeywordFields%5B%5D=name&revenueRange%5Bmin%5D=1000000&company_keywords%5B%5D=CNC%2520Machines&sortByField=%5Bnone%5D&sortAscending=false&personTitles%5B%5D=President&personTitles%5B%5D=Owner&personTitles%5B%5D=CMO&personTitles%5B%5D=CEO&personTitles%5B%5D=chiefmarketingofficer&personTitles%5B%5D=chiefexecutiveofficer&personTitles%5B%5D=chiefmarketingdirector&personLocations%5B%5D=UnitedStates"
    
    keyword = "Food and Beverage"

    results = fetch_people_data(API_ENDPOINT, keyword)
    for result in results:
        print(f"{result['name']} - {result['title']} at {result['organization']} with email: {result['email']}")
