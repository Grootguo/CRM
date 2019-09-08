

from django.utils.safestring import mark_safe
from django.template import Library
import json
import collections
import re

from rbac.models import Permission

register = Library()


@register.inclusion_tag("menu2.html")
def get_menu(request):

    permission_list = request.session.get("permission_list")
    print("permission_list",permission_list)
    permission_dict=collections.OrderedDict()

    current_path=request.path
    pids=[]
    for permission in permission_list:

        if permission.get("type") == "button":
            continue
        id=str(permission.get("id"))
        # permission["nodes"]=[]
        permission["tags"]=["0"]
        permission["text"]=permission.get("title")
        permission["href"]=permission.get("url") or "javascript:void(0)"
        permission_dict[id]=permission
        #######################
        if current_path == permission["href"]:

            pids = permission["pids"].split("/") if permission["pids"] else pids
            permission["backColor"] = "#636363"
            permission["color"] = "#fff"

        permission_dict[id] = permission
        #######################

    for pid in pids:
        if pid in permission_dict:
            permission_dict[pid]["state"] = {
                "expanded": True,
            }


    print("permission_dict",permission_dict)

    permission_tree=[]

    for permission_pk in permission_dict:
        pid=permission_dict[permission_pk]["pid"]
        if pid:

            if "nodes" in permission_dict[str(pid)]:
                permission_dict[str(pid)]["nodes"].append(permission_dict[permission_pk])
            else:
                permission_dict[str(pid)]["nodes"] = [permission_dict[permission_pk], ]
            permission_dict[str(pid)]["tags"]=[str(int(permission_dict[str(pid)]["tags"][0])+1)]

        else:
            permission_tree.append(permission_dict[permission_pk])

    print("permission_tree",permission_tree)
    return {"permission_tree":json.dumps(permission_tree)}



@register.simple_tag
def gen_role_url(request, rid):
    params = request.GET.copy()
    params._mutable = True
    params['rid'] = rid
    return params.urlencode()
