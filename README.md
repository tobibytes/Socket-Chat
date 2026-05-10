# Socket-Chat

A bare-metal chat server in Python — TCP sockets, one thread per connection, and a JSON-on-disk "database" for users and chat history.

## What it does

- `main.py` starts a TCP server on `0.0.0.0:5001` and spawns a thread per accepted client.
- `client.py` is a tiny prompt-and-respond client that connects, reads server prompts, and forwards user input back.
- `db.py` is a hand-rolled persistence layer:
  - `Database` — in-memory `users` + `chats`, serialized to `user_db.json` / `chat_db.json`.
  - `User`, `Chat`, `Message` — small dataclasses with `to_dict` / `load` round-tripping.
- The server walks the user through signup or login, then lets them open a chat with another user.

## Run it

```sh
# Server
python main.py

# Client (in another terminal)
python client.py
```

Then follow the prompts: username → name → which user to chat with → messages.

## Why

A hands-on exercise in:

- TCP socket programming with `socket` + `threading`
- Per-connection request/response loops
- Manual JSON serialization without an ORM
- Splitting wire concerns from domain models

No external dependencies — everything is `std`.

## Stack

Python 3 · `socket` · `threading` · `json`
