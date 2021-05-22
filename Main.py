import copy
import random

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

    def get_score(self, actions, flag_eval):
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
        if flag_eval and flag_end:
            return max(score) + 5, True
        elif flag_eval and not flag_end:
            return max(score), False
        elif flag_end and not flag_eval:
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


def population(len, chromosome_num):
    # chromosomes = [[random.randint(0,2) for i in range(len)] for j in range(200)]
    chromosome = [[np.random.choice(np.arange(0, 3), p=[0.5, 0.25, 0.25]) for i in range(len)] for j in
                  range(chromosome_num)]
    return chromosome


def convert_str(chro, num, length):
    chromosomes_s = []
    for i in range(num):
        s = ""
        for j in range(length):
            s += str(chro[i][j])
        chromosomes_s.append(s)
    return chromosomes_s


def fitness(chromosome, moves, num_chromosome, eval):
    g = Game([moves])
    g.load_next_level()
    scr = []
    final_result = {}
    for i in range(num_chromosome):
        # print(chromosome[i])
        if eval:
            s, flag_end = g.get_score(chromosome[i], True)
            final_result.setdefault(i, []).append(s)
            final_result.setdefault(i, []).append(flag_end)
            final_result.setdefault(i, []).append(chromosome[i])
        else:
            scr.append(g.get_score(chromosome[i], False))

        # print(scr[i])
    if not eval:
        return scr
    else:
        return final_result


def selection(scr, chromosome):
    temp_scores = scr
    temp_scores = np.sort(temp_scores)
    select_score = []
    select_chromosome_score = {}
    selected_number = []
    for i in range(int(len(scr) / 2)):
        for j in range(len(scr)):
            if scr[j] == temp_scores[-i - 1] and j not in selected_number:
                selected_number.append(j)
                select_score.append(scr[j])
                select_chromosome_score.setdefault(i, []).append(scr[j])
                select_chromosome_score.setdefault(i, []).append(chromosome[j])

                break
    # print(select_score)
    return select_score, select_chromosome_score


def crossover(scores, chromosome, num):
    cross = chromosome.copy()
    # print(cross)
    # print(cross.get(0)[1])
    new_chromosome = []

    for i in range(int(num / 10)):
        new_chromosome.append(cross.get(i)[1])

    for i in range(len(scores) - int(num / 20)):
        p1 = random.randint(0, 99)
        p2 = random.randint(0, 99)
        parent1 = chromosome.get(p1)[1]
        parent2 = chromosome.get(p2)[1]
        c1 = copy.deepcopy(parent1)
        c2 = copy.deepcopy(parent2)
        # print(c1 , c2)
        pt = random.randint(1, len(parent1) - 2)
        # print(pt)
        c1 = parent1[:pt] + parent2[pt:]
        c2 = parent2[:pt] + parent1[pt:]
        # print(c1 , c2 , pt )
        new_chromosome.append(c1)
        new_chromosome.append(c2)

    return new_chromosome


def mutation(chromosome):
    new_pass = []

    for i in range(int(0.25 * len(chromosome))):
        str = ""
        s = []
        if i in new_pass:
            continue
        else:
            new_pass.append(i)
        pt = random.randint(1, len(chromosome[i]) - 1)
        if chromosome[i][pt] == "1":
            for j in range(len(chromosome[i])):
                if j == pt:
                    s.append("0")
                else:
                    s.append(chromosome[i][j])

            chromosome[i] = str.join(s)
        else:
            x = np.random.choice(np.arange(0, 2), p=[0.7, 0.3])
            if x == 1:
                for j in range(len(chromosome[i])):
                    if j == pt:
                        s.append("2")
                    else:
                        s.append(chromosome[i][j])


            else:
                for j in range(len(chromosome[i])):
                    if j == pt:
                        s.append("0")
                    else:
                        s.append(chromosome[i][j])
            chromosome[i] = str.join(s)

    return chromosome


def evaluation(chromosome, moves, num_chromosome):
    final = fitness(chromosome, moves, num_chromosome, True)
    sort = sorted(final.items(), key=lambda x: x[1], reverse=True)

    return sort


def genetic(file_name, chromosome_num, n_iters):
    length, moves = read_file(file_name)
    chromosomes1 = population(length, chromosome_num)
    chromosomes_str = convert_str(chromosomes1, chromosome_num, length)
    scores_level = []
    for i in range(n_iters):
        print(i)
        if i == 0:
            scores = fitness(chromosomes_str, moves, chromosomes_num, False)
        else:
            scores = fitness(chromosomes_str, moves, chromosomes_num, False)
        scores_level.append(sum(scores) / len(scores))
        if abs(scores_level[i] - scores_level[i - 1] )< 0.00001 and i>0:
            print(scores_level[i], scores_level[i - 1],scores_level[i] - scores_level[i - 1] )
            break
        selected_score, selected_chromosomes = selection(scores, chromosomes_str)
        new_choromosomes = crossover(selected_score, selected_chromosomes, chromosome_num)
        chromosomes_str = mutation(new_choromosomes)
    sort_answer = evaluation(chromosomes_str, moves, chromosome_num)

    for i in range(len(sort_answer)):
        if sort_answer[i][1][1]:
            return sort_answer[i][1][0], sort_answer[i][1][1], sort_answer[i][1][2]

    return sort_answer[0][1][0], sort_answer[0][1][1], sort_answer[0][1][2]


if __name__ == "__main__":
    file_names = "level10.txt"
    chromosomes_num = 200
    n_iter = 500
    score, end, chromosome = genetic(file_names, chromosomes_num, n_iter)
    if end :
        print("pass the level with " + str(score)+" score and  with "+chromosome+ " moves.")
    else:
        print("cant pass the level best score : " + str(score) + "  with " + chromosome + " moves.")
