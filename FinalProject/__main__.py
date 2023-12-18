from Bot import Bot, ConsoleInteraction

if __name__ == "__main__":
    console_interaction = ConsoleInteraction()
    bot = Bot(console_interaction)
    bot.book.load("auto_save")

    commands = [
        "Add",
        "Search",
        "Edit",
        "Load",
        "Remove",
        "Save",
        "Congratulate",
        "View",
        "Exit",
    ]

    console_interaction.display_output(
        "Hello. I am your contact-assistant. What should I do with your contacts?"
    )

    while True:
        action = (
            console_interaction.get_input(
                "Type 'help' for a list of commands or enter your command: "
            )
            .strip()
            .lower()
        )

        if action == "help":
            format_str = str("{:%s%d}" % ("^", 20))
            for command in commands:
                console_interaction.display_output(format_str.format(command))
            action = (
                console_interaction.get_input("Enter your command: ").strip().lower()
            )

        bot.handle(action)

        if action in ["add", "remove", "edit"]:
            bot.book.save("auto_save")

        if action == "exit":
            break
