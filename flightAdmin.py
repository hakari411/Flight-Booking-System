import mysql.connector

mydb = mysql.connector.connect(host="localhost", user="root", passwd="root", database="fbs")
mycursor = mydb.cursor()


# DO NOT CHANGE PLANE SIZE THE WHOLE CODE WILL BREAK
# pre_book_percent = 32

plane_size = 180
covid_blocked_percentage = 45
# works best for 45% + blocked


def get_col_counts():
    return 6
    # can be changed for variable plane size


def get_row_counts():
    c = get_col_counts()
    r = int(plane_size / c)
    if (r * c) < plane_size:
        r = r + 1
    return r


rows = get_row_counts()
cols = get_col_counts()


def populate_seats(trip_id, covid_blocked_percentage):
    mycursor.execute('''SELECT * 
                        FROM seats 
                        WHERE trip_id IS NOT NULL 
                        AND trip_id={}'''.format(trip_id))

    if len(mycursor.fetchall()) > 0:
        for i in range(0, 180):
            mycursor.execute('''UPDATE seats 
                                SET status = {}, passenger_name = ''
                                WHERE seat_number = '{}'
                                AND trip_id = {}
                                '''.format(0, i + 1, trip_id))
            mydb.commit()
    else:
        for i in range(0, 180):
            mycursor.execute('''INSERT INTO seats
                                (seat_number, status, trip_id, passenger_name)
                                VALUES 
                                ({}, {}, {}, '')'''.format(i + 1, 0, trip_id))
            mydb.commit()

    global total_blocked_seats
    # global total_pre_booked_seats
    # can replace plane_size with 180
    seats_to_block = int((1.0 * plane_size * covid_blocked_percentage) / 100)
    # seats_to_pre_book = int(((plane_size - seats_to_block) * pre_book_percent * 1.0) / 100)
    if seats_to_block >= 1:
        block_every_nth = plane_size / seats_to_block
    else:
        block_every_nth = 0
    # if seats_to_pre_book >= 1:
    # pre_book_every_nth = plane_size / seats_to_pre_book
    # else:
    # pre_book_every_nth = 0
    n = 1.0
    # k = 1.0
    total_blocked_seats = 0
    # total_pre_booked_seats = 0
    seat_count = 0
    seat_number = -1
    for i in range(rows):
        for j in range(cols):
            seat_number += 1
            if seat_count < plane_size:
                seat_count = seat_count + 1
                if total_blocked_seats == 0 and seats_to_block > 0:
                    n = block_every_nth
                if n >= block_every_nth and total_blocked_seats <= seats_to_block:
                    mycursor.execute('''UPDATE seats 
                                           SET status = 1
                                           WHERE seat_number = {}
                                           AND trip_id = {}'''.format(seat_number, trip_id))
                    mydb.commit()
                    n = n - block_every_nth
                    total_blocked_seats = total_blocked_seats + 1
                # else:
                # if total_pre_booked_seats == 0 and seats_to_pre_book > 0:
                # k = pre_book_every_nth
                # if k >= pre_book_every_nth and total_pre_booked_seats <= seats_to_pre_book:
                #   plane_seat_details[seat_name] = "B"
                #  k = k - pre_book_every_nth
                # total_pre_booked_seats = total_pre_booked_seats + 1
                else:
                    pass
                n = n + 1
                # k = k + 1
            else:
                break

    mycursor.execute('''UPDATE trip
                        SET seats_left = seats_left - {}
                        where trip_id = {}'''
                     .format(total_blocked_seats, trip_id))
    mydb.commit()


def reset_bookings(trip_id):
    mycursor.execute('''UPDATE seats
                        SET status = 0, passenger_name="", passenger_id = 0
                        where trip_id = {}'''.format(trip_id))
    mydb.commit()
    mycursor.execute('''UPDATE trip
                        SET seats_left = 180
                        Where trip_id = {}'''.format(trip_id))
    mydb.commit()


# for i in range(0,12):
#    reset_bookings(i+1)
#    populate_seats(i+1, covid_blocked_percentage)

def delete_trips():
    # can be an admin level function that deletes all trips for current date
    pass
