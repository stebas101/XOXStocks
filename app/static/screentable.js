
// mock data
const headers = ["Name", "Age", "Country"];
const data = [
  ["Alice", 25, "USA"],
  ["Bob", 30, "Canada"],
  ["Charlie", 28, "UK"],
  ["David", 35, "Australia"]
];

let sortState = {};

const createTable = () => {
    const table = document.getElementById("screenTable");
    table.innerHTML = ""; // clear table content

    const thead = document.createElement("thead");
    const headerRow = document.createElement("tr");
    const tbody = document.createElement("tbody");

    // adding Bootstrap classes
    table.classList.add("table");
    table.classList.add("table-hover");
    thead.classList.add("table-primary")
    tbody.classList.add("table-group-divider");

    const sortArrow = ` <span class="arrow">${sortState.direction === 'asc' ? '↑' : '↓'}</span>`;
    headers.forEach((header, index) => {
        const th = document.createElement("th");
        th.textContent = header;
        th.innerHTML += (sortState.index === index ? sortArrow : '');
        // event listener for sorting:
        th.addEventListener("click", () => sortTable(index));
        headerRow.appendChild(th);
    });
    
    // for (let i=0; i<headers.length; i++) {
    //     item = headers[i];
    //     const th = document.createElement("th");
    //     th.textContent = item;
    //     // event listener for sorting:
    //     th.addEventListener("click", () => sortTable(i));
    //     headerRow.appendChild(th);
    // }

    thead.appendChild(headerRow)
    table.appendChild(thead);

    for (dataRow of data) {
        const row = document.createElement("tr");
        for (item of dataRow) {
            const td = document.createElement("td");
            td.textContent = item;
            row.appendChild(td);
        }
        tbody.appendChild(row);
    }

    table.appendChild(tbody);

};


// let sortDirection = {};

const sortTable = (columnIndex) => {
    // toggle sort direction
    // sortDirection[columnIndex] = !sortDirection[columnIndex];

    // Determine sorting direction
    if (sortState.index === columnIndex) {
    sortState.direction = sortState.direction === "asc" ? "desc" : "asc";
    } else {
    sortState = { index: columnIndex, direction: "asc" };
    }

    // sort data
    data.sort((a, b) => {
        const valueA = a[columnIndex];
        const valueB = b[columnIndex];

        if (typeof valueA === "number" && typeof valueB === "number") {
          return sortState.direction === "asc" ? valueA - valueB : valueB - valueA;
        } else {
          return sortState.direction === "asc"
            ? valueA.toString().localeCompare(valueB.toString())
            : valueB.toString().localeCompare(valueA.toString());
        }
    });

    // Recreate the table with sorted data
    createTable();
};

createTable();