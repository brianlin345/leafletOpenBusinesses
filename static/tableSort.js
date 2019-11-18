function sortTableNumeric(col) {
  var swapped, table, tableRows, rowCount, firstRow, secondRow, currSwap, sortDirection, swapCount;
  swapped = true;
  swapCount = 0;
  sortDirection = "aescending"
  while (swapped) {
    swapped = false;
    table = document.getElementById("businessTable");
    tableRows = table.rows

    for (rowCount = 1; rowCount < (tableRows.length - 1); rowCount++) {
      currSwap = false;
      firstRow = tableRows[rowCount].getElementsByTagName("td")[col];
      secondRow = tableRows[rowCount + 1].getElementsByTagName("td")[col];

      if (sortDirection == "aescending") {
        if (firstRow.innerHTML.toLowerCase() < secondRow.innerHTML.toLowerCase()) {
          currSwap = true;
          break;
        }
      } else if (sortDirection == "descending") {
        if (firstRow.innerHTML.toLowerCase() > secondRow.innerHTML.toLowerCase()) {
          currSwap = true;
          break;
        }
      }
    }

    if (currSwap) {
      tableRows[rowCount].parentNode.insertBefore(tableRows[rowCount + 1], tableRows[rowCount]);
      swapped = true;
      swapCount++;
    } else {
      if (swapCount == 0 && sortDirection == "aescending") {
        sortDirection = "descending";
        swapped = true;
      }
    }
  }

}
