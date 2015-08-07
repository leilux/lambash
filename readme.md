##lambash

lambash is lam[b<del>d</del>a]-[ba]sh. (⇀‸↼‶)

![](https://raw.githubusercontent.com/leilux/lambash/master/screenshot.png)

*Core Python Programming* Exercises 14.9

*Shells*. Create a shell (operating system interface) program. Present a command-line interface that accepts operating system commands for execution (any platform).

Extra credit 1: Support pipes (see the dup(), dup2(), and pipe() functions in the os module). This piping procedure allows the standard output of one process to be connected to the standard input of another.

Extra credit 2: Support inverse pipes using parentheses, giving your shell a functional programming-like interface. In other words, instead of piping commands like ...

```bash
ps -ef | grep root | sort -n +1
```

... support a more functional style like...

```lisp
sort(grep(ps -ef, root), -n, +1)
```

