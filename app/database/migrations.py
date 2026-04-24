from app.database.connection import db

def init_db():
    """
    
    """

    with db.get_cursor() as cursor:
        # Create words table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS words (
                id SERIAL PRIMARY KEY,
                word TEXT NOT NULL,
                pos VARCHAR(20) NOT NULL,
                language_code VARCHAR(10) NOT NULL,
                lemma TEXT,
                UNIQUE (word, pos, language_code)
            );
            """
        )

        # Create translations table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS translations (
                id SERIAL PRIMARY KEY,
                source_word_id INTEGER NOT NULL REFERENCES words(id) ON DELETE CASCADE,
                target_word_id INTEGER NOT NULL REFERENCES words(id) ON DELETE CASCADE,
                direction VARCHAR(10) NOT NULL,
                UNIQUE (source_word_id, target_word_id, direction)
            );
            """
        )

        # Create indexes
        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_words_word_lang
            ON words (word, language_code);
            """
        )

        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_translations_source
            ON translations (source_word_id);
            """
        )

        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_translations_target
            ON translations (target_word_id);
            """
        )

    print("✅ Tables and indexes verified / created successfully.")

if __name__ == "__main__":
    init_db()