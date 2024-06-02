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

    # Function to update the average rating for establishment and food item
    def averating(self):
        self.cursor.execute("UPDATE establishment SET averating = COALESCE((SELECT averating FROM (SELECT estno, AVG(rating) AS averating FROM review GROUP BY estno) sq WHERE establishment.estno = sq.estno), 0)")
        self.cursor.execute("UPDATE food SET averating = COALESCE((SELECT averating FROM (SELECT foodno, AVG(rating) AS averating FROM review GROUP BY foodno) sq WHERE food.foodno = sq.foodno), 0)")

    # Function for the main menu
    def main_menu(self):
        while True:
            clear()
            print("\n" + "="*40)
            print("          Main Menu - Food Review          ")
            print("="*40)
            print("[1] Review Management")
            print("[2] Establishment Management")
            print("[3] Food Item Management")
            print("[4] Report Generation")
            print("[5] User Management")
            print("[0] Exit")
            print("="*40)
            choice = input(">> Enter your choice: ")
            print("="*40)

            if choice == '1':
                self.review_management_menu()
            elif choice == '2':
                self.establishment_management_menu()
            elif choice == '3':
                self.food_item_management_menu()
            elif choice == '4':
                self.report_management_menu()
            elif choice == '5':
                self.user_management_menu()
            elif choice == '0':
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
        print("4. Back to Main Menu")
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
            self.averating()
            input("Press Enter to proceed back to main menu")
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
                            self.averating()
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
            self.averating()
        elif choice == '4':
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
            self.averating()
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
            self.averating()
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

    # Function to update an establishment
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
        print("2. View all food reviews for an establishment or a food item")
        print("3. View all food items from an establishment")
        print("4. View all food items from an establishment that belong to a food type {meat | veg | etc.}")
        print("5. View all reviews made within a month for an establishment or a food item")
        print("6. View all establishments with a high average rating (rating >= 4). (ratings from 1-5; highest is 5)")
        print("7. View all food items from an establishment arranged according to price")
        print("8. Search food items from any establishment based on a given price range and/or food type")
        print("9. Exit")
        report_choice = (input("Enter choice: "))
        if report_choice == '9':
            print("Going back to main menu")
            self.main_menu()
        elif report_choice == '1':
            clear()
            self.show_food_establishments()
        elif report_choice == '2':
            clear()
            self.show_reviews()
        elif report_choice == '3':
            self.show_food_items_from_establishment()
        elif report_choice == '4':
            self.show_food_items_from_establishment_and_food_type()
        elif report_choice == '5':
            self.show_reviews_within_month()
        elif report_choice == '6':
            self.show_establishments_with_high_average_rating()
        elif report_choice == '7':
            clear()
            self.view_food_from_est_by_price()
        elif report_choice == '8':
            clear()
            self.view_food_based_on_criteria()
        else:
            input("Invalid choice. Press Enter to proceed")
            self.report_management_menu()

        if int(report_choice) in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
            input("Press Enter to proceed back to main menu")
            self.main_menu()

    # 1. View all food establishments
    def show_food_establishments(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT estno, estname FROM establishment order by estno")
        food_establishments = cursor.fetchall()
        print("Establishments:")
        for unit in food_establishments:
            print(unit[0], " | ", unit[1])
        print("\n")

    # 2. View all food reviews for an establishment or a food item
    def show_reviews(self):
        clear()
        print("Would you like to view the reviews of  ")
        print ("[1] Food establishment")
        print ("[2] Food item")
        choice = (input("Enter index of choice: "))
        
        # Validate choice
        if not choice.isdigit():
            input("Invalid choice. Press enter to return.")
            self.report_management_menu()
        else:
            choice = int(choice)

        if choice == 1:
            self.show_food_establishments()
            est_choice = (input("Enter the index of the establishment that you want to see reviews of: "))

            # Validate choice
            if not est_choice.isdigit():
                input("Invalid choice. Press enter to return.")
                self.report_management_menu()
            else:
                est_choice = int(est_choice)

            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM review where estno = %s order by reviewno", (est_choice,))
            food_reviews = cursor.fetchall()
        elif choice == 2:
            self.show_food_items_from_establishment()
            food_choice = (input("Enter the index of the food item that that you want to see reviews of : "))

            # Validate choice
            if not food_choice.isdigit():
                input("Invalid choice. Press enter to return.")
                self.report_management_menu()
            else:
                food_choice = int(food_choice)

            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM review where foodno = %s order by reviewno", (food_choice,))
            food_reviews = cursor.fetchall()
        else:
            input("Invalid choice. Press enter to return.")
            self.report_management_menu()

        if food_reviews != []:
            print("Here are all the food review. \n \n")
            print(f"No  | Text Description     | Rating | Review Date | Food No | Est No | User No")
            for item in food_reviews:
                if item[4] != None:
                    print(f"{item[0]:<3} | {item[1]:<20} | {item[2]:<6} | {item[3]}  | {item[4]:<7} | {item[5]:<6} | {item[6]:<3}")
                else:
                    print(f"{item[0]:<3} | {item[1]:<20} | {item[2]:<6} | {item[3]}  | None    | {item[5]:<6} | {item[6]:<3}")
            print("\n")
        else:
            print("There are food reviews that match your criteria \n")

    # 3. View all food items from an establishment
    def show_food_items_from_establishment(self):
        while True:
            try:
                estno = int(input("Enter establishment number: "))

                self.cursor.execute("SELECT estno FROM establishment WHERE estno = %s", (estno,))
                if not self.cursor.fetchone():
                    print("Establishment number does not exist. Please enter a valid establishment number.")
                    continue

                sql = """SELECT food.foodno, food.foodname, food.price, food.foodtype
                        FROM food
                        WHERE food.estno = %s"""
                self.cursor.execute(sql, (estno,))
                food_items = self.cursor.fetchall()
                if not food_items:
                    print("No food items found for this establishment.")
                else:
                    print("| {:<10} | {:<30} | {:<10} | {:<15} |".format("Food No", "Food Name", "Price", "Type"))
                    print("|" + "-"*12 + "|" + "-"*32 + "|" + "-"*12 + "|" + "-"*17 + "|")
                    for item in food_items:
                        print("| {:<10} | {:<30} | {:<10} | {:<15} |".format(item[0], item[1], item[2], item[3]))
                break
            except ValueError:
                print("Invalid input. Please enter a valid number.")
            except mysql.connector.Error as err:
                print(f"Database error: {err}")
                break
    
    # 4. View all food items from an establishment that belong to a food type {meat | veg | etc.}.
    def show_food_items_from_establishment_and_food_type(self):
        try:
            while True:
                estno = input("Enter establishment number: ")
                if not estno.isdigit():
                    print("Invalid input. Please enter a valid number.")
                    continue
                estno = int(estno)
                
                self.cursor.execute("SELECT estno FROM establishment WHERE estno = %s", (estno,))
                if not self.cursor.fetchone():
                    print("Establishment number does not exist. Please enter a valid establishment number.")
                    continue
                break

            self.cursor.execute("SELECT DISTINCT foodtype FROM food")
            food_types = self.cursor.fetchall()
            
            if not food_types:
                print("No food types found.")
                return
            
            print("Food types:")
            valid_food_types = [food_type[0] for food_type in food_types]
            for food_type in valid_food_types:
                print(food_type)
            
            while True:
                foodtype = input("Enter food type: ")
                if foodtype not in valid_food_types:
                    print("Invalid food type. Please enter a valid food type.")
                    continue

                sql = """SELECT * FROM food WHERE estno = %s AND foodtype = %s"""
                self.cursor.execute(sql, (estno, foodtype))
                food_items = self.cursor.fetchall()

                if not food_items:
                    print("No food items found for this establishment and food type.")
                    retry = input("Would you like to enter another food type? (y/n): ")
                    if retry.lower() != 'y':
                        break
                else:
                    max_price_length = max(len(f"{item[3]:.2f}") for item in food_items)
                    price_header = "Price".ljust(max_price_length)

                    print(f"| Food No | Food Name          | Rating | {price_header} | Food Type       | Est No |")
                    print(f"|---------|--------------------|--------|{'-' * (max_price_length + 2)}|-----------------|--------|")
                    for item in food_items:
                        price = f"{item[3]:.2f}".ljust(max_price_length)
                        print(f"| {item[0]:<7} | {item[1]:<18} | {item[2]:<6} | {price} | {item[4]:<15} | {item[5]:<6} |")
                    break
        except ValueError:
            print("Invalid input. Please enter valid numbers.")
        except mysql.connector.Error as err:
            print(f"Database error: {err}")

    # 5. View all reviews made within a month for an establishment or a food item;
    def show_reviews_within_month(self):
        try:
            while True:
                estno = input("Enter establishment number (or 0 to skip): ")
                if not estno.isdigit():
                    print("Invalid input. Please enter a valid number.")
                    continue
                estno = int(estno)
                if estno != 0:
                    self.cursor.execute("SELECT estno FROM establishment WHERE estno = %s", (estno,))
                    if not self.cursor.fetchone():
                        print("Establishment number does not exist. Please enter a valid establishment number.")
                        continue
                break

            foodno = 0
            if estno == 0:
                while True:
                    foodno = input("Enter food item number: ")
                    if not foodno.isdigit():
                        print("Invalid input. Please enter a valid number.")
                        continue
                    foodno = int(foodno)
                    self.cursor.execute("SELECT foodno FROM food WHERE foodno = %s", (foodno,))
                    if not self.cursor.fetchone():
                        print("Food item number does not exist. Please enter a valid food item number.")
                        continue
                    break

            while True:
                month = input("Enter month (1-12): ")
                if not month.isdigit() or not (1 <= int(month) <= 12):
                    print("Invalid input. Please enter a valid month between 1 and 12.")
                    continue
                month = int(month)
                break

            if estno == 0 and foodno == 0:
                print("You must enter either an establishment number or a food item number.")
                return

            sql = "SELECT * FROM review WHERE (estno = %s OR foodno = %s) AND MONTH(date) = %s"
            self.cursor.execute(sql, (estno, foodno, month))
            reviews = self.cursor.fetchall()

            if not reviews:
                print("No reviews found for the given criteria.")
            else:
                max_text_length = max(len(review[1]) for review in reviews)
                header_length = len("Text Description")
                max_length = max(max_text_length, header_length)
                text_header = "Text Description".ljust(max_length)
                print(f"| Review No | {text_header} | Rating | Date       | Food No | Est No | User No |")
                print(f"|-----------|{'-' * (max_length + 2)}|--------|------------|---------|--------|---------|")
                for review in reviews:
                    review_date = review[3].strftime('%Y-%m-%d')
                    text = review[1].ljust(max_length)
                    print(f"| {review[0]:<9} | {text} | {review[2]:<6} | {review_date:<10} | {review[4] or 'None':<7} | {review[5]:<6} | {review[6]:<7} |")
        except ValueError:
            print("Invalid input. Please enter valid numbers.")
        except mysql.connector.Error as err:
            print(f"Database error: {err}")

    # 6. View all establishments with a high average rating (rating >= 4). (ratings from 1-5; highest is 5);
    def show_establishments_with_high_average_rating(self):
        try:
            sql = "SELECT * FROM establishment WHERE averating >= 4"
            self.cursor.execute(sql)
            establishments = self.cursor.fetchall()

            if not establishments:
                print("No establishments found with an average rating of 4 or higher.")
            else:
                print("{:<10} {:<50} {:<10}".format("Est No", "Est Name", "Avg Rating"))
                print("-" * 70)
                for est in establishments:
                    print("{:<10} {:<50} {:<10}".format(est[0], est[1], est[2]))
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
    
    # 7. View all food items from an establishment arranged according to price;
    def view_food_from_est_by_price(self):
        self.show_food_establishments()
        est_number = (input("From what establishment would you like to browse by price: "))

        if not est_number.isdigit():
            input("Invalid choice. Press enter to return.")
            self.report_management_menu()
        else:
            est_number = int(est_number)

        cursor = self.connection.cursor()
        cursor.execute("SELECT count(estno) FROM establishment")
        est_count = cursor.fetchone()
        if est_number < 0 or est_number > est_count[0]:
            input("Invalid establishment number. Press enter to return.")
            self.report_management_menu()        

        cursor.execute("SELECT * FROM food WHERE estno = %s ORDER BY price", (est_number,))
        food_items = cursor.fetchall()
        if food_items != []:
            max_food_name_length = max(len(item[1]) for item in food_items)
            max_food_type_length = max(len(item[4]) for item in food_items)
            
            max_food_name_length = max(max_food_name_length, len("Food Name"))
            max_food_type_length = max(max_food_type_length, len("Food Type"))
            
            food_name_header = "Food Name".ljust(max_food_name_length)
            food_type_header = "Food Type".ljust(max_food_type_length)
            
            print(f"Here are all the food items from establishment #{est_number}.\n")
            print(f"| No  | {food_name_header} | Rating | Price  | {food_type_header} | Est No |")
            print(f"|-----|{'-' * (max_food_name_length + 2)}|--------|--------|{'-' * (max_food_type_length + 2)}|--------|")

            for item in food_items:
                food_name = item[1].ljust(max_food_name_length)
                food_type = item[4].ljust(max_food_type_length)
                print(f"| {item[0]:<3} | {food_name} | {item[2]:<6} | {item[3]:<6} | {food_type} | {item[5]:<6} |")
            print("\n")
        else:
            input("There are no food items in this establishment..")
            self.report_management_menu()

    # Function to search for food based on criteria
    def view_food_based_on_criteria(self):
        self.show_food_establishments()
        est_number = (input("From what establishment would you like to browse by price: "))

        # Validate establishment number
        if not est_number.isdigit():
            input("Invalid choice. Press enter to return.")
            self.report_management_menu()
        else:
            est_number = int(est_number)
        cursor = self.connection.cursor()
        cursor.execute("SELECT count(estno) FROM establishment")
        count_est = cursor.fetchone()
        if 0 > est_number or est_number > count_est[0]:
            input("Invalid choice. Press enter to return.")
            self.report_management_menu()
        
        print("Would you like to browse by ")
        print ("[1] Price range")
        print ("[2] Food Type")
        print ("[3] Price range and food type")
        sort_choice = (input("Enter index of choice: "))
        
        # Validate sort choice
        if not sort_choice.isdigit():
            input("Invalid choice. Press enter to return.")
            self.report_management_menu()
        else:
            sort_choice = int(sort_choice)

        # Search for food items based on criteria
        if sort_choice not in [1, 2, 3]:
            input("Invalid choice. Press enter to return.")
            self.report_management_menu()
        else:
            if sort_choice == 1:
                min_range = (input("What is the lower limit of the price range: "))
                max_range = (input("What is the upper limit of the price range: "))
                if not min_range.isdigit() or not max_range.isdigit():
                    input("Invalid choice. Press enter to return.")
                    self.report_management_menu()
                else:
                    min_range = int(min_range)
                    max_range = int(max_range)
                    cursor.execute("SELECT * FROM food WHERE price BETWEEN %s AND %s and estno = %s", (min_range, max_range, est_number))
                    food_items = cursor.fetchall()
            elif sort_choice == 2:
                print("Here are the different food types:")
                cursor.execute("SELECT distinct foodtype FROM food")
                food_types = cursor.fetchall()
                index = 1
                for item in food_types:
                    print(f"[{index:<2}] | {item[0]:<10}")
                    index += 1
                type_choice = (input("Enter index of choice: "))

                # Validate food type choice
                if not type_choice.isdigit():
                    input("Invalid choice. Press enter to return.")
                    self.report_management_menu()
                else:
                    type_choice = int(type_choice)-1
                    if type_choice > len(food_types)-1 or type_choice < 0:
                        input("Invalid choice. Press enter to return.")
                        self.report_management_menu()
                    else:
                        cursor.execute("SELECT * FROM food WHERE foodtype = %s and estno = %s;", (food_types[type_choice][0], est_number))
                        food_items = cursor.fetchall()
            elif sort_choice == 3:
                min_range = (input("What is the lower limit of the price range: "))
                max_range = (input("What is the upper limit of the price range: "))
            
                # Validate price range
                if not min_range.isdigit() or not max_range.isdigit():
                    input("Invalid choice. Press enter to return.")
                    self.report_management_menu()
                else:
                    min_range = int(min_range)
                    max_range = int(max_range)
                print("Here are the different food types:")
                cursor.execute("SELECT distinct foodtype FROM food")
                food_types = cursor.fetchall()
                index = 1
                for item in food_types:
                    print(f"[{index:<3}] | {item[0]:<10}")
                    index += 1
                type_choice = (input("Enter index of choice: "))

                if not type_choice.isdigit():
                    input("Invalid choice. Press enter to return.")
                    self.report_management_menu()
                else:
                    type_choice = int(type_choice)-1
                    if type_choice > len(food_types)-1 or type_choice < 0:
                        input("Invalid choice. Press enter to return.")
                        self.report_management_menu()
                    else:
                        cursor.execute("SELECT * FROM food WHERE price BETWEEN %s AND %s AND foodtype = %s and estno = %s;", (min_range, max_range, food_types[type_choice][0], est_number))
                        food_items = cursor.fetchall()

        if food_items:
            print("Here are the food item/s that match your criteria.")
            
            max_food_name_length = max(len(item[1]) for item in food_items)
            max_food_type_length = max(len(item[4]) for item in food_items)
            
            max_food_name_length = max(max_food_name_length, len("Food Name"))
            max_food_type_length = max(max_food_type_length, len("Food Type"))
            
            food_name_header = "Food Name".ljust(max_food_name_length)
            food_type_header = "Food Type".ljust(max_food_type_length)
            
            print(f"| No  | {food_name_header} | Rating | Price  | {food_type_header} | Est No |")
            print(f"|-----|{'-' * (max_food_name_length + 2)}|--------|--------|{'-' * (max_food_type_length + 2)}|--------|")
            
            for item in food_items:
                food_name = item[1].ljust(max_food_name_length)
                food_type = item[4].ljust(max_food_type_length)
                print(f"| {item[0]:<3} | {food_name} | {item[2]:<6} | {item[3]:<6} | {food_type} | {item[5]:<6} |")
            print("\n")
        else:
            print("There is no food item that matches your criteria.")

    def user_management_menu(self):
        clear()
        print("User Generation Menu:")
        print("0. Return to main menu")
        print("1. View all Users")
        print("2. Create a new user")
        print("3. Update password")
        print("4. Delete user")
        report_choice = (input("Enter choice: "))
        if report_choice == '0':
            print("Returning to main menu")
            self.main_menu()
        elif report_choice == '1':
            clear()
            self.show_users()
        elif report_choice == '2':
            clear()
            self.add_user()
        elif report_choice == '3':
            self.update_password()
        elif report_choice == '4':
            self.delete_user()
        else:
            input("Invalid choice. Press Enter to proceed")
            self.report_management_menu()

        if int(report_choice) in [1, 2, 3, 4]:
            input("Press Enter to proceed back to main menu")
            self.main_menu()

    # Function to show all users
    def show_users(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT userno, username FROM user")
        users = cursor.fetchall()
        print("Users:")

        max_username_length = max(len(unit[1]) for unit in users)
        max_username_length = max(max_username_length, len("Food Name"))
        username_header = "Food Name".ljust(max_username_length)

        print(f"| No  | {username_header} |")
        print(f"|-----|{'-' * (max_username_length + 2)}|")
        for unit in users:
            print(f"| {unit[0]:<3} | {unit[1]:<{max_username_length}} |")
        print("\n")

    # Function to show all users
    def add_user(self):
        print('You are going to create a new user.')
        username = input("Enter username: ")
        password = input("Enter password: ")
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO `user` (`username`, `password`) VALUES (%s, %s)", (username, password))
        print("User successfully created.")

    # User validation
    def validate_user(self, username, password):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM user")
        users = cursor.fetchall()

        validated = False
        for unit in users:
            if username == unit[1]:
                if password == unit[2]:
                    validated = True

        return validated

    # Function to update a password of an existing user
    def update_password(self):
        print('You are going to update the password of a user.')
        username = input("Enter username: ")
        password = input("Enter current password: ")

        validated = self.validate_user(username, password)

        if validated == False:
            input("Invalid username or password. Press Enter to return.")
            self.user_management_menu()
        else:
            new_password = input("Enter new password: ")
            cursor = self.connection.cursor()
            cursor.execute("UPDATE user SET password = %s WHERE username = %s", (new_password, username))
            print("User password successfully changed.")

    def delete_user(self):
        print('You are going to delete a user. Enter the proper credentials to delete your account.')
        username = input("Enter username: ")
        password = input("Enter current password: ")

        validated = self.validate_user(username, password)

        if validated == False:
            input("Invalid username or password. Press Enter to return.")
            self.user_management_menu()
        else:
            cursor = self.connection.cursor()
            cursor.execute("DELETE from user WHERE username = %s", (username,))
            print("User successfully Deleted.")

################################

# Main Menu System
cli = FoodReviewCLI("localhost", "foodproject", "cmsc127", "foodproject")
cli.averating()
cli.main_menu()
