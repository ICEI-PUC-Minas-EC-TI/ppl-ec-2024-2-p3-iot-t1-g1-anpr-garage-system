CREATE DATABASE Sistema_ANPR
USE Sistema_ANPR

-- -----------------------------------------------------
-- Table Sistema_ANPR.Mensalista
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS Mensalista (
    
    id_mensalista INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(150) NOT NULL,
    CPF CHAR(11) NOT NULL,  
    RG VARCHAR(20) NOT NULL,
    status INT NOT NULL,
    CHECK (status IN (0,1)) 
);

-- -----------------------------------------------------
-- Table Sistema_ANPR.Garagem
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS Garagem (

    id_garagem INT PRIMARY KEY AUTO_INCREMENT,
    capacidade INT NOT NULL,
    hora_abertura TIME NOT NULL,  
    hora_fechamento TIME NOT NULL,  
    nome VARCHAR(150) NOT NULL,
    cidade VARCHAR(100) NOT NULL,
    estado VARCHAR(100) NOT NULL,
    CEP CHAR(8) NOT NULL,  
    numero INT NOT NULL,
    rua VARCHAR(150) NOT NULL
);

-- -----------------------------------------------------
-- Table Sistema_ANPR.Carro
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS Carro (
    id_carro INT PRIMARY KEY AUTO_INCREMENT,
    id_garagem INT NOT NULL,
    id_mensalista INT DEFAULT NULL,
    marca VARCHAR(150) NOT NULL,
    cor VARCHAR(50) NOT NULL,
    modelo VARCHAR(50) NOT NULL,
    placa CHAR(7) NOT NULL,
    ano INT NOT NULL, 
    FOREIGN KEY (id_mensalista) REFERENCES Mensalista(id_mensalista),
    FOREIGN KEY (id_garagem) REFERENCES Garagem(id_garagem)
);

-- -----------------------------------------------------
-- Table Sistema_ANPR.Fluxo
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS Fluxo (

    id_fluxo INT NOT NULL AUTO_INCREMENT,
    id_garagem INT NOT NULL,
    id_carro INT NOT NULL,
    entrada DATETIME NOT NULL,
    saida DATETIME NOT NULL,
    PRIMARY KEY (id_fluxo),
    FOREIGN KEY (id_garagem) REFERENCES Garagem(id_garagem),
    FOREIGN KEY (id_carro) REFERENCES Carro(id_carro),
    CHECK (saida > entrada)
);