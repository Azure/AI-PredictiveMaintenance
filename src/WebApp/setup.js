var http = require('http')
    fs = require('fs'),
    path = require('path'),
    url = require('url');

var initialSetupMarkerFilePath = 'D:\\home\\site\\wwwroot\\.setup';
var fullSetupMarkerFilePath = 'D:\\home\\site\\wwwroot\\READY';
var templateProvisioningInProgress = 'D:\\home\\site\\wwwroot\\setup.html';

http.createServer(function (req, res) {
    var url_parts = url.parse(req.url, true);
    var query = url_parts.query;

    fs.readFile(initialSetupMarkerFilePath, function(err) {
        fs.readFile(fullSetupMarkerFilePath, function(err) {
            if (err) {
                fs.readFile('setup.html',function (err, data) {
                    res.writeHead(200, {'Content-Type': 'text/html','Content-Length':data.length});
                    res.write(data);
                    res.end();
                });
            } else {
                res.writeHead(302, {
                        'Location': '/'
                });
                res.end();
            }
        });        
    });
}).listen(process.env.PORT);