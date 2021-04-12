{
    async function updateTable(root){
        const table = root.querySelector(".content-table");
        const response = await fetch(root.dataset.url);
        const headers = ['שם מוצר', 'יחידה', 'מחיר', 'אתר', 'מוצר בסיסי'];
        const data = await response.json();
        for(let val of data) {
            console.log(val);
        }
        // Clear Table
        table.querySelector("thead tr").innerHTML = '';
        table.querySelector("tbody").innerHTML = '';
        for (const header of headers){
            table.querySelector('thead tr').insertAdjacentHTML('afterbegin', `<th>${ header }</th>`);
        }
        for (const row of data){
            // console.log(row.Prod_Name);
            table.querySelector('tbody').insertAdjacentHTML('beforebegin', `
            <tr>
            <td>${ row.Base_Prod }</td>
            <td>${ row.Prod_Web }</td>
            <td>${ row.Prod_Price }</td>
            <td>${ row.Prod_Unit }</td>
            <td>${ row.Prod_Name }</td>
            </tr>
        `);
        }
    }
    async function updateHaim(root){
        const response = await fetch('/haim');
        const data = await response.json();
        console.log(data)
    }
    for (const root of document.querySelectorAll('.table-refresh[data-url]')){
        const table = document.createElement('table');
        table.classList.add('content-table')
        table.innerHTML = `
            <thead>
                <tr></tr>
            </thead>
            
            <tbody>
                <tr>
                    <td>Loading</td>
                </tr>  
            </tbody>
        `;
        root.append(table);
        updateHaim(root)
        // updateTable(root);
    }
}