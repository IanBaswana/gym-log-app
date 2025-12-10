# Parse Workout Routine

## Goal
Convert unstructured text describing a workout (e.g. from iPhone Notes) into a structured JSON format suitable for the GymLog application.

## Inputs
- **Raw Text**: A string containing the workout description.
  - Example: "Chest day. Bench press 135lbs 3x10, Incline 4x12. Flys 3 sets to failure."

## Output
- **JSON Object**: A list of exercises.
  ```json
  {
    "routineName": "Chest Day",
    "exercises": [
      {
        "name": "Bench Press",
        "sets": 3,
        "reps": "10",
        "weight": "135lbs",
        "notes": ""
      },
      ...
    ]
  }
  ```

## Tools & Scripts
- **Script**: `execution/parse_workout.py`
  - **Usage**: `python execution/parse_workout.py "raw text here"` or `python execution/parse_workout.py --file path/to/note.txt`

## Edge Cases
- **Missing Data**: If weight or reps are missing, infer from context or leave null.
- **Ambiguous headers**: If the user has multiple workouts in one note, try to parse the first distinct one or return an error.
- **Shorthand**: Handle common gym abbvs ("DB" -> Dumbbell, "BB" -> Barbell).
