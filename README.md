# sci-hub.py
基于Python的文献批量下载工具，使用sci-hub

## Background
由于之前使用并fork的sci-hub批量下载脚本疑似已失去维护，使用当前(2020.07)可用的sci-hub地址重新实现这一功能

## Install
1. 首先下载项目到本地
    ```shell
    $ git clone git@github.com:Stella3055/sci-hub.py.git
    ```
2. (可选)进入Python虚拟环境/Conda环境
    ```shell
    $ conda activate YOUR_ENV_NAME
    ```
3. 安装必要依赖
    ```shell
    $ python3 -m pip install -r ./requirements.txt
    ```

## Useage
1. 查看帮助
    ```shell
    $ ./scihub.py -h

    usage: scihub.py [-h] --file FILE [--scihuburl SCIHUBURL] [--downloadpath DOWNLOADPATH] [--proxy PROXY]
                    [--xpath XPATH]

    scihub.py is a script written in Python for batch query of research paper in sci-hub accroding to your
    DOI/PMID list

    optional arguments:
    -h, --help            show this help message and exit
    --file FILE, -f FILE  [REQUIRED]Your input file, one row for a DOI/PMID
    --scihuburl SCIHUBURL, -u SCIHUBURL
                            current sci-hub url, default = https://sci-hub.tw/
    --downloadpath DOWNLOADPATH, -d DOWNLOADPATH
                            output folder, will be created if not existed
    --proxy PROXY, -p PROXY
                            proxy, default = empty
    --xpath XPATH, -x XPATH
                            [EXPERIMENTAL]pdf download link xpath selector
    ```
2. 脚本读入**一个**DOI/PMID列表文件，**每个DOI/PMID占一行**
    ```shell
    $ cat ./sampleDoi.txt

    10.1002/ejoc.201601624
    10.1038/srep40880
    10.1002/cbdv.201700266
    10.1016/j.phytol.2017.04.023
    10.1016/j.tetlet.2017.02.019
    10.1007/s10600-017-1961-z
    10.1016/j.bmc.2017.02.054
    10.3390/md15020035
    10.1007/s11418-017-1080-y
    10.1021/acs.jnatprod.6b00860
    ```
3. 启动下载，必需参数为```--file/-f```指定读入的DOI/PMID列表文件
    ```shell
    $ ./scihub.py -f sampleDoi.txt
    Overall Progress:  10%|████▊          | 1/10 [00:05<00:51,  5.77s/paper]
    Current Progress:  14%|██████▌     | 224/1550 [00:01<00:10, 127.05KiB/s
    ```
4. 指定代理以加速下载，使用参数```--proxy/-p```， 该参数将重设```request```库的```http```和```https```代理，请自备梯子使用，代理格式为```[PROTOCOL]://[IP]:[PORT]```
    ```shell
    $ ./scihub.py -f sampleDoi.txt -p socks5://127.0.0.1:1080
    ```