# Signal Receiver

The receiver module uses 10-bit Analog-to-Digital (ADC) circuit to sample received radio signal from RF module and SYNC signal from  modulator. Both analog signals are expected to be bound between 0 and 5 V. The module transmits sampled signals through Serial with 115200 baudrate. A sample is formatted by following,

```
binary form of data:
        each last 5 bits: half of a sample
        each first 3 bits: character bits to show first byte and sync
        A: sync
        BBBBB: first 5 bits of a sample
        CCCCC: last 5 bits of a sample

    0b00ABBBBB      0b110CCCCC
  [ First byte ]  [ Second byte ]
```
where, A represents SYNC signal and is either 0 (0 V) or 1 (5 V), BBBBB are the first 5 bits of a sample of 10-bit radio signal, and CCCCC are the last 5 bits of the sample in the first byte. The first two zeros in the first byte and the first two ones in the second byte can be used to distinguish the two bytes to convert samples correctly.

## Binary file description

20181009_100023_binary.txt: w/ a person (15\~28, 28\~36, 151\~162, 164\~174, 237\~253, 257\~270)<br>
20181009_101055_binary.txt: w/ a person *(38\~70, 84\~110)*<br>
20181009_101420_binary.txt: w/ a person *(18\~36, 53\~69)*<br>
20181009_101635_binary.txt: w/ a person, w/ an iron plate *(20\~52, 62\~83)*<br>
20181009_102248_binary.txt: w/ a car *(42~58)*<br>
20181009_102508_binary.txt: w/ a car *(28\~36, 57\~59)*<br>
20181009_102849_binary.txt: w/ a car *(25\~32, 51\~57)*<br>
20181009_103752_binary.txt: w/ a person, w/ an iron plate *(19\~69, 69\~107)*<br>
20181009_104216_binary.txt: w/ a person, w/ an iron plate *(8\~47, 58\~92)*<br>
20181009_104446_binary.txt: w/ a person, w/ an iron plate (first), w/o the iron plate (second) *(10\~31, 41\~57, 59\~76, 85\~98)*<br>
20181009_105554_binary.txt: w/ a person *(21\~26, 26\~30, 38\~65, 65\~92)*<br>
20181009_110458_binary.txt: w/ a drone (DJI Phantom), w/o reflection tape *(1\~9, 36\~47, 62\~87, 106\~115)*<br>
20181009_110901_binary.txt: w/ a drone (DJI Phantom), w/o reflection tape *(5\~16, 36\~43, 46\~49, 68\~76)*<br>
20181009_111450_binary.txt: w/ a drone (DJI Phantom), w/ reflection tape *(15\~22, 44\~49)*<br>
20181009_111734_binary.txt: w/ a drone (DJI Phantom), w/ reflection tape *(27\~37, 42\~50, 71\~80, 100\~110)*<br>
20181016_134334_binary.txt: background noise, a person at 5 sec *(36~41)*<br>
20181016_134532_binary.txt: w/ a car *(39\~58, 84\~103, 138\~147, 166\~174)*<br>
20181016_135124_binary.txt: w/ a person *(6\~30, 38\~62, 64\~80, 85\~98)*<br>
20181016_142025_binary.txt: from 35 second, w/ a drone (DJI Phantom), w/ reflection tape *(11\~16, 16\~21, 39\~52, 68\~74, 78\~84)*<br>
20181016_142531_binary.txt: w/ a drone (DJI Phantom), w/o reflection tape *(22\~27, 80\~84)*<br>


20181114_135427_binary.txt: w/ a person ~30m*<br>
20181114_140400_binary.txt: w/ a car ~40m ~5mi/h *(0\~16, 40\~57, 71\~86, 117\~135, 159\~182, 196\~218, 321\~341, 373\~381)*<br>
20181114_141258_binary.txt: w/ a car ~40m ~10mi/h *(0\~13, 31\~41, 70\~81, 99\~107, 127\~141, 157\~169, 192\~201, 219\~231, 255\~268, 284\~294)*<br>
20181114_142450_binary.txt: w/ a drone ~30m *(18\~23, 44\~46, 65\~70, 86\~96, 128\~136, 159\~165, 234\~236)*<br>

20181114_175502_binary.txt: w/ a person ~30m *(13\~38, 78\~98, 123\~142, 166\~170, 188\~197, 227\~231, 233\~244, 304\~322)*<br>
20181114_180324_binary.txt: w/ a car ~40m *(8\~15, 46\~60, 82\~97, 123\~129, 156\~173, 201\~224)*<br>
20181114_181316_binary.txt: w/ a drone ~15m*<br>


## To read the files

Use read_data.py

## Class labels

    0 - others
    1 - person
    2 - car
    3 - uav

    ex) 20181009_3_100023.wav is a UAV

## Tags

    ps - pitch shifted
    ts - time stretched
    ns - noise added
