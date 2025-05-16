from src.gsheet import setup_google_sheets, get_keywords, create_tab, write_data_to_tab
from src.apollo import fetch_people_data, fetch_dummy_people_data

# Constants defining the sheet name and the API endpoint for fetching data
SHEET_NAME = "ApolloAPIAutomation"
API_ENDPOINT = ""

def main():
    user_input = input("Enter 'Y' to run Apollo companies people search automation or 'N' to exit: ").strip().lower()
    if user_input != 'y':
        print("Exiting...")
        return

    try:
        # Attempt to initialize Google Sheets connection
        sheet = setup_google_sheets(SHEET_NAME)
        print("Google Sheets successfully initialized!")  # Success prompt
    except Exception as e:
        print("Failed to initialize Google Sheets connection:", e)
        return

    try:
        keywords = get_keywords(sheet)
        if not keywords:
            print("No keywords found, exiting.")
            return
    except ValueError as e:
        print("Error retrieving keywords:", e)
        return

    for keyword in keywords:
        print(f"Processing keyword: {keyword}")
        try:
            create_tab(sheet, keyword)
            data = fetch_people_data(API_ENDPOINT, keyword)
            # data = fetch_dummy_people_data()
        except Exception as e:
            print(f"Error fetching data for keyword '{keyword}':", e)
            continue

        try:
            formatted_data = [
                [
                    person.get('name', '').split()[0],  # First Name
                    ' '.join(person.get('name', '').split()[1:]),  # Last Name
                    person.get('title', ''),  # Title
                    person.get('organization', 'Unknown Company'),  # Company
                    person.get('organization', 'Unknown Company'),  # Company Name for Emails
                    person.get('email', 'No Email'),  # Email
                    'Verified'  # Email Status
                ]
                for person in data
            ]
            write_data_to_tab(sheet, keyword, formatted_data)
            print(f"Successfully wrote data to tab for keyword '{keyword}'.")
        except Exception as e:
            print(f"Error formatting or writing data for keyword '{keyword}':", e)

if __name__ == "__main__":
    main()
