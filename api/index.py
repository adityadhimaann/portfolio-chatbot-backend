def handler(request, response):
    # Set CORS headers
    response.headers.update({
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Content-Type': 'application/json'
    })
    
    # Handle OPTIONS request
    if request.method == 'OPTIONS':
        response.status_code = 200
        return ''
    
    # Handle GET request
    if request.method == 'GET':
        response.status_code = 200
        return {
            "message": "AdiDev Chatbot API is running!",
            "status": "active",
            "endpoints": {
                "chat": "/api/chat"
            }
        }
    
    # Default response
    response.status_code = 405
    return {"error": "Method not allowed"}
