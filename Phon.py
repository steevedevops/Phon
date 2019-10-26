# coding: UTF-8
__author__ = 'Steeve'
__version__ = '1.0.0'

import os
import re
import argparse
from beautifultable import BeautifulTable as btft

class GenericAplication():
    def __init__(self, arquivo, namearq, display ,binaryfile ,textfile):
        self.arquivo = arquivo
        self.namearq = namearq
        self.display = display
        self.binaryfile = binaryfile
        self.textfile = textfile        


    #  Funcao para pegar tudo que for depois dos dois pontos oseja os rotulos
    def __splitGetData(self, text, by, index):
        if not type(text) == str and hasattr(text, 'text'):
            text = text.text
        if type(text) == str:
            if type(by) == list:
                for b in by[1:]:
                    text = text.replace(b, by[0])
                by = by[0]
            if index < 0:
                index = len(text.split(by))-1
            return text.split(by)[index]
        elif type(text) == list:
            lst = []
            for x in text:
                lst.append(self.__splitGetData(x, by, index))
            return lst
        return text

    # Função para retirar os rotulos
    def __getRotulo(self, name, objRot):
        for rot in objRot:
            if name == rot['rotulo']:
                return rot                           
        return 'No Existe este rotulo'

    # Função para tirar os byte
    def __getByte(self, end, obj):
        for b in obj:                    
            if b['end'] == end:
                return True
        return False                

    def __conjInstrucoes(self, name):        
        conjinstru = [{
            'opcode' : '00',
            'name': 'NOP',
            'tamanho': 1
        },{
            'opcode' : '10',
            'name': 'LDR',
            'tamanho': 2
        },{
            'opcode' : '20',
            'name': 'STR',
            'tamanho': 2
        },{
            'opcode' : '30',
            'name': 'ADD',
            'tamanho': 2
        },{
            'opcode' : '40',
            'name': 'SUB',
            'tamanho': 2
        },{
            'opcode' : '50',
            'name': 'MUL',
            'tamanho': 2
        },{
            'opcode' : '60',
            'name': 'DIV',
            'tamanho': 2
        },{
            'opcode' : '70',
            'name': 'NOT',
            'tamanho': 1
        },{
            'opcode' : '80',
            'name': 'AND',
            'tamanho': 2
        },{
            'opcode' : '90',
            'name': 'OR',
            'tamanho': 2
        },{
            'opcode' : 'A0',
            'name': 'XOR',
            'tamanho': 2
        },{
            'opcode' : 'B0',
            'name': 'JMP',
            'tamanho': 2
        },{
            'opcode' : 'C0',
            'name': 'JEQ',
            'tamanho': 2
        },{
            'opcode' : 'D0',
            'name': 'JG',
            'tamanho': 2
        },{
            'opcode' : 'E0',
            'name': 'JL',
            'tamanho': 2
        },{
            'opcode' : 'F0',
            'name': 'HLT',
            'tamanho': 1
        },{            
            'name': 'byte',
            'tamanho': 1
        }]

        for inst in conjinstru:            
            if name == inst['name']:                                
                return inst
        return None


    def __verificaRotuloExist(self, obj, name):    
        for rot in obj:            
            if rot['rotulo'] == name:
                return True
        return False

    def __verificaInstrucoes(self, obj, name):    
        '''
            procura as intruções no objeto da tabela de instruções
        '''
        for rot in obj:            
            if rot['name'] == name:
                return True
        return False
    
    def __getJustInstructions(self, lines):  
        '''
         Funcoa para pegar soamente as instruções para seu usa da saida em un arquivo binario    
        '''
        progComple = []      
        for l in lines:
            for g in l.split(): 
                result = re.search(':', g)  
                if (result == None) and (g != 'text' and g != 'byte' and g != 'data'): 
                    #indica que nao e un rotulo e se nao for nem un campo de texto deixando asim 
                    # soamente as instrucoes e os valores das variaveis ou operando
                    progComple.append(g)                    
        return progComple


    def programaBinaria(self):    
        '''
            Função com o programa principal para monstar os arquivos 
            binarios as saidas e os arquivos texto
        '''    
        simbolData = []
        programBinary = []        
        endAtual = 0
        endAtualFinal = 0
        rotuloRedefinido = False

        # Faca a leitura do arquivo .asm
        fileData = open(self.arquivo, 'r')
        lines  = fileData.readlines()
        
        for x in range(2):
            if x==0: # Primeira pasagem pegando os rotulos e o endereço da memoria                
                for l in lines:                                                            
                    for g in l.split(): 
                        # For que vai pegar tudo que for rotulo para executar o programa.                       
                        result = re.search(':', g) # Tudo que for antes dos dois pontos são rotulos                                           
                        if result != None: 
                            rotu = self.__splitGetData(l,':',0)                                           
                            if len(simbolData) > 0: 
                                if self.__verificaRotuloExist(simbolData, rotu):
                                    rotuloRedefinido = self.__verificaRotuloExist(simbolData, rotu)
                                                                
                            simbolData.append({
                                "rotulo" : rotu,
                                "end" : endAtual
                            })

                        
                        if self.__conjInstrucoes(g.strip()) != None: # 
                            if g != 'text':                            
                                endAtual += self.__conjInstrucoes(g.strip())['tamanho']

                        if g == 'data':                                    
                            endAtual = 128                                        
            else: # Segunda pasagem pasagem pegando os rotulos e o endereço da memoria                               
                if rotuloRedefinido:
                    print('*****************************')
                    print('           ERROR!')
                    print('   Rótulo "'+rotu+'" redefinido')
                    print('*****************************')
                else:
                    endAtual = 0    
                    # Primeiro verifica se as intrucoes estao certo e as operações estao correto 
                    instrucoesvalida = True
                    achouText = False
                    achouData = False
                    achouByte = False
                    for l in lines:# Se a o rotulo nao e nem text e nem data vai dar um erro e se tiver instruções antes tambem vai dar erro                                                                            
                        for g in l.split(): # Se a Instruções nao existe vai dar un erro e se existe não vai dar erro no programa
                            # Oseja vai dar uma exeção baseandose em que o comando nao existe                                                           
                            if l.split() != 'text' and g != 'byte' and g != 'data':
                                self.__conjInstrucoes(g.strip()) 
                                    
                                                
                        if l.split()[0] == 'text':
                            achouText = True
                            if len(l.split()) > 1:                                     
                                instrucoesvalida = False
                                print('*****************************')
                                print('           ERROR!')
                                print(' Operando "'+l.split()[1]+'" inválido nesta instrução ')
                                print('*****************************')
                        elif l.split()[0] == 'data':
                            achouData = True
                            if len(l.split()) > 1:             
                                instrucoesvalida = False
                                print('*****************************')
                                print('           ERROR!')
                                print(' Operando "'+l.split()[1]+'" inválido nesta instrução')
                                print('*****************************')                                    
                    
                        # se o tamanho da leitura e maior que 2 ouseja na linha ten 3 informacoes 
                        # posivelmente data ten que existir                            
                        elif len(l.split()) > 2: 
                            if l.split()[1] == 'byte' and achouByte == False:
                                achouByte = True
                                                
                    
                    if achouText == False:
                        instrucoesvalida = False
                        print('*****************************')
                        print('           ERROR!')
                        print(' Nome "text" não foi definido ')
                        print('*****************************')

                    if achouData == False:
                        instrucoesvalida = False
                        print('*****************************')
                        print('           ERROR!')
                        print(' Nome "data" não foi definido ')
                        print('*****************************')                                

                    if achouByte == False:
                        instrucoesvalida = False
                        print('*****************************')
                        print('           ERROR!')
                        print(' Nome "byte" não foi definido ')
                        print('*****************************')                                            
                    # Complete output binary file                 
                    if (self.binaryfile) and self.namearq:
                        programBinaryCompl = [] # Objeto que vai almacenar o programa completo com tudo os zeros para fazer a saida binaria
                        afterHlt = [] # Almacena os resultado depois do camndo HLT pois e o comando que indica que o programa finalizo.
                        count = 0
                        hltprogram = None
                        if len(self.__getJustInstructions(lines)) > 0:                        
                            for i in range(0, 258): # For que fara a inserção das 256 linha ou byte de saida no arquivo                           
                                if i <= (len(self.__getJustInstructions(lines))-1): # Verifica se a quantidade de endereco atual para pegar o indice do endereco no objeto para evitar erro desnecesario de programacao
                                    justInstruc = self.__getJustInstructions(lines)[i]                                
                                    if (self.__conjInstrucoes(justInstruc) != None) and (hltprogram == None): # verifica se e uma instrução da tabela de instrucoes se for ele almacena o objeto de uma maneira diferente
                                        binary = '{:0>8}'.format(bin(int(self.__conjInstrucoes(justInstruc)['opcode'], 16))[2:])
                                        decimalB = int(str(binary), 2)                                    
                                        programBinaryCompl.append(decimalB)

                                    elif (i < 128 and self.__conjInstrucoes(justInstruc) == None) and (hltprogram == None):
                                        endRot = self.__getRotulo(justInstruc, simbolData)['end']
                                        binary = '{:0>8}'.format(bin(endRot)[2:])
                                        decimalB = int(str(binary), 2)
                                        programBinaryCompl.append(decimalB)

                                    if justInstruc == 'HLT':                                    
                                        hltprogram = justInstruc
                                    elif hltprogram != None:                                    
                                        afterHlt.append(justInstruc)                                                                    
                                else:   
                                    if i >= 128 and len(afterHlt)-1 >= count:
                                        binary = '{:0>8}'.format(bin(int(afterHlt[count]))[2:])
                                        decimalB = int(str(binary), 2)
                                        programBinaryCompl.append(decimalB)
                                        count += 1
                                    else:
                                        binary = '{:0>8}'.format(bin(int(0))[2:])
                                        decimalB = int(str(binary), 2)                                    
                                        programBinaryCompl.append(decimalB)                            
                    
                    else:
                        if instrucoesvalida:
                            for l in lines:   
                                # Monta a tabela de instruções que vai printar no terminal e de como foi trabalhado em sala de aula                   
                                for g in l.split():
                                    result = re.search(':', g)                                            
                                    if result == None:                                                    
                                        if g != 'text' and g != 'byte' and g != 'data':
                                            if self.__conjInstrucoes(g.strip()) != None:                                            
                                                programBinary.append({
                                                    'end' : endAtual,
                                                    'conteudo' : '{:0>8}'.format(bin(int(self.__conjInstrucoes(g.strip())['opcode'], 16))[2:])                                  
                                                })
                                            elif endAtual < 128 and self.__conjInstrucoes(g.strip()) == None:
                                                endRot = self.__getRotulo(g.strip(),simbolData)['end']
                                                # print(endAtual,' Operando ',endRot)
                                                programBinary.append({
                                                    'end' : endAtual,
                                                    'conteudo' : '{:0>8}'.format(bin(endRot)[2:])
                                                })                                                                                                        
                                            else:
                                                # print(endAtual,' Intrucoes ',g)                                    
                                                programBinary.append({
                                                    'end' : endAtual,                                                                        
                                                    'conteudo' : '{:0>8}'.format(bin(int(g))[2:])                                 
                                                })                                                                    

                                            endAtualFinal = endAtual;
                                    
                                        if g != 'text' and g != 'byte':  
                                            endAtual += 1
                                            if g == 'data':                                    
                                                endAtual = 128
                    # Saida no terminal
                    if self.display and instrucoesvalida:                        
                        # para montar a tabela de instruções e fazer a saida binaria                
                        tableSimbolData = btft()
                        tableProgramBinary = btft()
                        contentTable = btft()

                        tableSimbolData.column_headers = ["Rotulo", "Endereço"]
                        for sd in simbolData:
                            tableSimbolData.append_row([sd['rotulo'], sd['end']])   

                        tableProgramBinary.column_headers = ['Endereço', 'Conteudo']
                        for pb in programBinary:
                            content = '- '+pb['conteudo']+' -'                        
                            tableProgramBinary.append_row([pb['end'],content])

                        
                        contentTable.append_row(["Tabela de Simbolo", "Programa Traduzido"])
                        contentTable.append_row([tableSimbolData, tableProgramBinary])
                        
                        contentTable.set_style(btft.STYLE_BOX_DOUBLED)
                        tableProgramBinary.set_style(btft.STYLE_BOX_DOUBLED)
                        tableSimbolData.set_style(btft.STYLE_BOX_DOUBLED)

                        print(contentTable)
                         
                    # Saida no arquivo text
                    if self.textfile and self.namearq and instrucoesvalida: 
                        tableSimbolData = btft()
                        tableProgramBinary = btft()
                        contentTable = btft()

                        tableSimbolData.column_headers = ["Rotulo", "Endereço"]
                        
                        for sd in simbolData:
                            tableSimbolData.append_row([sd['rotulo'], sd['end']])   

                        tableProgramBinary.column_headers = ['Endereço', 'Conteudo']

                        for pb in programBinary:
                            content = '- '+pb['conteudo']+' -'                        
                            tableProgramBinary.append_row([pb['end'],content])

                        
                        contentTable.append_row(["Tabela de Simbolo", "Programa Traduzido"])
                        contentTable.append_row([tableSimbolData, tableProgramBinary])
                        
                        contentTable.set_style(btft.STYLE_BOX_DOUBLED)
                        tableProgramBinary.set_style(btft.STYLE_BOX_DOUBLED)
                        tableSimbolData.set_style(btft.STYLE_BOX_DOUBLED)
                                    
                        file = open(self.namearq+'.txt', "w")
                        file.write(str(contentTable))                     
                        file.close()

                    # Saida do arquivo binario
                    if self.binaryfile and self.namearq and instrucoesvalida:                     
                        # make file                
                        newFile = open(self.namearq+'.bin', "wb")     
                        
                        newFileByteArray = bytearray(programBinaryCompl)
                        # write to file 
                        newFile.write(newFileByteArray)                

if __name__=='__main__':
    parser = argparse.ArgumentParser(prog='PROG', usage='%(prog)s [options]')

    parser.add_argument('-a', required=True, help='Caminho ou nome do arquivo .asm')
    parser.add_argument('-o', required=True, help='Nome de Saída para o arquivo .bin ou txt')
    parser.add_argument('-v', required=False, action='store_true', help='Visualizar o resultado no terminal')
    parser.add_argument('-b', required=False, action='store_true', help='Tipo de saída en un arquivo binario')
    parser.add_argument('-t', required=False, action='store_true', help='Tipo de saída en un arquivo txt')

    args = parser.parse_args()
    GenericAplication(arquivo=args.a, namearq=args.o, display=args.v, binaryfile=args.b, textfile=args.t).programaBinaria()
