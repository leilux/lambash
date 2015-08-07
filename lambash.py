#!/usr/bin/env python
#coding: utf-8

# ap1: support pipe
# ap2: Functional Programming Interface
#      ps -ef | grep root | sort -n -f
#      sort(grep(grep(ps -ef, root), ku), -n, -f)

import os
import sys
import re

debug = "for debug use format (#debug print '! ...'). "

def eval_pipe_cmd(cmds):

    length = len(cmds)
    for i in range(length):
        if i == 0:
            #debug print '! fist cmd'
            prevpip = None
            nextpip = os.pipe()
        elif i < (length - 1):
            #debug print '! middle cmd'
            nextpip = os.pipe()
        else:
            #debug print '! last cmd'
            nextpip = None

        eval_simple_cmd(cmds[i][0], cmds[i], prevpip, nextpip)
        # $end child
        prevpip = nextpip


def eval_simple_cmd(cmd, argv, prevpip, nextpip):

    if is_builtin_cmd(cmd): return

    cpid = os.fork()
    if cpid == 0:   #child
        if prevpip:
            #debug print '! have prev'
            os.dup2(prevpip[0], sys.stdin.fileno())   #stdin = pre_r
        if nextpip:
            #debug print '! have next'
            os.dup2(nextpip[1], sys.stdout.fileno())  #stdout = next_w
 
        os.execvpe(cmd, argv, os.environ)
 
    else:           # father
        #debug print '! $begin wait'
        os.wait()
        #debug print "! $end wait"
        if prevpip:
            # prev pipe read is useless for next cmd close it
            os.close(prevpip[0])
        if nextpip:
            # next pipe write will block the read of next pipe close it
            os.close(nextpip[1])

def is_builtin_cmd(cmd):
    if cmd == "exit":
        sys.exit()
    elif cmd == "&":
        return True
    return False


def CLI_eval(cmdline):
    if isinstance(cmdline, list):
        cmds = cmdline
    else:
        cmds = [ filter(lambda n: n!='', cmd.split(' ')) 
                for cmd in cmdline.split('|')]

    if len(cmds) == 1:
        eval_simple_cmd(cmds[0][0], cmds[0], 0, 0)
    else:
        eval_pipe_cmd(cmds)


def FPI_fun(exp, cmds=[]):
    # cmds is reference by address, the default cmds's address is const
    # change the address of cmds
    cmds = [i for i in cmds]
    m = re.match('(.*?)\((.*)\)', exp)
    # print 'id : ', id(cmds)
    if m:
        cmd, arg = m.groups()
        # first cmd
        args = arg.split(',')
        fircmd = args[0].split(' ')
        # second cmd
        seccmd = []
        seccmd.append(cmd)
        seccmd.extend(args[1:])
        # add to cmds
        cmds.extend([seccmd, fircmd])
        return cmds
    else:
        cmds.append(exp.split(' '))
        return cmds


def FPI_fun_ex(exp, cmds=[]):
    # cmds is reference by address, the default cmds's address is const
    # change the address of cmds
    cmds = [i for i in cmds]
    m = re.match('(.*?)\((.*\)) *,?(.*)\)', exp)
    if m:
        cmd, arg1, arg2 = m.groups()
        cmdl = [cmd] + arg2.split(',')

        cmds.append(cmdl) 
        return FPI_fun_ex(arg1, cmds)
    else:
        final_cmds = FPI_fun(exp, cmds)
        final_cmds.reverse()
        return final_cmds 


def FPI_eval(fpstr):
    cmds = FPI_fun_ex(fpstr)
    #print cmds
    cmdline = '|'.join([reduce(lambda x,y: x+' '+y, cmd) for cmd in cmds])
    #print repr(cmdline)
    CLI_eval(cmdline)


def is_FPI(cmdline):
    m = re.search('\(.*\)', cmdline)
    return bool(m)

def counter(x=[-1]):
    x[0] += 1
    return x[0]

if __name__ == "__main__":
    print '''\
Lambash 0.1v -- lambash is lam[bda]-[ba]sh. (⇀‸↼‶)
Type "exit" to exit.

support pipe
Functional Programming Interface
    ps -ef | grep root | sort -n -f
    sort(grep(grep(ps -ef, root), ku), -n, -f)
    '''

    while True:
        print '\x1b[32m' + "In [%d]:" % counter() + '\x1b[39m',
        cmdline = raw_input()
        if cmdline.strip() == '': continue

        if is_FPI(cmdline):
            FPI_eval(cmdline)
        else:
            CLI_eval(cmdline)
