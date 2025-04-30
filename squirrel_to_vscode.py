import xml.etree.ElementTree as ET
import json

# === CONFIG ===
path_to_aliases = r"C:\Users\YourName\.squirrel-sql\SQLAliases23.xml"  # <-- Update this
output_path = r"C:\Users\YourName\Desktop\sqlconnections.json"          # Output location

connections = []

def is_password_encrypted(password_text):
    """Check if a password looks encrypted (hex-encoded by SQuirreL)."""
    if not password_text:
        return False
    return len(password_text) > 20 and all(c in "0123456789abcdef" for c in password_text.lower())

# === PARSE XML ===
tree = ET.parse(path_to_aliases)
root = tree.getroot()

# Only get alias beans
for alias in root.findall(".//bean[@class='net.sourceforge.squirrel_sql.client.alias.Alias']"):
    name = alias.find('name').text if alias.find('name') is not None else ''
    url = alias.find('url').text if alias.find('url') is not None else ''
    username = alias.find('userName').text if alias.find('userName') is not None else ''
    password = alias.find('password').text if alias.find('password') is not None else ''

    if url.startswith("jdbc:jtds:sqlserver://"):
        url_body = url.replace("jdbc:jtds:sqlserver://", "")
        parts = url_body.split("/")
        if len(parts) >= 2:
            server_port = parts[0]
            database = parts[1]
            if ":" in server_port:
                server, port = server_port.split(":")
            else:
                server, port = server_port, '1433'
        else:
            server, port, database = "?", "?", "?"

        if is_password_encrypted(password):
            password = "MISSING_PASSWORD"

        connection = {
            "profileName": name,
            "server": f"{server},{port}",
            "database": database,
            "user": username,
            "password": password,
            "authenticationType": "SqlLogin",
            "options": {
                "encrypt": False
            }
        }
        connections.append(connection)

    elif url.startswith("jdbc:odbc:"):
        print(f"ODBC alias '{name}' skipped — manual handling needed.")
        continue
    else:
        print(f"Unknown URL type in alias '{name}' — skipping.")
        continue

# === SAVE OUTPUT ===
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(connections, f, indent=2)

print(f"\nExported {len(connections)} MSSQL connections to:\n{output_path}")
print("Check for 'MISSING_PASSWORD' entries and update them manually if needed.")