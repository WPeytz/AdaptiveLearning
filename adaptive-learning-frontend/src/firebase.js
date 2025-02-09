import { initializeApp } from "firebase/app";
import { getFirestore } from "firebase/firestore"; 
import { getAuth } from "firebase/auth"; 

const firebaseConfig = {
  apiKey: "AIzaSyAovTx7PHPOcl0TFsYblR3PvyKA1VCss-Y",
  authDomain: "adaptivelearning-ff09f.firebaseapp.com",
  databaseURL: "https://adaptivelearning-ff09f-default-rtdb.europe-west1.firebasedatabase.app",//http://192.168.0.93:8080
  projectId: "adaptivelearning-ff09f",
  storageBucket: "adaptivelearning-ff09f.firebasestorage.app",
  messagingSenderId: "304947427733",
  appId: "1:304947427733:web:1d52843cf21a9646245e9c",
  measurementId: "G-L1LCPLNPRK",
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
export const db = getFirestore(app);
export const auth = getAuth(app);