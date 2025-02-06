import threading
import ujson
import time
import numpy as np
import requests
import cv2
from socket import *
import argparse
import os

import torch

#처리 시간 등 기록용
import csv
import os.path
import keyboard
keyboard.add_hotkey("ctrl+s",lambda: savecsv())

num_device = 1
strmodel = "temp"
path_sv = "./evaluation/"+strmodel+"_"+str(num_device)+".csv"
if(not os.path.exists(path_sv)):
    with open(path_sv, 'w', newline='') as csvfile:
        wr = csv.writer(csvfile)
        wr.writerow(["processing","download","upload"])
        csvfile.close()

f = open(path_sv, 'a', newline='')
wr = csv.writer(f)
csvdatas=[]

def savecsv():
    if len(csvdatas)==0:
        return
    with open(path_sv, 'a', newline='') as csvfile:
        wr = csv.writer(csvfile)
        wr.writerows(csvdatas)

        n = len(csvdatas)

        csvfile.close()
        csvdatas.clear()
        print("save csv", n, len(csvdatas))
# 처리 시간 등 기록용

#데이터 처리 부분 : 구현되어야 하는 부분
def predict(message):

    return

#데이터 처리 쓰레드
bufferSize = 1024
def udpthread():

    while True:
        bytesAddressPair = ECHO_SOCKET.recvfrom(bufferSize)
        message = bytesAddressPair[0]
        predict(message)

if __name__ == '__main__':
    ##################################################
    ##arguments parsing
    parser = argparse.ArgumentParser(
        description='Object Map Generation Server',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    ##클라이언트에서 생성한 데이터의 알림을 받는 키워드
    ##클라이언트와 키워드 일치 필요
    ##','으로 연결하여 다중 키워드 등록
    ##ex)'image,segmentation'
    parser.add_argument(
        '--RKeywords', type=str,default='xxxx',
        help='Received keyword lists')
    ##서버에서 생성한 데이터를 등록하는 키워드
    ##유니크 키워드 생성 필요
    ##다른 서버 또는 기기에서 해당 데이터 이용 가능
    parser.add_argument(
        '--SKeywords', type=str,default='xxxx',
        help='Sendeded keyword lists')
    ##전송받는 데이터의 타입 설정.
    parser.add_argument(
        '--DataType', type=str, default='Image',
        help='Data type')
    ##서버 아이피.
    ##추후 서버 아이피와 포트가 변경되면 수정
    parser.add_argument(
        '--FACADE_SERVER_ADDR', type=str, default='http://143.248.6.25:35005',
        help='facade server address')
    parser.add_argument(
        '--ECHO_SERVER_IP', type=str, default='143.248.6.25',
        help='ip address')
    parser.add_argument(
        '--ECHO_SERVER_PORT', type=int, default=35001,
        help='port number')
    opt = parser.parse_args()
    ##arguments parsing

    ###CONNECT
    Data = {}

    capacity = 0
    ##Echo server

    ##통신 서버와 주고받을 키워드 등록 과정
    FACADE_SERVER_ADDR = opt.FACADE_SERVER_ADDR
    ReceivedKeywords = opt.RKeywords.split(',')
    SendKeywords = opt.SKeywords
    datatype = opt.DataType

    sess = requests.Session()
    strServerName = 'ObjectGaussianSplattingServer'
    sess.post(FACADE_SERVER_ADDR + "/Connect", ujson.dumps({
        # 'port':opt.port,'key': keyword, 'prior':opt.prior, 'ratio':opt.ratio
        'src': strServerName, 'type1': 'server', 'type2': 'test', 'keyword': SendKeywords, 'capacity':capacity, 'Additional': None
    }))
    ECHO_SERVER_ADDR = (opt.ECHO_SERVER_IP, opt.ECHO_SERVER_PORT)
    ECHO_SOCKET = socket(AF_INET, SOCK_DGRAM)
    for keyword in ReceivedKeywords:
        temp = ujson.dumps({'type1': 'connect', 'keyword': keyword, 'src': strServerName, 'type2': 'all'})
        ECHO_SOCKET.sendto(temp.encode(), ECHO_SERVER_ADDR)
        Data[keyword] = {}
    # Echo server connect
    ######################

    ####LOAD MODEL
    ##구현한 모델 로드
    device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
    print("Load model")

    ##서버 쓰레드 실행
    th1 = threading.Thread(target=udpthread)
    th1.start()
    print("thread start")