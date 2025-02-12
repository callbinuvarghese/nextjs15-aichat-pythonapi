# Using curl (for simple testing)

curl -X POST \
     -H "Content-Type: application/json" \
     -d '{
           "messages": [
             {"role": "user", "content": "Hello, I am testing the API."},
             {"role": "assistant", "content": "Hi there!"}
           ]
         }' \
     http://localhost:5000/chat/stream 
