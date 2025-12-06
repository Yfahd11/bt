# StudyLink – Design Notes

## Big picture

StudyLink is a toy project meant to show a simple matching idea:
students write down what they can help with and what they want help
with, and the program suggests partners whose strengths line up with
those needs.

Most of the interesting work happens in the `src/` package. The
`main.py` file is just a small text‑based user interface that calls
into those classes.

## Modules and classes

### `src.models`

* `Profile` – base class with an id and a name. It exists mainly so
  there is something to inherit from, and it provides a common
  `profile_summary` method.

* `Student` – extends `Profile` and adds fields for:
  - major
  - strengths (list of subjects they can help with)
  - needs (list of subjects they want help with)
  - rating information

  It also has helper methods like `can_help`, `needs_help`, and
  `add_rating`, plus an overridden `profile_summary` that prints
  out a more detailed description.

* `StudySession` – a small data class that records a meeting between
  two students. It stores both ids, the topic, an optional note, and
  an optional 1–5 rating. It has helpers to add notes and set the
  rating safely.

* `Availability` – a light‑weight class that stores a few free‑form
  time slots like `"Mon 3‑5"`. For this assignment it is not used
  heavily but shows how scheduling could be layered in later.

### `src.matching`

This module is where the matching logic lives.

* `MatchStrategy` – an abstract base class with a single method,
  `score_pair(seeker, candidate)`. Any matching approach can be
  plugged in here as long as it implements this method.

* `NeedsStrengthsOverlapStrategy` – a very small implementation of
  `MatchStrategy` that simply counts how many of the seeker's needs
  appear in the candidate's strengths list. More overlap means a
  higher compatibility score.

* `MatchEngine` – the main coordinator. It keeps:
  - a dictionary of all `Student` objects
  - a list of `StudySession` objects
  - an instance of `MatchStrategy`

  It can create or update students, record sessions, list sessions,
  and ask the strategy to rank possible partners for a given
  student. Results are sorted by score and by rating so that strong,
  well‑rated helpers float toward the top.

### `main.py`

This file glues everything together in a small text menu so it is
possible to try out the system by hand. It does a little bit of
basic input validation and catches common errors (like invalid ids)
so that the program does not crash in the middle of a run.

## Object‑oriented ideas used

* **Encapsulation** – data is kept in the model classes, and small
  helper methods handle things like rating updates. The `MatchEngine`
  also keeps its dictionaries private and only exposes what is
  needed through methods.

* **Inheritance / Polymorphism** – `Student` inherits from `Profile`
  and overrides `profile_summary`. If later there were different
  profile types (for example tutors and regular students) they could
  all share the same base type.

* **Strategy pattern** – matching logic is pulled out into its own
  interface. The engine just asks the strategy for scores. This
  makes it easier to swap in a different approach later without
  changing the rest of the code.
