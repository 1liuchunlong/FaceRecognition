import datetime
import os
import shutil
import time
import cv2 as cv
import numpy as np
import pymysql


import dlib
from App.face_save_mysql.FaceTools import FaceTools

#与数据库进行数据连接
def PutDatatoSql(uname):
    flag = 1
    con = pymysql.connect(host='localhost', password='root', user='root', port=3306,db='face_sql_db')
    # 创建游标对象
    cur = con.cursor()
    # 判断是否存在库
    #判断是否存在表 无则自动创建
    sql1 = r'''
                CREATE TABLE IF NOT EXISTS t_user (
                id int PRIMARY KEY NOT NULL auto_increment,
                uname VARCHAR(20) NOT NULL,
                created_time DATETIME )
                 '''
    cur.execute(sql1)
    # 编写查询数据的sql
    sql2 = 'select * from t_user where uname=%s '
    try:
        cur.execute(sql2,args=(uname))
        con.commit()
        # 处理结果集
        student = cur.fetchall()
        if student:
            con.close()
            flag = 2

            return flag
        else:
            print(uname)
    except Exception as e:
        print(e)
        print('查询数据失败')
        flag = 0
        return flag
    # 编写插入数据的sql
    print("这")
    sql3 = 'insert into t_user(uname,created_time) values(%s,%s)'
    dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        # 执行sql
        cur.execute(sql3, (uname,dt))
        # 提交事务
        con.commit()
        print('插入数据成功')
        flag=2
        return flag
    except Exception as e:
        print(e)
        con.rollback()
        print('插入数据失败')
        flag = 0
        return flag
    finally:
        # 关闭连接
        con.close()



def face_save_image(name,images):

    ########################插入用户表部分###########################

    faceTools = FaceTools()
    result = PutDatatoSql(name)
    if result == 1:
        print("here is result==1")
        return
    elif result == 2:
        print('22')
        # 可能存在数据库有记录 但是图像资源被删掉了，这种情况重新录入
        # if not os.path.exists('./Picture_resources/Stu_' + str(name)):  # 文件夹是否存在
        #     return
        # elif not os.listdir("./Picture_resources/Stu_" + str(name)):  # 文件夹里面是否有文件
        #     print("222")
        #     return
        # else:
        #     print('该用户已存在!')
    else:
        print('数据库未能成功连接')
    print("333")
    count = 0  # 统计照片数量
    path = "./Picture_resources/Stu_" + str(name)  # 人脸图片数据的储存路径

    face_detector = dlib.get_frontal_face_detector()

    for image in images:
        gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

        faces = face_detector(gray, 1)

        if not os.path.exists(path):  # 如果没有对应文件夹，自动生成
            os.makedirs(path)
        if len(faces) > 1: #一帧出现两张照片丢弃，原因：有人乱入，也有可能人脸识别出现差错
            print("有人混入录入失败")
            continue

        for face in faces:
            # cv.rectangle(frame, (x, y), (x + w, y + h), color=(0, 255, 0), thickness=2)
            image_ploted = cv.rectangle(gray, (face.left(), face.top()), (face.right(), face.bottom()),
                                        color=(0, 255, 0),
                                        thickness=2)
            count += 1
            cv.imwrite(path + '/' + str(count) + '.png', image_ploted)
            # 显示图片

            ##bug
            faceTools.add_FaceCoding(path + '/' + str(count) + '.png', name)

        print('已采集成功人脸照片数量为：' + str(count))

    print('采集照片成功,3秒后退出程序...')
    time.sleep(3)

# face_save_image("zhanhsan","000")



