import mysql.connector
import datetime
from os import system, name

# Function to clear the screen
def clear():
    if name == 'nt':
        _ = system('cls')  
    else:
        _ = system('clear')

class FoodReviewCLI:
    # Function to connect to database
    def __init__(self, host, user, password, database):
        try:
            self.connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            self.cursor = self.connection.cursor()
            print("Connected to database successfully.")
        except mysql.connector.Error as err:
            print(f"Error connecting to database: {err}")
            exit()

    # Function for the main menu
    def main_menu(self):
        while True:
            clear()
            print("\nFood Review CLI Menu:")
            print("1. Review Management")
            print("2. Establishment Management")
            print("3. Food Item Management")
            print("4. Report Generation")
            print("5. Exit")
            choice = input("Enter your choice: ")

            if choice == '1':
                self.review_management_menu()
            elif choice == '2':
                self.establishment_management_menu()
            elif choice == '3':
                self.food_item_management_menu()
            elif choice == '4':
                self.report_management_menu()
            elif choice == '5':
                print("Exiting Food Review CLI.")
                exit()
            else:
                print("Invalid choice. Please try again.")
                input("Press Enter to proceed")


    # Function for the review management
    def review_management_menu(self):
        print("\nReview Management Menu:")
        print("1. Add Review")
        print("2. Update Review")
        print("3. Delete Review")
        print("4. Search Reviews")
        print("5. Back to Main Menu")
        choice = input("Enter your choice: ")

        if choice == '1':
            # Get user input for review details (text, rating, date, estno, userno)
            text = input("Enter review text: ")
            while True:
                try:
                    rating = int(input("Enter rating (1-5): "))
                    if 1 <= rating <= 5:
                        break
                    else:
                        print("Invalid rating. Please enter a number between 1 and 5.")
                except ValueError:
                    print("Invalid input. Please enter a number.")
            date = input("Enter date (DD-MM-YYYY): ")
            estno = int(input("Enter establishment number: "))
            userno = int(input("Enter user number: "))
            self.add_review(text, rating, date, estno, userno)
        elif choice == '2':
            # Get review ID for update
            reviewno = int(input("Enter review ID to update: "))
            # Prompt user for specific update (text, rating, estno, foodno)
            update_choice = input("Update (text/rating/estno/foodno) or 'back' to menu: ")
            if update_choice.lower() == 'back':
                self.review_management_menu()
            elif update_choice.lower() == 'text':
                new_text = input("Enter new review text: ")
                self.update_review_text(new_text, reviewno)
            elif update_choice.lower() == 'rating':
                while True:
                    try:
                        new_rating = int(input("Enter new rating (1-5): "))
                        if 1 <= new_rating <= 5:
                            self.update_review_rating(new_rating, reviewno)
                            break
                        else:
                            print("Invalid rating. Please enter a number between 1 and 5.")
                    except ValueError:
                        print("Invalid input. Please enter a number.")
            elif update_choice.lower() in ('estno', 'foodno'):
                if update_choice.lower() == 'estno':
                    print("Update establishment number is not currently supported.")
                else:
                    print("Update food item number is not currently supported.")
                # Implement update_review_est_food_no function when supported
            else:
                print("Invalid choice. Please try again.")
        elif choice == '3':
            # Get review ID for deletion
            reviewno = int(input("Enter review ID to delete: "))
            self.delete_review(reviewno)
        elif choice == '4':
            # Allow searching by various criteria (text, rating, establishment, etc.)
            # Implement search logic using appropriate SQL queries
            print("Search functionality for reviews is not yet implemented.")
        elif choice == '5':
            pass  # Back to main menu
        else:
            clear()
            print("Invalid choice. Please try again.")
            self.review_management_menu()

    # Function for the food establishment management
    def establishment_management_menu(self):
        print("\nEstablishment Management Menu:")
        print("1. Add Establishment")
        print("2. Update Establishment")
        print("3. Delete Establishment")
        print("4. Search Establishment")
        print("5. Back to Main Menu")
        choice = input("Enter your choice: ")

        if choice == '1':
            # Get user input for establishment name
            estname = input("Enter establishment name: ")
            self.add_establishment(estname)
        elif choice == '2':
            # Get existing establishment name for update
            estname = input("Enter establishment name to update: ")
            new_estname = input("Enter new establishment name: ")
            self.update_establishment(new_estname, estname)
        elif choice == '3':
            # Get establishment name for deletion
            estname = input("Enter establishment name to delete: ")
            self.delete_establishment(estname)
        elif choice == '4':
            # Get establishment name for search
            estname = input("Enter establishment name to search: ")
            self.search_establishment(estname)
        elif choice == '5':
            pass  # Back to main menu
        else:
            print("Invalid choice. Please try again.")
            self.establishment_management_menu()

    # Function for the food item management
    def food_item_management_menu(self):
        print("\nFood Item Management Menu:")
        print("1. Add Food Item")
        print("2. Update Food Item Price")
        print("3. Delete Food Item")
        print("4. Search Food Item")
        print("5. Back to Main Menu")
        choice = input("Enter your choice: ")

        if choice == '1':
            # Get user input for food item details (name, price, type, estno)
            foodname = input("Enter food item name: ")
            while True:
                try:
                    price = float(input("Enter price: "))
                    if price >= 0:
                        break
                    else:
                        print("Invalid price. Please enter a non-negative number.")
                except ValueError:
                    print("Invalid input. Please enter a number.")
            foodtype = input("Enter food type: ")
            estno = int(input("Enter establishment number: "))
            self.add_food_item(foodname, price, foodtype, estno)
        elif choice == '2':
            # Get food item name for price update
            foodname = input("Enter food item name to update price: ")
            while True:
                try:
                    new_price = float(input("Enter new price: "))
                    if new_price >= 0:
                        self.update_food_item(new_price, foodname)
                        break
                    else:
                        print("Invalid price. Please enter a non-negative number.")
                except ValueError:
                    print("Invalid input. Please enter a number.")
        elif choice == '3':
            # Get food item name for deletion
            foodname = input("Enter food item name to delete: ")
            self.delete_food_item(foodname)
        elif choice == '4':
            # Get food item name for search
            foodname = input("Enter food item name to search: ")
            # Implement search logic using appropriate SQL queries
            print("Search functionality for food items is not yet implemented.")
        elif choice == '5':
            pass  # Back to main menu
        else:
            print("Invalid choice. Please try again.")
            self.food_item_management_menu()        

    def close(self):
        self.cursor.close()
        self.connection.close()

    # Function for the food review management
    # Review Management Functions
    def add_review(self, text, rating, date, estno, userno):
        try:
            # Validate rating is within range (1-5)
            if not (1 <= rating <= 5):
                raise ValueError("Rating must be between 1 and 5.")

            # Format date for SQL compatibility (example: '%Y-%m-%d')
            formatted_date = datetime.datetime.strptime(date, '%d-%M-%Y').strftime('%Y-%m-%d')

            # Check if establishment and user exist
            check_est_query = "SELECT estno FROM establishment WHERE estno = %s"
            check_user_query = "SELECT userno FROM user WHERE userno = %s"
            cursor = self.connection.cursor()
            cursor.execute(check_est_query, (estno,))
            est_exists = cursor.fetchone()
            cursor.execute(check_user_query, (userno,))
            user_exists = cursor.fetchone()

            if not est_exists or not user_exists:
                raise ValueError("Invalid establishment or user ID.")

            # Insert review
            sql = """INSERT INTO review (text, rating, date, foodno, estno, userno)
                    VALUES (%s, %s, STR_TO_DATE(%s, '%Y-%m-%d'), NULL, %s, %s)"""
            self.cursor.execute(sql, (text, rating, formatted_date, estno, userno))
            self.connection.commit()
            print("Review added successfully!")
        except ValueError as e:
            print(f"Error adding review: {e}")
        except mysql.connector.Error as err:
            print(f"Error adding review: {err}")

    def update_review_text(self, new_text, reviewno):
        try:
            sql = "UPDATE review SET text = %s WHERE reviewno = %s"
            self.cursor.execute(sql, (new_text, reviewno))
            self.connection.commit()
            if self.cursor.rowcount > 0:
                print("Review text updated successfully!")
            else:
                print("Review not found.")
        except mysql.connector.Error as err:
            print(f"Error updating review text: {err}")

    def update_review_rating(self, new_rating, reviewno):
        try:
        # Validate new_rating is within range (1-5)
            if not (1 <= new_rating <= 5):
                raise ValueError("Rating must be between 1 and 5.")
            sql = "UPDATE review SET rating = %s WHERE reviewno = %s"
            self.cursor.execute(sql, (new_rating, reviewno))
            self.connection.commit()
            if self.cursor.rowcount > 0:
                print("Review rating updated successfully!")
            else:
                print("Review not found.")
        except ValueError as e:
            print(f"Error: {e}")
        except mysql.connector.Error as err:
            print(f"Error updating review rating: {err}")

    def update_review_est_food_no(self, new_estno, new_foodno, reviewno):
        try:
            sql = "UPDATE review SET estno = %s, foodno = %s WHERE reviewno = %s"
            self.cursor.execute(sql, (new_estno, new_foodno, reviewno))
            self.connection.commit()
            if self.cursor.rowcount > 0:
                print("Review establishment & food item number updated successfully!")
            else:
                print("Review not found.")
        except mysql.connector.Error as err:
            print(f"Error updating review establishment & food item number: {err}")

    def delete_review(self, reviewno):
        try:
        # Confirmation prompt
            confirm = input(f"Are you sure you want to delete review #{reviewno}? (y/n): ")
            if confirm.lower() != 'y':
                print("Deletion cancelled.")
                return

            sql = "DELETE FROM review WHERE reviewno = %s"
            self.cursor.execute(sql, (reviewno,))
            self.connection.commit()
            print("Review deleted successfully!")
        except mysql.connector.Error as err:
            print(f"Error deleting review: {err}")

    # Establishment Management Functions
    # Function to add an establishment
    def add_establishment(self, estname):
        try:
            sql = "INSERT INTO establishment (estname) VALUES (%s)"
            self.cursor.execute(sql, (estname,))
            self.connection.commit()
            print("Establishment added successfully!")
        except mysql.connector.Error as err:
            print(f"Error adding establishment: {err}")

    # Function to delete an establishment
    def delete_establishment(self, estname):
        try:
        # Find establishment number (with error handling)
            sql = "SELECT estno FROM establishment WHERE estname = %s"
            self.cursor.execute(sql, (estname,))
            estno = self.cursor.fetchone()
            if estno is None:
                print(f"Establishment '{estname}' not found.")
                return

            # Confirmation prompt
            confirm = input(f"Are you sure you want to delete '{estname}' (including its reviews and food items)? (y/n): ")
            if confirm.lower() != 'y':
                print("Deletion cancelled.")
                return

            # Delete reviews referencing the establishment
            sql = "DELETE FROM review WHERE estno = %s"
            self.cursor.execute(sql, (estno[0],))  # Use first element of estno tuple
            self.connection.commit()

            # Delete food items belonging to the establishment
            sql = "DELETE FROM food WHERE estno = %s"
            self.cursor.execute(sql, (estno[0],))
            self.connection.commit()

            # Delete the establishment itself
            sql = "DELETE FROM establishment WHERE estname = %s"
            self.cursor.execute(sql, (estname,))
            self.connection.commit()
            print(f"Establishment '{estname}' deleted successfully!")
        except mysql.connector.Error as err:
            print(f"Error deleting establishment: {err}")

    # Function to search for an establishment
    def search_establishment(self, search_term):
        try:
            # Search for establishments by name (case-insensitive)
            search_query = """SELECT * FROM establishment WHERE estname LIKE %s"""
            cursor = self.connection.cursor()
            cursor.execute(search_query, ("%" + search_term + "%",))
            results = cursor.fetchall()

            if not results:
                print(f"No establishments found matching '{search_term}'.")
            else:
                # Display search results in a formatted table
                print("{:<10} {:<50}".format("ID", "Name"))
                print("-" * 60)
                for row in results:
                    estno, estname, averating = row
                    print("{:<10} {:<50}".format(estno, estname))

        except mysql.connector.Error as err:
            print(f"Error searching establishments: {err}")

    # Function to update and establishment
    def update_establishment(self, new_estname, estname):
        try:
            sql = "UPDATE establishment SET estname = %s WHERE estname = %s"
            self.cursor.execute(sql, (new_estname, estname))
            self.connection.commit()
            if self.cursor.rowcount > 0:
                print(f"Establishment '{estname}' updated successfully!")
            else:
                print(f"Establishment '{estname}' not found.")
        except mysql.connector.Error as err:
            print(f"Error updating establishment: {err}")

    # Food Item Management Functions
    # Function to search for a food item
    def search_food_item(self, search_term):
        try:
            # Search for food items by name (case-insensitive)
            search_query = """SELECT food.foodno, food.foodname, est.estname
                            FROM food
                            INNER JOIN establishment est ON food.estno = est.estno
                            WHERE food.foodname LIKE %s"""
            cursor = self.connection.cursor()
            cursor.execute(search_query, ("%" + search_term + "%",))
            results = cursor.fetchall()


            if not results:
                print(f"No food items found matching '{search_term}'.")
            else:
                # Display search results in a table
                print("{:<10} {:<50} {:<20}".format("ID", "Name", "Establishment"))
                print("-" * 80)
                for row in results:
                    foodno, foodname, estname = row
                    print("{:<10} {:<50} {:<20}".format(foodno, foodname, estname))


        except mysql.connector.Error as err:
            print(f"Error searching food items: {err}")

    # Function to delete a food item
    def delete_food_item(self, foodname):
        try:
        # Confirmation prompt
            confirm = input(f"Are you sure you want to delete '{foodname}'? (y/n): ")
            if confirm.lower() != 'y':
                print("Deletion cancelled.")
                return


            # Delete the food item
            sql = "DELETE FROM food WHERE foodname = %s"
            self.cursor.execute(sql, (foodname,))
            self.connection.commit()
            print(f"Food item '{foodname}' deleted successfully!")
        except mysql.connector.Error as err:
            print(f"Error deleting food item: {err}")

    # Function to search for food item
    def search_food_item(self, foodname):
        try:
            sql = "SELECT * FROM food WHERE foodname = %s"
            self.cursor.execute(sql, (foodname,))
            result = self.cursor.fetchone()
            if result is None:
                print(f"Food item '{foodname}' not found.")
            else:
                print(f"Food item details:")
                print(result)
        except mysql.connector.Error as err:
            print(f"Error searching for food item: {err}")

    # Function to update food item
    def update_food_item(self, new_price, foodname):
        try:
        # Validate price is a number
            if not isinstance(new_price, (int, float)):
                raise ValueError("Price must be a number.")
            sql = "UPDATE food SET price = %s WHERE foodname = %s"
            self.cursor.execute(sql, (new_price, foodname))
            self.connection.commit()
            if self.cursor.rowcount > 0:
                print(f"Food item '{foodname}' price updated successfully!")
            else:
                print(f"Food item '{foodname}' not found.")
        except ValueError as e:
            print(f"Error: {e}")
        except mysql.connector.Error as err:
            print(f"Error updating food item price: {err}")
    
    def report_management_menu(self):
        clear()
        print("Report Generation Menu:")
        print("1. View all food establishments")
        print("2. View all food reviews")
        print("3. View all food items from an establishment")
        print("4. View all reviews made from an establishment that belong to a food type")
        print("5. View all review made within a specific month")
        print("6. view all establishments with a high average rating")
        print("7. view all food items from an  establishment based on price")
        print("8. Search for a food item")
        print("9. Exit")
        report_choice = int(input("Enter choice: "))
        if report_choice == 9:
            print("Going back to main menu")
            self.main_menu()
        elif report_choice == 1:
            self.show_food_establishments()
        elif report_choice == 2:
            self.show_reviews()
        else:
            print("Invalid choice. Please try again.")
            self.report_management_menu()

        if report_choice in [ 1, 2, 3, 4, 5, 6, 7, 8, 9]:
            input("Press Enter to proceed back to main menu")
            self.report_management_menu()

    def show_food_establishments(self):
        clear()
        cursor = self.connection.cursor()
        cursor.execute("SELECT estno, estname FROM establishment order by estno")
        food_establishments = cursor.fetchall()
        print("Establishments:")
        for unit in food_establishments:
            print(unit[0], " | ", unit[1])
        print("\n")

    def show_reviews(self):
        clear()
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM review order by reviewno")
        food_reviews = cursor.fetchall()
        print("Here are all the food review. \n \n")
        print(f"No  | Text Description     | Rating | Review Date | Food No | Est No | User No")
        for item in food_reviews:
            print(f"{item[0]:<3} | {item[1]:<20} | {item[2]:<6} | {item[3]}  | {item[4]:<7} | {item[5]:<6} | {item[6]:<3}")
        print("\n")



# Main Menu System
cli = FoodReviewCLI("localhost", "root", "killjoy", "foodproject")
cli.main_menu()
