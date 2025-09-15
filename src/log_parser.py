import re
import pandas as pd

# Regex for common NGINX access log format
LOG_PATTERN = re.compile(
    r'(?P<ip>\d+\.\d+\.\d+\.\d+) - - \[(?P<time>.*?)\] '
    r'"(?P<method>GET|POST|PUT|DELETE|HEAD) (?P<url>\S+) HTTP.*" '
    r'(?P<status>\d{3}) (?P<size>\d+) "(?P<referrer>[^"]*)" "(?P<user_agent>[^"]*)"'
)

def parse_log_line(line):
    match = LOG_PATTERN.match(line)
    if match:
        return match.groupdict()
    return None

def parse_log_file(filepath):
    parsed_rows = []
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            data = parse_log_line(line)
            if data:
                parsed_rows.append(data)
    return pd.DataFrame(parsed_rows)
