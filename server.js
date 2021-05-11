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
        server: 'LAPTOP-VNSLHC31',  //update me
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
        req1._query('SELECT Base_Prod FROM [BraudeProject].[dbo].[AllProds] GROUP BY Base_Prod', function (err, recordSet){
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

    const puppeteer = require('puppeteer');
    (async () => {
        const browser = await puppeteer.launch({headless:false});
        const page = await browser.newPage();
        if(req.body.site === 'kishurit'){
            await page.goto('http://www.meshek-kishorit.org/47955-%D7%99%D7%A8%D7%A7%D7%95%D7%AA');
             await autoScroll(page);
             for(const row of req.body.purchaseList){
                 const quantity = row.quantity;
                 var id = 'div'+ '[id="' + row.realName + '"]';
                 const  div = await page.$(id);
                 for(let i=0;i<quantity;i++){
                    await div.$eval('div[class="add_item quantity"]',  el =>{
                        el.click({clickCount:1})
                });
                }
                // // const inputField = (await div.$eval('div[class="add_item quantity"]', updateQuantity(row.quantity)))
                // const addQuantity = await div.$('div[class="add_item quantity"]');
                // await addQuantity.click({clickCount:2})
                // await addQuantity.click({clickCount:row.quantity})
                // const inputField = (await div.$('div[class=add_item quantity]')).click({clickCount:row.quantity})
                // await inputField.type(row.quantity.toString())
            }
        }
        else{
            await page.goto('http://sultan.pricecall.co.il/');
            for(var row of req.body.purchaseList){
                // console.log(row.realName)
                var id = '[id="' + row.realName + '"]';
                console.log(id);
                console.log(row.quantity);
                console.log('---------');
                const  inputField = await page.$(id);
                await inputField.type(row.quantity.toString())
            }
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


async function autoScroll(page){
    await page.evaluate(async () => {
        await new Promise((resolve, reject) => {
            var totalHeight = 0;
            var distance = 100;
            var timer = setInterval(() => {
                var scrollHeight = document.body.scrollHeight;
                window.scrollBy(0, distance);
                totalHeight += distance;

                if(totalHeight >= scrollHeight){
                    clearInterval(timer);
                    resolve();
                }
            }, 100);
        });
    });
}