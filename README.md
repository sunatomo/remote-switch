# remote-switch

[Death Squared](https://ec.nintendo.com/JP/ja/titles/70010000002104) 
みたいなローカルしか対応してないSwitchのマルチプレイゲームをオンラインからプレイできるようにするシステム

サンプル<br>
https://www.youtube.com/watch?v=shvceLTOwho&feature=youtu.be

つまり、[Steam Remote Play Together](https://store.steampowered.com/remoteplay_together?l=japanese)のswitch版
<br>(ちなみにDeath Squaredはsteamの方が安い)

このシステムはswitchとbluetooth接続しているが、USBで接続したい場合はこっち<br>
[僕んちのNintendo Switchをネット越しで友人と共有してみよう！](https://note.com/neqlol/n/n7fa3f4dc2dca)


## 動作原理

```                                                                         
入力ルート
コントローラー --> ブラウザ --> インターネット --> joycontrolマシーン --> Bluetooth --> Switch

出力ルート
Switch --> momo(webrtc)マシーン -->  インターネット --> ブラウザ
```

出力ルートは switchの画面を共有できれば何でもいいが、momoがベストだと思われ([調査結果](real-time-streaming.md))

## 準備するもの

* joycontrolをインストールできるマシーン
  * Raspberry Pi
  * Ubuntu 
  * Ubuntu On VirtualBox  https://qiita.com/almtr/items/38a7f0c3056024532e8d
  * etc...
* momoをインストールできるマシーン
  * Raspberry Pi
  * Windows
  * etc...
* Bluetoothアダプタ(内臓でもOK) 
* ゲーム　ライブ配信環境
  * HDMIキャプチャ
  * 配信用PC
  * 高速インターネット回線

## セットアップ手順

### 入力ルート※
1. (デバイスに無ければ) Bluetoothアダプタ接続
    * `hciconfig` コマンドで `hci0` が出てくればOK
1. [joycontrol](https://github.com/mart1nro/joycontrol) インストール
    * [Raspberry Pi 最新化](https://search.yahoo.co.jp/search?p=raspberry+pi+%E3%82%BB%E3%83%83%E3%83%88%E3%82%A2%E3%83%83%E3%83%97)
1. インターネットからアクセスできるよう5000番ポートを開放
1. このレポジトリをclone

### 出力ルート※ 
1. HDMIキャプチャ接続
1. [momo](https://github.com/shiguredo/momo) インストール
    * バイナリがあるのでダウンロードして解凍
1. `test.html`と`webrtc.js`を置き換える（オプション）
1. インターネットからアクセスできるよう8080番ポートを開放

※それぞれ別のマシーンでもOK

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
