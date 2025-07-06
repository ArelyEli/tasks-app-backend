import json
from shared.db import get_connection

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
            result = cursor.execute("""
                DELETE FROM tasks
                WHERE id = %s AND user_id = %s
            """, (task_id, user_id))
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
            "body": json.dumps({"message": "Error deleting task", "error": str(e)})
        }

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Headers": "application/json,Content-Type,Authorization",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET,POST,PUT,DELETE,OPTIONS"
        },
        "body": json.dumps({"message": "Task deleted"})
    }
