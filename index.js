const express = require('express');
const sql = require('mssql');


const app = express()
app.use(express.static('public/'));
const config = {
        server: 'LAPTOP-VNSLHC31',
        user: 'Remez',
        password: '123456789',
        database: "BraudeProject",
        dialect: "mssql",
        port: 1433,
        dialectOptions: {
        instanceName: "SQLEXPRESS"
        },
        options:{
            encrypt: false
        }
    };
const conn = new sql.ConnectionPool(config);


app.get('/data', (req, res) =>{
    var record = conn.connect( function (err){
        if (err)
            throw err;
        var req = new sql.Request(conn);
        req._query('SELECT * FROM AllProds', function (err, recordSet){
           if (err) throw err;
           else
           {
               conn.close();
               // console.dir(recordSet[0])
               res.json(recordSet[0]);
           }

        });
    })
});

app.get('/haim', (req, res) =>{
    res.json('haim')
});



app.listen(3001,() => console.log('App Running'))