# real_time_recognize mac上的实时人脸识别程序

使用步骤：
1. 通过两种方法创建人脸数据库举例如下：
+ `python face_db.py --name='baby' --image='/Users/heliang/baby.jpg'` # 通过指定单人脸图片文件创建
+ `python face_db.py --name='owner'` # 通过摄像头捕捉人脸实现，感觉光照合适后就可以按空格/回车确认照片
> 创建的人脸数据库默认保存在 家目录/Pictures/head/ 下，也可以使用 --dir 参数指定到其他目录，可以前往查看保存的文件信息。主要是 .jpg 和 .npy 两种。

2. 运行如下命令即可通过摄像头实时识别人脸：
+ `python run_recognize.py` 同样可以使用 --dir 参数指定人脸数据库目录，默认同上。

3. 运行如下命令可以通过摄像头获取图像并在人脸上增加烟头和🕶️装屌。
+ `python decorate_face.py` 实现在摄像头人像上增加烟头和墨镜。

效果如下：
![./demo.gif](demo.gif)

# TODO
[*] 增加其它人脸实时操作逻辑，例如装饰等。当前增加了[烟头和墨镜](https://github.com/tomoncle/face-detection-induction-course)，后续可以考虑增加更多。
[ ] 增加异常情况处理：保存数据库时没有人脸图像报错...
[ ] 摄像头创建人脸数据库时也框选出选定的第一个人脸，实现更好的用户交互
[ ] 尝试用这个程序控制MAC人脸解锁，免去输入密码



ref: https://github.com/ageitgey/face_recognition
