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