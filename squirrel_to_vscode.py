import xml.etree.ElementTree as ET
import json

# Path to your SQLAliases23.xml
path_to_aliases = r"C:\Users\YourName\.squirrel-sql\SQLAliases23.xml"  # <-- CHANGE THIS
output_path = r"C:\Users\YourName\Desktop\sqlconnections.json"  # Output file path

connections = []

def is_password_encrypted(password_text):
    """Quick check if password looks encrypted."""
    if not password_text:
        return False
    return len(password_text) > 20 and all(c in "0123456789abcdef" for c in password_text.lower())

# Parse XML
tree = ET.parse(path_to_aliases)
root = tree.getroot()

for alias in root.findall('alias'):
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
            "profileName": name,  # <<< NEW: Friendly name
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
        print(f"ODBC alias '{name}' found — special handling needed. Skipping for now...")
        continue
    else:
        print(f"Unknown URL type for alias '{name}', skipping...")
        continue

# Save
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(connections, f, indent=2)

print(f"\nExported {len(connections)} MSSQL connections to {output_path}")
print("\nCheck for any 'MISSING_PASSWORD' fields and update them manually.")
