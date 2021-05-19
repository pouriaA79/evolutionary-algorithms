import numpy as np


class Game:
    def __init__(self, levels):
        # Get a list of strings as levels
        # Store level length to determine if a sequence of action passes all the steps

        self.levels = levels
        self.current_level_index = -1
        self.current_level_len = 0

    def load_next_level(self):
        self.current_level_index += 1
        self.current_level_len = len(self.levels[self.current_level_index])

    def get_score(self, actions):
        # Get an action sequence and determine the steps taken/score
        # Return a tuple, the first one indicates if these actions result in victory
        # and the second one shows the steps taken

        current_level = self.levels[self.current_level_index]
        steps = 0
        max_score = 0
        current_score = 0
        flag_end = True
        score = []

        for i in range(self.current_level_len):
            current_step = current_level[i]
            # jump in last step
            if current_step == '_' and actions[i] == '1' and i == self.current_level_len - 1:
                current_score += 1
            if (current_step == '_'):
                current_score += 1
            # destroy G
            elif current_step == 'G' and current_level[i - 1] != 'L' and i >= 1 and actions[i - 2] == '1':
                current_score += 2
            elif current_step == 'G' and actions[i - 1] == '1':
                current_score += 1
            elif current_step == 'L' and actions[i - 1] == '2':
                current_score += 1
            elif current_step == 'M' and actions[i - 1] == '1':
                current_score += 1
            elif current_step == 'M' and actions[i - 1] != '1':
                current_score += 2
            # extra jump
            # elif (current_step != 'G' or current_level[i - 1] == 'L') and actions[i - 2] == '1':
            #     current_score -= 0.5
            # elif current_step == '_' and actions[i - 1] == '1' and i == self.current_level_len - 2:
            #     current_score += 1
            #     print(current_score + 2)

            else:
                score.append(current_score)

                flag_end = False
                current_score = 0
        score.append(current_score)
        if flag_end:
            return max(score) + 5
        else:
            return max(score)



# g = Game(["____G_____"])
# g.load_next_level()

# This outputs (False, 4)
# print(g.get_score("1112220201"))

def read_file(name):
    file = open(name, 'r')
    str = file.readline()
    return len(str), str


def population(len):
    # chromosomes = [[random.randint(0,2) for i in range(len)] for j in range(200)]
    chromosomes = [[np.random.choice(np.arange(0, 3), p=[0.5, 0.25, 0.25]) for i in range(len)] for j in range(200)]
    return chromosomes


def convert_str(chro):
    chromosomes_str=[]
    for i in range(200):
        s = ""
        for j in range(length):
            s += str(chro[i][j])
        chromosomes_str.append(s)
    return chromosomes_str


def fitness(chromosomes, moves):
    g = Game([moves])
    g.load_next_level()
    scores=[]
    for i in range(200):
        print(chromosomes[i])
        scores.append(g.get_score(chromosomes[i]))
        print(scores[i])
    return scores



if __name__ == "__main__":
    file_name = "level3.txt"
    length, moves = read_file(file_name)
    chromosomes = population(length)
    chromosomes_str = convert_str(chromosomes)
    scores=fitness(chromosomes_str, moves)
    # print(scores)
