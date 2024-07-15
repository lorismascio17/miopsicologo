require('dotenv').config();
const express = require('express');
const mongoose = require('mongoose');
const bodyParser = require('body-parser'); 
const path = require('path'); // Per servire file statici (se necessario)
const cors = require('cors');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(bodyParser.json());
// Configurazione CORS - PERMETTE RICHIESTE DAL TUO DOMINIO GITHUB PAGES
app.use(cors({
    origin: 'https://lorismascio17.github.io/miopsicologo/' // Sostituisci con il tuo URL 
}));

// Connessione a MongoDB
mongoose.connect(process.env.MONGODB_URI, { 
  useNewUrlParser: true,
  useUnifiedTopology: true,
  serverSelectionTimeoutMS: 5000
})
.then(() => console.log('Connesso a MongoDB'))
.catch(err => console.error('Errore di connessione a MongoDB:', err));

// Schema e modello per le recensioni 
const reviewSchema = new mongoose.Schema({
    name: { type: String, required: true },
    email: { type: String, required: true },
    review: { type: String, required: true },
    approved: { type: Boolean, default: false },
    createdAt: { type: Date, default: Date.now }
});
const Review = mongoose.model('Review', reviewSchema);

// Rotta per ricevere le recensioni (SENZA AUTENTICAZIONE)
app.post('/api/reviews', async (req, res) => {
    try {
        // Controllo Base dell'Input:
        if (!req.body.name || !req.body.email || !req.body.review) {
          return res.status(400).json({ message: 'Nome, email e recensione sono obbligatori.' });
        }

        const newReview = new Review(req.body);
        await newReview.save(); 
        res.status(201).json({ message: 'Recensione inviata con successo.', review: newReview });

    } catch (error) {
        console.error("Errore durante il salvataggio della recensione:", error); 
        res.status(500).json({ message: 'Errore nel salvataggio della recensione' }); 
    }
});





// Serve la pagina testimonianze2.html
app.get('/testimonianze2.html', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'testimonianze2.html'));
});

// Serve l'applicazione frontend
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Gestore di errori generico
app.use((err, req, res, next) => {
  console.error('Errore del server:', err);
  res.status(500).json({ message: 'Errore del server' });
});

app.listen(PORT, () => {
  console.log(`Server in ascolto sulla porta ${PORT}`);
});
