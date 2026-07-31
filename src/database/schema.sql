CREATE TABLE IF NOT EXISTS mouvements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    montant REAL NOT NULL,
    type TEXT NOT NULL CHECK (type IN ('entree', 'depense', 'epargne')),
    categorie TEXT,
    note TEXT
);