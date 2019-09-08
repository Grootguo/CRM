
from rbac.models import Role


def initial_sesson(user,request):
    """
    功能：将当前登录人的所有权限录入session中
    :param user: 当前登录人
    """
    # 查询当前登录人的所有权限列表
    # 查看当前登录人的所有角色
    # ret=Role.objects.filter(user=user)
    print("request.user",request.user)
    permissions = Role.objects.filter(userinfo=request.user,permissions__isnull=False).\
                               values( "permissions__url",
                                        "permissions__title",
                                        "permissions__code",
                                        "permissions__pid",
                                        "permissions__pk",
                                        "permissions__type",
                                        "permissions__pids",
                                       ).distinct()
    print(permissions)
    permission_list = []

    for item in permissions:
        # 构建权限列表
        permission_list.append({
            "url":item["permissions__url"] or "",
            "id":item["permissions__pk"],
            "pid":item["permissions__pid"] or "",
            "title":item["permissions__title"],
            "type":item["permissions__type"],
            "pids":item["permissions__pids"],
        })

    # 将当前登录人的权限列表注入session中
    request.session["permission_list"] = permission_list
