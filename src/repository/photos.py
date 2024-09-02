from src.services.roles import RoleAccess
from src.database.models import Role




access_to_route_all = RoleAccess([Role.admin, Role.moderator])


#dependencies=[Depends(access_to_route_all)]







#user: User = Depends(auth_service.get_current_user)