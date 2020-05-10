import random
import os


def successornot():    # 根据随机数种子产生随机数，已验证过1000000000次，完全随机且概率完全相等
    random.seed()
    a1 = random.random()
    randomNum = (random.uniform(0, 1))
    random.seed(a1 + randomNum)
    a = (random.random())*100
    return a


def judge(judge_x):    # 该函数为查找强化成功率和强化消耗
    if judge_x < 3:
        S_rate = 100
        stone = 2
        potion = 0
    elif judge_x < 5:
        S_rate = 90
        stone = 3
        potion = 0
    elif judge_x == 5:
        S_rate = 80
        stone = 4
        potion = 1
    elif judge_x == 6:
        S_rate = 70
        stone = 4
        potion = 1
    elif judge_x == 7:
        S_rate = 60
        stone = 4
        potion = 1
    elif judge_x == 8:
        S_rate = 55
        stone = 5
        potion = 2
    elif judge_x == 9:
        S_rate = 50
        stone = 5
        potion = 2
    elif judge_x == 10:
        S_rate = 45
        stone = 5
        potion = 3
    elif judge_x == 11:
        S_rate = 40
        stone = 5
        potion = 3
    elif judge_x == 12:
        S_rate = 20
        stone =6
        potion = 4
    elif judge_x == 13:
        S_rate = 16
        stone = 6
        potion = 4
    elif judge_x == 14:
        S_rate = 15
        stone = 7
        potion = 5
    elif judge_x == 15:
        S_rate = 14
        stone = 7
        potion = 5
    elif judge_x == 16:
        S_rate = 13
        stone = 8
        potion = 6
    elif judge_x == 17:
        S_rate = 10
        stone = 8
        potion = 6
    elif judge_x == 18:
        S_rate = 8
        stone = 9
        potion = 7
    elif judge_x == 19:
        S_rate = 1
        stone = 9
        potion = 7
    else:
        S_rate = 0
    return S_rate, stone, potion


def data_rebound(judge_x, a, b):   #该函数用来确定复原消耗的复原钢和ap，a表示(0=90，1=95，2=100），b（0=武器，1=防具)
    iron = 0
    ap = 0
    if a == 0:
        if b == 0:
            if judge_x == 10:
                iron = 3
                ap = 0
            elif judge_x == 11:
                iron = 4
                ap = 0
            elif judge_x == 12:
                iron = 6
                ap = 0
            elif judge_x == 13:
                iron  = 9
                ap = 0
            elif judge_x == 14:
                iron = 12
                ap = 0
        if b == 1:
            if judge_x == 10:
                iron = 1
                ap = 0
            elif judge_x == 11:
                iron = 2
                ap = 0
            elif judge_x == 12:
                iron = 4
                ap = 0
            elif judge_x == 13:
                iron  = 6
                ap = 0
            elif judge_x == 14:
                iron = 7
                ap = 0
    elif a == 1:
        if b == 0:
            if judge_x == 10:
                iron = 8
                ap = 0
            elif judge_x == 11:
                iron = 14
                ap = 0
            elif judge_x == 12:
                iron = 21
                ap = 0
            elif judge_x == 13:
                iron = 29
                ap = 0
            elif judge_x == 14:
                iron = 40
                ap = 0
        if b == 1:
            if judge_x == 10:
                iron = 4
                ap = 0
            elif judge_x == 11:
                iron = 6
                ap = 0
            elif judge_x == 12:
                iron = 9
                ap = 0
            elif judge_x == 13:
                iron = 13
                ap = 0
            elif judge_x == 14:
                iron = 18
                ap = 0
    elif a == 2:
        if b == 0:
            if judge_x == 10:
                iron = 12
                ap = 0
            elif judge_x == 11:
                iron = 22
                ap = 0
            elif judge_x == 12:
                iron = 34
                ap = 0
            elif judge_x == 13:
                iron = 46
                ap = 0
            elif judge_x == 14:
                iron = 60
                ap = 0
        if b == 1:
            if judge_x == 10:
                iron = 8
                ap = 0
            elif judge_x == 11:
                iron = 12
                ap = 0
            elif judge_x == 12:
                iron = 18
                ap = 0
            elif judge_x == 13:
                iron = 26
                ap = 0
            elif judge_x == 14:
                iron = 34
                ap = 0
    return iron, ap


def strengthen(S_rate, a):    # 是否强化成功
    if S_rate >= a:
        b = 1
    else:
        b = 0
    return b


def protectornot(judge_x, prot, b):  # 根据是否有保护石以及目前强化等级进行成功+1以及失败惩罚
    Destruction = 0
    prot_stone = 0
    prot_stone_g = 0
    bind_able = 0
    re_judge = judge_x
    if judge_x < 8:
        if b == 1:
            judge_x = judge_x+1
        else:
            if prot == 0:
                judge_x = judge_x
                prot_stone = 1
            elif prot == 1:
                judge_x = judge_x-1
                prot_stone_g = 1
                bind_able = 1
            else:
                if judge_x < 5:
                    judge_x = judge_x-1
                else:
                    judge_x = 0
    elif judge_x == 11:
        if b == 1:
            judge_x = judge_x+1
        else:
            if prot == 1 or prot == 3:
                judge_x = judge_x - 1
                prot_stone_g = 1
                bind_able = 1
            else:
                judge_x = 0
                Destruction = 1
    elif judge_x > 11:
        if b == 1:
            judge_x = judge_x+1
        else:
            if prot == 1:
                judge_x = judge_x-1
                prot_stone_g = 1
                bind_able = 1
            else:
                judge_x = 0
                Destruction = 1
    elif judge_x == 10:
        if b == 1:
            judge_x = judge_x + 1
        else:
            if prot == 2:
                judge_x = judge_x
                prot_stone = 1
            elif prot == 1 or prot == 3:
                judge_x = judge_x - 1
                prot_stone_g = 1
                bind_able = 1
            else:
                judge_x = 0
                Destruction = 1
    else:
        if b == 1:
            judge_x = judge_x + 1
        else:
            if prot == 0 or prot == 3:
                judge_x = judge_x
                prot_stone = 1
            elif prot == 1:
                judge_x = judge_x - 1
                prot_stone_g = 1
                bind_able = 1
            else:
                judge_x = 0
                Destruction = 1
    return judge_x, Destruction, prot_stone, prot_stone_g, bind_able, re_judge


def enchant_weapon0(n):
    """从0开始依次为不义 正义 混沌 曙光 富饶 确凿 猎豹"""
    if n == 0:
        attack = 220
        defence = 0
        crit = 8
        balance = 0
        speed = 4
        resistance = -5
    elif n == 1:
        attack = 430
        defence = 0
        crit = 2
        balance = 2
        speed = 8
        resistance = 0
    elif n == 2:
        attack = 340
        defence = 0
        crit = 9
        balance = 0
        speed = 4
        resistance = -4
    elif n == 3:
        attack = 180
        defence = 0
        crit = 0
        balance = 0
        speed = 3
        resistance = 0
    elif n == 4:
        attack = 120
        defence = 0
        crit = 1
        balance = 1
        speed = 5
        resistance = 0
    elif n == 5:
        attack = 0
        defence = 0
        crit = 0
        balance = 5
        speed = 4
        resistance = 0
    elif n == 6:
        attack = -240
        defence = 0
        crit = 0
        balance = 2
        speed = 8
        resistance = 0
    else:
        attack = 0
        defence = 0
        crit = 0
        balance = 0
        speed = 0
        resistance = 0
    return attack, defence, crit, balance, speed, resistance


def enchant_weapon1(n):
    """从0开始依次为审判 断罪 花瓣 勇猛 天诛 野心 挑战 信念"""
    if n == 0:
        attack = 870
        defence = 0
        crit = 4
        balance = -1
        speed = 3
        resistance = -1
    elif n == 1:
        attack = 680
        defence = 0
        crit = 6
        balance = 0
        speed = 0
        resistance = 0
    elif n == 2:
        attack = 150
        defence = 0
        crit = 0
        balance = 3
        speed = 5
        resistance = 0
    elif n == 3:
        attack = 130
        defence = 0
        crit = 0
        balance = 5
        speed = 4
        resistance = 0
    elif n == 4:
        attack = 677
        defence = 0
        crit = 2
        balance = 0
        speed = 1
        resistance = 0
    elif n == 5:
        attack = 752
        defence = 0
        crit = 2
        balance = -1
        speed = 1
        resistance = 0
    elif n == 6:
        attack = 180
        defence = 0
        crit = 1
        balance = 1
        speed = 1
        resistance = 0
    elif n == 7:
        attack = 970
        defence = 0
        crit = 5
        balance = -1
        speed = 3
        resistance = 0
    else:
        attack = 0
        defence = 0
        crit = 0
        balance = 0
        speed = 0
        resistance = 0
    return attack, defence, crit, balance, speed, resistance


def enchant_armor0(n):
    """从0开始依次为冷静 哭泣 记忆 重述 时间 保平 努力 无尽的"""
    hp = 0
    if n == 0:
        attack = 245
        defence = 200
        crit = 2
        balance = 2
        speed = 2
        resistance = 4
    elif n == 1:
        attack = 145
        defence = 300
        crit = 2
        balance = 3
        speed = 2
        resistance = -1
    elif n == 2:
        attack = 245
        defence = 100
        crit = 2
        balance = 1
        speed = 2
        resistance = 2
    elif n == 3:
        attack = 145
        defence = 150
        crit = 1
        balance = 2
        speed = 2
        resistance = -1
    elif n == 4:
        attack = 0
        defence = 160
        crit = 4
        balance = -3
        speed = 0
        resistance = 6
        hp = 50
    elif n == 5:
        attack = 0
        defence = 0
        crit = 1
        balance = 1
        speed = 2
        resistance = -1
    elif n == 6:
        attack = 0
        defence = 112
        crit = 0
        balance = 0
        speed = 1
        resistance = 0
        hp = 35
    elif n == 7:
        attack = 0
        defence = 160
        crit = 5
        balance = -3
        speed = 0
        resistance = 8
        hp = 100
    else:
        attack = 0
        defence = 0
        crit = 0
        balance = 0
        speed = 0
        resistance = 0
    return attack, defence, crit, balance, speed, resistance, hp


def enchant_armor1(n):
    """从0开始依次为回音 远征 热忱 落叶 茉莉花 致命 烙印 保护 抵抗 犰狳 灵魂 私掠 结界"""
    if n == 0:
        attack = 365
        defence = -260
        crit = 0
        balance = 4
        speed = 1
        resistance = 2
    elif n == 1:
        attack = 285
        defence = 280
        crit = 1
        balance = 0
        speed = 0
        resistance = 4
    elif n == 2:
        attack = 282
        defence = -370
        crit = 0
        balance = 5
        speed = 0
        resistance = 0
    elif n == 3:
        attack = 0
        defence = 320
        crit = 1
        balance = 1
        speed = 0
        resistance = 2
    elif n == 4:
        attack = 140
        defence = -28
        crit = 0
        balance = 2
        speed = 0
        resistance = 0
    elif n == 5:
        attack = 0
        defence = 0
        crit = 3
        balance = -1
        speed = 0
        resistance = 0
    elif n == 6:
        attack = 0
        defence = 70
        crit = 6
        balance = -1
        speed = 0
        resistance = 7
    elif n == 7:
        attack = 0
        defence = 0
        crit = 5
        balance = -1
        speed = 0
        resistance = 5
    elif n == 8:
        attack = 0
        defence = 340
        crit = 1
        balance = 0
        speed = 0
        resistance = 5
    elif n == 9:
        attack = 0
        defence = 336
        crit = 0
        balance = 1
        speed = 0
        resistance = 0
    elif n == 10:
        attack = 465
        defence = -300
        crit = 0
        balance = 5
        speed = 1
        resistance = 3
    elif n == 11:
        attack = 285
        defence = 280
        crit = 3
        balance = 0
        speed = 0
        resistance = 5
    elif n == 12:
        attack = 0
        defence = 120
        crit = 7
        balance = -1
        speed = 0
        resistance = 8
    else:
        attack = 0
        defence = 0
        crit = 0
        balance = 0
        speed = 0
        resistance = 0
    return attack, defence, crit, balance, speed, resistance


def enchant_jewelry0(n):
    hp = 0
    """从0开始依次为亡者 隐隐 闪亮 小巧 迅速 有意义 多疑 洒脱 惊心动魄 宝物猎人 星光 封印的"""
    if n == 0:
        attack = 0
        defence = 0
        crit = 0
        balance = 5
        speed = 0
        resistance = 5
        hp = -450
    elif n == 1:
        attack = 0
        defence = 0
        crit = 2
        balance = 0
        speed = 1
        resistance = -3
    elif n == 2:
        attack = 0
        defence = 0
        crit = 0
        balance = 2
        speed = 0
        resistance = 3
        hp = -280
    elif n == 3:
        attack = 0
        defence = 0
        crit = 1
        balance = 0
        speed = 1
        resistance = -3
    elif n == 4:
        attack = 0
        defence = 0
        crit = 0
        balance = -8
        speed = 5
        resistance = 0
    elif n == 5:
        attack = 15
        defence = 0
        crit = 0
        balance = 0
        speed = 1
        resistance = 0
    elif n == 6:
        attack = 0
        defence = 130
        crit = 0
        balance = 0
        speed = 0
        resistance = 0
    elif n == 7:
        attack = 55
        defence = 0
        crit = 0
        balance = 0
        speed = 3
        resistance = 0
    elif n == 8:
        attack = 0
        defence = 145
        crit = 1
        balance = 0
        speed = 0
        resistance = -3
    elif n == 9:
        attack = 0
        defence = 200
        crit = 0
        balance = 2
        speed = 0
        resistance = 0
    elif n == 10:
        attack = 200
        defence = 0
        crit = 0
        balance = 0
        speed = 2
        resistance = 0
    elif n == 11:
        attack = 0
        defence = 500
        crit = 0
        balance = 0
        speed = 1
        resistance = 0
    else:
        attack = 0
        defence = 0
        crit = 0
        balance = 0
        speed = 0
        resistance = 0
    return attack, defence, crit, balance, speed, resistance, hp


def enchant_jewelry1(n):
    """从0开始依次为高尚的 热情 心灵 活力 金刚石 真相"""
    hp = 0
    if n == 0:
        attack = -100
        defence = 0
        crit = 0
        balance = 4
        speed = 0
        resistance = 0
    elif n == 1:
        attack = 0
        defence = 200
        crit = 0
        balance = 0
        speed = 0
        resistance = 0
    elif n == 2:
        attack = 30
        defence = 2
        crit = 0
        balance = 0
        speed = 0
        resistance = 0
    elif n == 3:
        attack = 0
        defence = 130
        crit = 0
        balance = 0
        speed = 0
        resistance = 0
        hp = 12
    elif n == 4:
        attack = 0
        defence = 62
        crit = 0
        balance = 0
        speed = 0
        resistance = 3
    elif n == 5:
        attack = 230
        defence = 0
        crit = 0
        balance = 0
        speed = 0
        resistance = 5
    else:
        attack = 0
        defence = 0
        crit = 0
        balance = 0
        speed = 0
        resistance = 0
    return attack, defence, crit, balance, speed, resistance, hp


def onlynum(s):
    s2 = s.lower()
    num = '0123456789'
    for c in s2:
        if c not in num:
            s = s.replace(c, '')
    if s is '':
        return ''
    else:
        return int(s)


def intplus(x):
    x = onlynum(x)
    if x is '':
        x = 0
    return x


def alladd(x, y):
    """x为装备位置选择，1武器 2防具 3首饰"""
    """y表示选择的精灵石属性序号"""
    """返回值为a攻击力b防御力c暴击d平衡e攻速f力量g敏捷h智力i意志j爆抗"""
    [a, b, c, d, e, f, g, h, i, j] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    if x == 1:
        if y == 0:
            c = 1
        elif y == 1:
            d = 1
        elif y == 2:
            e = 1
        elif y == 3:
            a = 1
        elif y == 4:
            b = 1
        elif y == 5:
            f = 1
        elif y == 6:
            g = 1
        elif y == 7:
            h = 1
        elif y == 8:
            i = 1
    elif x == 2:
        if y == 0:
            j = 1
        elif y == 1:
            b = 1
        elif y == 2:
            i = 1
        elif y == 3:
            g = 1
        elif y == 5:
            h = 1
        elif y == 6:
            f = 1
    elif x == 3:
        if y == 0:
            c = 1
        elif y == 1:
            d = 1
        elif y == 2:
            e = 1
        elif y == 3:
            h = 1
        elif y == 4:
            f = 1
        elif y == 5:
            i = 1
        elif y == 6:
            g = 1
        elif y == 7:
            j = 1
        elif y == 8:
            b = 1
    return a, b, c, d, e, f, g, h, i, j


            ########以下为自动强化源代码，非UI版##########


def data_strengthen(x, y):
    """该函数用来寻找武器装备强化的增量"""
    """返回攻击力（防御力），追伤，攻速（防具返回0）"""
    weapon_stren = [[0, 0, 0], [50, 50, 2], [100, 110, 4], [150, 170, 6], [250, 230, 8], [350, 290, 10], [450, 350, 12],
                    [550, 410, 14], [700, 485, 16], [850, 560, 18], [1000, 650, 20], [1500, 1000, 23], [2000, 1500, 26],
                    [2600, 2000, 30], [3300, 2500, 34], [4100, 3000, 38], [4600, 3750, 42], [5100, 4500, 46],
                    [5600, 5700, 50], [6100, 7200, 54], [6600, 12500, 58]]
    armor_stren = [[0, 0, 0], [13, 10, 0], [26, 22, 0], [39, 34, 0], [47, 46, 0], [75, 58, 0], [93, 70, 50],
                   [117, 82, 70], [141, 97, 100], [165, 112, 130], [189, 130, 170], [224, 200, 220], [259, 300, 300],
                   [294, 400, 500], [339, 500, 500], [384, 600, 500], [409, 750, 500], [434, 900, 500],
                   [459, 1140, 500], [484, 1440, 500], [509, 2500, 500]]
    if x == 0:
        a = weapon_stren[y]
    elif x == 1:
        a = armor_stren[y]
    return a
# judge_x = 0
# i = 1
# prot = 1
# c = 0
# while i:
#     S_rate = judge(judge_x)
#     a = successornot()
#     b = strengthen(S_rate, a)
#     judge_x, Destruction = protectornot(judge_x, prot, b)
#     # print(judge_x)
#     if Destruction == 1:
#         c = c+1;
#     if judge_x>=20:
#         i = 0
# print(judge_x, c)
#     # i = input()





