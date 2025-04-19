from pos_system import POS, Item
import re

#main menu
def main():
    pos = POS()          #making an object of the pos system

    while True:
        print("\n============= POS System ===========")
        print("\n1. Add item to the basket")
        print("2. Delete item from the basket")
        print("3. Update item in basket")
        print("4. View basket")
        print("5. Generate bill")
        print("6. Search bill")
        print("7. Generate Tax file")
        print("8. Exit")
        print("========================================")


        choice = input("\nEnter your choice (1-8): ").strip()
        if not (choice.isdigit() and 1 <= int(choice) <= 8):
            print("Invalid choice. Please choose a number between 1 and 8.")
            continue



        if choice == "1":
            #validating item code
            while True:
                code = input("\nEnter item code: ").strip()
                if re.match(r'^[A-Za-z0-9_]+$', code):
                    break
                else:
                    print("Invalid input. Only letters, numbers and underscores are allowed for the item code.")

            #validating internal price
            while True:
                ip = input("\nEnter internal price Rs: ").strip()
                if ip.replace('.', '', 1).isdigit():
                    ip = float(ip)
                    if ip > 0:
                        break
                print("Invalid input. Enter a numeric value greater than to zero.")

            #validating discount
            while True:
                disc = input("\nEnter discount Rs: ").strip()
                if disc.replace('.', '', 1).isdigit():
                    disc = float(disc)
                    if disc >= 0:
                        break
                print("Invalid input. Enter a positive numeric value.")

            #validating sale price
            while True:
                sp = input("\nEnter sale price Rs: ").strip()
                if sp.replace('.', '', 1).isdigit():
                    sp = float(sp)
                    if sp >= 0:
                        break
                print("Invalid input. Enter a positive numeric value.")

            #validating Quantity
            while True:
                qty = input("\nEnter quantity: ").strip()
                if qty.isdigit():
                    qty = int(qty)
                    if qty > 0:
                        break
                print("Quantity must be a positive whole number.\n")

            item = Item(code, ip, disc, sp, qty)
            pos.add_item(item)


        elif choice == "2":
            while True:
                try:
                    line_no = int(input("\nEnter line number to delete: "))
                    if line_no <= 0:
                        print("Invalid input. Please enter a positive line number greater than zero.")
                        continue         # Ask the user to input again
                    pos.delete_item(line_no)
                    break
                except ValueError:
                    print("Invalid input. Please enter a numeric value.")
                    continue

        elif choice == "3":
            while True:
                try:
                    line_no = int(input("\nEnter line number to update: "))
                    if line_no <= 0:
                        print("Invalid input. Please enter a positive line number greater than zero.")
                        continue

                     # Validate Sale Price
                    while True:
                        sp = input("Enter new Sale Price (leave blank to keep current): ").strip()
                        if sp == "":
                            new_sp = None
                            break
                        elif sp.replace('.', '', 1).isdigit():
                            sp = float(sp)
                            if sp >= 0:
                                new_sp = sp
                                break
                        print("Invalid input. Enter a positive numeric value or leave blank.")

                    # Validate Discount
                    while True:
                        disc = input("Enter new Discount (leave blank to keep current): ").strip()
                        if disc == "":
                            new_disc = None
                            break
                        elif disc.replace('.', '', 1).isdigit():
                            disc = float(disc)
                            if disc >= 0:
                                new_disc = disc
                                break
                        print("Invalid input. Enter a positive numeric value or leave blank.")

                    # Validate Quantity
                    while True:
                        qty = input("Enter new Quantity (leave blank to keep current): ").strip()
                        if qty == "":
                            new_qty = None
                            break
                        elif qty.isdigit():
                            qty = int(qty)
                            if qty > 0:
                                new_qty = qty
                                break
                        print("Quantity must be a positive whole number or leave blank.")

                    pos.update_item(line_no, new_sp, new_disc, new_qty)
                    break                                # Exit loop after successful update

                except ValueError:
                    print("Invalid input. Please enter a numeric value.")
                    continue

        elif choice == "4":
            pos.show_basket()

        elif choice == "5":
            pos.generate_bill()

        elif choice == "6":
            while True:
                bill_no = input("\nEnter Bill Number (e.g. BILL001): ").strip()
                if re.match(r'BILL\d+', bill_no):            # checking if bills are in format "BILL001"
                    pos.search_bill(bill_no)
                    break
                print("Invalid Bill number. Please enter a valid Bill number (e.g., BILL001).")

        elif choice == "7":
            pos.generate_final_tax_file()


        elif choice == "8":
            print("Exiting POS system. Goodbye!")
            break



if __name__ == "__main__":
    main()




