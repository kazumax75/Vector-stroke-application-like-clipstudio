# Vector stroke application like clipstudio

マウスやペンタブレット入力によるストロークを編集できるアプリです。
This application allows you to edit strokes made by mouse or pen tablet input.

## Overview

マウスやペンタブレットで入力されたトラックポイントをDouglas−Peuckerアルゴリズムで間引き、残った点をキーポイントとしたCatmull–Rom Spline曲線でストローク描画しています。
キーポイント上で右ドラッグすることでストロークを編集できます。
別ウィンドウのトラックバーで線の色や太さを変更できます。

# Demo
https://www.youtube.com/watch?v=ephADfQnPC4


## Requirement
- Python 3.8.5
- opencv
- numpy


## Usage
pip install opencv-python
pip install numpy
python main.py

## Reference
http://wakaba-technica.sakura.ne.jp/library/interpolation_catmullrom_spline.html


## Author
Kazuma Kikuya
[FB](https://www.facebook.com/profile.php?id=100030409253259)
[qiita](https://qiita.com/Kazuma_Kikuya)

## Licence
MIT


