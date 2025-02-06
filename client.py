
#preprocessing : data download를 위해 통신 서버에 해당 데이터 로드 요청
##전체 데이터의 수
##프레임 데이터 구조
# 이미지 id(int), 이미지의 자세(float, 12 or 6)
# contour point 수(int),contour vector(float, N*2)
# rect(float,x,y,width,height)

nFrames = 100 #데이터를 받아오면 교체
ids = range(1,100) #추후 수정

#맵 생성 방식
#1) 점진적 : 프레임 정보를 한번씩 보내면 갱신
#2) 전체 데이터를 전송하면 한번에 생성

#request object map generation
for id in ids:
    #id로 이미지 다운로드
    #이미지, contour, rect 정보 전송
    print(id)
    
#결과 다운로드