import os
import random


def get_post_img(filedir=os.path.abspath(os.path.dirname(__file__))):
    basedir = os.path.abspath(os.path.join(filedir, os.pardir))
    imgdir = "/static/images/post_img/"
    images = [img for img in os.listdir(basedir + imgdir)]

    # random image URI:
    random_img = random.choice(images)

    return "{}{}".format(str(imgdir), random_img)

