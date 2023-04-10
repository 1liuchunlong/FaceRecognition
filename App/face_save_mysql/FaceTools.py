import face_recognition
import numpy
from os import listdir, path
from App.face_save_mysql.FaceSQL import FaceSQL


class FaceTools:
    def __init__(self):
        try:
            self.facesql = FaceSQL()
        except:
            print("数据库连接错误")

    def encoding_FaceStr(self, image_face_encoding):
        # 将numpy array类型转化为列表
        encoding__array_list = image_face_encoding.tolist()
        # 将列表里的元素转化为字符串
        encoding_str_list = [str(i) for i in encoding__array_list]
        # 拼接列表里的字符串
        encoding_str = ','.join(encoding_str_list)
        return encoding_str

    def decoding_FaceStr(self, encoding_str):
        # print("name=%s,encoding=%s" % (name, encoding))
        # 将字符串转为numpy ndarray类型，即矩阵
        # 转换成一个list
        dlist = encoding_str.strip(' ').split(',')
        # 将list中str转换为float
        dfloat = list(map(float, dlist))
        face_encoding = numpy.array(dfloat)
        return face_encoding

    def add_Face(self, image_name, id):
        # 加载本地图像文件到一个numpy ndarray类型的对象上
        image = face_recognition.load_image_file("./photo/" + image_name)
        # 返回图像中每个面的128维人脸编码
        # 图像中可能存在多张人脸，取下标为0的人脸编码，表示识别出来的最清晰的人脸
        image_face_encoding = face_recognition.face_encodings(image)[0]
        encoding_str = self.encoding_FaceStr(image_face_encoding)
        print("存入数据库成功=================")
        # 将人脸特征编码存进数据库
        self.facesql.saveFaceData(id, encoding_str)

    def add_FaceCoding(self,image_name, id):
        image=face_recognition.load_image_file(image_name)
        image_face_encoding = face_recognition.face_encodings(image)[0]
        encoding_str = self.encoding_FaceStr(image_face_encoding)
        print("存入数据库成功=================")
        # 将人脸特征编码存进数据库
        self.facesql.saveFaceData(id, encoding_str)


    def updata_Face(self, image_name, id):
        # 加载本地图像文件到一个numpy ndarray类型的对象上
        image = face_recognition.load_image_file("./photo/" + image_name)
        # 返回图像中每个面的128维人脸编码
        # 图像中可能存在多张人脸，取下标为0的人脸编码，表示识别出来的最清晰的人脸
        image_face_encoding = face_recognition.face_encodings(image)[0]
        encoding_str = self.encoding_FaceStr(image_face_encoding)
        # 将人脸特征编码更新数据库
        self.facesql.updateFaceData(id, encoding_str)

    def sreach_Face(self, id):
        face_encoding_strs = self.facesql.sreachFaceData(id)
        # 人脸特征编码集合
        face_encodings = []
        # 人脸特征姓名集合
        face_names = []
        for row in face_encoding_strs:
            name = row[0]
            face_encoding_str = row[1]
            # 将从数据库获取出来的信息追加到集合中
            face_encodings.append(self.decoding_FaceStr(face_encoding_str))
            face_names.append(name)
        return face_names, face_encodings

    def load_faceOfDataBase(self):
        try:
            face_encoding_strs = self.facesql.allFaceData()
        except:
            print("数据库连接错误")
        # 人脸特征编码集合
        face_encodings = []
        # 人脸特征姓名集合
        face_names = []
        for row in face_encoding_strs:
            name = row[0]
            face_encoding_str = row[1]
            # 将从数据库获取出来的信息追加到集合中
            face_encodings.append(self.decoding_FaceStr(face_encoding_str))
            face_names.append(name)
        return face_names, face_encodings

