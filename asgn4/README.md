### CSC 349, Programming Assignment 4

Included are three sample inputs and outputs for your Programming Assignment 4
implementations.

Due to the nature of the assignment, not every program will always produce the
same output -- the log(n)-approximation and exact solution can be built from
graphs such that there is only one correct and predictable solution, but the
2-approximations will certainly vary.

For these reasons, your programs will be tested with a Python script that will
attempt to parse your output, rather than with diff. I have included part of
the script with these sample inputs and outputs. You should ensure that if you
run, for example:

```
>$ ./compile.sh
>$ ./run.sh in1.txt > my1.txt
>$ python3 read_covers.py my1.txt
```
...the script correctly parses and echoes back your output. Do not alter this
script! It expects your output to look similar to mine (each vertex cover on
its own line, with vertices following a colon and separated by spaces), and
your three vertex covers should be printed in the same order as mine.

_If I can't parse your output, you will almost certainly get no credit._

To summarize:
 * Your program should read a graph from a file. Sample files are given here.
 * Your program should print its output to `stdout`.
 * Your output should look similar to the samples, but need not match exactly.
 * Your output might contain different vertices, depending on the graph.
 * Your output _must_ be readable by `read_covers.py`.
