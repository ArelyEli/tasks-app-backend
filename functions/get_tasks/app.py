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

    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT id, title, description, completed, created_at
                FROM tasks
                WHERE user_id = %s
            """, (user_id,))
            tasks = [Task(**row).model_dump(mode="json") for row in cursor.fetchall()]
        conn.close()
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Error fetching tasks", "error": str(e)})
        }

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Headers": "application/json,Content-Type,Authorization",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET,POST,PUT,DELETE,OPTIONS"
        },
        "body": json.dumps(tasks)
    }
