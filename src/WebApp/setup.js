var http = require('http')
    fs = require('fs'),
    path = require('path');

http.createServer(function (req, res) {
    
    var spawn = require("child_process").spawn;
    
    child = spawn("powershell.exe", [path.join(__dirname, 'setup.ps1')]);
    child.stdout.on("data",function(data) {
        console.log("Powershell Data: " + data);
    });
    child.stderr.on("data",function(data) {
        console.log("Powershell Errors: " + data);
    });
    child.on("exit",function() {
        res.writeHead(200, { 'Content-Type': 'text/html' });
        res.end(fs.readFileSync(path.join(__dirname, 'blankArmTemplate.json')));
    });
}).listen(process.env.PORT);
