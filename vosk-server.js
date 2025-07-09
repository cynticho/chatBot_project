const express = require('express');
const path = require('path');
const { VoskRecognizer } = require('vosk');

const app = express();
const port = 5000;

// Le modèle de reconnaissance vocale
const model = new VoskRecognizer({
  modelPath: path.join(__dirname, 'model'),
  lang: 'fr'
});

app.use(express.static('public'));  // Sert ton modèle à partir de ce répertoire

app.listen(port, () => {
  console.log(`Server is running at http://localhost:${port}`);
});
