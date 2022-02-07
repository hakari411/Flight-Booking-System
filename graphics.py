# imports required
from tkinter import *
from PIL import ImageTk, Image
import mysql.connector

# setting up connection
mydb = mysql.connector.connect(host="localhost", user="root", passwd="root", database="fbs")
mycursor = mydb.cursor()

# starting tkinter window
root = Tk()
root.title("Flyter - 12th Board Project")

# defining the needed globals
menu_listbox = Listbox(root, width=155, height=15)
button_list = {}
booked_seats = {}
active_buttons = 0


# defining functions
def select_seat(seat_number):
    global active_buttons
    if button_list[seat_number].cget("bg") == "#f2efe6":
        button_list[seat_number].config(bg="green", fg="green")
        active_buttons += 1
        booked_seats[seat_number] = seat_number
        # print(booked_seats)
        return 1
    else:
        return 0


def unselect_seat(seat_number):
    global active_buttons
    if button_list[seat_number].cget("bg") == "green":
        button_list[seat_number].config(bg="#f2efe6", fg="#f2efe6")
        active_buttons -= 1
        booked_seats.pop(seat_number)
        # print(booked_seats)


def book_seats(seat_number):
    c = int(size_box.get("1.0", "end"))
    if select_seat(seat_number) != 1:
        unselect_seat(seat_number)
    if active_buttons > c:
        unselect_seat(seat_number)


def confirm_booking(passenger_array, trip_id):
    i = 0
    for key in booked_seats:
        print(i)
        print(passenger_array[i])
        mycursor.execute('''UPDATE seats
                            SET status = {},passenger_id = "{}"
                            WHERE seat_number = {}'''
                         .format(2, passenger_array[i], key))
        mydb.commit()
        i += 1

    mycursor.execute('''UPDATE trip
                        SET seats_left = seats_left - {}
                        where trip_id = {}'''
                     .format(active_buttons, trip_id))
    mydb.commit()


def confirm_travellers(passenger_box_array, passenger_array):
    for i in range(0, len(passenger_box_array)):
        passenger_name = passenger_box_array[i].get("1.0", "end").strip()
        passenger_array.append(passenger_name)


def place_labels(seats_window):
    Label(seats_window, text="A", bg="#dfe8e9", font=("Times New Roman", 13)).place(x=65, y=5)
    Label(seats_window, text="B", bg="#dfe8e9", font=("Times New Roman", 13)).place(x=115, y=5)
    Label(seats_window, text="C", bg="#dfe8e9", font=("Times New Roman", 13)).place(x=165, y=5)

    Label(seats_window, text="D", bg="#dfe8e9", font=("Times New Roman", 13)).place(x=320, y=5)
    Label(seats_window, text="E", bg="#dfe8e9", font=("Times New Roman", 13)).place(x=370, y=5)
    Label(seats_window, text="F", bg="#dfe8e9", font=("Times New Roman", 13)).place(x=420, y=5)

    for i in range(0, 30):
        row_number = i + 1
        y_coord = row_number * 30
        Label(seats_window, text="{}".format(row_number), bg="#dfe8e9", font=("Times New Roman", 13)).place(x=10,
                                                                                                            y="{}".format(
                                                                                                                y_coord))


def pull_seats(seats_window, trip_det):
    route_id = get_route_id(trip_det[1], trip_det[2])
    # print(route_id)
    trip_id = get_trip_id(trip_det[0], route_id, trip_det[3])
    # print(trip_id)

    seat_number = 1
    for i in range(0, 30):
        for j in range(0, 6):
            mycursor.execute('''SELECT status
                                FROM seats
                                WHERE trip_id = {}
                                and seat_number = {}'''
                             .format(trip_id, seat_number))

            status = mycursor.fetchall()[0][0]
            seat_number += 1

            if j <= 2:
                a = 58 + (j * 50)
                b = ((i + 1) * 30)
                if status == 0:
                    x = i * 6 + j + 1
                    button = Button(seats_window, text=x, activebackground="black",
                                    activeforeground="#c7ffd8",
                                    bd=2, bg="#f2efe6", fg="#f2efe6", relief=RIDGE,
                                    height=1, width=3, command=lambda bound_x=x: book_seats(bound_x))
                    button.place(x="{}".format(a), y="{}".format(b))
                    button_list[x] = button

                elif status == 1:
                    button = Button(seats_window,
                                    bd=2, bg="red", fg="red", relief=RIDGE,
                                    height=1, width=3, state=DISABLED, command="")
                    button.place(x="{}".format(a), y="{}".format(b))

                elif status == 2:
                    button = Button(seats_window,
                                    bd=2, bg="blue", fg="blue", relief=RIDGE,
                                    height=1, width=3, state=DISABLED, command="")
                    button.place(x="{}".format(a), y="{}".format(b))

            else:
                a = 163 + (j * 50)
                b = ((i + 1) * 30)
                if status == 0:
                    x = i * 6 + j + 1
                    button = Button(seats_window, text=x, activebackground="black",
                                    activeforeground="#c7ffd8",
                                    bd=2, bg="#f2efe6", fg="#f2efe6", relief=RIDGE,
                                    height=1, width=3, command=lambda bound_x=x: book_seats(bound_x))
                    button.place(x="{}".format(a), y="{}".format(b))
                    button_list[x] = button
                elif status == 1:
                    button = Button(seats_window,
                                    bd=2, bg="red", fg="red", relief=RIDGE,
                                    height=1, width=3, state=DISABLED, command="")
                    button.place(x="{}".format(a), y="{}".format(b))

                elif status == 2:
                    button = Button(seats_window,
                                    bd=2, bg="blue", fg="blue", relief=RIDGE,
                                    height=1, width=3, state=DISABLED, command="")
                    button.place(x="{}".format(a), y="{}".format(b))
    # print(available_buttons)


def page2(trip_det):
    seats_window = Toplevel(root)
    seats_window.geometry("940x940")
    seats_window.title("Seat Selection Window")
    seats_window.configure(bg="#dfe8e9")
    seats_window.resizable(width=False, height=False)

    place_labels(seats_window)
    pull_seats(seats_window, trip_det)

    route_id = get_route_id(trip_det[1], trip_det[2])
    trip_id = get_trip_id(trip_det[0], route_id, trip_det[3])

    passenger_array = []
    passenger_box_array = []
    c = int(size_box.get("1.0").strip())
    temp = ""
    for i in range(0, c):
        Label(seats_window, text="Passenger {}'s Full Name:".format(i + 1), bg="#dfe8e9",
              font=("Times New Roman", 13)).place(x=730, y=10 + i * 90)
        name = Text(seats_window, height=2, width=23)
        passenger_box_array.append(name)
        name.place(x=730, y=40 + i * 90)
        temp = 120 + i * 90

    Button(seats_window, text="Confirm Travellers", bg="#545454", fg="#f6f6ef", pady="3", padx="4",
           font=("Times New Roman", 13),
           command=lambda: confirm_travellers(passenger_box_array, passenger_array)).place(x=750, y=temp)

    Button(seats_window, text="Confirm Booking", bg="#545454", fg="#f6f6ef", pady="3", padx="9",
           font=("Times New Roman", 13),
           command=lambda: confirm_booking(passenger_array, trip_id)).place(x=750, y=890)


def call_trip(trip_det):
    page2(trip_det)


def get_route_id(dpt_city, arr_city):
    mycursor.execute('''SELECT route_id
                        FROM route
                        WHERE dpt_city = '{}' 
                        AND arr_city = '{}' '''
                     .format(dpt_city, arr_city))

    """because it will return a list fo tuples so double index"""
    return mycursor.fetchall()[0][0]


def get_trip_id(p_id, r_id, date):
    # print(">{}<".format(p_id))
    # print(">{}<".format(r_id))
    # print(">{}<".format(date))

    mycursor.execute('''SELECT trip_id
                        FROM trip
                        WHERE plane_id = {} 
                        AND route_id = {}
                        AND DATE(trip_date) = '{}'
                        '''
                     .format(p_id, r_id, date))

    return mycursor.fetchall()[0][0]


def check_trip(trip_details):
    trip_det = trip_details
    a = trip_details[0]
    b = get_route_id(trip_details[1], trip_details[2])
    c = dpt_date_box.get("1.0", "end").strip()
    if len(c) == 0:
        c = ""
    else:
        c = dpt_date_box.get("1.0", "end")

    # print(">{}<".format(c))

    query1 = '''SELECT *
                FROM trip
                where (plane_id IS NOT NULL AND plane_id = {})
                AND (route_id IS NOT NULL AND route_id = {})
                AND (trip_date IS NOT NULL AND trip_date = "{}" ) '''.format(a, b, c.strip())

    # print(query1)

    mycursor.execute(query1)
    if len(mycursor.fetchall()) > 0:
        call_trip(trip_det)
    else:
        pass
        # need to add a or some way to get back to main screen and inform user
        # that this trip does not exist


def proceed():
    selected = menu_listbox.curselection()
    selected_trip = ""
    if selected:
        selected_trip = menu_listbox.get(selected)
        check_trip(selected_trip)
    # add an else clause to put up error boxes for multiple selections


def swap(l, dst):
    a = l.get("1.0", "end").lower().strip()
    b = dst.get("1.0", "end").lower().strip()

    lvng_from_box.delete('1.0', "end")
    lvng_from_box.insert("1.0", b)

    dst_box.delete('1.0', "end")
    dst_box.insert("1.0", a)

    menu_listbox.delete(0, "end")


def establish(arr, c):
    # need to use c in the thing displayed in listbox
    flight_info_header = Label(
        text="Flight ID\t\t Departure City\t\t Arrival City\t Departure Date\t Departure Time\t Arrival Time",
        bg="#dfe8e9", font=("Times New Roman", 13))

    flight_info_header.place(x=47, y=540)
    menu_listbox.place(x=47, y=580)

    defaultText = '''No flights are available that match your parameters.
                     The most common errors include spelling mistakes, not enough seats and no flights on that route.
                     Please try changing your input parameters.'''
    count = 0
    for val in arr:
        menu_listbox.insert(END, val)
        count += 1

    if count == 0:
        menu_listbox.insert(END, defaultText)


def search(lvng, dst, dpt_date, size):
    possible_flights = []
    a = lvng.get("1.0", "end").lower()
    b = dst.get("1.0", "end").lower()
    c = dpt_date.get("1.0", "end").lower()
    d = int(size_box.get("1.0").strip())
    route_id = 0

    mycursor.execute(''' SELECT route_id 
                         FROM route 
                         WHERE dpt_city = '{}' 
                         AND arr_city = '{}' 
                         '''.format(a.strip(), b.strip()))
    for x in mycursor.fetchone():
        route_id = x

    mycursor.execute('''SELECT trip.plane_id, route.dpt_city, route.arr_city,
                        DATE(trip.trip_date), route.dpt_time, route.arr_time
                        FROM route
                        JOIN trip ON trip.route_id = route.route_id
                        WHERE trip.seats_left > {}
                        AND trip.route_id = {}
                '''.format(d, route_id))

    for x in mycursor.fetchall():
        x = list(x)
        possible_flights.append(x)

    menu_listbox.delete(0, "end")

    establish(possible_flights, c)


def page1():
    global swap_photo
    global banner

    """standard global requirement for the next 4"""

    global lvng_from_box
    global dst_box
    global dpt_date_box
    global size_box

    root.geometry("1200x900")
    root.resizable(width=False, height=False)
    root.configure(bg="#dfe8e9")

    banner = ImageTk.PhotoImage(Image.open(r"C:\Users\Dell\PythonProj\FlightSystem\images\Flyter_Banner.png"))
    Label(image=banner).place(x=0, y=0)

    Label(text="Leaving From", bg="#dfe8e9", font=("Times New Roman", 13)).place(x=47, y=422)
    lvng_from_box = Text(root, height=2, width=23)
    lvng_from_box.place(x=47, y=452)

    swap_photo = PhotoImage(file=r"C:\Users\Dell\PythonProj\FlightSystem\images\finalSwap.png")
    swap_button = Button(root, bg="white", image=swap_photo, height=25, width=30,
                         command=lambda: swap(lvng_from_box, dst_box))
    swap_button.place(x=260, y=456)

    Label(text="Destination", bg="#dfe8e9", font=("Times New Roman", 13)).place(x=327, y=422)
    dst_box = Text(root, height=2, width=23)
    dst_box.place(x=327, y=452)

    Label(text="Departure Date", bg="#dfe8e9", font=("Times New Roman", 13)).place(x=560, y=422)
    dpt_date_box = Text(root, height=2, width=23)
    dpt_date_box.place(x=560, y=452)

    Label(text="No. Of Tickets", bg="#dfe8e9", font=("Times New Roman", 13)).place(x=793, y=422)
    size_box = Text(root, height=2, width=23)
    size_box.place(x=793, y=452)

    Button(text="Search", bg="#545454", fg="#f6f6ef", pady="3", padx="4", font=("Times New Roman", 13),
           command=lambda: search(lvng_from_box, dst_box, dpt_date_box, size_box)).place(x=1050, y=452)

    # clicked = StringVar()
    # sort_menu = OptionMenu(root, clicked, "Earliest", "Cheapest", "Quickest", "Most Seats Left")
    # sort_menu.config(bg="#545454", fg="#f6f6ef", pady="3", padx="4", font=("Times New Roman", 13))
    # sort_menu["menu"].config(bg="#545454", fg="#f6f6ef", font=("Times New Roman", 12))
    # clicked.set("Sort By")
    # sort_menu.place(x=1040, y=540)

    Button(text="Exit", bg="#545454", fg="#f6f6ef", pady="3", padx="4", font=("Times New Roman", 13),
           command=quit).place(x=47, y=850)

    Button(text="Proceed", bg="#545454", fg="#f6f6ef", pady="3", padx="4", font=("Times New Roman", 13),
           command=lambda: proceed()).place(x=1050, y=850)


page1()
root.mainloop()
