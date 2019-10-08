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


    def programaBinaria(self):
        pgbinary = []

        fileData = open(self.arquivo, 'r')
        lines  = fileData.readlines()
        
        for x in range(2):

            if x==0:
                for l in lines:
                    # print(l.split())
                    result = re.search(':', l)
                    if result != None:
                        print(self.__splitGetData(l,':',0))        

                fileData.close()
                print('Primeiro paso ',x);
            else:                
                print('Segundo paso ',x);


if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--arq', required=True, help='ASAMBLY file with data')

    args = parser.parse_args()
    GenericAplication(arquivo=args.arq).programaBinaria()

    # Example
    # python Phon.py --arq data.txt
