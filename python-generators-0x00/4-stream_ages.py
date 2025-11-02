# Simulated users database (you can imagine these are fetched from a real DB)
users = [
    {"name": "Alice", "age": 22},
    {"name": "Bob", "age": 30},
    {"name": "Charlie", "age": 27},
    {"name": "Diana", "age": 25},
    {"name": "Eve", "age": 29},
    {"name": "Frank", "age": 33}
]

# Generator to yield user ages one by one
def stream_user_ages():
    for user in users:       # Loop 1
        yield user["age"]

# Function to calculate average age using the generator
def calculate_average_age():
    total_age = 0
    count = 0
    for age in stream_user_ages():   # Loop 2
        total_age += age
        count += 1
    
    average_age = total_age / count if count > 0 else 0
    print(f"Average age of users: {average_age:.2f}")

# Run the script
calculate_average_age()
