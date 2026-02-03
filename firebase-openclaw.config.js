// firebase-openclaw.config.js
// Custom Firebase configuration for OpenClaw with seamless authentication

const { initializeApp } = require('firebase/app');
const { getFirestore, collection, addDoc, getDocs, doc, getDoc, updateDoc, deleteDoc } = require('firebase/firestore');
const { getAuth, signInWithEmailAndPassword, signInAnonymously } = require('firebase/auth');
const { getStorage, ref, uploadBytes, getDownloadURL } = require('firebase/storage');

// Your Firebase configuration from the earlier code
const firebaseConfig = {
  apiKey: "AIzaSyAUspE9Rju6jw8eP62pJKuVcLlijkxHSjo",
  authDomain: "netto-ai-85b6b.firebaseapp.com",
  projectId: "netto-ai-85b6b",
  storageBucket: "netto-ai-85b6b.firebasestorage.app",
  messagingSenderId: "365613993136",
  appId: "1:365613993136:web:d1451339b51f264e4dbf75",
  measurementId: "G-FYT6FLQ8CR"
};

class FirebaseOpenClawIntegration {
  constructor() {
    this.app = null;
    this.db = null;
    this.auth = null;
    this.storage = null;
    this.initialized = false;
  }

  async initialize() {
    try {
      this.app = initializeApp(firebaseConfig);
      this.db = getFirestore(this.app);
      this.auth = getAuth(this.app);
      this.storage = getStorage(this.app);
      this.initialized = true;
      console.log('Firebase OpenClaw integration initialized successfully');
      return true;
    } catch (error) {
      console.error('Error initializing Firebase OpenClaw integration:', error);
      return false;
    }
  }

  // Firestore methods
  async addDocument(collectionName, data) {
    if (!this.initialized) await this.initialize();
    try {
      const docRef = await addDoc(collection(this.db, collectionName), data);
      return { success: true, id: docRef.id };
    } catch (error) {
      console.error('Error adding document:', error);
      return { success: false, error: error.message };
    }
  }

  async getDocuments(collectionName) {
    if (!this.initialized) await this.initialize();
    try {
      const querySnapshot = await getDocs(collection(this.db, collectionName));
      const documents = [];
      querySnapshot.forEach((doc) => {
        documents.push({ id: doc.id, ...doc.data() });
      });
      return { success: true, documents };
    } catch (error) {
      console.error('Error getting documents:', error);
      return { success: false, error: error.message };
    }
  }

  async getDocument(collectionName, docId) {
    if (!this.initialized) await this.initialize();
    try {
      const docRef = doc(this.db, collectionName, docId);
      const docSnap = await getDoc(docRef);
      
      if (docSnap.exists()) {
        return { success: true, data: { id: docSnap.id, ...docSnap.data() } };
      } else {
        return { success: false, error: 'Document not found' };
      }
    } catch (error) {
      console.error('Error getting document:', error);
      return { success: false, error: error.message };
    }
  }

  async updateDocument(collectionName, docId, data) {
    if (!this.initialized) await this.initialize();
    try {
      const docRef = doc(this.db, collectionName, docId);
      await updateDoc(docRef, data);
      return { success: true };
    } catch (error) {
      console.error('Error updating document:', error);
      return { success: false, error: error.message };
    }
  }

  async deleteDocument(collectionName, docId) {
    if (!this.initialized) await this.initialize();
    try {
      const docRef = doc(this.db, collectionName, docId);
      await deleteDoc(docRef);
      return { success: true };
    } catch (error) {
      console.error('Error deleting document:', error);
      return { success: false, error: error.message };
    }
  }

  // Storage methods
  async uploadFile(filePath, fileData, contentType = 'application/octet-stream') {
    if (!this.initialized) await this.initialize();
    try {
      const storageRef = ref(this.storage, filePath);
      const snapshot = await uploadBytes(storageRef, fileData, { contentType });
      const downloadURL = await getDownloadURL(snapshot.ref);
      return { success: true, url: downloadURL, name: snapshot.metadata.name };
    } catch (error) {
      console.error('Error uploading file:', error);
      return { success: false, error: error.message };
    }
  }

  // Auth methods
  async signIn(email, password) {
    if (!this.initialized) await this.initialize();
    try {
      const userCredential = await signInWithEmailAndPassword(this.auth, email, password);
      return { success: true, user: userCredential.user };
    } catch (error) {
      console.error('Error signing in:', error);
      return { success: false, error: error.message };
    }
  }

  async signInAnonymously() {
    if (!this.initialized) await this.initialize();
    try {
      const userCredential = await signInAnonymously(this.auth);
      return { success: true, user: userCredential.user };
    } catch (error) {
      console.error('Error signing in anonymously:', error);
      return { success: false, error: error.message };
    }
  }
}

module.exports = FirebaseOpenClawIntegration;