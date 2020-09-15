# remote-switch

[Death Squared](https://ec.nintendo.com/JP/ja/titles/70010000002104) 
みたいなローカルしか対応してないSwitchのマルチプレイゲームをオンラインからプレイできるようにするシステム

## 動作原理

```
コントローラー --> PC/スマホ --> インターネット --> joycontrolマシーン --> Bluetooth --> Switch 
```

※ このシステムはコントローラ入力のみなので、映像のシェアはLine LiveやZoomなどで要対応<br>
※ オンライン側はスマホ一台だけだと画面が見れない

## 準備するもの

* joycontrolをインストールできるマシーン
  * Raspberry Pi
  * Ubuntu 
  * Ubuntu On VirtualBox  https://qiita.com/almtr/items/38a7f0c3056024532e8d
  * etc...
* Bluetoothアダプタ(内臓でもOK) 
* ゲーム　ライブ配信環境
  * HDMIキャプチャ
  * 配信用PC
  * 高速インターネット回線

## セットアップ手順

1. (デバイスに無ければ) Bluetoothアダプタ接続
    * `hciconfig` コマンドで `hci0` が出てくればOK
1. [joycontrol](https://github.com/mart1nro/joycontrol) インストール
    * [Raspberry Pi 最新化](https://search.yahoo.co.jp/search?p=raspberry+pi+%E3%82%BB%E3%83%83%E3%83%88%E3%82%A2%E3%83%83%E3%83%97)
1. インターネットからアクセスできるよう5000番ポートを開放
1. [ライブ配信環境設定](https://search.yahoo.co.jp/search?p=Switch+%E3%83%A9%E3%82%A4%E3%83%96%E9%85%8D%E4%BF%A1)
1. このレポジトリをclone

## 接続手順

### ローカル側

1. コントローラーコードを決めて、オンライン側に共有する<br>今回は`qwerty`を例とする

1. このレポジトリの`app.py`を起動
```
sudo python3 app.py 0　qwerty
```

2. ↓のメッセージがでたら、Switchで [持ちかた/順番を変える](https://www.nintendo.co.jp/support/switch/controller/index.html) 画面を開いて接続されるのを待つ
```
Waiting for Switch to connect... Please open the "Change Grip/Order" menu
```

### オンライン側

1. ブラウザでラズパイの5000にアクセス
1. コントローラーコードを入力
1. コントローラを PC or スマホに接続


### (応用) 複数コントローラ接続

1. USB Bluetoothアダプタ等で増設し、`hciconfig` コマンドで `hci1` `hci2` ... が出るようにする
2. `sudo python3 app.py 1` などhciの後ろの数字を引数に指定
3. オンライン側は `5000+数字` 番ポートにアクセス