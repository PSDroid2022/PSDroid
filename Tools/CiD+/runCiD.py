#coding=utf-8
import os
import shutil
import shlex
import threadpool
import threading
from subprocess import Popen, PIPE
from threading import Timer

JAR_PATH = "OriginCiD31.jar"
SAVECSV_DIR = "CiDAppRunLog"
Android_jar = "/home/ys/下载/ci-d33-master/libs/android-platforms"
RECORD_TXT = "record_cid.txt"

all_solved = {}


def get_apk_lst():
    apk_paths = []
    apk_base = '~/apks'
    apks = os.listdir(apk_base)
    for apk in apks:
        if apk.endswith('.apk'):
            apk_path = os.path.join(apk_base, apk)
            print(apk_path)
            apk_paths.append(apk_path)
    print('total apks:', len(apk_paths))
    return apk_paths


class Analysis:
    def __init__(self):
        self.max_jobs = 10
        self.lock = threading.Lock()

    def run(self, cmd, timeout_sec, savefile):
        fdout = open(savefile, "w+")
        proc = Popen(shlex.split(cmd), stdout=fdout, stderr=PIPE)
        timer = Timer(timeout_sec, proc.kill)
        try:
            timer.start()
            # stdout, stderr = proc.communicate()
            print(proc.stderr.readlines())
        finally:
            timer.cancel()

    def process_one(self, args):
        apk = args
        rslash_pos = apk.rfind('/')
        apk_name = apk[rslash_pos + 1:]
        output_file = os.path.join(SAVECSV_DIR, apk_name + ".txt")
        print(output_file)

        try:
            self.lock.acquire()
            with open(RECORD_TXT, "a+") as fw:
                fw.write(apk_name)
                fw.write("\n")
            self.lock.release()

            # xxx.apk platforms testoutput CDA.txt output.csv testoutput
            print("[+] PreSolving " + apk_name)
            CMD = "java -Xms2G -Xmx8G -XX:MaxNewSize=2048m " \
                  "-jar " + JAR_PATH + " " + apk + " " + Android_jar

            self.run(CMD, 20 * 60, output_file)

        except Exception as e:
            print(e, apk_name)

        dir_path = os.path.join("~Tools/CiD/OriginCiD31", apk_name[:-4] + ".apk.unzip")
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)
        return

    def start(self):
        apks = get_apk_lst()
        print("[+] Analysing {} files".format(len(apks)))
        args = [apk for apk in apks]
        pool = threadpool.ThreadPool(self.max_jobs)
        requests = threadpool.makeRequests(self.process_one, args)
        [pool.putRequest(req) for req in requests]
        pool.wait()


if __name__ == '__main__':

    if not os.path.exists("unzipFiles"):
        os.mkdir("unzipFiles")

    if os.path.exists(RECORD_TXT):
        with open(RECORD_TXT, "r") as fr:
            solved = fr.read().split("\n")
            for item in solved:
                all_solved[item] = 1

    if not os.path.exists(SAVECSV_DIR):
        os.mkdir(SAVECSV_DIR)
    analysis = Analysis()
    analysis.start()
