ar http = require('http')
    fs = require('fs'),
    path = require('path');

var fullSetupMarkerFilePath = 'D:\\home\\site\\READY';
var templateProvisioningInProgress = 'D:\\home\\site\\wwwroot\\setup.html';

http.createServer(function (req, res) {
    
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