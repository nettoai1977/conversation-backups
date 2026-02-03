#!/usr/bin/env node
// test-firebase-integration.js
// Simple test script to verify the Firebase integration

const FirebaseOpenClawIntegration = require('./firebase-openclaw.config.js');

async function testFirebaseIntegration() {
  console.log('Testing Firebase OpenClaw Integration...');
  
  const firebase = new FirebaseOpenClawIntegration();
  
  try {
    // Test initialization
    const initResult = await firebase.initialize();
    console.log('Initialization result:', initResult);
    
    if (initResult) {
      console.log('Firebase integration initialized successfully!');
      
      // Test basic functionality - get documents from a test collection
      const testResult = await firebase.getDocuments('test_collection');
      console.log('Test collection query result:', testResult);
    } else {
      console.log('Failed to initialize Firebase integration');
    }
  } catch (error) {
    console.error('Error during test:', error);
  }
}

// Run the test
testFirebaseIntegration();