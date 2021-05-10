# Discord emoji stealer

StealEmoji.py has a command `stealemoji` that takes a message id as an argument, then finds an emoji and its id in the message with regex, makes an https request to get the emoji file and create a custom server emoji.

There is also a command `makeemoji` in Makeemoji.py which takes the message attachment url, make an https request and use its content to create an emoji.
