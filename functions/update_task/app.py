import json
from shared.db import get_connection
from shared.models import TaskUpdate

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
        body = json.loads(event["body"])
        task_data = TaskUpdate(**body)
    except Exception as e:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Invalid request", "error": str(e)})
        }

    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            result = cursor.execute("""
                UPDATE tasks
                SET title = %s, description = %s, completed = %s
                WHERE id = %s AND user_id = %s
            """, (
                task_data.title,
                task_data.description,
                task_data.completed,
                task_id,
                user_id
            ))
        conn.commit()
        conn.close()

        if result == 0:
            return {
                "statusCode": 404,
                "body": json.dumps({"message": "Task not found"})
            }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Error updating task", "error": str(e)})
        }

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Headers": "application/json,Content-Type,Authorization",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET,POST,PUT,DELETE,OPTIONS"
        },
        "body": json.dumps({"message": "Task updated"})
    }
