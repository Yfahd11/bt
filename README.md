# StudyLink – Peer Study Matchmaker

StudyLink is a small Python project that helps students find good
study partners based on the subjects they are strong in and the
topics where they want extra help.

The project is written using basic object‑oriented ideas:
* encapsulation (private attributes and helper methods)
* inheritance and polymorphism (Profile → Student)
* a simple Strategy pattern for the matching logic

The program is intentionally simple and runs in a terminal, but the
classes are separated so they could be reused in a GUI or web app
later on.

## How to run it

1. Open a terminal in the project folder (the one that has `main.py`).
2. Make sure you are using Python 3.10 or newer.
3. Run:

   ```bash
   python main.py
   ```

You should see a text menu with options to create a profile, find
matches, log sessions, and so on.

## Running the tests

From the same folder you can run the tests with:

```bash
python -m unittest discover
```

The tests live in the `tests/` directory and cover the small pieces
of logic in the model and matching modules.
