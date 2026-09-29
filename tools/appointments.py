# Mock slots data
appointments = {
        "09/11/2026": ["10:00am","12:00pm","01:00pm"],
        "09/12/2026": ["10:00am","12:00pm","01:00pm"],
        "09/13/2026": ["10:00am","12:00pm","01:00pm"],
    }

# tools
## get availability
def get_available_appointments(date):
    return {
        "date": date,
        "available_appointments": appointments.get(date, [])
    }


## Creating bookings and manage booking list
bookings = []

def book_appointment(customer_id, date, time):
    

    available_times = appointments.get(date, [])

    if time in available_times:
        booking = {
            "customer_id": customer_id,
            "date": date,
            "time": time
        }

        bookings.append(booking)

        return booking

    else:
        return { "error": "Requested appointment time is not available." }
