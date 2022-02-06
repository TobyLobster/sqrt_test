## 6502 Integer Square Root - which is best? ##

The purpose of this page is to compare the performance and memory cost of several different implementations of a 16 bit integer square root on the 6502 CPU, to find out which is best.
This function is sometimes known as isqrt, and conventionally it rounds down the result, so the result fits in 8 bits.

See the Wikipedia page for [integer square root](https://en.wikipedia.org/wiki/Integer_square_root) for details of algorithms.

We execute each routine exhaustively over all 65536 possible inputs, record the cycle count for each and graph the results.

### Implementations tested
All implementations have been sourced from the internet and reformatted for the acme assembler. See [here](https://github.com/TobyLobster/sqrt_test/tree/main/sqrt) for the actual files.

| file     | origin                                                           | notes                                          |
| -------- | ---------------------------------------------------------------- | ---------------------------------------------- |
| sqrt1.a  | https://codebase64.org/doku.php?id=base:fast_sqrt                |                                                |
| sqrt2.a  | http://www.6502.org/source/integers/root.htm                     |                                                |
| sqrt3.a  | http://www.txbobsc.com/aal/1986/aal8611.html#a1                  | a table based solution.                        |
| sqrt5.a  | http://www.txbobsc.com/aal/1986/aal8609.html#a8                  |                                                |
| sqrt6.a  | https://www.bbcelite.com/master/main/subroutine/ll5.html         | from the BBC Micro game Elite.                 |
| sqrt7.a  | http://6502org.wikidot.com/software-math-sqrt                    |                                                |
| sqrt9.a  | https://github.com/TobyLobster/sqrt_test/blob/main/sqrt/sqrt9.a  | a table based solution, my version of sqrt3.a tweaked for performance. |
| sqrt10.a | https://github.com/TobyLobster/sqrt_test/blob/main/sqrt/sqrt10.a | my version of sqrt1.a tweaked for performance. |
| sqrt11.a | https://github.com/TobyLobster/sqrt_test/blob/main/sqrt/sqrt11.a | a table based solution, using binary search. from [here](http://forum.6502.org/viewtopic.php?p=90611#p90611) fixed and tweaked for performance. |

I've omitted implementations sqrt4.a and sqrt8.a as they calculate squares by adding successive odd numbers. This turns out to be extremely slow for anything but small numbers.

### Python Script
After assembling each file using [acme](https://github.com/meonwax/acme), we use [py65mon](https://github.com/mnaberez/py65/blob/master/docs/index.rst) to load and execute the binary 6502, check the results are accurate and record the cycle count.
The results are then output to a CSV file for graphing in a spreadsheet.

### Results

All algorithms provide the correct results. We graph the cycle count of each algorithm over all possible inputs.

![SQRT Performance Comparison](./sqrt.png)

| file     | memory (bytes) | worst case cycles | average cycle count |
| -------- | -------------: | ----------------: | ------------------: |
| sqrt1.a  |             59 |               354 |               317.7 |
| sqrt2.a  |             73 |               923 |               846.5 |
| sqrt3.a  |            796 |               138 |                43.8 |
| sqrt5.a  |             67 |               766 |               731.0 |
| sqrt6.a  |             55 |               574 |               522.9 |
| sqrt7.a  |             42 |               519 |               501.5 |
| sqrt9.a  |            847 |               129 |                39.8 |
| sqrt10.a |            169 |               262 |               229.7 |
| sqrt11.a |            595 |               333 |               268.8 |

All cycle counts include the final RTS, but not any initial JSR. Add 6 cycles for an initial 'JSR sqrt' instruction.

### Conclusion

It's a speed vs memory trade off.
* If speed is all important and you can afford 847 bytes of memory then use the fastest routine sqrt9.a.
* If you can't afford 847 bytes of memory, try sqrt10.a (169 bytes) or sqrt1.a (59 bytes).
* If every byte counts, choose sqrt7.a (42 bytes).

Note: The fastest routines are table based (e.g. sqrt9.a) and have two tables of squares (512 bytes). This memory cost can be shared with a fast multiply routine like https://everything2.com/user/eurorusty/writeups/Fast+6502+multiplication which uses the same tables.
