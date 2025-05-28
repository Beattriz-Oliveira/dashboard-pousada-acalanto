# Preenchendo o banco de dados com dados ficitícios com a biblioteca Faker.
from faker import Faker
import mysql.connector
import random
from datetime import timedelta

# Conexão com o Banco de Dados
bd= mysql.connector.connect(host='127.0.0.1', user='root', password='1452', database='Acalanto')

cursor= bd.cursor()

# Geração de dados com Faker
fk= Faker('pt_br')

def Cliente():
    uf= ['AC', 'AL', 'AP','AM', 'BA','CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO']
    for _ in range(200):
        nome= fk.first_name()
        sobrenome= fk.last_name()
        telefone= fk.phone_number()
        email= fk.email()
        estado= random.choice(uf)
        cursor.execute('select email from Cliente where email = %s', (email,))
        result= cursor.fetchall()
        if result:
            continue
        cursor.execute('insert into Cliente(nome, sobrenome, telefone, email, estado) values (%s,%s,%s,%s,%s)', (nome, sobrenome, telefone, email, estado))
        
def Tipo_Quarto():
    tipos=[("Individual", 50.00),("Duplo", 100.00),("Familiar",250.00),("Luxo",350.00)]
    for descricao,preco in tipos:
        cursor.execute('insert into tipo_quarto(descricao, preco_diaria) values (%s,%s)', (descricao,preco))

def Quarto():
    cursor.execute('select count(*) from Quarto')
    quartos= cursor.fetchone()[0]
    cursor.execute('select id_tipo_quarto from tipo_quarto')
    tipos= [t[0] for t in cursor.fetchall()]
    
    if quartos <=20:
        for _ in range(20 - quartos):
            situacao= random.choice(['Livre', 'Ocupado', 'Em Limpeza'])
            id_tipo = random.choice(tipos)
            cursor.execute('insert into Quarto(situacao,id_tipo_quarto) values (%s,%s)', (situacao,id_tipo))

def Categoria():
    categorias=['Alimentos', 'Bebidas', 'Higiene', 'Brinquedos', 'Roupas']
    cursor.execute('select count(*) from Categoria') 
    categoria_cont= cursor.fetchone()[0]
    
    # Limitando os ids de Categoria para 5
    if categoria_cont <5: 
         for nome_categoria in categorias[:5 - categoria_cont]:
            cursor.execute('insert into Categoria(nome_categoria) values (%s)', (nome_categoria,))
        
def Subcategoria():
    subcategorias = {
        'Alimentos': ["Coxinha", "Empada de frango", "Pastel de carne", "Esfirra de queijo", "Bolo de fubá", "Broa de milho", "Pão de queijo", "Biscoito de polvilho"],
        'Bebidas': ["Água mineral", "Suco de laranja", "Refrigerante de cola", "Chá verde", "Café em pó", "Leite integral", "Água de coco", "Cerveja artesanal"],
        'Higiene': ["Sabonete líquido", "Shampoo", "Condicionador", "Creme dental", "Escova de dentes", "Fio dental", "Papel higiênico", "Desodorante"],
        'Brinquedos': ["Bola de futebol", "Boneca de pano", "Carrinho de controle remoto", "Quebra-cabeça de 500 peças", "Blocos de montar", "Jogo da memória", "Urso de pelúcia", "Pião de madeira"],
        'Roupas': ["Camiseta de algodão", "Calça jeans", "Vestido floral", "Shorts de moletom", "Jaqueta de couro", "Camisa social", "Meias de lã", "Boné esportivo"]
    }
    
    # Recuperar o id_categoria com base no nome da categoria
    for categoria, subcats in subcategorias.items(): 
        cursor.execute('select id_categoria from Categoria where nome_categoria = %s', (categoria,))
        categoria_result = cursor.fetchall()
        if categoria_result:
            id_categoria = categoria_result[0][0]
            
            # Inserindo as subcategorias
            for subcategoria in subcats: 
                cursor.execute('insert into Subcategoria (id_categoria, nome_subcategoria) values (%s, %s)', (id_categoria, subcategoria))

def Produto():
    cursor.execute('select id_categoria, id_subcategoria, nome_subcategoria from Subcategoria')
    ids_produtos= cursor.fetchall()
    
    # Puxando os ids da Subcategoria
    for id_categoria, id_subcategoria,nome_subcategoria in ids_produtos: 
        estoque_atual= random.randint(1,200)
        preco_unitario= round(random.uniform(5.0, 60.0), 2)
        valor_custo= round(random.uniform(0.5, 0.8), 2)
        cursor.execute('insert into Produto(nome, id_categoria, id_subcategoria, estoque_atual, preco_unitario, valor_custo) values (%s, %s, %s, %s, %s, %s)', (nome_subcategoria, id_categoria, id_subcategoria, estoque_atual, preco_unitario, valor_custo))

def Hospedagem():
    # Verificando os quartos já ocupados
    cursor.execute('select id_quarto from Quarto')
    quartos = [q[0] for q in cursor.fetchall()]
    
    # Verificando clientes cadastrado
    cursor.execute('select id_cliente from Cliente')
    clientes= [c[0] for c in cursor.fetchall()]
    
    # Inserindo os dados na tabela Hospedagem
    for id_cliente in clientes:
        num_hospedagens = random.randint(1, 3)
        for _ in range(num_hospedagens):
            id_quarto = random.choice(quartos)
            data_entrada = fk.date_between(start_date='-6M', end_date='today')
            data_saida = data_entrada + timedelta(days=random.randint(1, 15))
            cursor.execute('insert into Hospedagem(id_cliente, id_quarto, data_entrada, data_saida) values (%s, %s, %s, %s)', (id_cliente, id_quarto, data_entrada, data_saida))

def Venda():
     # Buscar clientes
    cursor.execute('SELECT id_cliente FROM Cliente')
    clientes = [c[0] for c in cursor.fetchall()]

    # Buscar hospedagens organizadas por cliente
    cursor.execute('SELECT id_cliente, data_entrada, data_saida FROM Hospedagem')
    hospedagens_por_cliente = {}
    for id_cliente, entrada, saida in cursor.fetchall():
        hospedagens_por_cliente.setdefault(id_cliente, []).append((entrada, saida))

    for id_cliente in clientes:
        num_vendas = random.randint(2, 5)  # Vendas por cliente

        for _ in range(num_vendas):
            # 30% de chance da venda ocorrer durante hospedagem
            if id_cliente in hospedagens_por_cliente and random.random() < 0.3:
                entrada, saida = random.choice(hospedagens_por_cliente[id_cliente])
                data_venda = fk.date_between(start_date=entrada, end_date=saida)
            else:
                data_venda = fk.date_between(start_date='-6M', end_date='today')

            # Inserir venda com cliente
            cursor.execute('insert into Venda(data_venda, id_cliente) values (%s, %s)', (data_venda, id_cliente)) 

def Itens_Venda():
    cursor.execute('SELECT id_produto, valor_custo FROM Produto')
    produtos = cursor.fetchall()

    cursor.execute('SELECT id_venda FROM Venda')
    vendas = [v[0] for v in cursor.fetchall()]

    for id_venda in vendas:
        num_itens = random.randint(1, 5)
        valor_total = 0

        for _ in range(num_itens):
            id_produto, valor_custo = random.choice(produtos)
            qtde = random.randint(1, 10)
            cursor.execute(
                'INSERT INTO Itens_Venda(id_produto, id_venda, qtde) VALUES (%s, %s, %s)',
                (id_produto, id_venda, qtde)
            )
            valor_total += qtde * valor_custo

        # Atualiza o valor total na tabela Venda
        cursor.execute(
            'UPDATE Venda SET valor_total = %s WHERE id_venda = %s',
            (valor_total, id_venda)
        )

def Pagamento():
    formas = ['Dinheiro', 'Cartão de Crédito', 'Cartão de Débito', 'Pix']

    # Buscar somente vendas já com valor_total > 0
    cursor.execute('SELECT id_venda, data_venda FROM Venda WHERE valor_total > 0')
    vendas = cursor.fetchall()

    for id_venda, data_venda in vendas:
        forma_pagamento = random.choice(formas)

        # Buscar o valor atualizado direto da tabela
        cursor.execute('SELECT valor_total FROM Venda WHERE id_venda = %s', (id_venda,))
        valor_total = cursor.fetchone()[0]

        data_pagamento = fk.date_between(start_date=data_venda, end_date='+15d')

        cursor.execute(
            'INSERT INTO Pagamento(id_venda, data_pagamento, forma_pagamento, valor) VALUES (%s, %s, %s, %s)',
            (id_venda, data_pagamento, forma_pagamento, valor_total)
        )

# Inserindo os dados
Cliente()
Tipo_Quarto()
Quarto()
Categoria()
Subcategoria()
Produto()
Hospedagem()
Venda()
Itens_Venda()
Pagamento()


# Confirmação de alteração
bd.commit()
print("Dados Inseridos com Sucesso!")

# Encerramento de atividade
cursor.close()
bd.close()