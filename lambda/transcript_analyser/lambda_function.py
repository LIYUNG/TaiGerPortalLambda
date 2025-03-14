import json
from db import get_keywords_collection
from main import analyze_transcript


def lambda_function(event, context):
    path = event.get('path')
    method = event.get('httpMethod')

    if path == '/analyze':
        if method == 'POST':
            return post_analyze_courses(event)

        elif method == "GET":
            return get_keywords(event)

        else:
            return {
                'statusCode': 405,
                'body': json.dumps('Method Not Allowed')
            }
    elif path == '/hello':
        if method == 'GET':
            return lambda_hello_world(event)
        else:
            return {
                'statusCode': 405,
                'body': json.dumps('Method Not Allowed')
            }
    # Additional routes...
    else:
        return {
            'statusCode': 404,
            'body': json.dumps('Not Found')
        }


def lambda_hello_world(event):
    # This function is triggered by an event and returns a response.
    message = "Hello, world!"

    # Print statement logs to CloudWatch logs
    print(message)

    return {
        'statusCode': 200,
        'body': json.dumps({'message': message})
    }


def get_keywords(event):
    keywords = get_keywords_collection()
    print(keywords)

    return {
        'statusCode': 200,
        'body': json.dumps({'keywords': keywords})
    }


def post_analyze_courses(event):
    # Get the body from the event
    body = event.get('body')

    # If the body is JSON, parse it
    if body:
        try:
            body = json.loads(body)  # Parse the body as JSON
        except json.JSONDecodeError:
            return {
                'statusCode': 400,
                'body': json.dumps('Invalid JSON format')
            }

    # Now you can work with the request body
    print("Request body:", body)

    result = analyze_transcript(body['courses'],
                       body['student_id'],
                       body['student_name'],
                       body['factor'],
                       body['language'],
                       body['courses_taiger_guided'],
                       body['requirement_ids'])

    return {
        'statusCode': 200,
        'body': result
    }
