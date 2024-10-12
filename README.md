# 思路
1. 通过USB调试和ADB获取手机截图
2. 截取目标区域
3. OCR识别出两个数字，并得到比较结果
4. ADB绘制大于/小于号
5. 获取下一题截图，重复1

# 使用方法：
1. 安装ADB安卓调试工具,链接：[ADB下载](https://dl.google.com/android/repository/platform-tools-latest-windows.zip?hl=zh-cn)，解压到某个空文件夹里即可（我的是K:\adb\platform-tools\adb.exe）。
2. 安装tesseract-OCR识别工具，链接：[tesseract](https://github.com/UB-Mannheim/tesseract/releases/download/v5.4.0.20240606/tesseract-ocr-w64-setup-5.4.0.20240606.exe)，[官网下载介绍地址](https://github.com/UB-Mannheim/tesseract/wiki)（记住安装路径，我的是K:\Tesseract-OCR\tesseract.exe）。
3. 开启手机开发者选项，并开启USB调试。
4. 手机USB连接到电脑上
5. 启动小猿口算pk界面，然后运行上述python程序即可。（不同机型窗口位置不一样，需要自己微调一下，有问题可以网上搜一下怎么查看手机屏幕位置）
6. python的依赖主要是opencv-python和adb，也可以无脑:`pip install opencv-python pytesseract keyboard numpy'
7. 本人还做了多位数乘法选项，但是效果一般，能者也可以来优化一下。
