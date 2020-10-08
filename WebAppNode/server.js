if (process.env.NODE_ENV !== 'production') {
  require('dotenv').config()
}
var PythonShell = require('python-shell');
//var pyshell = new PythonShell('test.py');
var options = {
  mode: 'text',
  encoding: 'utf8',
  pythonPath: 'C:\\Users\\Ahmad\\AppData\\Local\\Programs\\Python\\Python35\\python',
  pythonOptions: ['-u'], // get print results in real-time
  scriptPath: './',
  args: ['2','3']
};

//let pyshell = new PythonShell('test.py',options);
const mongo = require("mongodb");
const assert = require("assert");

var url ="mongodb://localhost:27017/DayCareDataBase";
const express = require('express')
const app = express()
const bcrypt = require('bcrypt')
const passport = require('passport')
const flash = require('express-flash')
const session = require('express-session')
const methodOverride = require('method-override')
const initializePassport = require('./passportConfig')
initializePassport(
  passport,
  email => users.find(user => user.email === email),
     id => users.find(user => user.id === id)
)

app.use('/assets',express.static('assets'))
app.set('view engine', 'ejs')
app.use(express.urlencoded({ extended: false }))


app.use(session({
  secret: process.env.SESSION_SECRET,
  resave: false,
  saveUninitialized: false
}))
app.use(passport.initialize())
app.use(passport.session())

// Connect flash
app.use(flash());

// Global variables
app.use(function(req, res, next) {
  res.locals.success_msg = req.flash('success_msg');
  res.locals.error_msg = req.flash('error_msg');
  res.locals.error = req.flash('error');
  next();
});
app.use(methodOverride('_method'))

app.get('/', checkAuthenticated, (req, res) => {
    
    res.render('index.ejs',{name: req.user.name})
})
var users = [];

app.get('/login', checkNotAuthenticated, (req, res) => {
   
    mongo.connect(url,function(err,db){
        assert.equal(null,err);
        var cursor = db.collection('CenterUsers').find();
        cursor.forEach(function(doc,err){
            assert.equal(null,err);
            users.push(doc);
            
        },function(){
            //console.log(users)
            db.close();
            res.render('login')         
        })
    
    })
  
})

app.post('/login', checkNotAuthenticated, passport.authenticate('local', {
  successRedirect: '/',
  failureRedirect: '/login',
  failureFlash: true,
  session : true

}))
   


app.get('/register', checkNotAuthenticated, (req, res) => {
  res.render('register.ejs')
})

app.post('/register', checkNotAuthenticated, async (req, res) => {
    const hashedPassword = await bcrypt.hash(req.body.pass, 10)
    let errors = [];
    const { name, lastname, email, pass, pass2 } = req.body;
    //console.log(name)
    //console.log(lastname)
    //console.log(email)
    //console.log(pass)
    //console.log(pass2)
    try {
        if (pass != pass2) {
        errors.push({ msg: 'Passwords do not match' });
        }

        if (pass.length < 6) {
            errors.push({ msg: 'Password must be at least 6 characters' });
        }
        
        if (errors.length > 0) {
            res.render('register.ejs', {
                errors,
                name,
                email,
            });
        }
        else{
            var item ={
                name: name +" "+lastname,
                email: email,
                password: hashedPassword
            };

            mongo.connect(url,function(err,db){
                assert.equal(null,err);
                db.collection('CenterUsers').insertOne(item,function(err,result){
                    assert.equal(null,err);
                    console.log("User Inserted")
                    db.close();
                })
            })
            req.flash(
                        'success_msg',
                        'You are now registered and can log in'
                    );
            res.redirect('/login')
        }  
    } 
    catch {
        console.log("Error Occured")
        res.render('newparent.ejs', {
                        errors,
                        name,
                        email,
                    });
    }
})

app.get('/logout', (req, res) => {
  req.logOut();
  req.flash('success_msg', 'You are logged out');
  res.redirect('/login')
})


app.get('/newparent',checkAuthenticated, (req,res) =>{

    res.render('newparent.ejs')
})

app.post('/newparent', checkAuthenticated, async (req, res) => {
    const hashedPassword = await bcrypt.hash(req.body.pass, 10)
    let errors = [];
    const { name, lastname, email, pass, pass2 } = req.body;
    //console.log(name)
    //console.log(lastname)
    //console.log(email)
    //console.log(pass)
    //console.log(pass2)
    try {
        if (pass != pass2) {
        errors.push({ msg: 'Passwords do not match' });
        }

        if (pass.length < 6) {
            errors.push({ msg: 'Password must be at least 6 characters' });
        }
        
        if (errors.length > 0) {
            res.render('newparent.ejs', {
                errors,
                name,
                email,
            });
        }
        else{
            var item ={
                name: name +" "+lastname,
                email: email,
                password: hashedPassword
            };

            mongo.connect(url,function(err,db){
                assert.equal(null,err);
                db.collection('RegisteredParents').insertOne(item,function(err,result){
                    assert.equal(null,err);
                    console.log("Parent Inserted")
                    db.close();
                })
            })
            req.flash(
                        'success_msg',
                        'Parent successfully inserted'
                    );
            res.redirect('/')
            
            
        }  
    } 
    catch {
        console.log("Error Occured")
        res.render('newparent.ejs', {
                        errors,
                        name,
                        email,
                    });
    }
})
app.get('/init',checkAuthenticated, (req,res) =>{
    let pyshell = new PythonShell('test2.py',options);
    console.log('We are in!!')
    res.redirect('/')
})


function checkAuthenticated(req, res, next) {
    //console.log(req.isAuthenticated())
    if (req.isAuthenticated()) {
    return next()
  }

  res.redirect('/login')
}

function checkNotAuthenticated(req, res, next) {
  //console.log(req.isAuthenticated())
  if (req.isAuthenticated()) {
    return res.redirect('/')
  }
  next()
}

app.listen(3010,function() {console.log("App Running on port 3010")})