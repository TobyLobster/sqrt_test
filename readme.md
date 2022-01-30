<style>
td.myTableLeft {
  text-align: left;
}
td.myTableCentre {
  text-align: centre;
}
td.myTableRight {
  text-align: right;
}
</style>

## 6502 Integer Square Root - which is best? ##

The purpose of this page is to compare the performance and memory cost of several different implementations of a 16 bit integer square root on the 6502 CPU, to find out which is best.
This function is sometimes known as isqrt, and conventionally it rounds down the result, so the result fits in 8 bits.

See the Wikipedia page for [integer square root](https://en.wikipedia.org/wiki/Integer_square_root) for details of algorithms.

We execute each routine exhaustively over all 65536 possible inputs, record the cycle count for each and graph the results.

### Implementations tested
All implementations have been sourced from the internet and reformatted for the acme assembler.

| file     | origin                                                           |
| -------- | ---------------------------------------------------------------- |
| sqrt1.a  | https://codebase64.org/doku.php?id=base:fast_sqrt                |
| sqrt2.a  | http://www.6502.org/source/integers/root.htm                     |
| sqrt3.a  | http://www.txbobsc.com/aal/1986/aal8611.html#a1                  |
| sqrt5.a  | http://www.txbobsc.com/aal/1986/aal8609.html#a8                  |
| sqrt6.a  | https://www.bbcelite.com/master/main/subroutine/ll5.html         |
| sqrt7.a  | http://6502org.wikidot.com/software-math-sqrt                    |
| sqrt9.a  | https://github.com/TobyLobster/sqrt_test/blob/main/sqrt/sqrt9.a  |
| sqrt10.a | https://github.com/TobyLobster/sqrt_test/blob/main/sqrt/sqrt10.a | 

sqrt9.a is my version of sqrt3.a tweaked for performance.

sqrt10.a is my version of sqrt1.a tweaked for performance.

### Python Script
After assembling each file using [acme](https://github.com/meonwax/acme), we use [py65mon](https://github.com/mnaberez/py65/blob/master/docs/index.rst) to load and execute the binary 6502, check the results are accurate and record the cycle count.
The results are then output to a CSV file for graphing in a spreadsheet.

### Results

All algorithms proved to be correct. We graph the cycle count of each algorithm over all possible inputs.

![SQRT Performance Comparison](./sqrt.png)

<table>
<tr>
<th onclick="sortTable(0)">file</th>
<th onclick="sortTable(1)">memory (bytes)</th>
<th onclick="sortTable(2)">worst case cycles</th>
<th onclick="sortTable(3)">average cycle count</th>
</tr>
<tr><td class="myTableLeft">sqrt1.a</td>  <td class="myTableRight"> 59</td> <td class="myTableRight">354</td> <td class="myTableRight">317.7</td></tr>
<tr><td class="myTableLeft">sqrt2.a</td>  <td class="myTableRight"> 73</td> <td class="myTableRight">923</td> <td class="myTableRight">846.5</td></tr>
<tr><td class="myTableLeft">sqrt3.a</td>  <td class="myTableRight">796</td> <td class="myTableRight">138</td> <td class="myTableRight"> 43.8</td></tr>
<tr><td class="myTableLeft">sqrt5.a</td>  <td class="myTableRight"> 67</td> <td class="myTableRight">766</td> <td class="myTableRight">731.0</td></tr>
<tr><td class="myTableLeft">sqrt6.a</td>  <td class="myTableRight"> 55</td> <td class="myTableRight">574</td> <td class="myTableRight">522.9</td></tr>
<tr><td class="myTableLeft">sqrt7.a</td>  <td class="myTableRight"> 42</td> <td class="myTableRight">519</td> <td class="myTableRight">501.5</td></tr>
<tr><td class="myTableLeft">sqrt9.a</td>  <td class="myTableRight">847</td> <td class="myTableRight">129</td> <td class="myTableRight"> 39.8</td></tr>
<tr><td class="myTableLeft">sqrt10.a</td> <td class="myTableRight">184</td> <td class="myTableRight">280</td> <td class="myTableRight">244.0</td></tr>
</table>

<script>
 function sortTable(n) {
  var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
  table = document.getElementById("myTable2");
  switching = true;
  // Set the sorting direction to ascending:
  dir = "asc";
  /* Make a loop that will continue until
  no switching has been done: */
  while (switching) {
    // Start by saying: no switching is done:
    switching = false;
    rows = table.rows;
    /* Loop through all table rows (except the
    first, which contains table headers): */
    for (i = 1; i < (rows.length - 1); i++) {
      // Start by saying there should be no switching:
      shouldSwitch = false;
      /* Get the two elements you want to compare,
      one from current row and one from the next: */
      x = rows[i].getElementsByTagName("TD")[n];
      y = rows[i + 1].getElementsByTagName("TD")[n];
      /* Check if the two rows should switch place,
      based on the direction, asc or desc: */
      if (dir == "asc") {
        if (x.innerHTML.localeCompare(y.innerHTML, undefined, {numeric: true, sensitivity: 'base'}) > 0) {
          // If so, mark as a switch and break the loop:
          shouldSwitch = true;
          break;
        }
      } else if (dir == "desc") {
        if (x.innerHTML.localeCompare(y.innerHTML, undefined, {numeric: true, sensitivity: 'base'}) < 0) {
          // If so, mark as a switch and break the loop:
          shouldSwitch = true;
          break;
        }
      }
    }
    if (shouldSwitch) {
      /* If a switch has been marked, make the switch
      and mark that a switch has been done: */
      rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
      switching = true;
      // Each time a switch is done, increase this count by 1:
      switchcount ++;
    } else {
      /* If no switching has been done AND the direction is "asc",
      set the direction to "desc" and run the while loop again. */
      if (switchcount == 0 && dir == "asc") {
        dir = "desc";
        switching = true;
      }
    }
  }
}
</script>

All cycle counts include the final RTS, but not any initial JSR. Add 6 cycles for an initial 'JSR sqrt' instruction.

### Conclusion

It's a speed vs memory trade off.
* If speed is all important and you can afford 847 bytes of memory then use the fastest routine sqrt9.a.
* If you can't afford 847 bytes of memory, try sqrt10.a (184 bytes) or sqrt1.a (59 bytes).
* If every byte counts, choose sqrt7.a (42 bytes).

Note: The fastest routine (sqrt9.a) has two tables of squares (512 bytes). This memory cost can be shared with a fast multiply routine like https://everything2.com/user/eurorusty/writeups/Fast+6502+multiplication which uses the same tables.
