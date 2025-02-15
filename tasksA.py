import sqlite3
import subprocess
from dateutil.parser import parse
from datetime import datetime
import json
from pathlib import Path
import os
import requests
from scipy.spatial.distance import cosine
from dotenv import load_dotenv
from fastapi import HTTPException


load_dotenv()

AIPROXY_TOKEN = os.getenv('AIPROXY_TOKEN')


def A1(email="22f3002191@ds.study.iitm.ac.in"):
    try:
        process = subprocess.Popen(
            ["uv", "run", "https://raw.githubusercontent.com/sanand0/tools-in-data-science-public/tds-2025-01/project-1/datagen.py", email],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        stdout, stderr = process.communicate()
        if process.returncode != 0:
            raise HTTPException(status_code=500, detail=f"Error: {stderr}")
        return stdout
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Error: {e.stderr}")
# A1()
def A2(prettier_version="prettier@3.4.2", filename="/data/format.md"):
    command = [r"C:\Program Files\nodejs\npx.cmd", prettier_version, "--write", filename]
    try:
        subprocess.run(command, check=True)
        print("Prettier executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

def A3(filename='/data/dates.txt', targetfile='/data/dates-wednesdays.txt', weekday=2):
    input_file = filename
    output_file = targetfile
    weekday = weekday
    weekday_count = 0

    with open(input_file, 'r') as file:
        weekday_count = sum(1 for date in file if parse(date).weekday() == int(weekday)-1)


    with open(output_file, 'w') as file:
        file.write(str(weekday_count))

def A4(filename="/data/contacts.json", targetfile="/data/contacts-sorted.json"):
    # Load the contacts from the JSON file
    with open(filename, 'r') as file:
        contacts = json.load(file)

    # Sort the contacts by last_name and then by first_name
    sorted_contacts = sorted(contacts, key=lambda x: (x['last_name'], x['first_name']))

    # Write the sorted contacts to the new JSON file
    with open(targetfile, 'w') as file:
        json.dump(sorted_contacts, file, indent=4)

def A5(log_dir_path='/data/logs', output_file_path='/data/logs-recent.txt', num_files=10):
    log_dir = Path(log_dir_path)
    output_file = Path(output_file_path)

    # Get list of .log files sorted by modification time (most recent first)
    log_files = sorted(log_dir.glob('*.log'), key=os.path.getmtime, reverse=True)[:num_files]

    # Read first line of each file and write to the output file
    with output_file.open('w') as f_out:
        for log_file in log_files:
            with log_file.open('r') as f_in:
                first_line = f_in.readline().strip()
                f_out.write(f"{first_line}\n")



def A6(doc_dir_path='/data/docs', output_file_path='/data/docs/index.json'):
    index_data = {}
    
    for root, _, files in os.walk(doc_dir_path):
        for file in files:
            if file.endswith('.md'):
                relative_path = os.path.relpath(os.path.join(root, file), doc_dir_path).replace('\\', '/')
                
                with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                    h1_lines = [line[2:].strip() for line in f if line.startswith('# ')]
                    if h1_lines:
                        title = h1_lines[0] if len(h1_lines) == 1 else ", ".join(h1_lines)
                        index_data[relative_path] = title

    with open(output_file_path, 'w', encoding='utf-8') as f:
        json.dump(index_data, f, indent=4)


def A7(filename='/data/email.txt', output_file='/data/email-sender.txt'):
    # Read the content of the email
    with open(filename, 'r') as file:
        email_content = file.readlines()

    sender_email = "sujay@gmail.com"
    for line in email_content:
        if "From" == line[:4]:
            sender_email = (line.strip().split(" ")[-1]).replace("<", "").replace(">", "")
            break

    # Get the extracted email address

    # Write the email address to the output file
    with open(output_file, 'w') as file:
        file.write(sender_email)

import base64
def png_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        base64_string = base64.b64encode(image_file.read()).decode('utf-8')
    return base64_string
# def A8():
#     input_image = "data/credit_card.png"
#     output_file = "data/credit-card.txt"

#     # Step 1: Extract text using OCR
#     try:
#         image = Image.open(input_image)
#         extracted_text = pytesseract.image_to_string(image)
#         print(f"Extracted text:\n{extracted_text}")
#     except Exception as e:
#         print(f"❌ Error reading or processing {input_image}: {e}")
#         return

#     # Step 2: Pass the extracted text to the LLM to validate and extract card number
#     prompt = f"""Extract the credit card number from the following text. Respond with only the card number, without spaces:

#     {extracted_text}
#     """
#     try:
#         card_number = ask_llm(prompt).strip()
#         print(f"Card number extracted by LLM: {card_number}")
#     except Exception as e:
#         print(f"❌ Error processing with LLM: {e}")
#         return

#     # Step 3: Save the extracted card number to a text file
#     try:
#         with open(output_file, "w", encoding="utf-8") as file:
#             file.write(card_number + "\n")
#         print(f"✅ Credit card number saved to: {output_file}")
#     except Exception as e:
#         print(f"❌ Error writing {output_file}: {e}")

def A8(filename='/data/credit_card.txt', image_path='/data/credit_card.png'):
    # Construct the request body for the AIProxy call
    body = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "There is 8 or more digit number is there in this image, with space after every 4 digit, only extract the those digit number without spaces and return just the number without any other characters"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{png_to_base64(image_path)}"
                        }
                    }
                ]
            }
        ]
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {AIPROXY_TOKEN}"
    }

    # Make the request to the AIProxy service
    response = requests.post("http://aiproxy.sanand.workers.dev/openai/v1/chat/completions",
                             headers=headers, data=json.dumps(body))
    # response.raise_for_status()

    # Extract the credit card number from the response
    result = response.json()
    # print(result); return None
    card_number = result['choices'][0]['message']['content'].replace(" ", "")

    # Write the extracted card number to the output file
    with open(filename, 'w') as file:
        file.write(card_number)
# A8()





import os
import json
import sqlite3
import requests
from scipy.spatial.distance import cosine

def get_embedding(text):
    """
    Fetches text embedding using GPT-4o Mini via AI Proxy.
    """
    api_token = os.getenv("AIPROXY_TOKEN")
    if not api_token:
        raise ValueError("AIPROXY_TOKEN environment variable not set.")
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_token}"
    }
    data = {
        "model": "text-embedding-3-small",
        "input": [text]
    }
    
    try:
        response = requests.post("https://aiproxy.sanand.workers.dev/openai/v1/embeddings", headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        if "data" not in result or not result["data"]:
            raise ValueError("Empty embedding response.")
        return result["data"][0]["embedding"]
    except requests.RequestException as e:
        raise RuntimeError(f"Embedding request failed: {str(e)}")

def A9(filename='/data/comments.txt', output_filename='/data/comments-similar.txt'):
    """
    Finds the most similar pair of comments using GPT-4o Mini embeddings and writes them to output file.
    """
    if not os.path.exists(filename):
        return {"error": f"{filename} not found"}
    
    with open(filename, 'r', encoding='utf-8') as f:
        comments = [line.strip() for line in f if line.strip()]
    
    if len(comments) < 2:
        return {"error": "Not enough comments to compare."}
    
    try:
        embeddings = []
        for comment in comments:
            try:
                embeddings.append(get_embedding(comment))
            except RuntimeError as e:
                return {"error": f"Failed to get embedding: {str(e)}"}
        
        min_distance = float('inf')
        most_similar = (None, None)
    
        for i in range(len(comments)):
            for j in range(i + 1, len(comments)):
                distance = cosine(embeddings[i], embeddings[j])
                if distance < min_distance:
                    min_distance = distance
                    most_similar = (comments[i], comments[j])
    
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(most_similar[0] + '\n')
            f.write(most_similar[1] + '\n')
    
        return {"status": "success", "most_similar": most_similar}
    except Exception as e:
        return {"error": str(e)}

def A10(db_path='/data/ticket-sales.db', output_filename='/data/ticket-sales-gold.txt'):
    """
    Calculates total sales for 'Gold' ticket type from SQLite database and writes the result to output file.
    """
    if not os.path.exists(db_path):
        return {"error": f"Database {db_path} not found."}
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Ensure the table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='tickets'")
        if not cursor.fetchone():
            return {"error": "Table 'tickets' not found in database."}
        
        cursor.execute("SELECT SUM(units * price) FROM tickets WHERE type = 'Gold'")
        result = cursor.fetchone()
        total_sales = result[0] if result and result[0] is not None else 0
    
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(str(total_sales))
    
        return {"status": "success", "total_sales": total_sales}
    except sqlite3.Error as e:
        return {"error": f"Database error: {str(e)}"}
    except Exception as e:
        return {"error": str(e)}
    finally:
        if conn:
            conn.close()
