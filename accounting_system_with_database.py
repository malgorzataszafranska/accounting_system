import os
from ast import literal_eval

def display_commands():
    print("You can find here available Commands:")
    print("introduction")
    print("balance")
    print("sale")
    print("purchase")
    print("account")
    print("list")
    print("warehouse")
    print("review")
    print("end")

def validate_files():
    """Check if existing files are in the correct format."""
    issues_found = False
    
    # Check account_balance.txt
    if os.path.exists('account_balance.txt'):
        try:
            with open('account_balance.txt', 'r') as f:
                content = f.read().strip()
                float(content)  # Try to convert to float
            print("✓ account_balance.txt format is valid")
        except ValueError:
            print("✕ account_balance.txt format is invalid. Should contain only a number.")
            print(f"Current content: {content}")
            issues_found = True

    # Check warehouse.txt
    if os.path.exists('warehouse.txt'):
        try:
            with open('warehouse.txt', 'r') as f:
                content = f.read().strip()
                warehouse_dict = literal_eval(content)
                # Verify structure
                for product, details in warehouse_dict.items():
                    if not isinstance(details, dict):
                        raise ValueError("Product details must be a dictionary")
                    if 'price' not in details or 'quantity' not in details:
                        raise ValueError("Product details must contain 'price' and 'quantity'")
            print("✓ warehouse.txt format is valid")
        except Exception as e:
            print("✕ warehouse.txt format is invalid.")
            print(f"Error: {str(e)}")
            print(f"Current content: {content}")
            issues_found = True

    # Check operations.txt
    if os.path.exists('operations.txt'):
        try:
            with open('operations.txt', 'r') as f:
                lines = f.readlines()
                for i, line in enumerate(lines, 1):
                    if not (line.startswith('Balance update:') or 
                           line.startswith('Purchase:') or 
                           line.startswith('Sale:')):
                        raise ValueError(f"Invalid operation format at line {i}")
            print("✓ operations.txt format is valid")
        except Exception as e:
            print("✕ operations.txt format is invalid.")
            print(f"Error: {str(e)}")
            issues_found = True

    return not issues_found  # Return True if all files are valid

def balance(account_balance, operations):
    try:
        amount = float(input("Enter the amount to add or subtract: EUR "))
        account_balance += amount
        operations.append(f"Balance update: {amount} EUR")
        print(f"New account balance: {account_balance:.2f} EUR\n")
    except ValueError:
        print("Invalid input. Please enter a correct value.\n")
    return account_balance

def sale(account_balance, warehouse, operations):
    try:
        product = input("Enter the product name: ")
        price = float(input("Enter the product price: EUR "))
        quantity = int(input("Enter the quantity sold: "))
        if product in warehouse and warehouse[product]['quantity'] >= quantity:
            total_sale = price * quantity
            account_balance += total_sale
            warehouse[product]['quantity'] -= quantity
            operations.append(f"Sale is: {quantity}x {product} at {price:.2f} EUR each, total EUR{total_sale:.2f}")
            print(f"Sale successful. {total_sale:.2f} EUR added to account. New balance: {account_balance:.2f} EUR\n")
        else:
            print("Insufficient stock or product not found.\n")
    except ValueError:
        print("Invalid input. Please enter numeric values for price and quantity.\n")
    return account_balance

def purchase(account_balance, warehouse, operations):
    try:
        product = input("Enter the product name: ")
        price = float(input("Enter the product price: EUR "))
        quantity = int(input("Enter the quantity purchased: "))
        total_cost = price * quantity
        if total_cost <= account_balance:
            account_balance -= total_cost
            if product in warehouse:
                warehouse[product]['quantity'] += quantity
                warehouse[product]['price'] = price
            else:
                warehouse[product] = {'price': price, 'quantity': quantity}
            operations.append(f"Purchase: {quantity}x {product} at {price:.2f} EUR each, total: {total_cost:.2f} EUR")
            print(f"Purchase is successful. {total_cost:.2f} EUR deducted from account. New balance: {account_balance:.2f} EUR\n")
        else:
            print("Insufficient funds for this purchase.\n")
    except ValueError:
        print("Invalid input. Please enter numeric values for price and quantity.\n")
    return account_balance

def check_account_balance(account_balance):
    print(f"Current account balance: {account_balance:.2f} EUR")

def list_inventory(warehouse):
    if warehouse:
        print("Current inventory:")
        for product, details in warehouse.items():
            print(f"- {product}: {details['price']:.2f} EUR, Quantity: {details['quantity']}\n")
    else:
        print("The warehouse is empty.\n")

def warehouse_status(warehouse):
    product = input("Enter the product name to check: ")
    if product in warehouse:
        print(f"{product}: {warehouse[product]['price']:.2f} EUR, Quantity: {warehouse[product]['quantity']}\n")
    else:
        print(f"{product} not found in the warehouse.\n")

def review_operations(operations):
    try:
        if operations:
            from_index = input("Enter the starting index (leave empty to show from the beginning): ")
            to_index = input("Enter the ending index (leave empty to show up to the last one): ")
            if not from_index:
                from_index = 0
            else:
                from_index = int(from_index)
            if not to_index:
                to_index = len(operations)
            else:
                to_index = int(to_index)

            if 0 <= from_index < to_index <= len(operations):
                print("Recorded operations:")
                for i, operation in enumerate(operations[from_index:to_index], start=from_index):
                    print(f"{i}: {operation}")
            else:
                print("Invalid range. Please try again.\n")
        else:
            print("No operations recorded.\n")
    except ValueError:
        print("Invalid input. Please enter valid indices.\n")

def save_state(account_balance, warehouse, operations):
    """Save program state to files."""
    try:
        # Save account balance
        with open('account_balance.txt', 'w') as f:
            f.write(str(account_balance))
        
        # Save warehouse inventory
        with open('warehouse.txt', 'w') as f:
            f.write(str(warehouse))
        
        # Save operations history
        with open('operations.txt', 'w') as f:
            for operation in operations:
                f.write(operation + '\n')
                
        print("Program state saved successfully.")
    except Exception as e:
        print(f"Error saving program state: {e}")

def load_state():
    """Load program state from files."""
    account_balance = 0.0
    warehouse = {}
    operations = []
    
    try:
        # Load account balance
        if os.path.exists('account_balance.txt'):
            with open('account_balance.txt', 'r') as f:
                account_balance = float(f.read().strip())
        
        # Load warehouse inventory
        if os.path.exists('warehouse.txt'):
            with open('warehouse.txt', 'r') as f:
                warehouse = literal_eval(f.read().strip())
        
        # Load operations history
        if os.path.exists('operations.txt'):
            with open('operations.txt', 'r') as f:
                operations = [line.strip() for line in f.readlines()]
        
        print("Program state loaded successfully.")
    except Exception as e:
        print(f"Error loading program state: {e}")
        print("Starting with default empty state.")
    
    return account_balance, warehouse, operations

def main():
    # Check existing files first
    if os.path.exists('account_balance.txt') or os.path.exists('warehouse.txt') or os.path.exists('operations.txt'):
        print("\nChecking existing data files...")
        if not validate_files():
            response = input("Issues found with data files. Do you want to start with empty state? (yes/no): ")
            if response.lower() != 'yes':
                print("Please fix the data files and restart the program.")
                return

    # Load saved state at startup
    account_balance, warehouse, operations = load_state()
    
    print("\nHello! This program will simulate operations on a company's account and a warehouse. ")
    display_commands()

    while True:
        command = input("\nPlease enter a command: ").lower()

        if command == "balance":
            account_balance = balance(account_balance, operations)
        elif command == "sale":
            account_balance = sale(account_balance, warehouse, operations)
        elif command == "purchase":
            account_balance = purchase(account_balance, warehouse, operations)
        elif command == "account":
            check_account_balance(account_balance)
        elif command == "list":
            list_inventory(warehouse)
        elif command == "warehouse":
            warehouse_status(warehouse)
        elif command == "review":
            review_operations(operations)
        elif command == "introduction":
            print("This is a short intro how to navigate and simulate a typical product cycle. \n"
                  "First of all, you have to have money booked on an account. \n"
                  "It will be shown in a balance. Later you can purchase or sale something. \n"
                  "Everytime you purchase/sale something, you can check its status in the warehouse.\n")
        elif command == "end":
            # Save state before exiting
            save_state(account_balance, warehouse, operations)
            print("Program state saved. Terminating the program.")
            break
        else:
            print("This command is invalid. Please try again.")

        display_commands()

if __name__ == "__main__":
    main()