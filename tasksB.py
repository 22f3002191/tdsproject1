import os

# B1 & B2: Security Checks
def B12(filepath):
    if filepath.startswith('/data'):
        return True
    else:
        return False

# B3: Fetch Data from an API and Save it
def B3(url, save_path):
    if not B12(save_path):
        return "Error: Save path must be inside /data directory."
    import requests
    response = requests.get(url)
    with open(save_path, 'w') as file:
        file.write(response.text)
    return f"Data fetched from {url} and saved to {save_path}"

# B4: Clone a Git Repo and Make a Commit
def B4(repo_url, commit_message):
    if not B12('/data/repo'):
        return "Error: Repo path must be inside /data directory."
    import subprocess
    subprocess.run(["git", "clone", repo_url, "/data/repo"])
    subprocess.run(["git", "-C", "/data/repo", "commit", "-am", commit_message])
    return "Git repo cloned and commit made."

# B5: Run SQL Query on SQLite or DuckDB
def B5(db_path, query, output_filename):
    if not B12(db_path):
        return "Error: Database path must be inside /data directory."
    import sqlite3, duckdb
    conn = sqlite3.connect(db_path) if db_path.endswith('.db') else duckdb.connect(db_path)
    cur = conn.cursor()
    cur.execute(query)
    result = cur.fetchall()
    conn.close()
    with open(output_filename, 'w') as file:
        file.write(str(result))
    return f"Query executed and results saved to {output_filename}"

# B6: Web Scraping and Save Data
def B6(url, output_filename):
    if not B12(output_filename):
        return "Error: Output path must be inside /data directory."
    import requests
    result = requests.get(url).text
    with open(output_filename, 'w') as file:
        file.write(str(result))
    return f"Scraped data from {url} and saved to {output_filename}"

# B7: Image Processing (Resize if specified)
def B7(image_path, output_path, resize=None):
    if not B12(image_path) or not B12(output_path):
        return "Error: Both input and output paths must be inside /data directory."
    from PIL import Image
    img = Image.open(image_path)
    if resize:
        img = img.resize(resize)
    img.save(output_path)
    return f"Image saved to {output_path}"

# B8: Audio Transcription (using OpenAI's Whisper API)
def B8(audio_path):
    if not B12(audio_path):
        return "Error: Audio file path must be inside /data directory."
    import openai
    with open(audio_path, 'rb') as audio_file:
        return openai.Audio.transcribe("whisper-1", audio_file)

# B9: Convert Markdown to HTML
def B9(md_path, output_path):
    if not B12(md_path) or not B12(output_path):
        return "Error: Both input and output paths must be inside /data directory."
    import markdown
    with open(md_path, 'r') as file:
        html = markdown.markdown(file.read())
    with open(output_path, 'w') as file:
        file.write(html)
    return f"Markdown converted to HTML and saved to {output_path}"

# B10: API Endpoint to Filter CSV and Return JSON Data (Flask)
from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/filter_csv', methods=['POST'])
def filter_csv():
    data = request.json
    csv_path, filter_column, filter_value = data['csv_path'], data['filter_column'], data['filter_value']
    if not B12(csv_path):
        return jsonify({"error": "CSV path must be inside /data directory."}), 400
    import pandas as pd
    df = pd.read_csv(csv_path)
    filtered = df[df[filter_column] == filter_value]
    return jsonify(filtered.to_dict(orient='records'))

# Sample Usage
if __name__ == "__main__":
    # Start Flask server for B10
    app.run(debug=True)
