# -*- coding: utf-8 -*-
import pymysql
from datetime import datetime
import re
import sys
import os
from dotenv import load_dotenv

# .env fájl betöltése
load_dotenv()

db_config = {
    'host': os.getenv('DB_HOST'),
    'port': int(os.getenv('DB_PORT', 3306)),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME'),
    'charset': os.getenv('DB_CHARSET', 'utf8mb4'),
    'cursorclass': pymysql.cursors.DictCursor
}

client = os.getenv('CLIENT')

INPUT_FILE = "/opt/twampy/log.txt"
timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def parse_time(value_str):
    try:
        if value_str.endswith("ms"):
            return float(value_str.replace("ms", ""))
        elif value_str.endswith("us"):
            return float(value_str.replace("us", "")) / 1000
        elif value_str.endswith("%"):
            return float(value_str.replace("%", ""))
        elif value_str.endswith("sec"):
            return float(value_str.replace("sec", "")) * 1000
        else:
            raise ValueError(f"Ismeretlen formatum: {value_str}")
    except Exception as e:
        print(f"Error in a parse_time function: {e}")
        raise

def parse_line(line):
    match = re.match(r"^\s*(\w+):\s+([\d\.a-z%]+)\s+([\d\.a-z%]+)\s+([\d\.a-z%]+)\s+([\d\.a-z%]+)\s+([\d\.a-z%]+)", line)
    if match:
        try:
            direction = match.group(1)
            min_val = parse_time(match.group(2))
            max_val = parse_time(match.group(3))
            avg_val = parse_time(match.group(4))
            jitter = parse_time(match.group(5))
            loss = parse_time(match.group(6))
            return (timestamp, direction, min_val, max_val, avg_val, jitter, loss, client)
        except Exception as e:
            print(f"Error in procesing the line: {e}")
    return None

# Sorok feldolgozása
results = []
try:
    #with open(INPUT_FILE, "r") as file:
    with open(INPUT_FILE, "r", encoding="latin1") as file:  # vagy encoding="windows-1250"
        for line in file:
            if any(direction in line for direction in ["Outbound", "Inbound", "Roundtrip"]):
                parsed = parse_line(line)
                if parsed:
                    results.append(parsed)
except FileNotFoundError:
    print(f"Error: the input file is missing: {INPUT_FILE}")
    sys.exit(1)
except Exception as e:
    print(f"Error during reading the input file: {e}")
    sys.exit(1)

if not results:
    print("No data in the input file.")
    sys.exit(0)

try:
    connection = pymysql.connect(**db_config)
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS network_stats (
                id INT AUTO_INCREMENT PRIMARY KEY,
                timestamp DATETIME,
                direction VARCHAR(20),
                min_ms FLOAT,
                max_ms FLOAT,
                avg_ms FLOAT,
                jitter_ms FLOAT,
                loss_percent FLOAT,
                hostname VARCHAR(128)
            )
            """)
            insert_query = """
            INSERT INTO network_stats
            (timestamp, direction, min_ms, max_ms, avg_ms, jitter_ms, loss_percent, hostname)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.executemany(insert_query, results)
        connection.commit()
    print("Data succesfully stored in the database.")
except pymysql.MySQLError as e:
    print(f"Database error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"General error: {e}")
    sys.exit(1)
