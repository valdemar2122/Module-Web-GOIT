import requests

user_1 = {"nickname": "Jack", "age": 23, "sex": "m"}
user_2 = {"nickname": "Jhon", "age": 21, "sex": "m"}
user_3 = {"nickname": "MARY", "age": 44, "sex": "f"}
user_4 = {"nickname": "readmond", "age": 11, "sex": "m"}

action = input("CRUD: ")

if action == "C":
    response = requests.post(
        "http://127.0.0.1:5000/users",
        json=user_1,
    )

    print(response.status_code)
    print(response.text)

    response = requests.post(
        "http://127.0.0.1:5000/users",
        json=user_2,
    )

    print(response.status_code)
    print(response.text)

    response = requests.post(
        "http://127.0.0.1:5000/users",
        json=user_3,
    )

    print(response.status_code)
    print(response.text)
elif action == "U":
    response = requests.put("http://127.0.0.1:5000/users/2", json=user_4)
    print(response.status_code)
    print(response.text)
elif action == "D":
    response = requests.delete("http://127.0.0.1:5000/users/0")
    print(response.status_code)
    print(response.text)
