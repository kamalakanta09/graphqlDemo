import requests
import json

# Define your GraphQL query
query = """
{
  matches {
    matchId 
    id
    heading 
    timestamp 
    summary 
    description 
    apitype 
    homeId 
    homeName 
    home_code 
    away_id 
    awayName 
    away_code 
    read_time 
    tag 
    publish 
    enabled 
    is_moderated 
    mod_desc 
    approved 
    thumbnails 
    images
  }
}
"""

# Define your request headers
headers = {
    'Content-Type': 'application/json',
}

# Define your request payload
payload = {
    'query': query
}

# Make the POST request to your GraphQL endpoint
response = requests.post('http://127.0.0.1:5000/graphql', headers=headers, json=payload)

# Print the response content
print(response.json())
