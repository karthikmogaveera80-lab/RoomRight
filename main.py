
rooms = []
students = []
waiting_list = []

def add_room():
    room_no = input("Enter room number: ")
    room_type = input("Enter type (s for single /d for double /t for triple): ").lower()

    capacities = {"s": 1, "d": 2, "t": 3}

    if room_type not in capacities:
        print("Invalid room type!")
        return

    for room in rooms:
        if room["room_no"] == room_no:
            print("Room already exists!")
            return

    rooms.append({
        "room_no": room_no,
        "type": room_type,
        "capacity": capacities[room_type],
        "occupants": []
    })

    print("Room added successfully!")


def apply_hostel():
    name = input("Enter student name: ")

    if any(s["name"].lower() == name.lower() for s in students):
        print("Student already registered!")
        return

    try:
        year = int(input("Enter year of study (1-4): "))
        distance = float(input("Enter distance from home in km: "))
    except ValueError:
        print("Enter valid numeric values!")
        return

    if year not in range(1, 5) or distance < 0:
        print("Invalid year or distance!")
        return

    preference = input(
        "Preferred room (s for single/d for double/t for triple): "
    ).lower()

    if preference not in ["s", "d", "t"]:
        print("Invalid room preference!")
        return

    students.append({
        "name": name,
        "year": year,
        "distance": distance,
        "preference": preference,
        "room_no": None,
        "got_first_preference": False
    })

    print("Application submitted successfully!")


def allocate_rooms():
    global waiting_list

    waiting_list = []

    # Higher year first, then greater distance
    ordered_students = sorted(
        [s for s in students if s["room_no"] is None],
        key=lambda s: (-s["year"], -s["distance"], s["name"].lower())
    )

    for student in ordered_students:
        matching_rooms = [
            r for r in rooms
            if r["type"] == student["preference"]
            and len(r["occupants"]) < r["capacity"]
        ]

        if matching_rooms:
            room = matching_rooms[0]
            room["occupants"].append(student["name"])
            student["room_no"] = room["room_no"]
            student["got_first_preference"] = True
            print(student["name"], "allocated to room", room["room_no"])
        else:
            waiting_list.append(student["name"])
            print(student["name"], "added to waiting list.")

    print("Allocation process completed!")


def swap_rooms():
    name1 = input("Enter first student name: ")
    name2 = input("Enter second student name: ")

    s1 = next(
        (s for s in students if s["name"].lower() == name1.lower()),
        None
    )
    s2 = next(
        (s for s in students if s["name"].lower() == name2.lower()),
        None
    )

    if not s1 or not s2:
        print("Student not found!")
        return

    if s1["room_no"] is None or s2["room_no"] is None:
        print("Both students must have allocated rooms!")
        return

    if s1["name"] == s2["name"]:
        print("Choose two different students!")
        return

    room1 = next(r for r in rooms if r["room_no"] == s1["room_no"])
    room2 = next(r for r in rooms if r["room_no"] == s2["room_no"])

    # Check that each room can accommodate the other student
    if len(room1["occupants"]) > room1["capacity"] or \
       len(room2["occupants"]) > room2["capacity"]:
        print("Swap not possible!")
        return

    room1["occupants"].remove(s1["name"])
    room2["occupants"].remove(s2["name"])

    room1["occupants"].append(s2["name"])
    room2["occupants"].append(s1["name"])

    s1["room_no"], s2["room_no"] = s2["room_no"], s1["room_no"]

    print("Room swap completed successfully!")


def show_vacancies():
    print("\n--- ROOM VACANCIES ---")

    for room in rooms:
        vacancy = room["capacity"] - len(room["occupants"])
        print(
            "Room:", room["room_no"],
            "| Type:", room["type"],
            "| Capacity:", room["capacity"],
            "| Occupied:", len(room["occupants"]),
            "| Vacancies:", vacancy
        )

    # Automatically show all students who have not been allocated
    waiting_students = [
        student["name"]
        for student in students
        if student["room_no"] is None
    ]

    print("\n--- WAITING LIST ---")

    if waiting_students:
        for name in waiting_students:
            print(name, "- Waiting for Room")
    else:
        print("No students waiting.")



def fairness_report():
    allocated = [s for s in students if s["room_no"] is not None]
    first_preference = sum(
        1 for s in allocated if s["got_first_preference"]
    )

    print("\n--- FAIRNESS REPORT ---")
    print("Total applications:", len(students))
    print("Students allocated:", len(allocated))
    print("Students waiting:", len(waiting_list))
    print("First preferences received:", first_preference)

    if allocated:
        percentage = first_preference / len(allocated) * 100
        print("First preference percentage:", round(percentage, 2), "%")
    else:
        print("No students have been allocated yet.")

def check_student_status():
    name = input("Enter your student name: ")

    student = next(
        (s for s in students if s["name"].lower() == name.lower()),
        None
    )

    if student is None:
        print("Student application not found.")
    elif student["room_no"] is not None:
        print("Status: Room Allocated")
        print("Room Number:", student["room_no"])
    else:
        print("Status: Waiting for Room")
        print("Please wait for the next allocation.")

def main():
    while True:
        print("\n=======================================================================================================\n" 
        " ROOMRIGHT HOSTEL SYSTEM\n"
        "=======================================================================================================")
        print("1. Add Room")
        print("2. Apply for Hostel")
        print("3. Allocate Rooms")
        print("4. Swap Rooms")
        print("5. Show Vacancies and Waiting List")
        print("6. Fairness Report")
        print("7. Check Student Status")
        print("8. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_room()
        elif choice == "2":
            apply_hostel()
        elif choice == "3":
            allocate_rooms()
        elif choice == "4":
            swap_rooms()
        elif choice == "5":
            show_vacancies()
        elif choice == "6":
            fairness_report()
        elif choice == "7":
            check_student_status()
        elif choice == "8":
            print("Thank you for using RoomRight!")
            break
        else:
            print("Invalid choice! Try again.")


if __name__ == "__main__":
    main()
