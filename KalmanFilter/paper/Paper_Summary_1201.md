1. A Single Microphone Kalman Filter-Based Noise Canceller
'''
KF를 활용하여 
   (1) speech model에서 parameter를 추정하고 
   (2) KF를 통해 signal을 추출하는 과정인데, 
parameter를 추정하지 않는 방식을 제안한다
'''

2. Application of Kalman filter to noise reduction in multichannel data
'''
KF multichannel을 적용/Magnetotelluric method를 사용하여 noise 줄이기를 시도한다(2D나 3D data에서 장점이 드러나는 방식). 
또한 다른 데이터 녹음 방식(Multichannel magnetotelluric data recorded in multi-site experiment)에 대해서도 소개.
'''

3. Image noise smoothing using a modified Kalman filter
'''
Markov random field에 기반을 둔 이미지 모델에 대해 KF(smoother)와 multi-innovation KF를 동시에 적용한 것에 대해 소개함.
'''

4. Kalman Filter in Speech Enhancement
'''
parameter 추정을 위한 새 알고리즘을 제안한다. 
다른 종류들의 노이즈로 테스트를 진행함.
 * Ch1. 모델 설명, KF가 적용된 부분 설명
 * Ch2. filter 튜닝, KF parameter 최적값 결정을 위한 알고리즘 소개
 * Ch3. AR model 순서 결정을 위한 알고리즘 제안
 * Ch4. NOIZEUS(noizy speech corpus)로 질적/양적 테스트
 * Ch5. 결론 및 추후 작업 기술
'''
 
5. Kalman Filter-Based Single Microphone Noise Canceller
'''
AR model에서 KF를 적용하는 것은 효율적이다. 
KF 적용 시 parameter 추정을 하지 않는 방법을 제안.
'''

6. Noise Reduction in Speech Signals Using Discrete-time Kalman Filters Combined with Wavelet Transforms
'''
Discrete-time KF + Wavelet transforms Combination method. 
Wavelet transforms는 스펙트럼 왜곡을 최소화한다. 
KF가 나은지, KF+Wt가 나은지 비교하는 내용.
'''

7. Noise Reduction using Kalman Filter
'''
노이즈를 제거하는 것이 중요하다. 
additive noise를 제거하기 위해 MSE를 최소화하는 KF를 적용한다.
'''
