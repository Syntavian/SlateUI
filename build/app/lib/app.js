const http = require("http");
const fs = require("fs");
const path = require("path");

const publicPath = "./public";
const extensionContent = {
    ".html": "text/html", 
    ".js": "text/javascript",
    ".css": "text/css",
    ".json": "application/json",
    ".png": "image/png",
    ".jpg": "image/jpg",
    ".wav": "audio/wav",
};

http.createServer((request, response) => {
    const contentPath = publicPath + ((request.url === "/") ? "/index.html" : request.url);
    
    fs.readFile(contentPath, (error, content) => {
        if (error) {
            response.writeHead(500);
            response.end(`Error: ${error}`);
        } else {
            response.writeHead(200, { "Content-Type": extensionContent[path.extname(contentPath)] });
            response.end(content, "utf-8");
        }
    });
}).listen(8000);

console.log("Server running at http://127.0.0.1:8000/");
