## 6502 Integer Square Root - which is best? ##

The purpose of this page is to compare the performance of several different implementations of a 16 bit integer square root on the 6502 CPU, to find out which is best.
This function is sometimes known as isqrt, and conventionally it rounds down the result, so the result fits in 8 bits.
See the Wikipedia page for [integer square root](https://en.wikipedia.org/wiki/Integer_square_root) for details of algorithms.

We execute each routine exhaustively over all 65536 possible inputs, record the cycle count for each and graph the results.

### Implementations tested
| file    | origin                                                    |
| ------- | --------------------------------------------------------- |
| sqrt1.a | https://codebase64.org/doku.php?id=base:fast_sqrt         |
| sqrt2.a | http://www.6502.org/source/integers/root.htm              |
| sqrt3.a | http://www.txbobsc.com/aal/1986/aal8611.html#a1           |
| sqrt5.a | http://www.txbobsc.com/aal/1986/aal8609.html#a8           |
| sqrt6.a | https://www.bbcelite.com/master/main/subroutine/ll5.html  |
| sqrt7.a | http://6502org.wikidot.com/software-math-sqrt             |


### Python Script
After assembling each file using [acme](https://github.com/meonwax/acme), we use [py65mon](https://github.com/mnaberez/py65/blob/master/docs/index.rst) to load and execute the binary 6502, check the results are accurate and record the cycle count.
The results are then output to a CSV file for graphing in a spreadsheet.

### Results

We graph the cycle count of each algorithm over all possible inputs.

![SQRT Performance Comparison](./sqrt.png)

| file    | average cycle count |
| ------- | ------------------- |
| sqrt1.a | 317.7               |
| sqrt2.a | 846.5               |
| sqrt3.a |  43.8               |
| sqrt5.a | 731.0               |
| sqrt6.a | 522.9               |
| sqrt7.a | 501.5               |

All cycle counts include the final RTS, but not any initial JSR. Add 6 cycles for an initial 'JSR sqrt' instruction.

### Conclusion

If speed is all important and you can afford to use 1K of memory then go with the fastest routine sqrt3.a.
If you can't afford 1K of memory, then go for the next fastest (and much smaller) sqrt1.a.
