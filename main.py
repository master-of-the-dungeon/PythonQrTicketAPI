import qrcode
import sqlite3
from PIL import Image, ImageDraw, ImageFont

def create_blank_image(width, height, color=(255, 255, 255)):
    image = Image.new("RGB", (width, height), color)
    return image

def connect_to_database():
    """Connects to the SQLite3 database."""
    return sqlite3.connect("tickets.db")

def create_table():
    """Creates the table in the SQLite3 database."""
    connection = connect_to_database()
    cursor = connection.cursor()

    try:
        cursor.execute("""CREATE TABLE tickets (
            name VARCHAR(255),
            ticket_number INT,
            price INT,
            type TEXT,
            date TEXT,
            address TEXT,
            attendance INT,
            qr_code BLOB
        )""")
    except sqlite3.OperationalError:
        pass

    connection.commit()




def add_ticket(name, ticket_number, price, ticket_type, date, address, qr_code, attendance):
    """Adds a ticket to the SQLite3 database."""
    connection = connect_to_database()
    cursor = connection.cursor()

    cursor.execute("INSERT INTO tickets (name, ticket_number, price, type, date, address, attendance, qr_code) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                   (name, ticket_number, price, ticket_type, date, address, attendance, qr_code))

    connection.commit()

def generate_qr_code(name, ticket_number, price, ticket_type):
    """Generates a QR code for a ticket."""

    qr_code_data = f"{name}:{ticket_number}:{price}:{ticket_type}"

    qr_code_image = qrcode.make(qr_code_data)
    qr_code = qr_code_image.tobytes()

    return qr_code


def get_all_tickets():
    """Gets all tickets from the SQLite3 database."""
    connection = connect_to_database()
    cursor = connection.cursor()

    cursor.execute("SELECT name, ticket_number, price, type, date, address, attendance, qr_code FROM tickets")

    tickets = []

    for row in cursor:
        ticket = {
            "name": row[0],
            "ticket_number": row[1],
            "price": row[2],
            "type": row[3],
            "date": row[4],
            "address": row[5],
            "attendance": row[6],
            "qr_code": row[7]
        }
        tickets.append(ticket)

    return tickets



def check_qr_code(qr_code):
    """Checks a QR code against the SQLite3 database."""

    connection = connect_to_database()
    cursor = connection.cursor()

    cursor.execute("SELECT name FROM tickets WHERE qr_code = ?", (qr_code,))

    row = cursor.fetchone()

    if row is not None:
        return row[0]
    else:
        return None

def get_ticket_by_number(ticket_number):
    """Get a ticket by its ticket number from the SQLite3 database."""
    connection = connect_to_database()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM tickets WHERE ticket_number = ?", (ticket_number,))

    row = cursor.fetchone()

    if row is not None:
        ticket = {
            "name": row[0],
            "ticket_number": row[1],
            "price": row[2],
            "type": row[3],
            "date": row[4],
            "address": row[5],
            "qr_code": row[6]
        }
        return ticket
    else:
        return None

def create_qr_image(ticket):
    """Create an image with QR code and ticket information."""
    width = 1080
    height = 1920

    blank_image = create_blank_image(width, height)
    qr_code_data = f"Name: {ticket['name']}  \nTicket Number: {ticket['ticket_number']}  \nType: {ticket['type']}  \nDate: {ticket['date']}  \nAddress: {ticket['address']}"
    qr_code_image = qrcode.make(qr_code_data)
    qr_code_image = qr_code_image.resize((width * 2 // 3, width * 2 // 3))

    qr_position = ((width - qr_code_image.width) // 2, (height - qr_code_image.height) // 3)
    blank_image.paste(qr_code_image, qr_position)

    draw = ImageDraw.Draw(blank_image)
    font = ImageFont.truetype("arial.ttf", 50)

    name_text = f"Ticket Holder: {ticket['name']}"
    draw.text((qr_position[0], qr_position[1] + qr_code_image.height + 20), name_text, font=font, fill=(0, 0, 0))

    date_text = f"Date: {ticket['date']}"
    draw.text((qr_position[0], qr_position[1] + qr_code_image.height + 20 + 60), date_text, font=font, fill=(0, 0, 0))

    address_text = f"Address: {ticket['address']}"
    draw.text((qr_position[0], qr_position[1] + qr_code_image.height + 20 + 120), address_text, font=font,
              fill=(0, 0, 0))

    return blank_image

def insert_test_data():
    connection = connect_to_database()
    cursor = connection.cursor()

    test_data = [
        ('John Doe', 1, 50, 'Regular', '2023-08-15', '123 Main St', 0, 'sample_qr_code_data_1'),
        ('Jane Smith', 2, 60, 'VIP', '2023-08-16', '456 Elm St', 0, 'sample_qr_code_data_2'),
        ('Michael Johnson', 3, 75, 'Regular', '2023-08-17', '789 Oak St', 0, 'sample_qr_code_data_3'),
        ('Emily Davis', 4, 80, 'VIP', '2023-08-18', '101 Maple St', 0, 'sample_qr_code_data_4'),
        ('William Brown', 5, 55, 'Regular', '2023-08-19', '111 Pine St', 0, 'sample_qr_code_data_5'),
    ]

    cursor.executemany("INSERT INTO tickets (name, ticket_number, price, type, date, address, attendance, qr_code) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", test_data)

    connection.commit()
    connection.close()



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
        print("7. Insert test data")

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
        elif option == "7":
            insert_test_data()

if __name__ == "__main__":
    main()
