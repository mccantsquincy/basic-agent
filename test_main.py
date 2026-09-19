from main import book_appointment, bookings

def test_unavailable_appointment():
    result = book_appointment(
        customer_id="cust_001",
        date="09/12/2026",
        time="3:00pm"
    )

    assert result["error"] =="Requested appointment time is not available."

    assert bookings == []

def test_available_appointment():
    result = book_appointment(
        customer_id="cust_001",
        date="09/12/2026",
        time="12:00pm"
    )

    assert result["customer_id"] == "cust_001"
    assert result["date"] == "09/12/2026"
    assert result["time"] == "12:00pm"

    assert result in bookings