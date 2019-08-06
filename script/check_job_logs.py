#! /usr/bin/env python

import os
import re
import sys

def relavent_logfiles(jobs_dir, p):
    """Generator yielding relevant output log file name"""
    # p = '.*_model_chr[1-9][0-9]?\.o.*'
    for file in os.listdir("../joblogs/" + jobs_dir):
        if re.match(p, file):
            yield file
#带有 yield 的函数不再是一个普通函数，而是一个生成器generator，可用于迭代
#yield就是 return 返回一个值，并且记住这个返回的位置，下次迭代就从这个位置后(下一行)开始。

def check_job_logs(jobs_dir, p):
    """Checks all log files in a jobs log directory to make sure they
    turn out ok.

    Makes sure the model script processed all genes it set out to"""
    
    nfiles = 0
    nprobs = 0
    for file in relavent_logfiles(jobs_dir, p):
        nfiles += 1
        if os.stat('../joblogs/' + jobs_dir + file).st_size == 0:
		#判断文件大小
            # File is empty
            nprobs += 1
            print "%s is empty." % file
        with open('../joblogs/' + jobs_dir + file, 'r') as lf:
            # Go to last line.
            for line in lf:
                pass
			#最后存储在line中的值即为文件最后一行
            nums = line.strip().split(' / ')
            assert len(nums) == 2
			#Python assert（断言）用于判断一个表达式，在表达式条件为 false 的时候触发异常。
            if nums[0] != nums[1] or nums[1] == '0':
                nprobs += 1
                print "Problem with %s" % file
                print nums
                if nprobs > 20:
                    print "Too many problems"
                    print "%i files check so far" % nfiles
                    return
    print "%i files found" % nfiles
    print "%i check out" % (nfiles - nprobs)

if __name__ == "__main__":
    p = '.*_model_chr[1-9][0-9]?\.o.*'
    check_job_logs(sys.argv[1], p)
