def handler(request, response):
    # Set CORS headers
    response.headers.update({
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Content-Type': 'application/json'
    })
    
    # Handle OPTIONS request
    if request.method == 'OPTIONS':
        response.status_code = 200
        return ''
    
    # Handle POST request
    if request.method == 'POST':
        try:
            data = request.json if hasattr(request, 'json') and request.json else {}
            message = data.get('message', 'No message provided')
            session_id = data.get('session_id', 'default')
        except:
            message = 'Invalid JSON data'
            session_id = 'error'
        
        response.status_code = 200
        return {
            "response": f"You said: {message}. This is the AdiDev Assistant. I can help you learn about Aditya's background, skills, and projects.",
            "session_id": session_id
        }
    
    # Default response
    response.status_code = 405
    return {"error": "Method not allowed"}
