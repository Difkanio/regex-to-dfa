class Token:
    def __init__(self, token_type: str, value: str):
        self.token_type: str = token_type
        self.value: str = value

class Lexer:
    def  __init__(self, input : str, alphabet : list[str]):
        self.source : str = input
        self.source_position : int = 0
        self.alphabet = alphabet
        self.alphabet.append( 'ε')
        self.special_symobls = ['+', '*', '(', ')', '{' , '}', ',']
        self.num_parentesis : int = 0

    #Procces substring to find next token
    #Compplexity O(n^2) where n is the length of the string
    def get_symbol_token(self, string : str) -> list[str]:
        token_set = set(self.alphabet)
        n = len(string)
        dp = [False] * (n + 1)
        dp[0] = True
        tokenized_result = [[] for _ in range(n + 1)]

        for i in range(1, n + 1):
            for j in range(i):
                if dp[j] and string[j:i] in token_set:
                    dp[i] = True
                    tokenized_result[i] = tokenized_result[j] + [string[j:i]]
                    break

        if dp[n]:
            return tokenized_result[n]
        else:
            raise LexerError(f"String {string} cannot be formed by alpabet {self.alphabet}", self.source, string)
        
    #Check if string can be formed by alphabet unambigously
    #Complexity O(n^2) where n is the length of the string
    def check_ambigous_string(self, string: str):
        n = len(string)
        
        dp = [0] * (n + 1)
        
        dp[0] = 1
        
        alphabet_set = set(self.alphabet)
        
        for i in range(1, n + 1):
            for word in alphabet_set:
                if i >= len(word) and string[i-len(word):i] == word:
                    dp[i] += dp[i-len(word)]
        
        if dp[n] < 1:
            raise LexerError(f"String {string} cannot be formed by alpabet {self.alphabet}", string, string)
        if dp[n] > 1:
            raise LexerError(f"String {string} can be formed by alpabet {self.alphabet} in more than one way", string, string)
    
    #See what the next token is
    def peek(self) -> Token:
        old_position: int = self.source_position
        token: Token = self.next()
        self.source_position = old_position
        return token

    #Get next token
    #Worst case complexity O(n^3) where n is the length of the string
    def next(self) -> Token:
        buffer : str = ""

        #Check EOF
        if self.source_position == len(self.source):
            return Token("EOF","EOF")
        elif self.source_position > len(self.source):
            raise Exception()
        
        if self.source[self.source_position] == "ε":
            token = Token("SYMBOL", self.source[self.source_position])
            self.source_position += 1
            return token

        #Check for escape character
        if self.source[self.source_position] == '\\':
            self.source_position += 1
            if self.source[self.source_position] not in self.special_symobls:
                raise LexerError(f'Symbol {self.source[self.source_position]} in {self.source} is not meta character',self.source, self.source[self.source_position])
            token = Token("SYMBOL",self.source[self.source_position])
            self.source_position += 1
            return token

        #Get integer for {
        if self.source_position > 0 and self.source[self.source_position].isalnum() and self.source[self.source_position-1] == "{":
            while self.source_position < len(self.source) and self.source[self.source_position].isalnum():
                buffer += self.source[self.source_position]
                self.source_position += 1
            if not buffer.isnumeric():
                raise LexerError(f'Unknown symbol occured in curly brackets', buffer, buffer)
            
            return Token("INT", buffer)
            
        #Get integer for }
        if self.source_position > 0 and self.source[self.source_position].isalnum() and self.source[self.source_position-1] == ",":
            while self.source_position < len(self.source) and self.source[self.source_position].isalnum():
                buffer += self.source[self.source_position]
                self.source_position += 1
            if not buffer.isnumeric():
                raise LexerError(f'Unknown symbol occured in curly brackets', buffer, buffer)
            
            return Token("INT", buffer)
        
        #Check for symbol
        if self.source[self.source_position].isalnum():
            while self.source_position < len(self.source) and self.source[self.source_position].isalnum():
                buffer += self.source[self.source_position]
                self.source_position += 1
            
            self.check_ambigous_string(buffer)
            buffer_list = self.get_symbol_token(buffer)
            token = Token("SYMBOL", buffer_list[0])
            self.source_position = self.source_position - len(buffer) + len(buffer_list[0])
            return token

        #Check for operator
        if self.source[self.source_position] in self.special_symobls:
            if self.source[self.source_position] == '(':
                self.num_parentesis += 1
            if self.source[self.source_position] == ')':
                self.num_parentesis -= 1
            
            if self.num_parentesis < 0:
                raise LexerError(f'Unbalanced parentesis in {self.source} in position {self.source_position}', self.source, self.source)

            operator : str = self.source[self.source_position]
            self.source_position += 1
            return Token(operator,operator)
        
        raise LexerError(f'Unkonwn symbol {self.source[self.source_position]} in position {self.source_position}', self.source, self.source)


class LexerError(ValueError):
    def __init__(self, message: str, string: str, token: str):
        self.message: str = message
        self.string: str = string
        self.token: str = token