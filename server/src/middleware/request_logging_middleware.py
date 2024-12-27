import time
import os
import json
from flask import request, g
from werkzeug.local import LocalProxy
from common.logging import logger


def log_request_details():
    """
    Middleware to log detailed request information

    Logs include:
    - Request method
    - Request path
    - Client IP
    - User agent
    - Request headers
    - Request body (for non-binary content)
    - Timing information
    """
    # Start timing the request
    g.request_start_time = time.time()

    # Log request details
    log_data = {
        'method': request.method,
        'path': request.path,
        'remote_addr': request.remote_addr,
        # 'user_agent': request.user_agent.string,
        # 'headers': dict(request.headers),
        # 'content_type': request.content_type
    }

    # try:
    #     # Only log if content is JSON or form data
    #     if request.is_json:
    #         log_data['body'] = request.get_json(silent=True)
    #     elif request.form:
    #         log_data['body'] = dict(request.form)
    # except Exception as e:
    #     log_data['body_parse_error'] = str(e)

    # Log the request details at debug level
    logger.debug(f"Incoming Request: {json.dumps(log_data, indent=4)}")

    return log_data


def log_response_details(response):
    """
    Middleware to log response details and request duration

    Logs include:
    - Response status code
    - Response content type
    - Request duration
    """
    # Calculate request duration
    request_duration = time.time() - g.request_start_time

    log_data = {
        'status_code': response.status_code,
        'content_type': response.content_type,
        'duration_ms': round(request_duration * 1000, 2)
    }

    # Log the response details at debug level
    logger.debug(f"Outgoing Response: {json.dumps(log_data, indent=2)}")

    return response


def register_request_logging_middleware(app):
    """
    Register request and response logging middleware
    """
    app.before_request(log_request_details)
    # app.after_request(log_response_details)
