const shell = require('shelljs');
const fs = require("fs");

var lines = [];
var resposta = [];
var temp = [];

const csv = fs.readFileSync('../repos-python.csv', 'utf8');

function processData(csv) {
    var csvLines = csv.split(/\r\n|\n/);
    var headers = csvLines[0].split(',');
    for (var i=1; i<csvLines.length; i++) {
        var data = csvLines[i].split(',');
        if (data.length == headers.length) {
            var tarr = [];
            for (var j=0; j<headers.length; j++) {
                tarr.push(headers[j]+":"+data[j]);
            }
            lines.push(tarr);
        }
    }
    return lines;
}

var repos = processData(csv);

repos.forEach(element => {
    var url = element[8];
    var nome = element[0];
    if (shell.exec('git clone --depth 1 ' + url.slice(4)).code === 0) {
        temp = shell.exec('cloc --include-lang=Python --csv --quiet ' + nome.slice(5));
        resposta = resposta.concat('\n' + nome + temp);
        shell.exec('rm -rf ' + nome.slice(5));
        
    }
    else {
        shell.echo('Error: Git commit failed');
        shell.exit(1);
    }
});

fs.writeFileSync('LOCpython.csv', resposta);