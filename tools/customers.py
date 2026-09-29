# customer data
customers = {
    "555-123-4567": {
        "customer_id": "cust_001",
        "name": "John Doe"
    },
    "555-987-6543": {
        "customer_id": "cust_002",
        "name": "Jane Smith"
    }
}

# tools
## search customer
def customer_lookup(phone):
    return customers.get(phone, [])

