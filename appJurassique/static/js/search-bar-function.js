function searchBarFunctionPersonnels(colonne) {
  var input, filter, table, tr, td, i, txtValue;
  input = document.getElementById("searchBarPersonnel");
  filter = input.value.toUpperCase();
  table = document.getElementById("tablePersonnels");
  tr = table.getElementsByTagName("tr");

  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[colonne];
    if (td) {
      txtValue = td.textContent || td.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }
  }
}
