# coding: UTF-8
__author__ = 'Steeve'
__version__ = '1.0.0'

import os
import re
import argparse
from beautifultable import BeautifulTable as btft

class GenericAplication():
    def __init__(self, arquivo, namearq, desplay ,binaryfile ,textfile):
        self.arquivo = arquivo
        self.namearq = namearq
        self.desplay = desplay
        self.binaryfile = binaryfile
        self.textfile = textfile        

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

    def __getRotulo(self, name, objRot):
        for rot in objRot:
            if name == rot['rotulo']:
                return rot                           
        return 'No Existe este rotulo'

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


    def __getJustInstructions(self, lines):  
        progComple = []      
        for l in lines: # percorre todas as linhas do arquivo
            for g in l.split(): # Limpa os espaço de cada linha percorrido o mostra tudo um abaixo de outro
                result = re.search(':', g)  
                if (result == None) and (g != 'text' and g != 'byte' and g != 'data'): # somente faz se o result for null que 
                    #indica que nao e un rotulo e se nao for nem un campo de texto deixando asim 
                    # soamente as instrucoes e os valores das variaveis                                                            
                    progComple.append(g)                    
        return progComple


    def programaBinaria(self):        
        simbolData = []
        programBinary = []        
        endAtual = 0
        endAtualFinal = 0

        fileData = open(self.arquivo, 'r')
        lines  = fileData.readlines()
        
        for x in range(2):
            if x==0: # Primeira pasagem pegando os rotulos e o endereço da memoria                
                for l in lines:                                                            
                    for g in l.split():                        
                        result = re.search(':', g)                                            
                        if result != None:
                            # print(endAtual,' Rotulos '+' - '+self.__splitGetData(g,':',0))
                            simbolData.append({
                                "rotulo" : self.__splitGetData(l,':',0),
                                "end" : endAtual
                            })
                        
                        if self.__conjInstrucoes(g.strip()) != None:
                            # print(endAtual,' - ',g)
                            if g != 'text':                            
                                endAtual += self.__conjInstrucoes(g.strip())['tamanho']

                        if g == 'data':                                    
                            endAtual = 128                                        
            else: # Segunda pasagem pasagem pegando os rotulos e o endereço da memoria                               
                endAtual = 0

                # Complete output binary file                 
                if (self.binaryfile) and self.namearq:
                    programBinaryCompl = []
                    afterHlt = []                    
                    count = 0
                    hltprogram = None
                    if len(self.__getJustInstructions(lines)) > 0:                        
                        for i in range(0, 258):                            
                            if i <= (len(self.__getJustInstructions(lines))-1):                                
                                justInstruc = self.__getJustInstructions(lines)[i]                                
                                if (self.__conjInstrucoes(justInstruc) != None) and (hltprogram == None):                                                                        
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
                        # print(programBinaryCompl)
                # Simple ouput file like the work we do in the classroom    
                else:                
                    for l in lines:                      
                        for g in l.split():
                            result = re.search(':', g)                                            
                            if result == None:                                                    
                                if g != 'text' and g != 'byte' and g != 'data':
                                    if self.__conjInstrucoes(g.strip()) != None:
                                        # print(endAtual,' Intrucoes ',self.__conjInstrucoes(g.strip()))                                    
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
                if self.desplay:
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
                if self.textfile and self.namearq: 
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
                if self.binaryfile and self.namearq:                     
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
    GenericAplication(arquivo=args.a, namearq=args.o, desplay=args.v, binaryfile=args.b, textfile=args.t).programaBinaria()
