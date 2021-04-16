const http = require('http');
const express = require('express');
const path = require("ejs");
const app = express();
const port = 3000;

/////////////////////////////////connection to DB
const sql = require('mssql');
const config = {
        server: 'DESKTOP-LRQKMNU\\SQLEXPRESS',  //update me
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

//var conn= new sql.ConnectionPool(config);

//register view engine
app.set('view engine','ejs');
app.set('views','./public/views');

app.use(express.static('./public/styleEJS'));

app.get('/',(req,res)=>{
    var conn= new sql.ConnectionPool(config);
    res.render('HomePage',{title:'Home Page'});
    conn.close();
})
/*test*/
app.get('/testpage',(req,res)=>{
    res.render('testpage.ejs');
})
app.get('/testdata',(req,res)=>{
    var conn= new sql.ConnectionPool(config);
    var record = conn.connect( function (err){
        if (err)
            throw err;
        var req = new sql.Request(conn);
        req._query('SELECT * FROM AllProds', function (err, recordSet){
           if (err) throw err;
           else
           {
               conn.close();
               res.json(recordSet[0][1]);
           }

        });
    })
});
/*test end*/

app.get('/Home',(req,res)=>{
    res.render('Home',{title:'Home'});
})
app.get('/Products2',(req,res)=>{
    res.render('Products.ejs');
})
app.get('/Products',(req,res)=>{
    var conn= new sql.ConnectionPool(config);
    //res.render('Products',{title:'Products'});
    var record = conn.connect( function (err){
        if (err)
            throw err;
        var req = new sql.Request(conn);
        req._query('SELECT * FROM AllProds', function (err, recordSet){
           if (err) throw err;
           else
           {
               conn.close();
               //res.send("test");
               //res.render('Products.ejs');
               res.json(recordSet[0]);
               //return recordSet;
           }

        });
    })
});

//if we get into team page we will go to about page
app.get('/team',(req,res)=>{
    res.redirect('/Products');
})

app.use((req,res)=>{
    res.status(404).render('404');
})

app.listen(port, () => {console.log('Server run');})
