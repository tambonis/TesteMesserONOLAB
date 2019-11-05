# Resolução Teste Messer - ONOVOLAB - Tiago Tambonis

# 1 - Construção (pasta API)

$ docker build -t testemesserfinal . 

# 2 - Levantar a API

$ docker run -e ROOT_URL=http://localhost -e MONGO_URL=mongodb://localhost:27017 --network="host" -p 5000:5000 testemesserfinal

# 3 - Exemplo de como rodar

Após executar os comandos anteriores rode o notebook ConsumoAPI.ipynb para visualizar como utilizar a API. 
Uma proposta de análise de exemplo utilizada chama-se Proposta.txt e está no formato adequado ao MongoDB.

# 4 - Bônus

Bonus: A base de dados pode conter um sério problema. Na sua opinião, qual seria? - Escreva a resposta no README do github

Sugiro que o problema estado associados aos campos ApplicationIncome: Renda e CoapplicationIncome: Renda familiar. 
É possível que uma pessoa seja a única fonte de renda de uma família e neste caso estes campos seriam iguais.
