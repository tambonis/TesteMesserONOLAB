# Resolução Teste Messer/ONOVOLAB - Predição de empréstimo pessoal

Tiago Tambonis

# 0 - Clone o repositório
$ git clone "https://github.com/tambonis/TesteMesserONOLAB.git"

# 1 - Construção (pasta API)

$ docker build -t testemesserfinal . 

# 2 - Levantar a API

$ docker run -e ROOT_URL=http://localhost -e MONGO_URL=mongodb://localhost:27017 --network="host" -p 5000:5000 testemesserfinal

# 3 - Exemplo de como rodar

Após executar os comandos anteriores, rode o notebook ConsumoAPI.ipynb para visualizar como utilizar a API. 
Uma proposta de análise de exemplo utilizada chama-se Proposta.txt e está no formato json.
O Resultado esperado é { "_id" : ObjectId("5dc1772d139e24bbbadacd09"), "Emprestar" : "Y", "ID" : "LP001002", "Quantidade (milhares)" : 141.41 } que é inserido no banco de dados "results". No caso, "Emprestar" : "Y" indica que o crédito deve ser concedido e a "Quantidade (milhares)" : 141.41 indica a quantidade ideal para emprestar. 

# 4 - Bônus

Bonus: A base de dados pode conter um sério problema. Na sua opinião, qual seria? - Escreva a resposta no README do github

Sugiro que o problema esteja associado aos campos ApplicationIncome: Renda e CoapplicationIncome: Renda familiar. 
É possível que uma pessoa seja a única fonte de renda de uma família e neste caso estes campos seriam iguais. Existem outros problemas associados aos dados, porém, esperados.

# 5 - Observações

5.1 - A conteinerização não é a ideal e, devido a isto, é necessário que o MongoDB esteja rodando na máquina onde o teste será realizado.

5.2 - Tanto a classificação como a regressão devem ser melhoradas futuramente.
