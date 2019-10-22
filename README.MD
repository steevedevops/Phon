%include '../util.asm'

section .text
global  _start

maior:
    cmp rdi, rsi ; compara a o rdi com rsi parametros recibido por fora da chamada da funcao
    jg fima ; compara se e maior pula no fima
    jle fimb ; compara se e menor ou igual pula no fimb

fima: mov rax, rdi  ; se a comparação for maior almacena pasa o rdi no rax as funcao sempre retorna no rax
    ret ; retorno o valor no rax
fimb: mov rax, rsi  ; se a comaracao for menor almacena e pasa o segudo parametro que a funcao uma funcao retorna e pasa ele no rax de novo      
	ret ; retorna o rax   funcao ten que retornar valor no rax

_start:            
	mov		rdi, prompta ; lea o valor da entrada e e pasa ela no rdi
    call    printstr ; printa o valor que foi lido e pasado no rdi pois ele print o que ten no rdi
	call	readint ; lea o intero que foi informado
    mov    r12, rax ; como as funcao de leitura sempree retorna no rax entao pasa o rax no r12 por que r12 e uma variaveis comun

    mov		rdi, promptb ; lea o valor da entrada e e pasa ela no rdi
    call    printstr ; printa o valor que foi lido e pasado no rdi pois ele print o que ten no rdi
	call	readint ; lea o segundo intero que foi informado
    mov    r15, rax ; pasa o retorno da leitura da seguna funcao no r15

    mov     rdi,r12 ; move r12 que foi lido na linha 20     
    mov     rsi, r15 ; move r12 que foi lido na linha 25     
    call    maior ; chama a funcao maior que va a receber os parametros lidos la encima linha 27 28

    mov		rdi, rax ; como as funcao sempre retorna rax move ese retorno no rdi para poder printar o string
	call 	printint ; printa o valor que esta no rdi
	call 	endl    ; funcao que vem do utiles para fazer quebra linha
    call    exit ; finaliza o programa
    
section	.data
    prompta	db 'Valor a: ', 0 ;  valor a  lindo desde un promt
    promptb	db 'Valor b: ', 0 ; valor b lido desde un  promt








datalog
rebeca
jeanus
progol
fusiclip 
alice ship
ciao

from beautifultable import BeautifulTable

subtableb = BeautifulTable()
subtable = BeautifulTable()
subtable.column_headers = ["name", "rank", "gender"]
subtable.append_row(["Jacob", 1, "boy"])
subtable.append_row(["Isabella", 1, "girl"])

subtableb.column_headers = ["name", "rank", "gender"]
subtableb.append_row(["Jacob", 1, "boy"])
subtableb.append_row(["Isabella", 1, "girl"])

parent_table = BeautifulTable()
parent_table.append_row(["Sample text", "Another sample text"])
parent_table.append_row([subtable, subtableb])
parent_table.set_style(BeautifulTable.STYLE_BOX_DOUBLED)
subtable.set_style(BeautifulTable.STYLE_BOX_DOUBLED)
subtableb.set_style(BeautifulTable.STYLE_BOX_DOUBLED)
print(parent_table)