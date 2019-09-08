from django.test import TestCase

# Create your tests here.


comment_list=[

    {"id":1,"content":"...","Pid":None},
    {"id":2,"content":"...","Pid":None},
    {"id":3,"content":"...","Pid":None},
    {"id":4,"content":"...","Pid":1},
    {"id":5,"content":"...","Pid":1},
    {"id":6,"content":"...","Pid":4},
    {"id":7,"content":"...","Pid":3},
    {"id":8,"content":"...","Pid":7},
    {"id":9,"content":"...","Pid":None},

]






import collections


comment_dict=collections.OrderedDict()


for comment in comment_list:

    comment["children_comments"]=[]
    comment_dict[comment["id"]]=comment




ret=[]

for comment in comment_dict:

    if comment_dict[comment]["Pid"]:
        pid=comment_dict[comment]["Pid"]

        comment_dict[pid]["children_comments"].append(comment_dict[comment])

    else:
        ret.append(comment_dict[comment])


print(ret)



