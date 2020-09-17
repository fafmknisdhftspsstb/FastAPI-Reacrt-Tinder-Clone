from fastapi import HTTPException, status

EXCEPTIONS = {
    'user_exists': HTTPException(status_code=400, detail="Username already exists"),

    'invalid_credentials' : HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}),

    'inactive_user': HTTPException(status_code=400, detail="Inactive user"),
    
    'invalid_username_or_password' : HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}),

}