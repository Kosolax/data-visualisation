const express = require('express')
const app = express()
const mysql = require("mysql2")
const cors = require('cors');

app.use(cors())

var connection;

function initConnection() {
    connection = mysql.createConnection({
        host: process.env.DB_DOCKER_IP || "localhost",
        user: 'root',
        password: '',
        port: process.env.DB_EXTERNAL_PORT || 3306,
        database: "au_bon_beurre"
    });
}

app.get('/allunit', (req, res) => {
    initConnection();
    connection.query('select * from units;', function(err, rows, fields) {
        if (err) throw err;
        res.send(rows)
    });
    connection.end()
})

app.get('/unit/:unitId', (req, res) => {
    initConnection();
    connection.query('select * from automatons where id_unit = ' + req.params.unitId + ';', function(err, rows, fields) {
        if (err) throw err;
        res.send(rows)
    });
    connection.end()
})

app.get('/productions/:unitId/:automateId', (req, res) => {
    initConnection();
    connection.query('select * from productions where id_automaton = ' + req.params.automateId + ' AND id_unit = ' + req.params.unitId + ' ORDER BY generatedTime;', function(err, rows, fields) {
        if (err) throw err;
        res.send(rows)
    });
    connection.end()
})

app.listen(8080, () => {
    console.log("Serveur à l'écoute")
})