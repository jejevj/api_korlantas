from flask import request
import bcrypt
from ...extensions import db
from ...models.user import User
from ...models.role import Role
from ...models.mobile_blacklist_token import MobileBlacklistToken
from ...utils.responses import ok, not_found, bad_request, created, conflict, unauthorized
from ...utils.pagination import clamp_per_page
from . import bp
from ...utils.jwt_helper import generate_token,decode_token  

from . import bp

def is_token_blacklisted(token: str) -> bool:
    """Check if the token is blacklisted."""
    blacklisted_token = MobileBlacklistToken.query.filter_by(token=token).first()
    return blacklisted_token is not None


@bp.get("/protected")
def protected_route():
    token = request.headers.get("Authorization")

    if not token:
        return unauthorized("Token is missing")
    
    token = token.split(" ")[1]
    
    if is_token_blacklisted(token):
        return unauthorized("Token has been invalidated (blacklisted)")
    
    try:    
        user_data = decode_token(token)
        if not user_data:
            return unauthorized("Invalid or expired token")

    except Exception as e:
        
        return unauthorized(str(e))
    
    return ok({"message": "Access granted to protected route"})


@bp.post("/auth/login")
def login():
    """
    Login with username and password, return JWT token if valid.
    """
    data = request.get_json(silent=True) or {}

    if not isinstance(data, dict):
        return bad_request("Body must be a JSON object")
    
    required_fields = ["username", "password"]
    missing_fields = [field for field in required_fields if field not in data or not data[field]]
    if missing_fields:
        return bad_request(f"Missing required field(s): {', '.join(missing_fields)}")

    username = data["username"]
    password = data["password"]

    # Fetch user based on username
    user = User.query.filter_by(username=username).first()
    if not user:
        return unauthorized("Invalid credentials")
    
    # Check if password matches
    if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        return unauthorized("Invalid credentials")
    
    # Check the user's role
    user_role = Role.query.filter_by(id=user.role_id).first()
    if user_role is None or user_role.role != "operator":
        return unauthorized("Only users with the 'operator' role can log in")
    
    # Generate JWT token
    token = generate_token(user.id, user.username, user.role_id)

    # Retrieve company and location details
    company = user.company  # Since the User model has a relationship with Company
    location = user.location  # Since the User model has a relationship with Location
    
    # Prepare response data
    response_data = {
        "token": token,
        "user": user.to_dict(),  # Include user details as usual
        "company": {
            "name": company.company_name,  # Company name
            "logo": company.company_logo  # Company logo (if available)
        },
        "location": {
            "id": location.id,  # Location ID
            "name": location.name  # Location name
        }
    }
    
    return ok(response_data, "Login successful")



@bp.post("/auth/logout")
def logout():
    """
    Log out the user by blacklisting the JWT token.
    """
    token = request.headers.get("Authorization")

    if not token:
        return unauthorized("Token is missing")
    
    token = token.split(" ")[1]
    
    
    # token = token.split(" ")[1]
    
    if is_token_blacklisted(token):
        return unauthorized("Already Logout")
    
    user_data = decode_token(token)

    if not user_data:
        return unauthorized("Invalid or expired token")
    
    blacklisted_token = MobileBlacklistToken(token=token)
    db.session.add(blacklisted_token)
    db.session.commit()

    return ok({"message": "Successfully logged out"}, "Logout successful")