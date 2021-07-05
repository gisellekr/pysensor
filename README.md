# pysensor
Python Sensor

실행 파일로 만들기

pyinstaller -w -F main.py

(pyinstaller가 없다면 >> pip install pyinstaller 로 설치)


dist 폴더에 main.exe가 생김

dist 폴더에 configdata.conf 파일을 복사

dist 폴더 파일을 복사해서 사용하면 됨.



동네예보 조회 OPEN API가 2.0으로 버전업 되면서,

전달되는 Data가 조금 변경됨.

변경된 내용(URL, Data Parsing) 적용.
