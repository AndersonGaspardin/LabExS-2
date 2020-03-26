const shell = require('shelljs');
const fs = require("fs");

const repos = [{ nome: "mypy", url: "https://github.com/python/mypy" },
{ nome: "500lines", url: "https://github.com/gvanrossum/500lines" },
{ nome: "pegen", url: "https://github.com/gvanrossum/pegen" },
{ nome: "mypy_extensions", url: "https://github.com/python/mypy_extensions" },
{ nome: "cpython", url: "https://github.com/gvanrossum/cpython" },
{ nome: "mypy", url: "https://github.com/gvanrossum/mypy" },
{ nome: "mypy-dummy", url: "https://github.com/gvanrossum/mypy-dummy" },
{ nome: "python-memcached", url: "https://github.com/gvanrossum/python-memcached" },
{ nome: "pytype", url: "https://github.com/gvanrossum/pytype" },
{ nome: "arq", url: "https://github.com/gvanrossum/arq" },
{ nome: "welcome-wagon-2018", url: "https://github.com/gvanrossum/welcome-wagon-2018" },
{ nome: "peps", url: "https://github.com/ilevkivskyi/peps" },
{ nome: "cpython", url: "https://github.com/emilyemorehouse/cpython" }
];


var resposta= [];
var temp = [];



repos.forEach(element => {
    var url = element.url;
    var nome = element.nome;
    if (shell.exec('git clone --depth 1 ' + url).code === 0) {
        temp = shell.exec('cloc --include-lang=Python --csv --quiet ' + nome);
        resposta = resposta.concat('\n' + nome + temp);
        shell.exec('rm -rf ' + nome);
        
    }
    else {
        shell.echo('Error: Git commit failed');
        shell.exit(1);
    }
});

fs.writeFileSync('LOC.csv', resposta);