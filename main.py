import random

PERSON = 2
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


def generate_rand():

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
    sum_1 = 0
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
    return sum(inn) / len(inn)


def calc_pi(data, user, i, sum_consume):
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



def find_pi_max(data, user, i, sum_consume):
    # print 'find_pi_max in', i
    user_copy = user
    matrix_element = calc_pi(data, user, i, sum_consume)
    tmp1 = user[i]
    for status in range(0, 1 << PER_REQUEST):
        user_copy[i] = status
        tmp2 = calc_pi(data, user_copy, i, sum_consume)
        if tmp2 > matrix_element:
            matrix_element = tmp2
            tmp1 = status

    return tmp1


if __name__ == '__main__':

    # generate_rand()

    # read data from file
    data = []
    f = open("rand.txt", 'r')
    fin = f.readlines()
    sum_consume = 0
    for index in range(0, PERSON * PER_REQUEST):
        dat = fin[index].split("\t")
        satisfy = int(dat[0])
        consume = int(dat[1][:-1])
        sum_consume = consume
        data.append((satisfy, consume))

    user = []
    tmp = 0
    for i in range(0, PERSON):
        user.append(0)

    flag = False
    while not flag:
        for t in range(0, PERSON):
            tm = t
            tmp = find_pi_max(data, user, tm, sum_consume)
            if user[tm] != tmp:
                user[tm] = tmp
                flag = False
                break
            else:
                flag = True

    for i in range(0, PERSON):
        print str(user[i]) + '\t'

    print '\n'
    print calc_pi(data, user, -1, sum_consume)
