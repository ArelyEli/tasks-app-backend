import json
import uuid
from shared.db import get_connection
from shared.models import TaskCreate

def lambda_handler(event, context):
    try:
        user_id = event["requestContext"]["authorizer"]["claims"]["sub"]
    except Exception:
        return {
            "statusCode": 401,
            "body": json.dumps({"message": "Unauthorized"})
        }

    try:
        body = json.loads(event["body"])
        task_data = TaskCreate(**body)
    except Exception as e:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Invalid request", "error": str(e)})
        }

    task_id = str(uuid.uuid4())

    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO tasks (id, user_id, title, description, completed)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                task_id,
                user_id,
                task_data.title,
                task_data.description,
                False
            ))
        conn.commit()
        conn.close()
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Error saving task", "error": str(e)})
        }

    return {
        "statusCode": 201,
        "headers": {
            "Access-Control-Allow-Headers": "application/json,Content-Type,Authorization",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET,POST,PUT,DELETE,OPTIONS"
        },
        "body": json.dumps({"id": task_id, "message": "Task created"})
    }
