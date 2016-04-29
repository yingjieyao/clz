#coding=utf8
import random
import time
import copy

person = [2, 3, 150]
PER_SIZE_TIMES = 1 # 每个次数的人，运行多少次
PER_REQUEST = 2
SUM_SATISFY = 100
MAX_CONSUME = 1000

A = 1.5
B = 1
C = 1


class Need:
    satisfy = 0
    consume = 0

    def __init__(self, next_satisfy, next_consume):
        self.satisfy = next_satisfy
        self.consume = next_consume


def generate_rand(PERSON):

    out = open('rand.txt', 'w')
    for it in range(0, PERSON):
        ev = []
        cur_sum = 0
        for req in range(0, PER_REQUEST):
            tmp_satisfy = random.randint(1, SUM_SATISFY)
            tmp_consume = random.randint(1, MAX_CONSUME)
            cur_sum += tmp_satisfy
            ev.append((tmp_satisfy, tmp_consume))

        left = SUM_SATISFY
        for req in range(0, PER_REQUEST):
            tmp_satisfy = int(ev[req][0] * 100.0 / cur_sum + 0.5)
            if req == PER_REQUEST - 1:
                tmp_satisfy = left
            out.write(str(tmp_satisfy) + '\t' + str(ev[req][1]) + '\n')
            left -= tmp_satisfy
    out.close()


def variance(inn):
    length = len(inn)
    sum_1 = 0.0
    sum2 = 0.0
    if length == 0:
        return 0
    for i in range(0, length):
        sum_1 += inn[i]
        sum2 += inn[i] * inn[i]
    sum_1 /= length
    sum2 /= length
    return sum2 - sum_1 * sum_1


def average(inn):
    if len(inn) == 0:
        return 0
    return sum(inn) * 1.0 / len(inn)


def calc_pi(data, user, i, sum_consume, PERSON):
    tmp_satisfy = []
    tmp_consume = []
    for _ in range(0, PERSON):
        tmp_satisfy.append(0)
        tmp_consume.append(0)

    schema = 0
    for j in range(0, PERSON)[::-1]:
        schema <<= PER_REQUEST
        schema = schema | user[j]

    for it in range(0, PERSON * PER_REQUEST):
        if (schema >> it) & 1:
            tmp_satisfy[it / PER_REQUEST] += data[it][0]
            tmp_consume[it / PER_REQUEST] += data[it][1]

    if i != -1:
        return A * tmp_satisfy[i] / PERSON / 100.0 - B\
                / 2500.0 * variance(tmp_satisfy) - C * sum(tmp_consume) * 1.0\
                / sum_consume
    else:
        return A * average(tmp_satisfy) / 100.0 - B\
                / 2500.0 * variance(tmp_satisfy) - C * sum(tmp_consume) * 1.0\
                / sum_consume



def find_pi_max(data, user, i, sum_consume, PERSON):
    # print 'find_pi_max in', i
    user_copy = user
    matrix_element = calc_pi(data, user, i, sum_consume, PERSON)
    tmp1 = user[i]
    for status in range(1, 1 << PER_REQUEST):
        user_copy[i] = status
        tmp2 = calc_pi(data, user_copy, i, sum_consume, PERSON)
        if tmp2 > matrix_element:
            matrix_element = tmp2
            tmp1 = status

    return tmp1


def deal_with(PERSON):

    print 'deal with %d PERSONS' % PERSON
    generate_rand(PERSON)

    # read data from file
    data = []
    f = open("rand.txt", 'r')
    fin = f.readlines()
    sum_consume = 0
    for index in range(0, PERSON * PER_REQUEST):
        dat = fin[index].split("\t")
        satisfy = int(dat[0])
        consume = int(dat[1][:-1])
        sum_consume += consume
        data.append((satisfy, consume))

    start = time.clock()

    user = []
    tmp = 0
    for i in range(0, PERSON):
        user.append(0)

    flag = False
    while not flag:
        for t in range(0, PERSON):
            tm = t
            tmp = find_pi_max(data, copy.copy(user), tm, sum_consume, PERSON)
            if user[tm] != tmp:
                user[tm] = tmp
                flag = False
                break
            else:
                flag = True

    print "program run", time.clock() - start
    print "select ", user
    # for i in range(0, PERSON):
    #     print str(user[i]) + '\t'

    # print '\n'
    print 'result score: ', calc_pi(data, copy.copy(user), -1, sum_consume, PERSON)

if __name__ == '__main__':
    for PERSON in person:
        for ti in range(0, PER_SIZE_TIMES):
            deal_with(PERSON)
