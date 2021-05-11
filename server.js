const http = require('http');
const bodyParser = require('body-parser');
const express = require('express');
const path = require("ejs");
const app = express();
const port = 3000;
// https://www.youtube.com/watch?v=6IOrp8HgnJU&t=355s
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
var urlencodedParser = bodyParser.urlencoded({ extended: false })
//register view engine
app.set('view engine','ejs');
app.set('views','./public/views');
app.use(express.json({limit: '1mb'}));
app.use(express.static('./public/styleEJS'));
app.use( express.static( "./public/png" ) );
app.use( express.static( "./public/views" ) );
app.use( express.static( "./public/views/partials" ) );

app.get('/',(req,res)=>{
    var conn= new sql.ConnectionPool(config);
    res.render('NewHomePage',{title:'Home Page'});
    conn.close();
})

app.get('/new',(req,res)=>{
    var conn= new sql.ConnectionPool(config);
    res.render('NewHomePage',{title:'Home Page'});
    conn.close();
})

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



app.get('/Products2',(req,res)=>{
    res.render('Products.ejs');
})
app.get('/Products',(req,res)=>{
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
               res.json(recordSet[0]);
           }

        });
    })
});

app.get('/buy',(req,res)=>{
    res.render('buy.ejs');
})

app.get('/submit',(req,res)=>{
    res.render('submitlst.ejs');
})

app.get('/totalSum',(req,res)=>{
    res.render('TotalSum.ejs');
})

//get the basic names of the products
app.get('/basicNames',(req,res)=>{
    var conn= new sql.ConnectionPool(config);
    var record = conn.connect( function (err){
        if (err)
            throw err;
        var req1 = new sql.Request(conn);
        req1._query('  SELECT Base_Prod FROM [BraudeProject].[dbo].[AllProds] GROUP BY Base_Prod', function (err, recordSet){
           if (err) throw err;
           else
           {
               conn.close();
               res.json(recordSet[0]);
           }
        });
    })
});

//get the cost and the webs of the basic products
app.get('/basicNamesCost',(req,res)=>{
    var conn=new sql.ConnectionPool(config);
    var record=conn.connect(function(err){
        if(err)
            throw err;
        var req2=new sql.Request(conn);
        req2._query('SELECT Prod_Id_Web,Base_Prod,Prod_Web,Prod_Price,Prod_Unit,Prod_Name FROM AllProds',function (err, recordSet){
            if (err) throw err;
            else {
                conn.close();
                res.json(recordSet[0]);
            }
        });
    })
})
app.post('/Pup', urlencodedParser,(req,res)=>{
        console.log(req.body);
    const puppeteer = require('puppeteer');
    (async () => {
        const browser = await puppeteer.launch({headless:false});
        const page = await browser.newPage();
        if(req.body.site === 'kishurit'){
            await page.goto('http://www.meshek-kishorit.org/47955-%D7%99%D7%A8%D7%A7%D7%95%D7%AA?page=1');
            await page.screenshot({ path: 'kishurit.png' });
        }
        else{
            await page.goto('http://sultan.pricecall.co.il/');

            const  x = await page.$('[id="350"]');
            await x.type('4', {delay: 5})



  //             const data = await page.evaluate(() => {
  //                 const tds = Array.from(document.querySelectorAll('table tr td'))
  //                 return tds.map(td => td.innerText)
  // });
  //             console.log(data);
  //           var i = 0;
  //            for(var row in data)
  //            {
  //                if(data[row] !== ''){
  //                    console.log(data[row]);
  //                    i =  i + 1;
  //                }
  //            }
  //            console.log(i)
            await page.screenshot({ path: 'sultan.png' });

        }


  // await browser.close();
})();
res.send('Good Pic')


});
//if we get into team page we will go to about page
app.get('/team',(req,res)=>{
    res.redirect('/Products');
})

app.use((req,res)=>{
    res.status(404).render('404');
})


app.listen(port, () => {console.log('Server run');})

//     console.log(req.body);
//     const puppeteer = require('puppeteer');
//     (async () => {
//         const browser = await puppeteer.launch({headless:false});
//         const page = await browser.newPage();
//         if(req.body.site === 'kishurit'){
//             await page.goto('http://www.meshek-kishorit.org/47955-%D7%99%D7%A8%D7%A7%D7%95%D7%AA?page=1');
//             await page.screenshot({ path: 'kishurit.png' });
//         }
//         else{
//             await page.goto('http://sultan.pricecall.co.il/');
//               const data = await page.evaluate(() => {
//                   const tds = Array.from(document.querySelectorAll('table tr td'))
//                   return tds.map(td => td.innerText)
//   });
//               console.log(data);
//             var i = 0;
//              for(var row in data)
//              {
//                  if(data[row] !== ''){
//                      console.log(data[row]);
//                      i =  i + 1;
//                  }
//              }
//              console.log(i)
//             await page.screenshot({ path: 'sultan.png' });
//
//         }
//
//
//   await browser.close();
// })();
// res.json('Good Pic')