import os
import pytesseract
import cv2
import numpy as np
import time
import subprocess
import keyboard
import sys

ADB_PATH = r'K:\adb\platform-tools\adb.exe'  # 确保ADB路径已设置

# 配置Tesseract OCR的路径
pytesseract.pytesseract.tesseract_cmd = r'K:\Tesseract-OCR\tesseract.exe'

not_found_count = 0
last_not_found_time = 0


def take_screenshot():
    """
    截取屏幕并直接传输到内存
    """
    start_time = time.time()
    try:
        # 使用更高效的方式获取截图数据
        proc = subprocess.Popen([ADB_PATH, "exec-out", "screencap", "-p"], stdout=subprocess.PIPE)
        result = proc.stdout.read()
        proc.terminate()
        
        # 处理字节数据，避免编码问题
        if result[0:4] == b'\x89PNG':
            image = np.frombuffer(result, np.uint8)
            image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        else:
            raise ValueError("Screenshot data is not in expected format.")
    except Exception as e:
        print(f"Error decoding screenshot: {e}")
        return None
    end_time = time.time()
    print(f"Screenshot time: {end_time - start_time:.4f} seconds")
    return image


def recognize_numbers_chengfa(image):
    """
    使用OCR识别题目
    """
    start_time = time.time()
    # 裁剪出第一个数字的区域
    first_number_area = image[600:700, 200:365]
    # 裁剪出第二个数字的区域
    second_number_area = image[600:700, 410:560]

    first_number_area_gray = cv2.cvtColor(first_number_area, cv2.COLOR_BGR2GRAY)
    second_number_area_gray = cv2.cvtColor(second_number_area, cv2.COLOR_BGR2GRAY)

    # 显示裁剪出的数字区域
    # show_image(first_number_area, "First Number Area")
    # show_image(second_number_area, "Second Number Area")

    # 二值化
    _, thresh1 = cv2.threshold(first_number_area_gray, 150, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    _, thresh2 = cv2.threshold(second_number_area_gray, 150, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    
    text1 = pytesseract.image_to_string(thresh1, config='--psm 6 --oem 3 -c tessedit_char_whitelist=0123456789')  # 使用更精确的模式
    text2 = pytesseract.image_to_string(thresh2, config='--psm 6 --oem 3 -c tessedit_char_whitelist=0123456789')

    # 去除空格和换行符
    text1 = text1.replace(' ', '').replace('\n', '')
    text2 = text2.replace(' ', '').replace('\n', '')

    print(f"OCR识别结果: {text1, text2}")
    try:
        numbers = [int(text1), int(text2)]
    except ValueError:
        print("OCR识别结果非数字")
        numbers = []
    end_time = time.time()
    print(f"OCR耗时: {end_time - start_time:.4f}s")
    return numbers


def recognize_numbers(image):
    """
    使用OCR识别题目
    """
    start_time = time.time()
    # 裁剪出第一个数字的区域
    first_number_area = image[600:700, 300:460]
    # 裁剪出第二个数字的区域
    second_number_area = image[600:700, 620:780]

    first_number_area_gray = cv2.cvtColor(first_number_area, cv2.COLOR_BGR2GRAY)
    second_number_area_gray = cv2.cvtColor(second_number_area, cv2.COLOR_BGR2GRAY)

    # 显示裁剪出的数字区域
    # show_image(first_number_area, "First Number Area")
    # show_image(second_number_area, "Second Number Area")

    # 二值化
    _, thresh1 = cv2.threshold(first_number_area_gray, 150, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    _, thresh2 = cv2.threshold(second_number_area_gray, 150, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    
    text1 = pytesseract.image_to_string(thresh1, config='--psm 6 --oem 3 -c tessedit_char_whitelist=0123456789')  # 使用更精确的模式
    text2 = pytesseract.image_to_string(thresh2, config='--psm 6 --oem 3 -c tessedit_char_whitelist=0123456789')

    # 去除空格和换行符
    text1 = text1.replace(' ', '').replace('\n', '')
    text2 = text2.replace(' ', '').replace('\n', '')

    print(f"OCR识别结果: {text1, text2}")
    try:
        numbers = [int(text1), int(text2)]
    except ValueError:
        print("OCR识别结果非数字")
        numbers = []
    end_time = time.time()
    print(f"OCR耗时: {end_time - start_time:.4f}s")
    return numbers


def show_image(image, window_name="Image"):
    """
    显示截图以便调试
    """
    if image is not None:
        cv2.imshow(window_name, image)
        print(image.shape)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


def calculate_comparison(numbers):
    """
    计算答案 (比较两个数字，输出大于或小于)
    """

    if len(numbers) < 2:
        current_time = time.time()
        print("未找到足够的数字进行比较")
        return None

    first, second = numbers[0], numbers[1]
    if first > second:
        answer = '>'
        print(f"计算出的答案: {first} > {second}")
    elif first < second:
        answer = '<'
        print(f"计算出的答案: {first} < {second}")
    else:
        answer = '='  # 如果需要处理相等情况
        print(f"计算出的答案: {first} = {second}")

    return answer


def calculate_chengfa(numbers):
    """
    计算答案 (两位乘法)
    """

    if len(numbers) < 2:
        current_time = time.time()
        print("未找到足够的数字")
        return None
        
    first, second = numbers[0], numbers[1]
    answer = first * second
    print(f"计算出的答案: {first} x {second} = {answer}")

    return answer


def draw_answer_on_phone(answer):
    """
    在手机屏幕上手绘答案
    """
    # 将答案转换为字符串并逐个数字绘制
    answer_str = str(answer)
    coordinates = {
        '0': [(100, 100), (200, 100), (200, 400), (100, 400), (100, 100)],
        '1': [(150, 100), (150, 400)],
        '2': [(100, 100), (200, 100), (100, 400), (200, 400)],
        '3': [(100, 100), (200, 100), (100, 200), (200, 300), (100, 400)],
        '4': [(150, 100), (100, 250), (200, 250), (150, 200), (150, 400)],
        '5': [(200, 100), (100, 100), (100, 250), (200, 250), (200, 400), (100, 400)],
        '6': [(100, 100), (100, 400), (200, 400), (200, 250), (100, 250)],
        '7': [(100, 100), (200, 100), (200, 400)],
        '8': [(100, 100), (200, 100), (100, 400), (200, 400), (100, 100)],
        '9': [(200, 250), (100, 250), (100, 100), (200, 100), (200, 400)]
    }

    start_x, start_y = 50, 1200  # 设置起始位置
    step_x = 0  # 设置步长
    for digit in answer_str:
        if digit in coordinates:
            path = coordinates[digit]
            for i in range(len(path) - 1):
                x1, y1 = path[i][0]+start_x+step_x, path[i][1] + start_y
                x2, y2 = path[i+1][0]+start_x+step_x, path[i+1][1] + start_y
                print(f"绘制线条 {digit}，坐标 ({x1}, {y1}) -> ({x2}, {y2})")
                subprocess.run([ADB_PATH, "shell", "input", "swipe", str(x1), str(y1), str(x2), str(y2), "100"])
            step_x += 150  # 数字之间增加步长


def simulate_handwriting(symbol):
    """
    模拟手写输入大于号或小于号
    """
    paths = {
        '>': [(600, 1400), (800, 1600), (600, 1800)],
        '<': [(800, 1400), (600, 1600), (800, 1800)]
    }
    if symbol not in paths:
        print(f"未定义{symbol}的手写路径")
        return

    path = paths[symbol]
    for i in range(len(path) - 1):
        x1, y1 = path[i]
        x2, y2 = path[i + 1]
        print(f"模拟手写{symbol}，坐标({x1}, {y1}) -> ({x2}, {y2})")
        subprocess.run([ADB_PATH, "shell", "input", "swipe", str(x1), str(y1), str(x2), str(y2), "100"])


def input_answer(answer):
    """
    输入比较符号答案
    """
    if answer in ['>', '<']:
        simulate_handwriting(answer)
    else:
        draw_answer_on_phone(answer)


def wait_for_next_question(prev_image):
    """
    等待下一题出现
    """
    start_time = time.time()
    while True:
        new_image = take_screenshot()
        if new_image is None:
            continue
        difference = cv2.absdiff(prev_image, new_image)
        diff_score = np.sum(difference)

        # 如果差异值超过一定阈值，说明题目更新了
        if diff_score > 5000:  # 根据实际情况调整阈值
            print("检测到新题目")
            
            end_time = time.time()
            print(f"等待新题目耗时: {end_time - start_time:.4f}s")
            return new_image

        time.sleep(0.01)

def main():
    """
    主函数，整合所有步骤
    """
    keyboard.add_hotkey('=', lambda: sys.exit("进程已结束"))  # 默认退出快捷键是“=”
    print("开始口算PK自动作答")
    try:
        model = input("请输入口算题型：1. 比校大小\n2. 两位乘法\n")
        if model == '1':
            while True:
                # 获取当前题目并识别
                full_image = take_screenshot()
                if full_image is None:
                    print("截图失败，请检查ADB路径是否正确")
                    continue
                # show_image(full_image, "Full Screenshot")  # 调试时显示截图
                numbers = recognize_numbers(full_image)
                answer = calculate_comparison(numbers)

                if answer is not None:
                    input_answer(answer)  # 输入答案
                    # full_image = wait_for_next_question(full_image)  # 等待下一题出现
                    time.sleep(0.3)
        elif model == '2':
            while True:
                # 获取当前题目并识别
                full_image = take_screenshot()
                if full_image is None:
                    print("截图失败，请检查ADB路径是否正确")
                    continue
                # show_image(full_image, "Full Screenshot")  # 调试时显示截图
                numbers = recognize_numbers_chengfa(full_image)
                answer = calculate_chengfa(numbers)

                if answer is not None:
                    input_answer(answer)  # 输入答案
                    # full_image = wait_for_next_question(full_image)  # 等待下一题出现
                    time.sleep(0.3)
    except SystemExit as e:
        print(e)


if __name__ == "__main__":
    main()