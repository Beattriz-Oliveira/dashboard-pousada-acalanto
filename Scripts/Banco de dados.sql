create database Acalanto;
use Acalanto;

create table Cliente(
id_cliente int primary key auto_increment,
nome varchar(50) not null,
sobrenome varchar(50) not null,
telefone varchar(20) unique not null,
email varchar(50) unique,
estado varchar(2) not null
);

create table Quarto(
id_quarto int primary key auto_increment,
situacao enum('Livre', 'Ocupado', 'Em Limpeza') not null
);

CREATE TABLE Tipo_Quarto (
    id_tipo_quarto INT AUTO_INCREMENT PRIMARY KEY,
    descricao VARCHAR(50),
    preco_diaria DECIMAL(10,2)
);

create table Hospedagem(
id_hospedagem int primary key auto_increment,
id_quarto int not null,
id_cliente int not null,
data_entrada date not null,
data_saida date not null,
qtde_dias int generated always as (datediff(data_saida, data_entrada))stored,
valor_total decimal(10,2) generated always as (qtde_dias * 35.00) stored,
foreign key (id_quarto) references Quarto(id_quarto),
foreign key (id_cliente) references Cliente(id_cliente)
);

create table Categoria(
id_categoria int primary key auto_increment,
nome_categoria varchar(50) not null
);

create table Subcategoria(
id_subcategoria int primary key auto_increment,
id_categoria int not null,
nome_subcategoria varchar(50) not null,
foreign key (id_categoria) references Categoria(id_categoria)
);

create table Produto(
id_produto int primary key auto_increment,
nome varchar(50) not null,
id_categoria int not null,
id_subcategoria int not null,
estoque_atual int not null,
preco_unitario decimal(10,2) not null,
valor_custo decimal(10,2) not null,
foreign key (id_categoria) references Categoria(id_categoria),
foreign key (id_subcategoria) references Subcategoria(id_subcategoria)
);

create table Venda(
id_venda int primary key auto_increment,
data_venda date not null,
valor_total decimal(10,2) default 0.00
);

create table itens_venda(
id_itens int primary key auto_increment,
id_produto int not null,
id_venda int not null,
qtde int not null,
foreign key (id_produto) references Produto(id_produto),
foreign key (id_venda) references Venda(id_venda)
);

create table Pagamento(
id_pagamento int primary key auto_increment,
id_venda int not null,
forma_pagamento varchar(50),
data_pagamento date not null,
valor decimal(10,2) not null,
foreign key (id_venda) references Venda(id_venda)
);

alter table Quarto add column id_tipo_quarto int;
alter table Quarto add foreign key  (id_tipo_quarto) references tipo_quarto(id_tipo_quarto);
alter table Venda add column id_cliente int;
alter table Venda  add foreign key  (id_cliente) references cliente(id_cliente);

select* from Venda;

update Venda set data_venda = "15-05-2025" where data_venda is null;