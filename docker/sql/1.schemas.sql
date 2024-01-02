
CREATE TABLE User (
    idUser INT AUTO_INCREMENT PRIMARY KEY,
    firstName VARCHAR(50) NOT NULL,
    lastName VARCHAR(50) NOT NULL,
    phoneNumber VARCHAR(20),
    email VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE AccountType (
    idAccountType INT AUTO_INCREMENT PRIMARY KEY,
    typeName VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE Account (
    idAccount INT AUTO_INCREMENT PRIMARY KEY,
    idUser INT,
    idAccountType INT,
    accountNumber VARCHAR(20) UNIQUE NOT NULL,
    balance DECIMAL(15, 2) DEFAULT 0.00,
    FOREIGN KEY (idUser) REFERENCES User(idUser),
    FOREIGN KEY (idAccountType) REFERENCES AccountType(idAccountType)
);

CREATE TABLE Credit (
    idCredit INT AUTO_INCREMENT PRIMARY KEY,
    idAccount INT,
    amount DECIMAL(15, 2),
    FOREIGN KEY (idAccount) REFERENCES Account(idAccount)
);

CREATE TABLE Transaction (
    idTransaction INT AUTO_INCREMENT PRIMARY KEY,
    idAccount INT,
    amount DECIMAL(15, 2),
    type ENUM('Incoming', 'Outgoing'),
    transactionDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (idAccount) REFERENCES Account(idAccount)
);

CREATE TABLE AccountLimit (
    idAccount INT,
    currentLimit DECIMAL(15, 2),
    PRIMARY KEY (idAccount),
    FOREIGN KEY (idAccount) REFERENCES Account(idAccount)
);
