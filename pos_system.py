import json
import os

class Item:
    #constructor for each item
    def __init__(self,item_code, internal_price,discount,sale_price,quantity):
        self.item_code = item_code
        self.internal_price = float(internal_price)
        self.discount = float(discount)
        self.sale_price = float(sale_price)
        self.quantity = int(quantity)

    # to get the total in a line
    def line_total(self):
        return round(self.sale_price * self.quantity,2)

    #to make each product into a dictionary , key value format
    def to_dict(self):
        return {
            "item_code" : self.item_code,
            "internal_price" : self.internal_price,
            "discount" : self.discount,
            "sale_price" : self.sale_price,
            "quantity" : self.quantity,
            "checksum" : self.calculate_checksum()
        }
    #calculate checksum
    def calculate_checksum(self):
        cap, low, num = 0, 0, 0
        for c in self.item_code:
            if c.isupper():
                cap += 1
            if c.islower():
                low += 1
            if c.isdigit() or c == '.':
                num += 1
        return cap + low + num


class POS:
    #constructor for POS System
    def __init__(self):
        self.basket = []
        self.bills = {}
        self.bill_count = 1

    #adding items to basket
    def add_item(self,item):
        self.basket.append(item)
        print("Item added to basket successfully!")

    #deleting items from the basket
    def delete_item(self,line_no):
        if not self.basket:       # Check if the basket is empty
            print("Your basket is empty. No items to delete")
            return
        index = line_no - 1
        if 0 <= index < len(self.basket):
            self.basket.pop(index)
            print("Item removed from basket successfully!")
        else:
            print(f"Line {line_no} doesn't exist. Please view the basket and try again")

    #updating item details from the basket
    def update_item(self, line_no, sale_price = None, discount = None, quantity = None):
        if not self.basket:       # Check if the basket is empty
            print("Your basket is empty. No items to update.")
            return
        index = line_no - 1
        if 0 <= index < len(self.basket):
            item = self.basket[index]
            if sale_price is not None:
                item.sale_price = float(sale_price)
            if discount is not None:
                item.discount = float(discount)
            if quantity is not None:
                item.quantity = int(quantity)
            print("Item updated successfully!")
        else:
            print(f"Line {line_no} doesn't exist.  Please view the basket and try again")


    #show the items in the basket
    def show_basket(self):
        if not self.basket:
            print("The basket is empty!")
            return

        print ("\n====== Current Basket =====")
        for i in range(len(self.basket)):
            item = self.basket[i]
            print(
                f"\nLine {i+1}: \n"
                f"   •  Item Code: {item.item_code}\n"
                f"   •  Internal Price: Rs.{item.internal_price}\n"
                f"   •  Sale Price: Rs.{item.sale_price}\n"
                f"   •  Discount: Rs.{item.discount}\n"
                f"   •  Quantity: {item.quantity}\n"
                f"   •  Line Total: Rs.{item.line_total()}\n"
                f"   •  Checksum: {item.calculate_checksum()}\n"
            )
        print("\n================================")

    #generating the bill
    def generate_bill(self):
        if not self.basket:
            print("Cannot generate bill. Basket is empty.")
            return

        #bill preview
        print("\n" + "=" * 40)
        print("BILL PREVIEW".center(40))
        print("=" * 40)

        for i in range(len(self.basket)):
            item = self.basket[i]
            print(
                f"{i+1}. {item.item_code}\t\t"
                f"Qty: {item.quantity}\t\t"
                f"Total: Rs.{item.line_total()}\t"
            )
        #grand total
        grand_total = round(sum(item.line_total() for item in self.basket),2)
        print("\n" + "-" * 50)
        print(f"GRAND TOTAL: Rs.{grand_total}".center(50))
        print("=" * 50)

        #user confirmation
        confirm = input("\nGenerate Bill? (y/n): ").strip().lower()
        if confirm != "y":
            print("Bill Generation Cancelled")
            return

        #save the bill
        bill_number = f"BILL{self.bill_count:03}"
        self.bills[bill_number] = {"items": self.basket[ : ], "grand_total": grand_total}   #getting a shallow copy of the basket
        print(f"\nBill {bill_number} generated successfully!")

        self.save_bill(bill_number)
        self.basket.clear()
        self.bill_count += 1


    def save_bill(self, bill_number):
        #point to the tax text file
        tax_file_path = "tax_transactions_test.json"

        new_tax_entries = [item.to_dict() for item in self.bills[bill_number]["items"]]

        #if tax file already exists, load it
        if os.path.exists(tax_file_path):
            try:
                with open(tax_file_path,"r") as f:
                    existing_data = json.load(f)
            except json.JSONDecodeError:
                print("Warning: Existing tax file was corrupted, starting fresh!")
                existing_data = []
        else:
            existing_data = []

        #combining old and new data
        updated_data = existing_data + new_tax_entries

        #saving the updated tax file
        with open(tax_file_path,"w") as f:
            json.dump(updated_data, f,indent = 4 )  #indent = 4 to increase human readability

        print(f"Tax data for this bill has been saved to {tax_file_path}")


    def search_bill(self,bill_number):
        if not self.bills:                    # Checks if the dictionary is empty
            print("Cannot Find bill. The bill dictionary is empty.")
            return
        if bill_number in self.bills:
            bill = self.bills[bill_number]
            print("\n" + "=" * 50)
            print(f"Bill number: {bill_number}".center(50))
            print("=" * 50)

            #printing the line items and their details
            line_number = 1
            for item in self.bills[bill_number]["items"]:
                print(f"\nLine {line_number}:")
                print(f"   Item code: {item.item_code}")
                print(f"   Internal price: Rs.{item.internal_price}")
                print(f"   Discount: {item.discount}")
                print(f"   Sale price: {item.sale_price}")
                print(f"   Quantity: {item.quantity}")
                print(f"   Checksum: {item.calculate_checksum()}")

                print(f"   Line total: {item.line_total()}")
                line_number += 1

            print("\n" + "-" * 50)
            print(f"Grand Total: Rs.{bill['grand_total']}".center(50))
            print("=" * 50 + "\n")

        else:
            print(f"Bill number: '{bill_number}' not found.\n")

    def show_tax_file_info(self):
        tax_file_path = "tax_transactions_test.json"

        print("\nTax File Information")
        print("-"*40)

        if os.path.exists(tax_file_path):
            print("Tax file is available.")
            print(f"File name: {tax_file_path}")
        else:
            print("Tax file not found.")
            print("Please generate at least one bill to create the tax file.")



























