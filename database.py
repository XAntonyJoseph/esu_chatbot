import sqlite3
import json

# Connect database
conn = sqlite3.connect("knowledge.db")

cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS knowledge (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT,
    intent TEXT,
    question TEXT,
    answer TEXT
)
""")

# Clear old data
cursor.execute("DELETE FROM knowledge")

# Load JSON
with open("knowledge.json", "r", encoding="utf-8") as file:

    data = json.load(file)

    faq_data = data["faq_data"]

    # Loop through categories
    for category, intents in faq_data.items():

        # Loop through intents
        for item in intents:

            intent = item["intent"]
            answer = item["answer"]

            # Loop through questions
            for question in item["questions"]:

                cursor.execute(
                    """
                    INSERT INTO knowledge
                    (category, intent, question, answer)
                    VALUES (?, ?, ?, ?)
                    """,
                    (
                        category,
                        intent,
                        question.lower(),
                        answer
                    )
                )

# Save
conn.commit()

conn.close()

print("Database updated successfully.")