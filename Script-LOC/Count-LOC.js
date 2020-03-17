const shell = require('shelljs');
const fs = require("fs");

const repos = [{ nome: "mypy", url: "https://github.com/python/mypy" },
{ nome: "500lines", url: "https://github.com/gvanrossum/500lines" },
{ nome: "TatSu", url: "https://github.com/neogeny/TatSu" },
{ nome: "pegen", url: "https://github.com/gvanrossum/pegen" },
{ nome: "pyxl3", url: "https://github.com/gvanrossum/pyxl3" },
{ nome: "mypy_extensions", url: "https://github.com/python/mypy_extensions" },
{ nome: "cpython", url: "https://github.com/gvanrossum/cpython" },
{ nome: "com2ann", url: "https://github.com/ilevkivskyi/com2ann" },
{ nome: "guidos_time_machine", url: "https://github.com/gvanrossum/guidos_time_machine" },
{ nome: "make-stub-files", url: "https://github.com/edreamleo/make-stub-files" },
{ nome: "mypy", url: "https://github.com/gvanrossum/mypy" },
{ nome: "asyncio", url: "https://github.com/gvanrossum/asyncio" },
{ nome: "ballot-box", url: "https://github.com/gvanrossum/ballot-box" },
{ nome: "pep550", url: "https://github.com/gvanrossum/pep550" },
{ nome: "mypy-dummy", url: "https://github.com/gvanrossum/mypy-dummy" },
{ nome: "peps", url: "https://github.com/phouse512/peps" },
{ nome: "python-memcached", url: "https://github.com/gvanrossum/python-memcached" },
{ nome: "pytype", url: "https://github.com/gvanrossum/pytype" },
{ nome: "cpython", url: "https://github.com/fake-python/cpython" },
{ nome: "arq", url: "https://github.com/gvanrossum/arq" },
{ nome: "stone", url: "https://github.com/gvanrossum/stone" },
{ nome: "pygl", url: "https://github.com/neogeny/pygl" },
{ nome: "welcome-wagon-2018", url: "https://github.com/gvanrossum/welcome-wagon-2018" },
{ nome: "peps", url: "https://github.com/ilevkivskyi/peps" },
{ nome: "cpython", url: "https://github.com/emilyemorehouse/cpython" },
];


var resposta= [];
var temp = [];



repos.forEach(element => {
    var url = element.url;
    var nome = element.nome;
    if (shell.exec('git clone --depth 1 ' + url).code === 0) {
        temp = shell.exec('cloc --csv --quiet ' + nome);
        resposta = resposta.concat('\n' + nome + temp);
        shell.exec('rm -rf ' + nome);
        
    }
    else {
        shell.echo('Error: Git commit failed');
        shell.exit(1);
    }
});

fs.writeFileSync('LOC.csv', resposta);