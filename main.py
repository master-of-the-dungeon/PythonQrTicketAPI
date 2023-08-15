from tickets_management import *


def main():
    """The main function of the application."""
    create_table()

    while True:
        print("Select an option:")
        print("1. Add new ticket")
        print("2. View all tickets")
        print("3. Check QR code")
        print("4. Create blank white image with QR code")
        print("5. Exit")
        print("6. Insert test data")

        option = input("Enter option: ")

        if option == "1":
            name = input("Enter name: ")
            ticket_number = input("Enter ticket number: ")
            price = int(input("Enter price: "))
            ticket_type = input("Enter type: ")
            date = input("Enter date: ")
            address = input("Enter address: ")
            qr_code = generate_qr_code(name, ticket_number, price, ticket_type)
            attendance = 0
            add_ticket(name, ticket_number, price, ticket_type, date, address, qr_code, attendance)
            print("Ticket added successfully!")

        elif option == "2":
            tickets = get_all_tickets()
            print('\n')
            for ticket in tickets:
                print("Name:", ticket['name'])
                print("Ticket Number:", ticket['ticket_number'])
                print("Price:", ticket['price'])
                print("Type:", ticket['type'])
                print("Date:", ticket['date'])
                print("Address:", ticket['address'])
                print("Attendance:", "Present" if ticket['attendance'] else "Absent")
                print("-----")
                print('\n')

        elif option == "3":
            qr_code = input("Enter QR code: ")
            name = check_qr_code(qr_code)
            if name is not None:
                print("The name of the ticket holder is:", name)
            else:
                print("The QR code is invalid.")

        elif option == "4":
            ticket_number = input("Enter ticket number: ")
            ticket = get_ticket_by_number(ticket_number)
            if ticket is not None:
                qr_image = create_qr_image(ticket)
                image_filename = f"{ticket['name']}.png"
                qr_image.save(image_filename)
                print(f"Image with QR code and name saved as '{image_filename}'")
            else:
                print(f"Ticket with number '{ticket_number}' not found.")

        elif option == "5":
            break
        elif option == "6":
            insert_test_data()

if __name__ == "__main__":
    main()
