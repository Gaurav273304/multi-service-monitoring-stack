from flask import Flask, jsonify
import mysql.connector
import os

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host=os.environ.get("DB_HOST", "db"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        database=os.environ.get("DB_NAME")
    )

@app.route("/health")
def health():
    return jsonify({"status": "ok"}), 200

@app.route("/visitors")
def visitors():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO visitors (visited_at) VALUES (NOW())")
        conn.commit()
        cursor.execute("SELECT COUNT(*) FROM visitors")
        count = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return jsonify({"total_visitors": count}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
