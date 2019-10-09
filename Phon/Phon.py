# coding: UTF-8
__author__ = 'Steeve'
__version__ = '1.0.0'

import os
import re
import argparse

class GenericAplication():
    def __init__(self, arquivo):
        self.arquivo = arquivo

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
                return rot['rotulo']                           
        return 'No Existe este rotulo'

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
            'opcode' : '100',# de A0  para cima
            'name': 'XOR',
            'tamanho': 2
        },{
            'opcode' : '110',
            'name': 'JMP',
            'tamanho': 2
        },{
            'opcode' : '120',
            'name': 'JEQ',
            'tamanho': 2
        },{
            'opcode' : '130',
            'name': 'JG',
            'tamanho': 2
        },{
            'opcode' : '140',
            'name': 'JL',
            'tamanho': 2
        },{
            'opcode' : '150',
            'name': 'HLT',
            'tamanho': 1
        }]

        for inst in conjinstru:            
            if name == inst['name']:                                
                return inst
        return None

    def programaBinaria(self):        
        simbolData = []
        instrucoes = []
        passo = 0

        fileData = open(self.arquivo, 'r')
        lines  = fileData.readlines()
        
        for x in range(2):
            if x==0:
                # Primeira pasagem pegando os rotulos e o endereço da memoria

                for l in lines: 
                    if (len(l.split()) == 1) and (l.split()[0] == 'text') and (endAtual == 0):
                        endAtual = 0                         
                    if (len(l.split()) == 1) and (l.split()[0] == 'data'):
                        endAtual = 128 

                    if (len(l.split()) == 1) and (l.split()[0] != 'text') and (l.split()[0] != 'data'):
                        print(endAtual,' - ',l.split()[0])
                        if endAtual >= 128:
                            endAtual += 1;
                        else:
                            endAtual += 2;


                    elif (len(l.split()) == 1) and (l.split()[0] == 'data'):
                        endAtual = 128
                    
                    elif (len(l.split()) > 1):                                                                    
                        result = re.search(':', l)
                        if result != None:                            
                            print(endAtual,' - ',self.__splitGetData(l,':',0))                      
                            simbolData.append({
                                "rotulo" : self.__splitGetData(l,':',0),
                                "end" : 5
                            })
                        else:
                            for g in l.split():
                                print(endAtual,' - ',g)
                                if endAtual >= 128:
                                    endAtual += 1;
                                else:
                                    endAtual += 2;
                            # print(l.split())
                fileData.close()                
                # print(self.__getRotulo('loop', simbolData))            
                print(self.__conjInstrucoes('STR'))                
            else: 
                # Conteudo da segunda pasagem no codigo                
                pass


if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--arq', required=True, help='ASAMBLY file with data')

    args = parser.parse_args()
    GenericAplication(arquivo=args.arq).programaBinaria()

    # Example
    # python Phon.py --arq data.txt
# print(len(l.split()),' - ',l.split())                                        