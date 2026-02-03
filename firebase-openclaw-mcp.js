#!/usr/bin/env node
// firebase-openclaw-mcp.js
// Custom Firebase MCP server for OpenClaw with seamless integration

const { createServer } = require('http');
const { parse } = require('querystring');
const FirebaseOpenClawIntegration = require('./firebase-openclaw.config.js');

class FirebaseMCP {
  constructor() {
    this.firebase = new FirebaseOpenClawIntegration();
    this.port = process.env.MCP_PORT || 8080;
  }

  async initialize() {
    await this.firebase.initialize();
  }

  async handleRequest(request, response) {
    const method = request.method;
    
    // Parse URL and extract action
    const urlParts = request.url.split('/');
    const action = urlParts[1];
    
    // Set CORS headers
    response.setHeader('Access-Control-Allow-Origin', '*');
    response.setHeader('Access-Control-Request-Method', '*');
    response.setHeader('Access-Control-Allow-Methods', 'OPTIONS, GET, POST, PUT, DELETE');
    response.setHeader('Access-Control-Allow-Headers', '*');
    
    if (method === 'OPTIONS') {
      response.writeHead(200);
      response.end();
      return;
    }
    
    let body = '';
    request.on('data', chunk => {
      body += chunk.toString();
    });
    
    request.on('end', async () => {
      try {
        let result;
        
        switch (action) {
          case 'addDocument':
            const addData = JSON.parse(body);
            result = await this.firebase.addDocument(addData.collectionName, addData.data);
            break;
            
          case 'getDocuments':
            const getData = JSON.parse(body);
            result = await this.firebase.getDocuments(getData.collectionName);
            break;
            
          case 'getDocument':
            const getDocData = JSON.parse(body);
            result = await this.firebase.getDocument(getDocData.collectionName, getDocData.docId);
            break;
            
          case 'updateDocument':
            const updateData = JSON.parse(body);
            result = await this.firebase.updateDocument(updateData.collectionName, updateData.docId, updateData.data);
            break;
            
          case 'deleteDocument':
            const deleteData = JSON.parse(body);
            result = await this.firebase.deleteDocument(deleteData.collectionName, deleteData.docId);
            break;
            
          case 'uploadFile':
            const uploadData = JSON.parse(body);
            result = await this.firebase.uploadFile(uploadData.filePath, uploadData.fileData, uploadData.contentType);
            break;
            
          case 'signIn':
            const signInData = JSON.parse(body);
            result = await this.firebase.signIn(signInData.email, signInData.password);
            break;
            
          case 'signInAnonymously':
            result = await this.firebase.signInAnonymously();
            break;
            
          case 'health':
            result = { status: 'healthy', timestamp: new Date().toISOString() };
            break;
            
          default:
            result = { error: `Unknown action: ${action}` };
            response.writeHead(404);
        }
        
        response.writeHead(200, { 'Content-Type': 'application/json' });
        response.end(JSON.stringify(result, null, 2));
      } catch (error) {
        console.error('Error handling request:', error);
        response.writeHead(500, { 'Content-Type': 'application/json' });
        response.end(JSON.stringify({ error: error.message }));
      }
    });
  }

  start() {
    const server = createServer((req, res) => {
      this.handleRequest(req, res);
    });

    server.listen(this.port, () => {
      console.log(`Firebase OpenClaw MCP server listening on port ${this.port}`);
      console.log(`Available endpoints:`);
      console.log(`  POST /addDocument - Add a document to a collection`);
      console.log(`  POST /getDocuments - Get all documents from a collection`);
      console.log(`  POST /getDocument - Get a specific document`);
      console.log(`  POST /updateDocument - Update a document`);
      console.log(`  POST /deleteDocument - Delete a document`);
      console.log(`  POST /uploadFile - Upload a file to storage`);
      console.log(`  POST /signIn - Sign in with email/password`);
      console.log(`  POST /signInAnonymously - Sign in anonymously`);
      console.log(`  GET  /health - Health check`);
    });
  }
}

// Initialize and start the server
async function main() {
  const mcp = new FirebaseMCP();
  await mcp.initialize();
  mcp.start();
}

if (require.main === module) {
  main().catch(console.error);
}

module.exports = FirebaseMCP;