# === Healthcare Value CLI Tool ===
# Menu Options:
# 1. Search Plans by State
# 2. Compare Average Rates by Metal Level in a State
# 3. View Plan Details by Plan Number (from a state-filtered list)
# 4. View Issuer Details
# 5. Exit

# === Imports ===
# Import necessary libraries to connect to PostgreSQL, securely get passwords, and exit the script
import psycopg2
import sys
import getpass

# === Database Connection Function ===
# This function prompts the user for their PostgreSQL password and returns a live database connection
def connect_db():
    try:
        # Prompt user for PostgreSQL password (input is hidden for security)
        password = getpass.getpass("Enter your PostgreSQL password: ")

        # Establish a connection to the PostgreSQL database using provided credentials
        connection = psycopg2.connect(
            host="localhost",                # Host where PostgreSQL is running
            database="healthcare_value_db",  # Name of the database
            user="postgres",                # SQL Database username
            password="postgres"                 # SQL Database Password entered by the user
        )

        return connection  # Return the connection object

    except Exception as e:
        # Print error message if connection fails and exit the program
        print("Database connection failed:", e)
        sys.exit()

# === Option 1: Search Plans by State ===
# This function retrieves plans based on a user-provided state code

def search_plans_by_state():
    # Ask user to enter a 2-letter state code (e.g., CA, NY)
    state_code = input("Enter a 2-letter state code (e.g., IL): ").upper()

    # Connect to the database
    conn = connect_db()
    cursor = conn.cursor()

    try:
        # SQL query to get plans from the PlanAttributes table for the entered state
        query = '''
        SELECT "PlanID", "PlanMarketingName", "MetalLevel", "IssuerID"
        FROM "PlanAttributes"
        WHERE "StateCode" = %s
        LIMIT 10;
        '''

        # Execute query with the provided state code as a parameter
        cursor.execute(query, (state_code,))
        results = cursor.fetchall()  # Fetch all matching rows

        # Print each matching plan if found
        if results:
            print(f"\n--- Plans available in {state_code} ---")
            for row in results:
                print(f"PlanID: {row[0]}, Name: {row[1]}, Metal: {row[2]}, IssuerID: {row[3]}")
        else:
            print(f"No plans found for state: {state_code}")

    except Exception as e:
        # Handle any error during query execution
        print("An error occurred while fetching plans:", e)

    finally:
        # Always close the cursor and connection
        cursor.close()
        conn.close()

# === Option 2: Compare Average Rates by Metal Level in a State ===
def compare_average_rates_by_metal_level():
    # Prompt the user to enter a 2-letter state code (e.g., CA)
    state_code = input("Enter a 2-letter state code (e.g., IL): ").upper()

    # Connect to the PostgreSQL database
    conn = connect_db()
    cursor = conn.cursor()

    try:
        # SQL query to calculate average individual rate per metal level
        query = '''
        SELECT "MetalLevel", ROUND(AVG("IndividualRate")::numeric, 2) AS avg_rate
        FROM "PlanAttributes" AS pa
        JOIN "Rates" AS r ON pa."PlanID" = r."PlanID"
        WHERE pa."StateCode" = %s
        GROUP BY "MetalLevel"
        ORDER BY avg_rate DESC;
        '''

        # Execute the query with the user-provided state code
        cursor.execute(query, (state_code,))

        # Fetch the results of the query
        results = cursor.fetchall()

        # If results were returned, display them to the user
        if results:
            print(f"\n--- Average Individual Rates by Metal Level in {state_code} ---")
            for row in results:
                metal_level = row[0]
                avg_rate = row[1]
                print(f"{metal_level}: ${avg_rate}")
        else:
            # Inform the user if there are no results for the given state
            print(f"No rate data found for state: {state_code}")

    except Exception as e:
        # Handle and print any error that occurs
        print("An error occurred while calculating average rates:", e)

    finally:
        # Ensure the database connection is closed regardless of outcome
        cursor.close()
        conn.close()

# === Option 3: View Plan Details by Plan Number (from a state-filtered list) ===

def view_plan_details_by_selection():
    # Step 1: Ask the user for a 2-letter state code
    state_code = input("Enter a 2-letter state code (e.g., IL): ").upper()

    # Connect to the database
    conn = connect_db()
    cursor = conn.cursor()

    try:
        # SQL query to retrieve basic plan information for the given state
        query = '''
        SELECT "PlanID", "PlanMarketingName", "MetalLevel", "IssuerID"
        FROM "PlanAttributes"
        WHERE "StateCode" = %s
        LIMIT 10;
        '''
        cursor.execute(query, (state_code,))
        plans = cursor.fetchall()

        # Check if any plans were found
        if not plans:
            print(f"No plans found for state: {state_code}")
            return

        # Display a numbered list of plans for user to choose from
        print(f"\n--- Available Plans in {state_code} ---")
        for idx, plan in enumerate(plans, start=1):
            print(f"{idx}. PlanID: {plan[0]} | Name: {plan[1]} | Metal: {plan[2]} | IssuerID: {plan[3]}")

        # Step 2: Prompt user to choose a plan number from the list
        selection = input("Enter the number of the plan you want to view in detail: ")

        # Validate the selection
        if not selection.isdigit() or int(selection) < 1 or int(selection) > len(plans):
            print("Invalid selection. Please enter a valid number from the list.")
            return

        # Get the PlanID corresponding to the selected number
        selected_plan_id = plans[int(selection) - 1][0]

        # Query for full plan details using the selected PlanID
        detail_query = '''
        SELECT *
        FROM "PlanAttributes"
        WHERE "PlanID" = %s;
        '''
        cursor.execute(detail_query, (selected_plan_id,))
        plan_details = cursor.fetchone()

        # Get column names to pair with values for display
        colnames = [desc[0] for desc in cursor.description]

        # Display full plan detail nicely
        print(f"\n--- Full Details for PlanID: {selected_plan_id} ---")
        for col, val in zip(colnames, plan_details):
            print(f"{col}: {val}")

    except Exception as e:
        print("An error occurred while retrieving plan details:", e)

    finally:
        # Clean up database resources
        cursor.close()
        conn.close()

# === Option 4: View Issuer Details ===
# This function retrieves issuer details based on IssuerID

def view_issuer_details():
    # Prompt user to input an IssuerID (e.g., 12345)
    issuer_id = input("Enter an Issuer ID: ")

    # Connect to the database
    conn = connect_db()
    cursor = conn.cursor()

    try:
        # SQL query to fetch issuer marketing name by issuer ID
        query = '''
        SELECT *
        FROM "Issuer"
        WHERE "IssuerID" = %s;
        '''

        # Execute the query with the user input
        cursor.execute(query, (issuer_id,))
        result = cursor.fetchone()

        # Display issuer details if found
        if result:
            print("\n--- Issuer Details ---")
            for i, col in enumerate(cursor.description):
                print(f"{col.name}: {result[i]}")
        else:
            print("No issuer found with the provided Issuer ID.")

    except Exception as e:
        # Catch and print any errors
        print("An error occurred while fetching issuer details:", e)

    finally:
        # Always close cursor and connection
        cursor.close()
        conn.close()

# === Main Menu ===
# This function displays the menu and routes the user to their selected option

def main():
    print("\n=== Healthcare Value CLI Tool ===")
    print("1. Search Plans by State")
    print("2. Compare Average Rates by State")
    print("3. View Plan Details by State Selecting a Plan Number from the List")
    print("4. View Issuer Details")
    print("5. Exit")

    # Ask user to choose an option
    choice = input("Select an option: ")

    # Route to correct function based on selection
    if choice == '1':
        search_plans_by_state()
    elif choice == '2':
        compare_average_rates_by_metal_level()
    elif choice == '3':
        view_plan_details_by_selection()
    elif choice == '4':
        view_issuer_details()
    elif choice == '5':
        # Exit the program
        print("Goodbye!")
        sys.exit()
    else:
        # Handle invalid selection
        print("Invalid selection. Try again.")

# === Script Entry Point ===
# This ensures the main menu continues to show in a loop until exit
if __name__ == "__main__":
    while True:
        main()
