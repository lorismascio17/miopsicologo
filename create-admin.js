require('dotenv').config();
const mongoose = require('mongoose');
const bcrypt = require('bcrypt');

const adminSchema = new mongoose.Schema({
  username: String,
  password: String
});

const Admin = mongoose.model('Admin', adminSchema);

mongoose.connect(process.env.MONGODB_URI, { useNewUrlParser: true, useUnifiedTopology: true })
  .then(() => console.log('Connesso a MongoDB'))
  .catch(err => console.error('Errore di connessione a MongoDB:', err));

async function createAdmin() {
  try {
    const existingAdmin = await Admin.findOne({ username: 'admin' });
    if (existingAdmin) {
      console.log('Un account amministratore esiste già.');
      mongoose.connection.close();
      return;
    }

    const hashedPassword = await bcrypt.hash('password123', 10); // Cambia 'password123' con una password sicura
    const newAdmin = new Admin({
      username: 'admin',
      password: hashedPassword
    });

    await newAdmin.save();
    console.log('Account amministratore creato con successo.');
  } catch (error) {
    console.error('Errore durante la creazione dell\'account amministratore:', error);
  } finally {
    mongoose.connection.close();
  }
}

createAdmin();