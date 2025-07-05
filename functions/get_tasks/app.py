import json

def lambda_handler(event, context):

    tasks = [
        {"id": 1, "title": "Tarea 1", "completed": False},
        {"id": 2, "title": "Tarea 2", "completed": True}
    ]

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(tasks)
    }
