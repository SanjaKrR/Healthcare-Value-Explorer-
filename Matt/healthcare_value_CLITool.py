# === Healthcare Value CLI Tool ===
# Menu Options:
# 1. Search Plans by State
# 2. Compare Average Rates by Metal Level in a State
# 3. Average Monthly Rate by Plan Type in a State
# 4. Top 5 Lowest Cost Plans in a State
# 5. View Plan Details by Plan Number (from a state-filtered list)
# 6. View Issuer Details
# 7. Exit

# === Imports ===
# Import necessary libraries to connect to PostgreSQL, securely get passwords, and exit the script
import psycopg2
import sys
import getpass

# === Database Connection Function ===
# This function prompts the user for their PostgreSQL password and returns a live database connection
def connect_db():
    try:
        # Prompt user for PostgreSQL password (input is hidden for security
        password = getpass.getpass("postgres")

        # Establish a connection to the PostgreSQL database using provided credentials
        connection = psycopg2.connect(
            host="localhost",                # Host where PostgreSQL is running
            database="HealthCareValue_DB1",  # Name of the database
            user="postgres",                 # SQL Database username
            password="postgres"              # SQL Database password (replace if needed)
        )
        return connection  # Return the connection object

    except Exception as e:
        # Print error message if connection fails and exit the program
        print("Database connection failed:", e)
        sys.exit()

# === Option 1: Search Plans by State ===
# This function retrieves non-dental, non-SHOP plans based on a user-provided state code
def search_plans_by_state():
    state_code = input("Enter a 2-letter state code (e.g., IL): ").upper()
    conn = connect_db()
    cursor = conn.cursor()

    try:
        query = '''
        SELECT "PlanID", "PlanMarketingName", "MetalLevel", "IssuerID"
        FROM "PlanAttributes"
        WHERE "StateCode" = %s
        AND "DentalOnlyPlan" != 'Yes'
        AND "MarketCoverage" != 'SHOP'
        LIMIT 10;
        '''
        cursor.execute(query, (state_code,))
        results = cursor.fetchall()

        if results:
            print(f"\n--- Plans available in {state_code} ---")
            for row in results:
                print(f"PlanID: {row[0]}, Name: {row[1]}, Metal: {row[2]}, IssuerID: {row[3]}")
        else:
            print(f"No plans found for state: {state_code}")

    except Exception as e:
        print("An error occurred while fetching plans:", e)

    finally:
        cursor.close()
        conn.close()

# === Option 2: Compare Average Rates by Metal Level in a State ===
# This function calculates the average individual rates per metal level for a given state
def compare_average_rates_by_metal_level():
    state_code = input("Enter a 2-letter state code (e.g., IL): ").upper()
    conn = connect_db()
    cursor = conn.cursor()

    try:
        query = '''
        SELECT "MetalLevel", ROUND(AVG("IndividualRate")::numeric, 2) AS avg_rate
        FROM "PlanAttributes" AS pa
        JOIN "Rates" AS r ON pa."PlanID" = r."PlanID"
        WHERE pa."StateCode" = %s
        AND pa."DentalOnlyPlan" != 'Yes'
        AND pa."MarketCoverage" != 'SHOP'
        GROUP BY "MetalLevel"
        ORDER BY avg_rate DESC;
        '''
        cursor.execute(query, (state_code,))
        results = cursor.fetchall()

        if results:
            print(f"\n--- Average Individual Rates by Metal Level in {state_code} ---")
            for row in results:
                print(f"{row[0]}: ${row[1]}")
        else:
            print(f"No rate data found for state: {state_code}")

    except Exception as e:
        print("An error occurred while calculating average rates:", e)

    finally:
        cursor.close()
        conn.close()

# === Option 3: Average Monthly Rate by Plan Type in a State ===
# This function shows average rates by plan type (e.g., HMO, PPO) for a given state
def average_rate_by_plan_type():
    state_code = input("Enter a 2-letter state code (e.g., IL): ").upper()
    conn = connect_db()
    cursor = conn.cursor()

    try:
        query = '''
        SELECT "PlanType", ROUND(AVG("IndividualRate")::numeric, 2) AS avg_rate
        FROM "PlanAttributes" AS pa
        JOIN "Rates" AS r ON pa."PlanID" = r."PlanID"
        WHERE pa."StateCode" = %s
        AND pa."DentalOnlyPlan" != 'Yes'
        AND pa."MarketCoverage" != 'SHOP'
        GROUP BY "PlanType"
        ORDER BY avg_rate DESC;
        '''
        cursor.execute(query, (state_code,))
        results = cursor.fetchall()

        if results:
            print(f"\n--- Average Monthly Rate by Plan Type in {state_code} ---")
            for row in results:
                print(f"{row[0]}: ${row[1]}")
        else:
            print(f"No rate data found for state: {state_code}")

    except Exception as e:
        print("An error occurred while calculating plan type averages:", e)

    finally:
        cursor.close()
        conn.close()

# === Option 4: Top 5 Lowest Cost Plans in a State ===
# This function lists the 5 lowest individual rate plans in a state (excluding dental/SHOP)
def top_lowest_cost_plans():
    state_code = input("Enter a 2-letter state code (e.g., IL): ").upper()
    conn = connect_db()
    cursor = conn.cursor()

    try:
        query = '''
        SELECT pa."PlanID", pa."PlanMarketingName", ROUND(MIN(r."IndividualRate")::numeric, 2) AS min_rate
        FROM "PlanAttributes" AS pa
        JOIN "Rates" AS r ON pa."PlanID" = r."PlanID"
        WHERE pa."StateCode" = %s
        AND pa."DentalOnlyPlan" != 'Yes'
        AND pa."MarketCoverage" != 'SHOP'
        GROUP BY pa."PlanID", pa."PlanMarketingName"
        ORDER BY min_rate ASC
        LIMIT 5;
        '''
        cursor.execute(query, (state_code,))
        results = cursor.fetchall()

        if results:
            print(f"\n--- Top 5 Lowest Cost Plans in {state_code} ---")
            for row in results:
                print(f"PlanID: {row[0]}, Name: {row[1]}, Rate: ${row[2]}")
        else:
            print(f"No cost data found for state: {state_code}")

    except Exception as e:
        print("An error occurred while retrieving cost data:", e)

    finally:
        cursor.close()
        conn.close()

# === Option 5: View Plan Details by Plan Number (from a state-filtered list) ===
# This function allows the user to view detailed info for a selected plan from a short list
def view_plan_details_by_selection():
    state_code = input("Enter a 2-letter state code (e.g., IL): ").upper()
    conn = connect_db()
    cursor = conn.cursor()

    try:
        query = '''
        SELECT "PlanID", "PlanMarketingName", "MetalLevel", "IssuerID"
        FROM "PlanAttributes"
        WHERE "StateCode" = %s
        AND "DentalOnlyPlan" != 'Yes'
        AND "MarketCoverage" != 'SHOP'
        LIMIT 10;
        '''
        cursor.execute(query, (state_code,))
        plans = cursor.fetchall()

        if not plans:
            print(f"No plans found for state: {state_code}")
            return

        print(f"\n--- Available Plans in {state_code} ---")
        for idx, plan in enumerate(plans, start=1):
            print(f"{idx}. PlanID: {plan[0]} | Name: {plan[1]} | Metal: {plan[2]} | IssuerID: {plan[3]}")

        selection = input("Enter the number of the plan you want to view in detail: ")

        if not selection.isdigit() or int(selection) < 1 or int(selection) > len(plans):
            print("Invalid selection. Please enter a valid number from the list.")
            return

        selected_plan_id = plans[int(selection) - 1][0]

        detail_query = '''
        SELECT * FROM "PlanAttributes"
        WHERE "PlanID" = %s;
        '''
        cursor.execute(detail_query, (selected_plan_id,))
        plan_details = cursor.fetchone()

        colnames = [desc[0] for desc in cursor.description]
        print(f"\n--- Full Details for PlanID: {selected_plan_id} ---")
        for col, val in zip(colnames, plan_details):
            print(f"{col}: {val}")

    except Exception as e:
        print("An error occurred while retrieving plan details:", e)

    finally:
        cursor.close()
        conn.close()

# === Option 6: View Issuer Details ===
# This function allows the user to retrieve issuer information by entering an IssuerID
def view_issuer_details():
    issuer_id = input("Enter an Issuer ID: ")
    conn = connect_db()
    cursor = conn.cursor()

    try:
        query = '''
        SELECT * FROM "Issuer"
        WHERE "IssuerID" = %s;
        '''
        cursor.execute(query, (issuer_id,))
        result = cursor.fetchone()

        if result:
            print("\n--- Issuer Details ---")
            for i, col in enumerate(cursor.description):
                print(f"{col.name}: {result[i]}")
        else:
            print("No issuer found with the provided Issuer ID.")

    except Exception as e:
        print("An error occurred while fetching issuer details:", e)

    finally:
        cursor.close()
        conn.close()

# === Main Menu ===
# This function displays the CLI menu and routes the user to their chosen option
def main():
    print("\n=== Healthcare Value CLI Tool ===")
    print("1. Search Plans by State")
    print("2. Compare Average Rates by Metal Level in a State")
    print("3. Average Monthly Rate by Plan Type in a State")
    print("4. Top 5 Lowest Cost Plans in a State")
    print("5. View Plan Details by Plan Number (from a state-filtered list)")
    print("6. View Issuer Details")
    print("7. Exit")

    choice = input("Select an option: ")

    if choice == '1':
        search_plans_by_state()
    elif choice == '2':
        compare_average_rates_by_metal_level()
    elif choice == '3':
        average_rate_by_plan_type()
    elif choice == '4':
        top_lowest_cost_plans()
    elif choice == '5':
        view_plan_details_by_selection()
    elif choice == '6':
        view_issuer_details()
    elif choice == '7':
        print("Goodbye!")
        sys.exit()
    else:
        print("Invalid selection. Try again.")

# === Script Entry Point ===
# This loop ensures the main menu keeps displaying until the user exits
if __name__ == "__main__":
    while True:
        main()

