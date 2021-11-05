# Open CV4のインストールと概要(r2cv-ocv)
OpenCV4のインストールとその概要を説明します。

## 目次
[1. Open CV4について](#1)

[2. 画像処理](#2)

[3.USBカメラの設定](#3)

[<R2CVに戻る>](https://github.com/nishibra/r2cv-1)

<a id="1"></a>
## 1. Open CV4について
### OpenCVとは
OpenCVはオープンソースの画像処理や機械学習のソフトウェアーのライブラリーです。
以下のサイトをご参照ください。

>参考サイト:
https://opencv.org/

### インストールの手順
#### SwapFile
OpenCVをコンパイルするときに大量のメモリーを使いますので、メモリーが4Gbyte以下の場合はディスクをメモリーとして使うSwapfileをインストールします。
```
$ git clone https://github.com/JetsonHacksNano/installSwapfile
$ cd installSwapfile
$ ./installSwapfile.sh
```
#### opencv4のインストール
Open cv4.*の最新版をインストールします、
インストールスクリプトinstall-opencv.shをダウンロードして実行してください。
```
$ wget --no-check-certificate https://raw.githubusercontent.com/milq/milq/master/scripts/bash/install-opencv.sh
$ chmod +x install-opencv.sh
$ ./install-opencv.sh
```
コンパイルには数時間かかります。

>参考サイト: http://milq.github.io/install-opencv-ubuntu-debian

#### opencv-pythonのインストール
```
$ sudo apt install python3-pip
$ sudo pip install opencv-python
```
#### OpenCVの動作確認
USBカメラの接続
Raspi4にUSBカメラを接続します。
```
$ ls /dev/video*
```
でカメラの接続を確認できます。

#### カメラ画像読み込みプログラム
まず$ homeディレクトリーにgitHubのairrcフォルダーのコピー作成します。cam_sample.pyを実行します。
```
$ cd airrc
$ python3 cam_sample.py
```
と入力してください。画面にカメラの画像が表示されればPython3とOpenCVは動作しています。

#### Open CVのサンプルプログラム
以下のディレクトリーにPythonのサンプルプログラムがあります。画像処理に興味のある方はいろいろ使ってみましょう。
```
ubuntu@ubuntu:~/OpenCV/samples/python$
  ~/OpenCV/samples/python$ python3 qrcode.py
  ~/OpenCV/samples/python$ python3 video.py
  ~/OpenCV/samples/python$ python3 houghlines.py
  ~/OpenCV/samples/python$ python3 stereo_match.py
```

Deep learning関連
```
  ~/OpenCV/samples/dnn$
```

<a id="2"></a>
## 2. 画像処理
### 色認識
・色認識　HSVが人の感覚と合うので色認識においては使用されます。探す色のHSV値にフィルターをかけます。次のプログラムはHSVのHueを数値化するプログラムです。
USBカメラをセットし、プログラムのあるディレクトリーにて以下を実行してください。
```
$ cd airrc
$ python3 hsv_color_set.py
```
![019](/pics-ocv/image019.png)

画面にカメラ画像とHue Barが表示されます。緑の線の上をタッチするとHueの下限値、緑線の下をタッチすると上限をセットできます。
その結果がカメラ画像に表示されます。ここで設定したHueの上下限を使えば色認識ができます。

### ステレオカメラ
ステレオカメラを使うと2つのカメラの視差から距離を求めることができます。
視差を求めるにはステレオ画像マッチング手法を使います。
マッチング手法にはSGM（Semi Global Matching）方式、SAD（Sum of Absolute Difference）方式などがありますが、変化のないところではマッチングできないため、赤外線や可視光でパターン照射を行っているものがあります。

![020](/pics-ocv/image020.png)

ここでは注目点を探してその点に対して視差から距離を求めます。
サンプルプログラムでは注目点として赤色を認識してその距離を求めます。
```
$ cd airrc
$ python3 color_stereo.py
```
![021](/pics-ocv/image021.png)

このプログラムでは赤色のものまでの座標と距離を計算します。

<a id="3"></a>
## 3.USBカメラの設定
### v4l2-ctl
OpenCVからWebカメラを設定する方法としてv4l2-ctlを使う方法があります。
>参考サイト: [v4l2-ctlで行うUSBカメラ設定方法まとめ](https://dev.classmethod.jp/articles/opencv-webcam-setting/)
```
$ sudo apt install v4l-utils
$ v4l2-ctl --list-formats-ext
```
### OpenCVでのカメラの設定
```c = cv2.VideoCapture (-1)
c.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M','J','P','G'))
c.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('Y','U','Y','V'))
c.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
c.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
c.set(cv2.CAP_PROP_FPS, 15)
c.set(cv.CAP_PROP_BUFFERSIZE,1)
```
### <カメラ関連参考資料>

> [サイズ変更・回転・切り抜き](https://axa.biopapyrus.jp/ia/opencv/image-crop.html)
>
> [Basics of OpenCV (Resizing, Cropping, Rotation, and some other image Attributes)](https://www.codespeedy.com/basics-of-opencv-resizing-cropping-rotation/)
>
> [YUY2とYUYVについて](https://www.argocorp.com/UVC_camera/Linux_YUY2_YUYV.html)
> 
> [TISカメラをPythonで動作させる方法](https://www.argocorp.com/UVC_camera/Linux_TIScam_Python.html)
>
> [LinuxでUVC(USB Video Class)タイプのUSBカメラを使う](https://qiita.com/nonbiri15/items/9593d61a2be81f2b31a9)
>
> [Raspberry Piに接続されているwebカメラの情報をv4l2-ctlで簡単に取得したい](https://qiita.com/nonbiri15/items/9593d61a2be81f2b31a9)
>
