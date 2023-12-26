from flask import Flask, request, Response, render_template

app = Flask(__name__)

# user_id, nickname, age, sex
user_fields = ("nickname", "age", "sex")
users = {}
users_count = 0


def validate_user(user):
    for user_field in user_fields:
        if user_field not in user:
            return False
    return True


@app.route("/users", methods=["POST"])
def create_user():
    global users_count
    user = request.json
    if not validate_user(user):
        return Response("Invalid user data", status=400)
    user["user_id"] = users_count
    users[users_count] = user
    users_count += 1

    return f" user has been created with data {user}"


@app.route("/users", methods=["GET"])
def get_users():
    nickname = request.args.get("nickname")

    if nickname:
        for user in users.values():
            if nickname == user["nickname"]:
                return user
        return f"User with {nickname} does not exist"

    return render_template("users.html", users=users)


@app.route("/users/<int:user_id>", methods=["GET", "PUT", "DELETE"])
def handle_user(user_id):
    if user_id not in users:
        return Response(f"User with id {user_id} does not exist", status=404)

    if request.method == "GET":
        return users[user_id]

    if request.method == "PUT":
        user = request.json

        if not validate_user(user):
            return Response("Invalid user data", 400)

        user["user_id"] = user_id
        users[user_id] = user

        return f"User {user_id} has been updated with data {user}"

    if request.method == "DELETE":
        del users[user_id]
        return f"User {user_id} has been deleted"


if __name__ == "__main__":
    app.run(debug=True)
