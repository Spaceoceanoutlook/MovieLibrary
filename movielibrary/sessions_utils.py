from fastapi import Request


def get_current_user_email(request: Request) -> str | None:
    return request.session.get("user_email")
