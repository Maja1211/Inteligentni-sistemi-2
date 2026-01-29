import random
import time
import math

class Agent:
    ident = 0

    def __init__(self):
        self.id = Agent.ident
        Agent.ident += 1

    def get_chosen_action(self, state, max_depth):
        pass


class RandomAgent(Agent):
    def get_chosen_action(self, state, max_depth):
        time.sleep(0.5)
        actions = state.get_legal_actions()
        return actions[random.randint(0, len(actions) - 1)]


class GreedyAgent(Agent):
    def get_chosen_action(self, state, max_depth):
        time.sleep(0.5)
        actions = state.get_legal_actions()
        best_score, best_action = None, None
        for action in actions:
            new_state = state.generate_successor_state(action)
            score = new_state.get_score(state.get_on_move_chr())
            if (best_score is None and best_action is None) or score > best_score:
                best_action = action
                best_score = score
        return best_action

class MinimaxAgent(Agent):

    def get_chosen_action(self, state, max_depth):
        import math
        time.sleep(0.5)

        moj_igrac_ord = state.get_on_move_ord()

        def minimax(stanje, dubina):
            if stanje.is_goal_state() or dubina == max_depth:
                moj = chr(ord('A') + moj_igrac_ord)
                igraci = list(state.spaceships_positions_dict.keys())
                protivnik = next(p for p in igraci if p != moj)

                return stanje.get_score(moj) - stanje.get_score(protivnik)

            trenutni_igrac_ord = stanje.get_on_move_ord()

            if trenutni_igrac_ord == moj_igrac_ord:
                # MAX
                najbolja_vrednost = -math.inf
                for akcija in stanje.get_legal_actions():
                    najbolja_vrednost = max(
                        najbolja_vrednost,
                        minimax(
                            stanje.generate_successor_state(akcija),
                            dubina + 1
                        )
                    )
                return najbolja_vrednost
            else:
                # MIN
                najbolja_vrednost = math.inf
                for akcija in stanje.get_legal_actions():
                    najbolja_vrednost = min(
                        najbolja_vrednost,
                        minimax(
                            stanje.generate_successor_state(akcija),
                            dubina + 1
                        )
                    )
                return najbolja_vrednost

        najbolja_akcija = None
        najbolja_vrednost = -math.inf

        for akcija in state.get_legal_actions():
            vrednost = minimax(
                state.generate_successor_state(akcija),
                1
            )
            if vrednost > najbolja_vrednost:
                najbolja_vrednost = vrednost
                najbolja_akcija = akcija

        return najbolja_akcija


class MinimaxABAgent(Agent):

    def get_chosen_action(self, state, max_depth):
        import math
        time.sleep(0.5)

        moj_igrac_ord = state.get_on_move_ord()

        def minimax_ab(stanje, dubina, alfa, beta):
            if stanje.is_goal_state() or dubina == max_depth:
                moj = chr(ord('A') + moj_igrac_ord)
                igraci = list(state.spaceships_positions_dict.keys())
                protivnik = next(p for p in igraci if p != moj)

                return stanje.get_score(moj) - stanje.get_score(protivnik)

            trenutni_igrac_ord = stanje.get_on_move_ord()

            if trenutni_igrac_ord == moj_igrac_ord:
                # MAX
                najbolja_vrednost = -math.inf
                for akcija in stanje.get_legal_actions():
                    vrednost = minimax_ab(
                        stanje.generate_successor_state(akcija),
                        dubina + 1,
                        alfa,
                        beta
                    )
                    najbolja_vrednost = max(najbolja_vrednost, vrednost)
                    alfa = max(alfa, najbolja_vrednost)
                    if alfa >= beta:
                        break
                return najbolja_vrednost
            else:
                # MIN
                najbolja_vrednost = math.inf
                for akcija in stanje.get_legal_actions():
                    vrednost = minimax_ab(
                        stanje.generate_successor_state(akcija),
                        dubina + 1,
                        alfa,
                        beta
                    )
                    najbolja_vrednost = min(najbolja_vrednost, vrednost)
                    beta = min(beta, najbolja_vrednost)
                    if alfa >= beta:
                        break
                return najbolja_vrednost

        najbolja_akcija = None
        najbolja_vrednost = -math.inf
        alfa = -math.inf
        beta = math.inf

        for akcija in state.get_legal_actions():
            vrednost = minimax_ab(
                state.generate_successor_state(akcija),
                1,
                alfa,
                beta
            )
            if vrednost > najbolja_vrednost:
                najbolja_vrednost = vrednost
                najbolja_akcija = akcija
            alfa = max(alfa, najbolja_vrednost)

        return najbolja_akcija


class MaxNAgent(Agent):

    def get_chosen_action(self, state, max_depth):
        import math
        time.sleep(0.5)

        igraci = list(state.spaceships_positions_dict.keys())
        indeks_mog_igraca = igraci.index(state.get_on_move_chr())

        def maxn(stanje, dubina):
            if stanje.is_goal_state() or dubina == 0:
                return tuple(stanje.get_score(i) for i in igraci)

            trenutni_igrac = stanje.get_on_move_chr()
            indeks_trenutnog = igraci.index(trenutni_igrac)

            najbolja_torka = None
            najbolja_vrednost = -math.inf

            for akcija in stanje.get_legal_actions():
                novo_stanje = stanje.generate_successor_state(akcija)
                torka = maxn(novo_stanje, dubina - 1)

                if torka[indeks_trenutnog] > najbolja_vrednost:
                    najbolja_vrednost = torka[indeks_trenutnog]
                    najbolja_torka = torka

            return najbolja_torka

        najbolja_akcija = None
        najbolja_vrednost = -math.inf

        for akcija in state.get_legal_actions():
            novo_stanje = state.generate_successor_state(akcija)
            torka = maxn(novo_stanje, max_depth - 1)

            if torka[indeks_mog_igraca] > najbolja_vrednost:
                najbolja_vrednost = torka[indeks_mog_igraca]
                najbolja_akcija = akcija

        return najbolja_akcija


#py .\main.py MinimaxAgent,MaxNAgent example_map.txt 10 0 5
#py .\main.py MinimaxABAgent,MinimaxABAgent example_map.txt 10 0 5
#py .\main.py MinimaxAgent,MinimaxAgent example_map.txt 10 0 5
# py .\main.py MaxNAgent,MaxNAgent four_player_map.txt 10 0 5
# py .\main.py MaxNAgent,MaxNAgent example_map.txt 10 0 5

