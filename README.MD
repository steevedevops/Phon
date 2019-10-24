# Welcome to Phon App!
###### English Description.
This is an application called Phon, its operation is to translate .asm file of ph1 for an output of a binary file with exactly **256 byte**. To use this app is easy, we just have to install some things..
###### Portugues Description
Esta é uma aplicação chamada Phon, sua operação é traduzir o arquivo .asm do ph1 para a saída de um arquivo binário com exatamente 256 bytes. Para usar este aplicativo é fácil, basta instalar algumas coisas.


## Requisitos para poder rodar o app

* Precisa ter instalado **virtualenv** ou **pip** são modulos de python
* Precisa  do módulo **beautifultable** instalado para poder ver os relatórios de tradução para binario.

## Instalação
* Primeiro instale o virtualenv ou o pip, se você não o tiver instalado
	
		sudo apt-get install python3-pip
		pip install virtualenv 
		
* **Opcional** ( Criar um ambiente python ou simplesmente instalar o módulo *beautifultable*)
		
	#### Documentação sobre o uso de este módulo
		https://github.com/pri22296/beautifultable
		https://beautifultable.readthedocs.io/en/latest/quickstart.html

*		pip install beautifultable

* Se você quiser usar o ambiente separado, faça o seguinte.

```						
	   python3 -m venv env  ou  virtualenv -p python3 env	   
	   source env/bin/activate
       pip install -r requirement.txt
```

## Uso
Explicando un poco sobre os argumentos do aplicativo.

|   | Descrição                                 |  Requerido | Argumento           |
|---|-------------------------------------------|------------|---------------------|
|-a |`'Caminho ou nome do arquivo .asm'`        |  Sim       | nome_do_arquivo.asm |
|-o |`Nome de Saída para o arquivo .bin ou txt` |  Sim       | nome_de_saida       |
|-v |`Visualizar o resultado no terminal`       |  Não       |                     |
|-b |`Tipo de saída en un arquivo binario`      |  Não       |                     |
|-t |`Tipo de saída en un arquivo txt`          |  Não       |                     |


Para executar o aplicativo, você deve executar os seguintes comandos


*	Se você quer uma saída de un arquivo texto

		python Phon.py -a dataSample/data.asm -o data -t


*	Se você quer uma saída de un arquivo binario com 256 byte de tamanho

		python Phon.py -a dataSample/data.asm -o data -b

*	Se você quer visualizar o resultado na terminal

		python Phon.py -a dataSample/data.asm -o data -v


*   Comando extra para extrair ou leer arquivo binario en linux
        
        hexdump -C nome_do_arquivo.bin









		      text
loop: LDR i
      SUB v5
      JEQ fim
      STR i
      JMP loop       
      SUB v5
fim:  HLT

      data
i:    byte 50
v5:   byte 5
v5:   byte 7