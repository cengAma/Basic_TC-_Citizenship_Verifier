const soap = require('soap');
const express = require('express');
const cookieParser = require('cookie-parser');
const session = require('express-session');
const ejs = require('ejs');
const app = express();
//var events = require('events');
//var eventEmitter = new events.EventEmitter();
var bodyParser = require('body-parser');

const ADRES = 'https://tckimlik.nvi.gov.tr/service/kpspublic.asmx?WSDL';

app.set('view engine', 'ejs');

app.use(express.urlencoded({ extended: false }));
app.use(express.static('public'));
app.use(bodyParser.urlencoded());
app.use(cookieParser('secret'));
app.use(session({
    cookie: { maxAge: null },
}));
//middleware
app.use((req, res, next) => {
    res.locals.message = req.session.message;
    delete req.session.message
    next();
})

//event
// var myEventHandler = function () {

//   }
//   eventEmitter.on('scream', myEventHandler);

var alertpost = 0;

app.get('/', (req, res) => {

    res.render('main.ejs');
});

app.get('/about', (req, res) => {
    console.log(req.params, req.body);
    res.render('about.ejs')
})

let degerler = {
    TCKimlikNo: '',
    Ad: '',
    Soyad: '',
    DogumYili: ''
};

app.post('/', (req, res) => {
    console.log(req.body);
    if (req.body.TCKimlikNo == '' || req.body.Ad == '' || req.body.Soyad == '' || req.body.DogumYili == '') {
        req.session.message = {
            type: 'danger',
            intro: 'Boş Alanlar!',
            message: 'Lütfen boşlukları doğru doldurunuz.'
        }
        console.log('bos');
        res.redirect('/');
    }
    else {
        degerler.TCKimlikNo = req.body.TCKimlikNo;
        degerler.Ad = req.body.Ad;
        degerler.Soyad = req.body.Soyad;
        degerler.DogumYili = req.body.DogumYili;

        soap.createClient(ADRES, (err, client) => {

            console.log(alertpost);
            client.TCKimlikNoDogrula(degerler, (err, result) => {
                if (result.TCKimlikNoDogrulaResult) {
                    req.session.message = {
                        type: 'success',
                        intro: 'Doğru',
                        message: 'Girilen Birey Türkiye Cumhuriyeti Vatandaşıdır'
                    }
                    res.redirect('/');
                    console.log('Bilgiler doğru');

                } else {
                    req.session.message = {
                        type: 'danger',
                        intro: 'Yanlış',
                        message: 'Girilen Birey Türkiye Cumhuriyeti Vatandaşı Değildir'
                    }
                    res.redirect('/');
                    console.log('Bilgiler hatalı');
                }
            });
        });

        console.log(degerler);
        //eventEmitter.emit('scream');

    }
});

console.log(alertpost);

//404 error
app.use(function (req, res) {
    res.status(404).render('404.ejs');
});

app.listen(3000, () => console.log("Server Up and running"));