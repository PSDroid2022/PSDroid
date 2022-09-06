# PSDroid Overview

PSDroid is a path-sensitive semantic analysis approach for automated detection of API compatibility usages in Android apps. 

PSDroid models the lifecycle of framework APIs, then builds an analyzer to extract relevant API invoking paths with usage constraints, concludes three types of API compatibility usage issues (i.e., without checks, partial checks and incorrect checks) and localizes incompatible API usages by resolving the usage patterns on API usage path with the augmented API lifecycle.

# Environment Configration
* Ubuntu 20.04
* Java: 1.8
* Android SDK: API 20+


Run PSDroid
```
./PSDroid.sh $apk
```
$apk indicates the app to run.

# Benchmark
4 Apk datasets are stored in "RQ*" folder


# Ouput

After running PSDroid, the issues report will be automatically generated. The report contains all the APIs invoked by app. 
The compatibility API usages are labeled with "crashApis: $j" which indicates the number of issues while "crashApisInMain: $j" indictes this API is incorrected invoked by the main code. An example is shown in the following (e.g., ownCloud.report).

```
#################################################
N 42 Potential Issue API: SDKCheck of <android.media.AudioManager: boolean isStreamMute(int)> is checking!!!
The life time of api is [23,31]
7call roads:
1 Mainhead roads:
!!!this api will crash on sdk 21 22 
Error road: <dummyMainClass: void dummyMainMethod(java.lang.String[])>[]--><dummyMainClass: com.owncloud.android.ui.preview.PreviewVideoActivity dummyMainMethod_com_owncloud_android_ui_preview_PreviewVideoActivity(android.content.Intent)>[]--><com.owncloud.android.ui.preview.PreviewVideoActivity: void onResume()>[]--><com.owncloud.android.ui.preview.PreviewVideoActivity: void preparePlayer()>[]--><com.google.android.exoplayer2.SimpleExoPlayer$Builder: com.google.android.exoplayer2.SimpleExoPlayer build()>[]--><com.google.android.exoplayer2.SimpleExoPlayer: void <init>(com.google.android.exoplayer2.SimpleExoPlayer$Builder)>[]--><com.google.android.exoplayer2.StreamVolumeManager: void <init>(android.content.Context,android.os.Handler,com.google.android.exoplayer2.StreamVolumeManager$Listener)>[]--><com.google.android.exoplayer2.StreamVolumeManager: boolean getMutedFromManager(android.media.AudioManager,int)>[]--><android.media.AudioManager: boolean isStreamMute(int)>
#1.the call statck between class <dummyMainClass: void dummyMainMethod(java.lang.String[])> to <android.media.AudioManager: boolean isStreamMute(int)>has compatibility isssues！
-----------------------------------------
6 Packageshead roads:
!!!this api will crash on sdk 21 22 
Error road: <com.google.android.exoplayer2.ForwardingPlayer: void decreaseDeviceVolume()>[]--><com.google.android.exoplayer2.SimpleExoPlayer: void decreaseDeviceVolume()>[]--><com.google.android.exoplayer2.StreamVolumeManager: void decreaseVolume()>[]--><com.google.android.exoplayer2.StreamVolumeManager: void updateVolumeAndNotifyIfChanged()>[]--><com.google.android.exoplayer2.StreamVolumeManager: boolean getMutedFromManager(android.media.AudioManager,int)>[]--><android.media.AudioManager: boolean isStreamMute(int)>
#1.the call statck between class <com.google.android.exoplayer2.ForwardingPlayer: void decreaseDeviceVolume()> to <android.media.AudioManager: boolean isStreamMute(int)>has compatibility isssues！
-----------------------------------------
...
crashApis:20
crashApisInMain:2
containsStatic:false
containsTry:true
7call by main package
-----------------------------------------
#################################################  
```

