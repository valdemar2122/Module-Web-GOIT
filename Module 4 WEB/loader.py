from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader("."))

template = env.get_template("users.html")

users = {
    0: {"nickname": "Jack", "age": 23, "sex": "m"},
    1: {"nickname": "Jhon", "age": 21, "sex": "m"},
    2: {"nickname": "MARY", "age": 44, "sex": "f"},
    3: {"nickname": "readmond", "age": 11, "sex": "m"},
}

output = template.render(users=users)


with open("output_users.html", "w") as fh:
    fh.write(output)
