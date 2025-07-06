import json
from shared.db import get_connection
from shared.models import Task

def lambda_handler(event, context):
    try:
        user_id = event["requestContext"]["authorizer"]["claims"]["sub"]
    except Exception:
        return {
            "statusCode": 401,
            "body": json.dumps({"message": "Unauthorized"})
        }

    task_id = event.get("pathParameters", {}).get("id")
    if not task_id:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Task ID is required"})
        }

    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT id, title, description, completed, created_at
                FROM tasks
                WHERE id = %s AND user_id = %s
            """, (task_id, user_id))
            row = cursor.fetchone()
        conn.close()

        if row is None:
            return {
                "statusCode": 404,
                "body": json.dumps({"message": "Task not found"})
            }

        task = Task(**row).model_dump(mode="json")
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Error fetching task", "error": str(e)})
        }

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(task)
    }
