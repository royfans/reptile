# coding=utf-8

# History: 2018/3/21
# Discrible: stitching video script
# Auto : RoyFans

import os

def stitching_video(filelist, output):
    os.system("ffmpeg -f concat -safe 0 -i " + filelist +" -c copy " + output)

if __name__ == '__main__':
    stitching_video('filelist1.txt', "D:/第一集.mp4")
