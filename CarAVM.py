import cv2


class Prediction:
    def __init__(self):
        '初始化参数'
        return

    def rotatePic(self, image, angle, center=None, scale=1.0):
        '''
        用于旋转图片的工具函数，旋转后图片大小不变，旋转之后无信息的部分填补为黑色
        :param image: 目标图像
        :param angle: 旋转角度，负数为顺时针，正数为逆时针
        :param center: 旋转中心，默认为图片的中央
        :param scale: 缩放参数
        :return: 旋转结果图片
        '''
        (h, w) = image.shape[:2]
        if center is None:
            center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, scale)
        rotated = cv2.warpAffine(image, M, (w, h))
        return rotated

    def pastePic(self, background, target, x=0, y=0):
        '''
        将图片黑色部分视为透明，拼贴两张图片，target图片在上
        :param background: 目标背景图
        :param target: 目标图片
        :param x: 粘贴的左上角x坐标位置
        :param y: 粘贴的右上角x坐标位置
        :return: 直接将结果写在background中进行返回
        '''
        target_h, target_w = target.shape[:2]
        '要处理的区域'
        roi = background[y:y+target_h, x:x+target_w]
        '获取mask'
        gray_target = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)
        ret, mask = cv2.threshold(gray_target, 10, 255, cv2.THRESH_BINARY)
        mask_inv = cv2.bitwise_not(mask)

        roi_res = cv2.bitwise_and(roi, roi, mask=mask_inv)
        target_res = cv2.bitwise_and(target, target, mask=mask)
        res = cv2.add(roi_res, target_res)

        background[y:y+target_h, x:x+target_w] = res


    def getNext(self):
        '获取下一帧及相关信息的函数'
        return

    def predict(self):
        '预测下一帧的内容'
        return

def showAndWait(image, name=None):
    cv2.imshow(name, image)
    cv2.waitKey(0)

if __name__ == '__main__':
    pred = Prediction()
    image = cv2.imread('./img.png')
    res = pred.rotatePic(image, -50)
    showAndWait(image, name='background')
    showAndWait(res, name='target')
    pred.pastePic(image, res)
