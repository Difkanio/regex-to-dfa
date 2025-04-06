# Regex to DFA Converter

This project implements a converter that takes a **regular expression (regex)** as input and builds a corresponding **Deterministic Finite Automaton (DFA)** using Python. The tool is useful for understanding lexical analysis, automata theory, and how regex engines work under the hood.

## ✨ Features

- Parses regular expressions with operators: `|`, `*`, `+`, `?`, `()`, `{}`
- Takes in input of a regex, and a list of characters that represents the alphabet
- Builds NFA (Non-deterministic Finite Automaton)
- Converts NFA to DFA using subset construction (powerset method)
- Minimizes the resulting DFA
- Provides a visualization of the DFA (optional)
- Simulates input strings against the generated DFA

## 📂 Project Structure

- lexer.py: lexer that converts regex into tokens used by the parser
- parse.py: parser that uses tokens to create parse tree made of nodes
- parse_nodes.py: nodes used by the parser in the parse tree
- parse_tree_visualizer.py: optional tool that can print the parse tree in the terminal
- interpreter.py: converts the parse tree to a dfa
- finite_automata.py: used to represent the automatons created by the interpreter
