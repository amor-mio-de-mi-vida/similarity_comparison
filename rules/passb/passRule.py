from src.rules.dig import armDetect, armTorsoAngle, legDetect
from src.rules.dig.ball_position import ball_position
from src.utils.logger import Log
from src.utils.util import arm_dis_ball, draw_messages

from src.utils import util
from copy import deepcopy
import cv2


def sum_rules(images, candidates, persons, balls):
    # 需要每张图片遍历的规则
    # all_mes = []
    mes = set()
    marks = []
    cnt = 0
    if len(images) == 1:  # 是图片
        if candidates[0] is None or persons[0] is None:
            mes.add("人体未被识别")
            return list(mes), marks
        else:
            try:
                if armDetect.detect_arm_status(images[0], candidates[0], persons[0]):
                    mes.add("手臂伸太直")
                if balls[0] is None:
                    mes.add("球未被识别")

            except Exception as e:
                mes.add("可能存在关键点识别不全的问题")
            return list(mes), marks
        # if not armTorsoAngle.detect(images[0], candidates[0], persons[0]):
        #     mes.add("手臂与躯干最大角度不应超过110°")
        # if not ball_position(images[0], candidates[0], persons[0], balls[0]):
        #     mes.add("击球时球离手腕位置太远")
        # if not armDetect.detect_arm_status(images[0], candidates[0], persons[0]):
        #     mes.add("手臂没有伸直")
        # all_mes.append(deepcopy(mes))
    else:  # 是视频
        # cnt = 0  # 记录球未被识别的次数
        for i in range(len(images)):
            marks.append(0)
            if candidates[i] is None or persons[i] is None:
                continue


            try:
                if balls[i] is not None:
                    if arm_dis_ball(candidates[i], persons[i], balls[i]) < 2:
                        if armDetect.detect_arm_status(images[i], candidates[i], persons[i]):
                            marks[i] = 1
                            mes.add("手臂伸太直")
                else:
                    cnt += 1
                    Log.error("球未被识别")
                    if armDetect.digWithoutBall(images[i], candidates[i], persons[i]):
                        if armDetect.detect_arm_status(images[i], candidates[i], persons[i]):
                            marks[i] = 1
                            mes.add("手臂伸太直")
            except Exception as e:
                Log.debug("可能存在关键点识别不全的问题")
            # 需要整体判断的规则
            # mes2 = set()
            # if not legDetect.detect(images, candidates, persons):
            # mes2.add("腿部动作有误")//先不考虑腿
            # if len(mes2) > 0:
            #     mes.add("腿部动作有误")
            #     for i in range(len(images)):
            #         image = images[i]
            #         image2 = draw_messages(image, mes2)
            #         images[i] = image2

            if len(mes) > 0:
                image = images[i]
                image2 = draw_messages(image, mes)
                image2 = util.draw_bodypose(image2, candidates[i], [persons[i]])
                images[i] = image2
            print(mes)
            # all_mes.append(deepcopy(mes))
            # mes.clear()
        if cnt >= (len(images) * 2) // 3:  # 容错
            mes.add("球未被识别")
            # all_mes.append(deepcopy(mes))
    return list(mes), marks
