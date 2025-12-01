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

function searchBarFunctionCampagnes(colonne) {
  var input, filter, table, tr, td, i, txtValue;
  input = document.getElementById("searchBarCampagne");
  filter = input.value.toUpperCase();
  table = document.getElementById("tableCampagnes");
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

function searchBarFunctionMateriels(colonne) {
  var input, filter, table, tr, td, i, txtValue;
  input = document.getElementById("searchBarMateriel");
  filter = input.value.toUpperCase();
  table = document.getElementById("tableMateriels");
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
