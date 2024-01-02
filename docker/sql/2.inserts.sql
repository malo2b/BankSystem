-- InsErer des types de compte (Current et Savings)
INSERT INTO AccountType (typeName) VALUES ('Current'), ('Savings');

-- InsErer un utilisateur Karl Marx
INSERT INTO User (firstName, lastName, phoneNumber, email)
VALUES ('Karl', 'Marx', '1234567890', 'karl.marx@example.com');

-- InsErer deux comptes pour Karl Marx (un Current et un Savings)
INSERT INTO Account (idUser, idAccountType, accountNumber, balance)
SELECT idUser, idAccountType, '123456789', 5000.00
FROM User, AccountType
WHERE firstName = 'Karl' AND lastName = 'Marx'
AND typeName = 'Current';

INSERT INTO Account (idUser, idAccountType, accountNumber, balance)
SELECT idUser, idAccountType, '987654321', 2000.00
FROM User, AccountType
WHERE firstName = 'Karl' AND lastName = 'Marx'
AND typeName = 'Savings';

-- InsErer un crEdit pour Karl Marx
INSERT INTO Credit (idAccount, amount)
SELECT idAccount, 1000.00
FROM Account
WHERE idUser = (SELECT idUser FROM User WHERE firstName = 'Karl' AND lastName = 'Marx')
LIMIT 1;

-- InsErer des transactions pour les comptes de Karl Marx
SET @idCurrent = (SELECT idAccount FROM Account WHERE idUser = (SELECT idUser FROM User WHERE firstName = 'Karl' AND lastName = 'Marx') AND idAccountType = 1);
SET @idSavings = (SELECT idAccount FROM Account WHERE idUser = (SELECT idUser FROM User WHERE firstName = 'Karl' AND lastName = 'Marx') AND idAccountType = 2);

INSERT INTO Transaction (idAccount, amount, type)
VALUES
    (@idCurrent, 150.00, 'Incoming'), -- Transaction entrante pour le compte Current
    (@idCurrent, 50.00, 'Outgoing'),  -- Transaction sortante pour le compte Current
    (@idSavings, 200.00, 'Incoming'), -- Transaction entrante pour le compte Savings
    (@idSavings, 100.00, 'Outgoing');  -- Transaction sortante pour le compte Savings

-- InsErer des enregistrements fictifs dans la table AccountLimit pour chaque compte
INSERT INTO AccountLimit (idAccount, currentLimit)
VALUES (@idCurrent, 5000.00), -- Limite fictive pour le compte Current
       (@idSavings, 3000.00); -- Limite fictive pour le compte Savings
