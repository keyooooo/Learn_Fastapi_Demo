from fastapi import APIRouter
from models import *
from pydantic import BaseModel,field_validator
from typing import Union,List
from fastapi.exceptions import HTTPException

student_api = APIRouter()

class StudentIn(BaseModel):
    sno : int
    pwd : str
    name : str
    clas_id : int
    courses : List[int] = []
    
    #后端数据校验，防止脏数据污染数据库，用pydantic的filed_validator实现
    #这里只用学号做一下简单的数据校验
    @field_validator("sno")
    def sno_validator(cls, value):
        assert value > 2000001 and value < 2026000 ,'学号在2000001--2026000'
        return value



@student_api.post("/")
async def add_student(student_in: StudentIn):
    
    #数据校验成功后，插入数据库

    # # (1)常用：create()方法
    student = await Student.create(sno=student_in.sno,pwd=student_in.pwd,name=student_in.name,clas_id=student_in.clas_id)

    # # (2)少用：save()方法,这个更加体现ORM这种思想
    # student = Student(sno=student_in.sno,pwd=student_in.pwd,name=student_in.name,clas_id=student_in.clas_id)
    # await student.save() #插入操作，一定需要await异步操作

    # #上面的操作没有涉及到多对多的关系，也就是student_course表没有数据插入
    #下面进行多对多关系绑定
    choose_course = await Course.filter(id__in=student_in.courses)
    await student.courses.clear() #清除操作
    await student.courses.add(*choose_course)
    return student

@student_api.delete("/{student_id}")
async def delete_student(student_id: int):

    student_obj = await Student.get_or_none(id=student_id)
    if not student_obj:
        raise HTTPException(status_code=404,detail=f"主键为{student_id}的学生不存在")
    target_name = student_obj.name
    await student_obj.delete()

    return {
        "操作": f"删除一个id={student_id}学生，名字为{target_name}"
    }

@student_api.put("/{student_id}")
async def update_student(student_id: int,student_in: StudentIn):
    # # (1)一个一个传入更新，而且这里和添加时一样，只能更新一对一和一对多的数据
    # Student.filter(id=student_id).update(sno=student_in.sno,pwd=student_in.pwd,name=student_in.name,clas_id=student_in.clas_id)

    # # (2)打包，再解包传入更新,也是只能更新一对一和一对多的数据
    # data = student_in.model_dump()
    # Student.filter(id=student_in.id).update(**data)

    # # *****如果想处理多对多关系数据,要进行如下操作*****
    data = student_in.model_dump()
    courses = data.pop("courses")
    #pop出来courses
    await Student.filter(id=student_id).update(**data)
    #到这里是更新除了courses外的数据,接下来就要对courses进行操作了
    edit_stu = await Student.get(id=student_id)
    choose_courses = await Course.filter(id__in=courses)
    await edit_stu.courses.clear()
    await edit_stu.courses.add(*choose_courses)

    return edit_stu
    
    



    return {
        "操作": f"更新一个id={student_id}学生"
    }

@student_api.get("/{student_id}")
async def get_one_student(student_id: int):
    # student = await Student.get(id=student_id)
    student = await Student.filter(id=student_id).values("name","courses__name")

    return student

@student_api.get("/")
async def get_all_students():
    # #(1)查询所有 all方法
    # students = await Student.all() 
    # for stu in students:
    #     print(stu.name,stu.sno)

    # #(2)过滤查询 filter方法：返回queryset列表对象
    # students = await Student.filter(clas_id = 1)
    # for stu in students:
    #     print(stu.name,stu.sno)

    # #(3)过滤查询 get方法:返回模型类对象
    # stu = await Student.get(id = 3)
    # print(stu.name)

    # #(4)模糊查询 filter方法:返回列表对象
    # '__gt'='>' '__gte'='>=' 同理__lt __lte
    # stus1 = await Student.filter(sno__gte=2024001)
    # print(stus1)
    # stus2 = await Student.filter(sno__in=[2024002,2024004])
    # print(stus2)
    # stus3 = await Student.filter(sno__range=[2024001,2024003])
    # print(stus3)

    # #(5)values查询 values方法:返回 '所需要查询的字段组成的字典' 所组成的列表
    # stu_info1 = await Student.all().values("id","name","sno")
    # print(stu_info1)
    # stu_info2 = await Student.filter(sno__range=[2024001,2024003]).values("name","sno")
    # print(stu_info2)

    # #(6)一对多查询
    # # 1.取其中一个学生的班级名
    geted_student = await Student.get(name="小王")
    # print(geted_student.name)
    # print(geted_student.sno)
    # print(await geted_student.clas.values("name"))
    # # 2.取全部学生的班级名
    # geted_students = await Student.all().values("name","clas__name")
    # print(geted_students)

    # #(7)多对多查询 可以直接用values方法 __column_name相当于跨表用外键查询字段信息
    print(await geted_student.courses.all())
    print(await geted_student.courses.all().values("name"))
    print(await geted_student.courses.all().values("name","teacher__name"))

    students = await Student.all().values("name","clas__name","courses__name")
    return students
    # return {
    #     # "查询学生信息" : stus3         #返回json文件显示所有字段内容
    #     # "查询学生某项信息" : stu_info2  #返回json文件显示values方法作用的字段内容}
    # }

# 相应页面
# @student_api.get("/index.html")
# async def get_all_students():

#     return