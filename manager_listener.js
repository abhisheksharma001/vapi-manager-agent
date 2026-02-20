const http = require('http');
const fs = require('fs');

const PORT = 3001;

const server = http.createServer((req, res) => {
  if (req.method === 'POST' && req.url === '/webhook') {
    let body = '';
    req.on('data', chunk => {
      body += chunk.toString();
    });
    req.on('end', () => {
      console.log('Received webhook payload!');
      fs.appendFileSync('received_logs.txt', `[${new Date().toISOString()}] ${body}\n\n`);
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ status: 'received' }));
    });
  } else {
    res.writeHead(404);
    res.end();
  }
});

server.listen(PORT, '0.0.0.0', () => {
  console.log(`Manager Agent Listener running on port ${PORT}`);
});
