from flask import jsonify
from logger import logger

def error_handler(error):
    """Global error handler for the application"""
    
    # Get error details
    status_code = getattr(error, 'code', 500)
    message = str(error)
    
    # Log the error
    logger.error(f'Error: {message}')
    if status_code == 500:
        logger.error(f'Stack trace: {error.__traceback__}')
    
    # Return error response
    response = {
        'error': message,
        'status_code': status_code
    }
    
    # Add stack trace in development
    if logger.is_development():
        response['stack_trace'] = str(error.__traceback__)
    
    return jsonify(response), status_code
