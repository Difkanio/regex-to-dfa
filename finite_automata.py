count_automata = 0

class FiniteAutomaton():
    def __init__(self, transitions : dict, start_state, accepting_states : set):
        self.transitions = transitions
        self.start_state = start_state
        self.accepting_states = accepting_states
    
    # Complexity O(n) where n is the number of transitions in the automaton
    def __str__(self):
        result = ""
        result += str(self.start_state) + "\n"
        for (state, symbol), next_states in self.transitions.items():
            if symbol != "":
                if isinstance(next_states, set):
                    for ns in next_states:
                        result += str(state) + " " + str(symbol) + " " + str(ns) + "\n"
                else:
                    result += str(state) + " " + str(symbol) + " " + str(next_states) + "\n"

        if isinstance(self.accepting_states, set):
            for accepted_state in self.accepting_states:
                result += str(accepted_state) + " "
        else:
            result += str(self.accepting_states)
    
        return result

class DFA(FiniteAutomaton):
    pass

class NFA(FiniteAutomaton):
    pass

class eNFA(FiniteAutomaton):
    pass


# Union of two eNFAs
# Time complexity is O(n) where n = max{a1, a2} where a1 and a2 are the number of accepted states in the 2 eNFAs
def eNFA_union(nfa1 : eNFA, nfa2 : eNFA) -> eNFA:
    # Create a new start state and accept state
    start_state = "start"
    accept_state = "accept"

    # Rename the states of the NFAs to avoid conflicts
    nfa1_renamed = changeName(nfa1, "a")
    nfa2_renamed = changeName(nfa2, "b")

    union = eNFA({}, start_state, {accept_state})

    # Add transitions from the new start state to the start states of the NFAs
    union.transitions.setdefault((start_state, "ε"), set()).update({nfa1_renamed.start_state, nfa2_renamed.start_state})

    union.transitions.update(nfa1_renamed.transitions)
    union.transitions.update(nfa2_renamed.transitions)

    # Add transitions from the accepting states of the NFAs to the new accept state
    if isinstance(nfa1_renamed.accepting_states, set):
        for accepted_state in nfa1_renamed.accepting_states:
            union.transitions.setdefault((accepted_state, "ε"), set()).add(accept_state)
    else:
        union.transitions.setdefault((nfa1_renamed.accepting_states, "ε"), set()).add(accept_state)
    
    if isinstance(nfa2_renamed.accepting_states, set):
        for accepted_state in nfa2_renamed.accepting_states:
            union.transitions.setdefault((accepted_state, "ε"), set()).add(accept_state)
    else:
        union.transitions.setdefault((nfa2_renamed.accepting_states, "ε"), set()).add(accept_state)

    return changeName(union)

# Concatenation of two eNFAs
# Time complexity is O(n) where n = max{a1, a2} where a1 and a2 are the number of accepted states in the 2 eNFAs
def eNFA_concat(nfa1 : eNFA, nfa2 : eNFA) -> eNFA:
    # Create a new start state and accept state
    start_state = "start"
    accept_state = "accept"

    # Rename the states of the NFAs to avoid conflicts
    nfa1_renamed = changeName(nfa1, "a")
    nfa2_renamed = changeName(nfa2, "b")

    concat = eNFA({}, start_state, {accept_state})

    concat.transitions.setdefault((start_state, "ε"), set()).update({nfa1_renamed.start_state})
    
    concat.transitions.update(nfa1_renamed.transitions)
    concat.transitions.update(nfa2_renamed.transitions)

    if isinstance(nfa1_renamed.accepting_states, set):
        for accepted_state in nfa1_renamed.accepting_states:
            concat.transitions.setdefault((accepted_state, "ε"), set()).add(nfa2_renamed.start_state)
    else:
        concat.transitions.setdefault((nfa1_renamed.accepting_states, "ε"), set()).add(nfa2_renamed.start_state)
    
    if isinstance(nfa2_renamed.accepting_states, set):
        for accepted_state in nfa2_renamed.accepting_states:
            concat.transitions.setdefault((accepted_state, "ε"), set()).add(accept_state)
    else:
        concat.transitions.setdefault((nfa2_renamed.accepting_states, "ε"), set()).add(accept_state)
    

    return changeName(concat)

# Kleene star of an eNFA
# Time complexity is O(n) where n is the number of accepted states in the eNFA
def eNFA_star(nfa : eNFA) -> eNFA:
    start_state = "start"

    nfa_renamed = changeName(nfa, "a")

    star = eNFA({}, start_state, {start_state})

    star.transitions.setdefault((start_state, "ε"), set()).update({nfa_renamed.start_state})

    for accepted_state in nfa_renamed.accepting_states:
        star.transitions.setdefault((accepted_state, "ε"), set()).add(nfa_renamed.start_state)
        star.accepting_states.add(accepted_state)

    star.transitions.update(nfa_renamed.transitions)

    return changeName(star)                                         

#Function that returns the eNfa repeated n times
#Time complexity is O(m * n) where n is the number of times the eNFA is repeated
#and m is the complexity of the eNFA_concat function
def eNFA_repeated(nfa : eNFA, num_repeats : int) -> eNFA:
    if num_repeats == 0:
        return eNFA({}, "start", {"start"})

    if num_repeats == 1:
        return nfa

    repeated = nfa
    for i in range(num_repeats - 1):
        repeated = eNFA_concat(repeated, nfa)

    return changeName(repeated)
    
# Change the name of the states of an eNFA
# Time complexity is O(n) where n is the number of transitions in the eNFA
def changeName(fa : FiniteAutomaton, string : str = "") -> FiniteAutomaton:
    num_states = 0
    visited_states = dict()

    new_start_state = "q" + string + str(num_states)
    visited_states[fa.start_state] = new_start_state
    num_states += 1

    new_accepting_states : set = set()


    for accepted_state in fa.accepting_states:
        if accepted_state in visited_states:
            new_accepting_states.add(visited_states[accepted_state])
        else:
            new_accepting_states.add("q" + string + str(num_states))
            visited_states[accepted_state] = "q" + string + str(num_states)
            num_states += 1

    renamed_automaton = FiniteAutomaton({}, new_start_state, new_accepting_states)

    for (state, symbol), next_states in fa.transitions.items():
        if state not in visited_states:
            visited_states[state] = "q" + string + str(num_states)
            num_states += 1
        
        if isinstance(next_states, set):
            for ns in next_states:
                if ns not in visited_states:
                    visited_states[ns] = "q" + string + str(num_states)
                    num_states += 1
                renamed_automaton.transitions.setdefault((visited_states[state], symbol), set()).add(visited_states[ns])
        else:
            if next_states not in visited_states:
                visited_states[next_states] = "q" + string + str(num_states)
                num_states += 1
            renamed_automaton.transitions.setdefault((visited_states[state], symbol), set()).add(visited_states[next_states])

    return renamed_automaton

def printAutomaton(fa : FiniteAutomaton):
    print("--------------------")
    print("Start state: ", fa.start_state)
    print("Transitions:")
    for (state, symbol), next_states in fa.transitions.items():
        if isinstance(next_states, set):
            for ns in next_states:
                print(f"({state}, {symbol}) -> {ns}")
        else:
            print(f"({state}, {symbol}) -> {next_states}")
    
    print("Accepting states: ", end="")
    for accepted_state in fa.accepting_states:
        print(accepted_state, end=" ")
    print(  )
    print("--------------------")

# Construct an eNFA that accepts a single symbol
# Time complexity is O(n) where n is the number of symbols in the alphabet
def construct_eNFA(alphabet : list[str], accepted_symbol) -> eNFA:
    enfa = eNFA({}, "START", ["ACCEPT"])

    for symbol in alphabet:
        if symbol == accepted_symbol:
            enfa.transitions.setdefault(("START", symbol), set()).add("ACCEPT")
        else:
            enfa.transitions.setdefault(("START", symbol), set()).add("DEAD_STATE")
        
        enfa.transitions.setdefault(("DEAD_STATE", symbol), set()).add("DEAD_STATE")
        enfa.transitions.setdefault(("ACCEPT", symbol), set()).add("DEAD_STATE")
    
    return enfa

#Calculate the epsilon closure of a state
#Time complexity is O(n) where n is the number of transitions in the eNFA
def epsilon_closure(start_state, transitions) -> list: 
    stack = [start_state]
    closure = [start_state]

    while stack:
        state = stack.pop()
        for (s, symbol), next_states in transitions.items():
            if symbol == "ε" and s == state:
                if isinstance(next_states, set):
                    for ns in next_states:
                        if ns not in closure:
                            closure.append(ns)
                            stack.append(ns)
                else:
                    if next_states not in closure:
                        closure.append(next_states)
                        stack.append(next_states)
                    
    return closure

#Convert an eNFA to a DFA
#Time complexity is O(n * m) where n is the number of transitions in the eNFA
#and m is the complexity of the epsilon_closure function
def eNFA_to_DFA(enfa : eNFA) -> DFA:
    global count_automata
    count_automata = 0
    dfa = DFA({}, "q0", set())
    visited_states = dict()

    start_state = enfa.start_state
    start_closure = epsilon_closure(start_state, enfa.transitions)
    visited_states[frozenset(start_closure)] = "q" + str(count_automata)
    count_automata += 1

    stack = [start_closure]
    while stack:
        closure = stack.pop()
        for symbol in enfa.transitions:
            if symbol[1] == "ε":
                continue

            next_closure = set()
            for state in closure:
                if (state, symbol[1]) in enfa.transitions:
                    next_states = enfa.transitions[(state, symbol[1])]
                    if isinstance(next_states, set):
                        for ns in next_states:
                            next_closure.update(epsilon_closure(ns, enfa.transitions))
                    else:
                        next_closure.update(epsilon_closure(next_states, enfa.transitions))
            
            if not next_closure:
                continue

            if frozenset(next_closure) not in visited_states:
                visited_states[frozenset(next_closure)] = "q" + str(count_automata)
                count_automata += 1
                stack.append(next_closure)

            dfa.transitions.setdefault((visited_states[frozenset(closure)], symbol[1]), set()).add(visited_states[frozenset(next_closure)])
    
    for state in visited_states:
        if any(accept_state in state for accept_state in enfa.accepting_states):
            dfa.accepting_states.add(visited_states[state])
    
    return dfa

#Minimize a DFA
#Time complexity is O(n^2) where n is the number of states in the DFA
def minimize_dfa(dfa):
    # Step 1: Remove unreachable states
    reachable = set()
    stack = [dfa.start_state]
    while stack:
        state = stack.pop()
        if state not in reachable:
            reachable.add(state)
            for (from_state, symbol), to_states in dfa.transitions.items():
                if from_state == state:
                    stack.extend(to_states)

    dfa.transitions = {k: v for k, v in dfa.transitions.items() if k[0] in reachable}
    dfa.accepting_states = {s for s in dfa.accepting_states if s in reachable}

    # Step 2: Merge equivalent states
    partition = [set(dfa.accepting_states), reachable - set(dfa.accepting_states)]
    new_partition = []

    while True:
        new_partition = []
        for block in partition:
            split = {}
            for state in block:
                key = []
                for symbol in {sym for (_, sym) in dfa.transitions}:
                    next_state = None
                    for (from_state, sym), to_states in dfa.transitions.items():
                        if from_state == state and sym == symbol:
                            next_state = list(to_states)[0]  # DFA should have exactly one next state per symbol
                            break
                    if next_state is not None:
                        for i, p in enumerate(partition):
                            if next_state in p:
                                key.append(i)
                                break
                    else:
                        key.append(None)
                key = tuple(key)
                if key not in split:
                    split[key] = set()
                split[key].add(state)
            new_partition.extend(split.values())
        if new_partition == partition:
            break
        partition = new_partition

    new_states = {frozenset(block): f"q{i}" for i, block in enumerate(partition)}
    start_state_block = next(block for block in partition if dfa.start_state in block)
    minimized_dfa = DFA({}, new_states[frozenset(start_state_block)], set())

    for block in partition:
        representative = next(iter(block))
        for symbol in {sym for (_, sym) in dfa.transitions}:
            next_state = None
            for (from_state, sym), to_states in dfa.transitions.items():
                if from_state == representative and sym == symbol:
                    next_state = list(to_states)[0]
                    break
            if next_state is not None:
                for p in partition:
                    if next_state in p:
                        minimized_dfa.transitions[(new_states[frozenset(block)], symbol)] = new_states[frozenset(p)]
                        break

        if block & dfa.accepting_states:
            minimized_dfa.accepting_states.add(new_states[frozenset(block)])

    return changeName(minimized_dfa)