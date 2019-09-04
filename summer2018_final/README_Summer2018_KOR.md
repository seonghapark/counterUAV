# Counter UAV - Summer 2018


## Folders
RealTime �������� �ǽð����� ���� ������ �Ǵ� txt ���� �����͸� ó���ϴ� �ڵ���� �ְ�,
WaveFile �������� range_test2.wav �����͸� ó���ϴ� �ڵ尡 �ֽ��ϴ�.
�ڵ�� �̸��� �ٲ�µ� ������ ó�� ������ ��ȣ�� �Űܼ� �̸��� �ٲ���ϴ�.


## 1. Read Data
RealTime���� txt ������ 11025����Ʈ ����(1��)�� �Ľ��Ѵ�. 


## 2. FFT


## 3. Threshold
FFT���� �޾ƿ� ������(50,1764) �� Threshold(�Ӱ谪)�� �������� �����͸� ������ �� Ư�� �ð��� ����� ������(1���� �迭)�� �����Ѵ�.
RealTime������ Amplitude�� -4�̻����� �Ͽ����ϴ�.
WaveFile������ Amplitude�� -12�̻�, Distance�� 24�̻����� �Ͽ���.


## 4. Filtering
### Kalman Filter (2)
http://www0.cs.ucl.ac.uk/staff/gridgway/kalman/kalman_example/Kalman_Example.html

### Extended Filter

### Particle Filter (4)
https://github.com/vinaykumarhs2020/lane_detection

## 5. Drawing
Threshold(1), Kalman Filter(2), Particle Filter(4)�� ����� ������ ��Ÿ������.
���� �ڵ��� pcolormesh�� scatter�� �ٲپ���.
WaveFile�� ���� full�̶�� �̸��� �� ������ �ִµ� �� ������ ��ǲ ������ ��ü�� �׸� �� �Դϴ�.