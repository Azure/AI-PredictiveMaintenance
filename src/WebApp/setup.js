var http = require('http')
    fs = require('fs'),
    path = require('path');

var fullSetupMarkerFilePath = 'D:\\home\\site\\FINISH';
var templateProvisioningInProgress = 'D:\\home\\site\\wwwroot\\setup.html';

http.createServer(function (req, res) {
            fs.readFile(fullSetupMarkerFilePath, function(err) {
                if (err) {
                    fs.readFile('setup.html',function (err, data) {
                        res.writeHead(200, {'Content-Type': 'text/html','Content-Length':data.length});
                        res.write(data);
                        res.end();
                    });
                } else {
                    res.writeHead(302, {
                        'Location': '/home'        
                    });
                    res.end();
                }
            });               
}).listen(process.env.PORT);