from fastapi import FastAPI, Depends, HTTPException, status

from app.schemas.user_schema import User
from app.api.endpoints.user import user_function as UserFunctions
from app.utils.constant.globals import UserRole

# Role based access control
class RoleChecker:
	def __init__(self, allowed_roles: list[str]):
		self.allowed_roles = allowed_roles

	# import auth
	def __call__(self, user: User = Depends(UserFunctions.get_current_user)):
		if not any(role.value in self.allowed_roles for role in user.role):
			# logger.debug(f"User with role {user.role} not in {self.allowed_roles}")
			raise HTTPException(status_code=403, detail="You are not allowed to access the API")


# Dependency to check if user is admin or editor
def admin_editor_only(current_user):
    if current_user.role not in [UserRole.ADMIN, UserRole.EDITOR]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Admin or Editor role required."
        )
    return current_user
