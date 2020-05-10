import time
import wx
import wx.xrc
from threading import Thread
from wx.lib.pubsub import pub
from qianghua import *
import re
import numpy
import math


global judge_x
judge_x = 0  # 当前的强化等级


class StrenThread(Thread):  # 关于自动强化的多线程
    global judge_x
    global time_sleep

    def __init__(self):
        Thread.__init__(self)
        self.start()

    def run(self):
        global target_x
        global judge_x
        global prot
        global count
        global damage
        global stone_x
        global potion_x
        global prot_stone_x
        global surface_s_rate
        global count_yes
        global prot_stone_gx
        global bind_able_x
        global auto_i
        global time_sleep
        global autostop
        global re_judge
        global rebound_checked
        global rebound_num
        reboundornot = 0
        while judge_x < target_x:  # 当前强化等级<指定等级
            S_rate, stone, potion = judge(judge_x)  # 查找当前等级强化花费
            a = successornot()
            true_s_rate = str(int(a)) + '/' + str(int(S_rate))
            b = strengthen(S_rate, a)             # 是否成功
            if b == 1:
                rebound_num = 0
            if judge_x == 10:
                if rebound_num >= 6:
                    b = 1
                    rebound_num = 0
            if judge_x == 11:
                if rebound_num >= 7:
                    b = 1
                    rebound_num = 0
            if judge_x == 12:
                if rebound_num >= 8:
                    b = 1
                    rebound_num = 0
            if judge_x == 13:
                if rebound_num >= 10:
                    b = 1
                    rebound_num = 0
            if judge_x == 14:
                if rebound_num >= 12:
                    b = 1
                    rebound_num = 0
            judge_x, destruction, prot_stone, prot_stone_g, bind_able, re_judge = protectornot(judge_x, prot, b)
            stone_x = stone_x + stone
            potion_x = potion_x + potion
            prot_stone_x = prot_stone_x + prot_stone
            prot_stone_gx = prot_stone_gx + prot_stone_g
            bind_able_x = bind_able_x - bind_able  # 解绑次数剩余
            count = count + 1
            if b == 1:
                count_yes = count_yes + 1
            surface_s_rate = count_yes / count
            if destruction == 1:
                if rebound_checked:
                    judge_x = re_judge
                    reboundornot = 1
                else:
                    reboundornot = 0
                    damage = damage + 1
                    bind_able_x = 3  # 重新选择武器，并且解绑次数恢复为3
            time.sleep(0.15+float(time_sleep))
            curr = (true_s_rate, judge_x, prot_stone_gx, bind_able_x, prot_stone_x, stone_x, potion_x, surface_s_rate,
                    count, damage, destruction, reboundornot)
            wx.CallAfter(self.postData, curr)
            if bind_able_x == 0:
                prot = 0
                break
            if autostop == 1:
                break
        if judge_x == target_x:
            wx.CallAfter(pub.sendMessage, "the_end", msg1="目标完成")

    def postData(self, curr):
        """Send Data to Auto_Streng"""
        # pub.sendMessage("update", msg=curr[0], msg2=curr[1], msg3=curr[2], msg4=curr[3], msg5=curr[4], msg6=curr[5],
        #                 msg7=curr[6], msg8=curr[7], msg9=curr[8], msg10=curr[9], msg11=curr[10])
        pub.sendMessage("update", msg=curr)


class JustJoke(Thread):
    global autojoke

    def __init__(self):
        Thread.__init__(self)
        self.start()

    def run(self):
        for local_i in range(6):
            if local_i == 0:
                local_str = "emmmmmm\r\n您可能输入错了"
            elif local_i == 1:
                local_str = "请检查您的输入"
            elif local_i == 2:
                local_str = "确定不检查吗\r\n好吧现在检查也没有用了\r\n啊哈哈哈哈哈"
            elif local_i == 3:
                local_str = "好吧\r\n您的电脑将在10s后自动关机\r\n大叫三声'我错了'即可取消\r\n谁让您输入错了呢" \
                            "\r\n关了本软件将直接自动关机哦~~"
            elif local_i == 4:
                time.sleep(5)
                local_str = "您叫了吗？"
            else:
                local_str = "好吧骗你的啦\r\n哈哈哈哈哈哈哈哈哈\r\n别打我~\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n" \
                            "我错了\r\n\r\n\r\n\r\n求你了,别打脸..."
                enable_i = 1
                wx.CallAfter(pub.sendMessage, "joker1", msg3=enable_i)
            time.sleep(2)
            wx.CallAfter(pub.sendMessage, "joker", msg2=local_str)


class DataThread(Thread):  # 装备模拟数据整合
    global data_inital
    global data_equipment

    def __init__(self):
        Thread.__init__(self)
        self.start()

    def run(self):
        data_equipment = numpy.array(data_inital) + numpy.array(weapon_att) + numpy.array(head_att) \
                         + numpy.array(hand_att) + numpy.array(foot_att) + numpy.array(coat_att) \
                         + numpy.array(leg_att) + numpy.array(belt_att) + numpy.array(earring_att) \
                         + numpy.array(brooch_att) + numpy.array(ring1_att) + numpy.array(ring2_att) \
                         + numpy.array(bcl_att) + numpy.array(craft_att) \
                         + numpy.array(store_att)

        wx.CallAfter(pub.sendMessage, "equipment", msge=data_equipment)
        time.sleep(1)


class AutoPanel(wx.Panel):
    global damage     # 碎掉的武器
    global stone_x    # 用掉的强化石
    global potion_x         # 用掉的强化药水
    global prot_stone_x     # 用掉的强化石
    global rate_add         # 增加的成功率
    global count_yes        # 强化成功的次数
    global prot_stone_gx    # 用掉的原谅石
    global bind_able_x      # 剩余解绑次数
    global judge_x
    global i
    global prot
    global c
    global count
    global iron_sum         # 复原钢总数
    global ap_sum           # ap总消耗量
    global re_judge
    global rebound_num
    global rebound_checked
    rebound_checked = 0
    i = 1  #
    prot = 4  # 初始默认不使用强化石
    c = 0
    count = 0  # 强化次数
    bind_able_x = 3         # 解绑次数初始化为3
    prot_stone_gx = 0
    rate_add = 0
    prot_stone_x = 0
    potion_x = 0
    stone_x = 0
    damage = 0
    count_yes = 0
    iron_sum = 0
    ap_sum = 0
    rebound_num = 0

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
#        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        gbSizer1 = wx.GridBagSizer(0, 0)
        gbSizer1.SetFlexibleDirection(wx.BOTH)
        gbSizer1.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.强化 = wx.Button(self, wx.ID_ANY, u"强化", wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer1.Add(self.强化, wx.GBPosition(5, 3), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        self.stop_auto = wx.Button(self, wx.ID_ANY, u"停止", wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer1.Add(self.stop_auto, wx.GBPosition(6, 3), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        self.find_things = wx.Button(self, wx.ID_ANY, u"武器强化\r\n成功率一览", wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer1.Add(self.find_things, wx.GBPosition(5, 5), wx.GBSpan(2, 1), wx.ALL | wx.EXPAND, 5)

        self.m_button2 = wx.Button(self, wx.ID_ANY, u"初始化", wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer1.Add(self.m_button2, wx.GBPosition(5, 4), wx.GBSpan(1, 1), wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.m_textCtrl1 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                       wx.TE_READONLY)
        gbSizer1.Add(self.m_textCtrl1, wx.GBPosition(0, 3), wx.GBSpan(1, 1),
                     wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.m_textCtrl2 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                       wx.TE_READONLY)
        gbSizer1.Add(self.m_textCtrl2, wx.GBPosition(0, 4), wx.GBSpan(1, 1),
                     wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.m_staticText2 = wx.StaticText(self, wx.ID_ANY, u"碎掉的武器", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText2.Wrap(-1)
        gbSizer1.Add(self.m_staticText2, wx.GBPosition(1, 0), wx.GBSpan(1, 1), wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.m_textCtrl4 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                       wx.TE_READONLY)
        gbSizer1.Add(self.m_textCtrl4, wx.GBPosition(1, 1), wx.GBSpan(1, 1), wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        m_radioBox2Choices = [u"90", u"95", u"100"]
        self.m_radioBox2 = wx.RadioBox(self, wx.ID_ANY, u"等级",
                                       wx.DefaultPosition, wx.DefaultSize, m_radioBox2Choices,
                                       1, wx.RA_SPECIFY_ROWS)
        self.m_radioBox2.SetSelection(1)
        gbSizer1.Add(self.m_radioBox2, wx.GBPosition(2, 0), wx.GBSpan(1, 2), wx.ALL, 5)

        m_radioBox3Choices = [u"武器", u"防具"]
        self.m_radioBox3 = wx.RadioBox(self, wx.ID_ANY, u"装备",
                                       wx.DefaultPosition, wx.DefaultSize, m_radioBox3Choices,
                                       1, wx.RA_SPECIFY_ROWS)
        self.m_radioBox3.SetSelection(0)
        gbSizer1.Add(self.m_radioBox3, wx.GBPosition(2, 2), wx.GBSpan(1, 1), wx.ALL, 5)

        self.m_staticText7 = wx.StaticText(self, wx.ID_ANY, u"强化花费", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText7.Wrap(-1)
        gbSizer1.Add(self.m_staticText7, wx.GBPosition(7, 0), wx.GBSpan(1, 1), wx.ALL | wx.ALIGN_RIGHT, 5)

        self.m_staticText8 = wx.StaticText(self, wx.ID_ANY, u"输入价格", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText8.Wrap(-1)
        gbSizer1.Add(self.m_staticText8, wx.GBPosition(7, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        self.m_staticText9 = wx.StaticText(self, wx.ID_ANY, u"强化石价格", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText9.Wrap(-1)
        gbSizer1.Add(self.m_staticText9, wx.GBPosition(8, 0), wx.GBSpan(1, 1),
                     wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 5)

        self.m_staticText10 = wx.StaticText(self, wx.ID_ANY, u"强化药水价格", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText10.Wrap(-1)
        gbSizer1.Add(self.m_staticText10, wx.GBPosition(8, 2), wx.GBSpan(1, 1),
                     wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_staticText11 = wx.StaticText(self, wx.ID_ANY, u"保护石价格", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText11.Wrap(-1)
        gbSizer1.Add(self.m_staticText11, wx.GBPosition(8, 4), wx.GBSpan(1, 1),
                     wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 5)

        self.m_textCtrl11 = wx.TextCtrl(self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer1.Add(self.m_textCtrl11, wx.GBPosition(8, 1), wx.GBSpan(1, 1), wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_textCtrl12 = wx.TextCtrl(self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer1.Add(self.m_textCtrl12, wx.GBPosition(8, 3), wx.GBSpan(1, 1), wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_textCtrl13 = wx.TextCtrl(self, wx.ID_ANY, u"3", wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer1.Add(self.m_textCtrl13, wx.GBPosition(8, 5), wx.GBSpan(1, 1), wx.ALL, 5)

        self.m_staticText4 = wx.StaticText(self, wx.ID_ANY, u"强化石", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText4.Wrap(-1)
        gbSizer1.Add(self.m_staticText4, wx.GBPosition(3, 0), wx.GBSpan(1, 1),
                     wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.m_staticText5 = wx.StaticText(self, wx.ID_ANY, u"强化保护石", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText5.Wrap(-1)
        gbSizer1.Add(self.m_staticText5, wx.GBPosition(5, 0), wx.GBSpan(1, 1),
                     wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.m_textCtrl5 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                       wx.TE_READONLY)
        gbSizer1.Add(self.m_textCtrl5, wx.GBPosition(3, 1), wx.GBSpan(1, 1), wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_staticText_rebound = wx.StaticText(self, wx.ID_ANY, u"复原钢数量和价格",
                                                  wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText_rebound.Wrap(-1)
        gbSizer1.Add(self.m_staticText_rebound, wx.GBPosition(5, 2), wx.GBSpan(1, 1),
                     wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 5)
        self.m_textCtrl_rebound = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                              wx.TE_READONLY)
        gbSizer1.Add(self.m_textCtrl_rebound, wx.GBPosition(6, 2), wx.GBSpan(1, 1),
                     wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_textCtrl_reprice = wx.TextCtrl(self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer1.Add(self.m_textCtrl_reprice, wx.GBPosition(7, 2), wx.GBSpan(1, 1), wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_staticText_renum = wx.StaticText(self, wx.ID_ANY, u"重铸次数", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText_renum.Wrap(-1)
        gbSizer1.Add(self.m_staticText_renum, wx.GBPosition(7, 3), wx.GBSpan(1, 1),
                     wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_textCtrl_renum = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                              wx.TE_READONLY)
        gbSizer1.Add(self.m_textCtrl_renum, wx.GBPosition(7, 4), wx.GBSpan(1, 1), wx.ALL, 5)

        self.m_button_rebound = wx.Button(self, wx.ID_ANY, u"赎回重铸", wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer1.Add(self.m_button_rebound, wx.GBPosition(6, 4), wx.GBSpan(1, 1),
                     wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 5)
        self.m_button_rebound.Enable(False)

        self.m_staticText18 = wx.StaticText(self, wx.ID_ANY, u"剩余解绑次数", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText18.Wrap(-1)
        gbSizer1.Add(self.m_staticText18, wx.GBPosition(3, 2), wx.GBSpan(1, 1),
                     wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_textCtrl6 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                       wx.TE_READONLY)
        gbSizer1.Add(self.m_textCtrl6, wx.GBPosition(5, 1), wx.GBSpan(1, 1),
                     wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.m_textCtrl7 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                       wx.TE_READONLY)
        gbSizer1.Add(self.m_textCtrl7, wx.GBPosition(4, 1), wx.GBSpan(1, 1),
                     wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.m_textCtrl17 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                        wx.TE_READONLY)
        gbSizer1.Add(self.m_textCtrl17, wx.GBPosition(4, 2), wx.GBSpan(1, 1), wx.ALL, 5)

        self.m_button4 = wx.Button(self, wx.ID_ANY, u"计算花费", wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer1.Add(self.m_button4, wx.GBPosition(9, 4), wx.GBSpan(1, 1),
                     wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.m_staticText6 = wx.StaticText(self, wx.ID_ANY, u"强化药水", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText6.Wrap(-1)
        gbSizer1.Add(self.m_staticText6, wx.GBPosition(4, 0), wx.GBSpan(1, 1),
                     wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.m_staticText1 = wx.StaticText(self, wx.ID_ANY, u"目标等级", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText1.Wrap(-1)
        gbSizer1.Add(self.m_staticText1, wx.GBPosition(0, 0), wx.GBSpan(1, 1),
                     wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.m_textCtrl3 = wx.TextCtrl(self, wx.ID_ANY, u"15", wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer1.Add(self.m_textCtrl3, wx.GBPosition(0, 1), wx.GBSpan(1, 1),
                     wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 5)

        self.m_button3 = wx.Button(self, wx.ID_ANY, u"自动强化", wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer1.Add(self.m_button3, wx.GBPosition(3, 3), wx.GBSpan(1, 1),
                     wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_staticText14 = wx.StaticText(self, wx.ID_ANY, u"强化速度", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText14.Wrap(-1)
        gbSizer1.Add(self.m_staticText14, wx.GBPosition(4, 3), wx.GBSpan(1, 1),
                     wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.m_textCtrl141 = wx.TextCtrl(self, wx.ID_ANY, u"0.15", wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer1.Add(self.m_textCtrl141, wx.GBPosition(4, 4), wx.GBSpan(1, 1),
                     wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_staticText15 = wx.StaticText(self, wx.ID_ANY, u"0最快,1最慢", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText15.Wrap(-1)
        gbSizer1.Add(self.m_staticText15, wx.GBPosition(3, 4), wx.GBSpan(1, 1),
                     wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.m_staticText13 = wx.StaticText(self, wx.ID_ANY, u"成功率", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText13.Wrap(-1)
        gbSizer1.Add(self.m_staticText13, wx.GBPosition(1, 2), wx.GBSpan(1, 1),
                     wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.m_textCtrl16 = wx.TextCtrl(self, wx.ID_ANY, u"表面成功率",
                                        wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY)
        gbSizer1.Add(self.m_textCtrl16, wx.GBPosition(1, 4), wx.GBSpan(1, 1), wx.ALL, 5)

        self.m_textCtrl151 = wx.TextCtrl(self, wx.ID_ANY, u"真成功率",
                                         wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY)
        gbSizer1.Add(self.m_textCtrl151, wx.GBPosition(1, 3), wx.GBSpan(1, 1), wx.ALL, 5)

        self.m_staticText17 = wx.StaticText(self, wx.ID_ANY, u"原谅石", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText17.Wrap(-1)
        gbSizer1.Add(self.m_staticText17, wx.GBPosition(6, 0), wx.GBSpan(1, 1),
                     wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_textCtrl161 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                         wx.TE_READONLY)
        gbSizer1.Add(self.m_textCtrl161, wx.GBPosition(6, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        self.m_staticText16 = wx.StaticText(self, wx.ID_ANY, u"强化次数", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText16.Wrap(-1)
        gbSizer1.Add(self.m_staticText16, wx.GBPosition(0, 2), wx.GBSpan(1, 1),
                     wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_staticText12 = wx.StaticText(self, wx.ID_ANY, u"总花费", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText12.Wrap(-1)
        gbSizer1.Add(self.m_staticText12, wx.GBPosition(9, 0), wx.GBSpan(1, 1),
                     wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_textCtrl15 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                        wx.TE_READONLY)
        gbSizer1.Add(self.m_textCtrl15, wx.GBPosition(9, 2), wx.GBSpan(1, 1), wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_textCtrl14 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                        wx.TE_READONLY)
        gbSizer1.Add(self.m_textCtrl14, wx.GBPosition(9, 1), wx.GBSpan(1, 1),
                     wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        m_radioBox1Choices = [u"强化保护石", u"原谅石", u"11保护石", u"自动选择", u"不使用"]
        self.m_radioBox1 = wx.RadioBox(self, wx.ID_ANY, u"保护石",
                                       wx.DefaultPosition, wx.DefaultSize, m_radioBox1Choices,
                                       1, wx.RA_SPECIFY_COLS)
        self.m_radioBox1.SetSelection(4)
        gbSizer1.Add(self.m_radioBox1, wx.GBPosition(0, 5), wx.GBSpan(5, 2), wx.ALL, 5)

        self.m_checkBox1 = wx.CheckBox(self, wx.ID_ANY, u"凯波乃强化石", wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer1.Add(self.m_checkBox1, wx.GBPosition(2, 3), wx.GBSpan(1, 1), wx.ALL, 5)

        self.m_checkBox_rebound = wx.CheckBox(self, wx.ID_ANY, u"自动重铸", wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer1.Add(self.m_checkBox_rebound, wx.GBPosition(2, 4), wx.GBSpan(1, 1), wx.ALL, 5)

        self.SetSizer(gbSizer1)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.强化.Bind(wx.EVT_BUTTON, self.click_ccc)
        self.stop_auto.Bind(wx.EVT_BUTTON, self.stp_auto)
        self.m_button2.Bind(wx.EVT_BUTTON, self.init_init)
        self.m_button4.Bind(wx.EVT_BUTTON, self.calculate)
        self.m_button3.Bind(wx.EVT_BUTTON, self.auto_streng)
        self.m_radioBox1.Bind(wx.EVT_RADIOBOX, self.protornot)
        self.m_checkBox1.Bind(wx.EVT_CHECKBOX, self.onChecked)
        self.find_things.Bind(wx.EVT_BUTTON, self.find_something)
        self.m_button_rebound.Bind(wx.EVT_BUTTON, self.rebound)
        self.m_checkBox_rebound.Bind(wx.EVT_CHECKBOX, self.rebound_checking)

        # create a pub receiver
        pub.subscribe(self.updateall, "update")
        pub.subscribe(self.updateend, "the_end")
        pass

    # Virtual event handlers, overide them in your derived class
    def click_ccc(self, event):   # 强化按钮
        global count
        global judge_x
        global i
        global prot
        global c
        global damage
        global stone_x
        global potion_x
        global prot_stone_x
        global rate_add
        global count_yes
        global surface_s_rate
        global prot_stone_gx
        global bind_able_x
        global re_judge
        global rebound_num
        S_rate, stone, potion = judge(judge_x)            # 查找强化成功率和消耗
        S_rate = S_rate + rate_add + rebound_num*2        # 实际成功率
        a = successornot()
        true_s_rate = str(int(a))+'/'+str(int(S_rate))
        self.m_textCtrl151.SetValue(true_s_rate)          # 在界面输出真成功率
        b = strengthen(S_rate, a)                         # 判断是否强化成功
        if b == 1:
            rebound_num = 0
        if judge_x == 10:
            if rebound_num >=6:
                b = 1
                rebound_num = 0
        if judge_x == 11:
            if rebound_num >= 7:
                b = 1
                rebound_num = 0
        if judge_x == 12:
            if rebound_num >= 8:
                b = 1
                rebound_num = 0
        if judge_x == 13:
            if rebound_num >= 10:
                b = 1
                rebound_num = 0
        if judge_x == 14:
            if rebound_num >= 12:
                b = 1
                rebound_num = 0
        judge_x, destruction, prot_stone, prot_stone_g, bind_able, re_judge = protectornot(judge_x, prot, b)  # 关于保护石
        prot_stone_gx = prot_stone_gx + prot_stone_g      # 原谅石
        self.m_textCtrl161.SetValue(str(prot_stone_gx))   # 输出到界面
        bind_able_x = bind_able_x - bind_able             # 解绑次数剩余
        if prot == 2 and judge_x == 10 and b == 0:
            rebound_num = rebound_num + 1
        self.m_textCtrl17.SetValue(str(bind_able_x))      # 输出解绑次数到界面
        if bind_able_x == 0:                              # 如果解绑次数为0
            self.m_radioBox1.EnableItem(1, False)         # 原谅石不能选
            self.m_radioBox1.EnableItem(3, False)
            self.m_radioBox1.SetSelection(0)              # 自动跳到不使用
            prot = 0
        self.m_textCtrl2.SetValue('+'+str(judge_x))       # 当前强化等级输出
        stone_x = stone_x+stone                           # 使用的强化石
        potion_x = potion_x+potion                        # 药水
        prot_stone_x = prot_stone_x + prot_stone          # 保护石
        self.m_textCtrl6.SetValue(str(prot_stone_x))      # 输出上面三个
        self.m_textCtrl5.SetValue(str(stone_x))
        self.m_textCtrl7.SetValue(str(potion_x))
        count = count+1                                   # 强化次数
        if b == 1:
            self.m_button_rebound.Enable(False)
            count_yes = count_yes + 1                     # 成功次数
        else:
            if (re_judge>9 and re_judge <15):
                self.m_button_rebound.Enable(True)
        surface_s_rate = count_yes/count                  # 表面成功率
        self.m_textCtrl16.SetValue(str(surface_s_rate*100)+'%')
        if destruction == 1:                              # 碎掉武器
            damage = damage + 1                           # 碎掉的武器+1
        else:
            self.m_button_rebound.Enable(False)
        if re_judge == 0:
            bind_able_x = 3                               # 重新选择武器，并且解绑次数恢复为3
            self.m_radioBox1.Enable(True)                 # 保护石选项可以使用
            self.m_textCtrl17.SetValue(str(bind_able_x))
            self.m_radioBox1.EnableItem(1, True)          # 原谅石可以使用
            self.m_radioBox1.EnableItem(3, True)          # 自动选择可以使用
        self.m_textCtrl4.SetValue(str(damage))            # 将碎掉的武器输出
        self.m_textCtrl1.SetValue(str(count))             # 输出强化次数
        event.Skip()

    def stp_auto(self, event):
        global autostop
        autostop = 1

    def find_something(self, event):
        print()

    def init_init(self, event):  # 初始化按钮
        global judge_x
        global i
        global prot
        global c
        global count
        global damage
        global stone_x
        global potion_x
        global prot_stone_x
        global surface_s_rate
        global count_yes
        global bind_able_x
        global prot_stone_gx
        global iron_sum
        global ap_sum
        global rebound_num
        iron_sum = 0
        ap_sum = 0
        rebound_num = 0
        damage = 0
        judge_x = 0
        i = 1
        c = 0
        count = 0
        stone_x = 0
        potion_x = 0
        prot_stone_x = 0
        surface_s_rate = 0
        count_yes = 0
        bind_able_x = 3  # 重新选择武器，并且解绑次数恢复为3
        prot_stone_gx = 0
        self.m_textCtrl161.SetValue(str(prot_stone_gx))  # 输出到界面
        self.m_textCtrl161.Update()
        self.m_textCtrl17.SetValue(str(bind_able_x))  # 输出解绑次数到界面
        self.m_radioBox1.EnableItem(1, True)  # 原谅石可以使用
        self.m_radioBox1.EnableItem(3, True)  # 可以自动选择
        self.m_textCtrl16.SetValue('表面成功率')
        self.m_textCtrl151.SetValue('当前成功率')
        self.m_textCtrl4.SetValue(str(damage))
        self.m_textCtrl1.SetValue(str(0))
        self.m_textCtrl2.SetValue('+' + str(judge_x))
        self.m_textCtrl5.SetValue(str(stone_x))
        self.m_textCtrl6.SetValue(str(prot_stone_x))
        self.m_textCtrl7.SetValue(str(potion_x))
        self.m_textCtrl14.SetValue(str(0))
        self.m_textCtrl15.SetValue(str(0) + '元')
        self.m_radioBox1.SetSelection(4)
        prot = 4
        self.m_textCtrl_rebound.SetValue(str(iron_sum))
        self.m_textCtrl_renum.SetValue(str(0))
        for i in range(0, 5):
            self.m_radioBox1.EnableItem(i, True)
        self.m_checkBox_rebound.Enable(True)
        event.Skip()

    def calculate(self, event):  # 计算花费
        global stone_x
        global potion_x
        global prot_stone_x
        global iron_sum
        money_stone = int(self.m_textCtrl11.GetValue())
        money_potion = int(self.m_textCtrl12.GetValue())
        money_protstonex = int(self.m_textCtrl13.GetValue())
        money_iron = int(self.m_textCtrl_reprice.GetValue())
        money1 = stone_x * money_stone + potion_x * money_potion + iron_sum * money_iron
        money2 = prot_stone_x * money_protstonex
        self.m_textCtrl14.SetValue(str(money1))
        self.m_textCtrl15.SetValue(str(money2) + '元')
        event.Skip()

    def protornot(self, event):  # 保护石判断
        global prot
        cd = self.m_radioBox1.GetStringSelection()    # 找到选定标签的名字
        cd = str(cd)
        prot = self.m_radioBox1.FindString(cd)        # 找到标签对应的flag（0-4）
        event.Skip()

    def onChecked(self, event):                           # 判断是否使用凯波乃
        global rate_add                                   # 申明全局变量，增加的成功率
        cu = event.GetEventObject()                       # 获取
        a = cu.GetValue()
        if a is True:                                     # 如果使用，增加10%
            rate_add = 10
        else:
            rate_add = 0
        event.Skip()

    def rebound_checking(self, event):
        global rebound_checked
        global judge_x
        rebound_checked = event.GetEventObject()
        rebound_checked = rebound_checked.GetValue()
        event.Skip()

    def auto_streng(self, event):
        global target_x
        global judge_x
        global prot
        global count
        global damage
        global stone_x
        global potion_x
        global prot_stone_x
        global surface_s_rate
        global count_yes
        global prot_stone_gx
        global bind_able_x
        global time_sleep
        global autostop
        autostop = 0
        target_x = (self.m_textCtrl3.GetValue())  # 输入的指定强化等级
        every_target = '1234567891011121314151617181920'
        judge_in = re.search(str(target_x), every_target)  # 与可能的强化等级进行匹配
        time_sleep = self.m_textCtrl141.GetValue()
        if judge_in is None:  # 如果匹配不成功，说明输入错误
            self.m_textCtrl3.SetValue('请输入目标强化等级(非0）')
        else:  # 匹配成功
            target_x = int(target_x)
            StrenThread()
        event.Skip()

    def updateall(self, msg):
        global rebound_checked
        true_s_rate = msg[0]
        judge_x = int(msg[1])
        prot_stone_gx = msg[2]
        bind_able_x = msg[3]
        prot_stone_x = msg[4]
        stone_x = msg[5]
        potion_x = msg[6]
        surface_s_rate = msg[7]
        count = msg[8]
        damage = msg[9]
        destruction = msg[10]
        reboundornot = msg[11]
        if judge_x > 14:
            self.m_checkBox_rebound.Enable(False)
            rebound_checked = False
        if destruction == 1:
            rebound_checked = True
            self.m_radioBox1.Enable(True)
            self.m_radioBox1.EnableItem(1, True)  # 原谅石可以使用
            self.m_radioBox1.EnableItem(3, True)  # 可以自动选择
            self.m_radioBox1.SetSelection(0)
        if reboundornot:
            rebound_click = 1
            global rebound_num
            global iron_sum
            global ap_sum
            global re_judge
            a = self.m_radioBox2.GetStringSelection()
            a = self.m_radioBox2.FindString(str(a))
            b = self.m_radioBox3.GetStringSelection()
            b = self.m_radioBox3.FindString(str(b))
            iron, ap = data_rebound(re_judge, a, b)
            iron_sum = iron_sum + iron
            ap_sum = ap_sum + ap
            self.m_textCtrl_rebound.SetValue(str(iron_sum))
            judge_x = re_judge
            self.m_textCtrl2.SetValue('+' + str(judge_x))
            self.m_radioBox1.SetSelection(4)
            self.m_radioBox1.Enable(False)
            bind_able_x = 0
            self.m_textCtrl17.SetValue(str(bind_able_x))
            rebound_num = rebound_num + rebound_click
            self.m_textCtrl_renum.SetValue(str(rebound_num))
        self.m_textCtrl151.SetValue(true_s_rate)  # 在界面输出真成功率
        self.m_textCtrl2.SetValue('+' + str(judge_x))
        self.m_textCtrl161.SetValue(str(prot_stone_gx))  # 输出到界面
        self.m_textCtrl17.SetValue(str(bind_able_x))  # 输出解绑次数到界面
        if bind_able_x == 0:  # 如果解绑次数为0
            self.m_radioBox1.EnableItem(1, False)  # 原谅石不能选
            self.m_radioBox1.EnableItem(3, False)
            self.m_radioBox1.SetSelection(4)  # 自动跳到不使用
        self.m_textCtrl6.SetValue(str(prot_stone_x))
        self.m_textCtrl5.SetValue(str(stone_x))
        self.m_textCtrl7.SetValue(str(potion_x))
        self.m_textCtrl16.SetValue(str(surface_s_rate))
        self.m_textCtrl1.SetValue(str(count))
        self.m_textCtrl4.SetValue(str(damage))  # 将碎掉的武器输出

    def updateend(self, msg1):
        global target_x
        global judge_x
        if target_x ==judge_x:
            self.m_textCtrl2.SetValue('+' + str(judge_x))
            self.m_textCtrl3.SetValue('目标完成')

    def rebound(self, event):
        rebound_click = 1
        global rebound_num
        global iron_sum
        global ap_sum
        global re_judge
        global judge_x
        global bind_able_x
        a = self.m_radioBox2.GetStringSelection()
        a = self.m_radioBox2.FindString(str(a))
        b = self.m_radioBox3.GetStringSelection()
        b = self.m_radioBox3.FindString(str(b))
        iron, ap = data_rebound(re_judge, a, b)
        iron_sum = iron_sum + iron
        ap_sum = ap_sum + ap
        self.m_textCtrl_rebound.SetValue(str(iron_sum))
        judge_x = re_judge
        self.m_textCtrl2.SetValue('+'+str(judge_x))
        self.m_radioBox1.SetSelection(4)
        self.m_radioBox1.Enable(False)
        bind_able_x = 0
        self.m_textCtrl17.SetValue(str(bind_able_x))
        rebound_num = rebound_num + rebound_click
        self.m_textCtrl_renum.SetValue(str(rebound_num))
        event.Skip()

    def __del__(self):
        pass


class MatPanel(wx.Panel):    # 垫子强化
    global level
    global rate_badd
    global b_damage
    global stone_bx
    global prot_stone_bx
    global bprot_stone_gx
    global potion_bx
    global b_prot
    global b_i
    global b_c
    global b_count
    global bcount_yes
    b_prot = 4
    b_i = 1
    b_c = 0
    b_count = 0
    bprot_stone_gx = 0
    prot_stone_bx = 0
    potion_bx = 0
    rate_badd = 0
    stone_bx = 0
    b_damage = 0
    bcount_yes = 0
    level = [[0, 3], [0, 3], [0, 3], [0, 3], [0, 3], [0, 3], [0, 3], [0, 3], [0, 3], [0, 3], [0, 3]]

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
#        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        gbSizer2 = wx.GridBagSizer(0, 0)
        gbSizer2.SetFlexibleDirection(wx.BOTH)
        gbSizer2.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.bm_button1 = wx.Button(self, wx.ID_ANY, u"强化", wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer2.Add(self.bm_button1, wx.GBPosition(4, 5), wx.GBSpan(2, 1), wx.ALL | wx.EXPAND, 5)

        self.bm_button2 = wx.Button(self, wx.ID_ANY, u"初始化", wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer2.Add(self.bm_button2, wx.GBPosition(4, 6), wx.GBSpan(2, 1),
                     wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL | wx.ALL | wx.EXPAND, 5)

        self.bm_textCtrl1 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                        wx.TE_READONLY)
        gbSizer2.Add(self.bm_textCtrl1, wx.GBPosition(0, 5), wx.GBSpan(1, 1),
                     wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.bm_textCtrl2 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                        wx.TE_READONLY)
        gbSizer2.Add(self.bm_textCtrl2, wx.GBPosition(0, 6), wx.GBSpan(1, 1),
                     wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.bm_staticText2 = wx.StaticText(self, wx.ID_ANY, u"碎掉的武器", wx.DefaultPosition, wx.DefaultSize, 0)
        self.bm_staticText2.Wrap(-1)
        gbSizer2.Add(self.bm_staticText2, wx.GBPosition(0, 2), wx.GBSpan(1, 1), wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.bm_textCtrl4 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                        wx.TE_READONLY)
        gbSizer2.Add(self.bm_textCtrl4, wx.GBPosition(0, 3), wx.GBSpan(1, 1), wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.bm_staticText3 = wx.StaticText(self, wx.ID_ANY, u"强化耗材", wx.DefaultPosition, wx.DefaultSize, 0)
        self.bm_staticText3.Wrap(-1)
        gbSizer2.Add(self.bm_staticText3, wx.GBPosition(1, 2), wx.GBSpan(1, 1),
                     wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 5)

        self.bm_staticText7 = wx.StaticText(self, wx.ID_ANY, u"强化花费", wx.DefaultPosition, wx.DefaultSize, 0)
        self.bm_staticText7.Wrap(-1)
        gbSizer2.Add(self.bm_staticText7, wx.GBPosition(7, 2), wx.GBSpan(1, 1), wx.ALL | wx.ALIGN_RIGHT, 5)

        self.bm_staticText8 = wx.StaticText(self, wx.ID_ANY, u"输入价格", wx.DefaultPosition, wx.DefaultSize, 0)
        self.bm_staticText8.Wrap(-1)
        gbSizer2.Add(self.bm_staticText8, wx.GBPosition(7, 3), wx.GBSpan(1, 1), wx.ALL, 5)

        self.bm_staticText9 = wx.StaticText(self, wx.ID_ANY, u"强化石价格", wx.DefaultPosition, wx.DefaultSize, 0)
        self.bm_staticText9.Wrap(-1)
        gbSizer2.Add(self.bm_staticText9, wx.GBPosition(8, 2), wx.GBSpan(1, 1),
                     wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 5)

        self.bm_staticText10 = wx.StaticText(self, wx.ID_ANY, u"强化药水价格", wx.DefaultPosition, wx.DefaultSize, 0)
        self.bm_staticText10.Wrap(-1)
        gbSizer2.Add(self.bm_staticText10, wx.GBPosition(8, 4), wx.GBSpan(1, 1),
                     wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 5)

        self.bm_staticText11 = wx.StaticText(self, wx.ID_ANY, u"保护石价格", wx.DefaultPosition, wx.DefaultSize, 0)
        self.bm_staticText11.Wrap(-1)
        gbSizer2.Add(self.bm_staticText11, wx.GBPosition(7, 4), wx.GBSpan(1, 1),
                     wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 5)

        self.bm_textCtrl11 = wx.TextCtrl(self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer2.Add(self.bm_textCtrl11, wx.GBPosition(8, 3), wx.GBSpan(1, 1), wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.bm_textCtrl12 = wx.TextCtrl(self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer2.Add(self.bm_textCtrl12, wx.GBPosition(8, 5), wx.GBSpan(1, 1), wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.bm_textCtrl13 = wx.TextCtrl(self, wx.ID_ANY, u"3", wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer2.Add(self.bm_textCtrl13, wx.GBPosition(7, 5), wx.GBSpan(1, 1), wx.ALL, 5)

        self.bm_staticText4 = wx.StaticText(self, wx.ID_ANY, u"强化石", wx.DefaultPosition, wx.DefaultSize, 0)
        self.bm_staticText4.Wrap(-1)
        gbSizer2.Add(self.bm_staticText4, wx.GBPosition(2, 2), wx.GBSpan(1, 1),
                     wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.bm_staticText5 = wx.StaticText(self, wx.ID_ANY, u"强化保护石", wx.DefaultPosition, wx.DefaultSize, 0)
        self.bm_staticText5.Wrap(-1)
        gbSizer2.Add(self.bm_staticText5, wx.GBPosition(4, 2), wx.GBSpan(1, 1),
                     wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.bm_textCtrl5 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                        wx.TE_READONLY)
        gbSizer2.Add(self.bm_textCtrl5, wx.GBPosition(2, 3), wx.GBSpan(1, 1), wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.bm_staticText18 = wx.StaticText(self, wx.ID_ANY, u"剩余解绑次数", wx.DefaultPosition, wx.DefaultSize, 0)
        self.bm_staticText18.Wrap(-1)
        gbSizer2.Add(self.bm_staticText18, wx.GBPosition(6, 2), wx.GBSpan(1, 1),
                     wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.bm_textCtrl6 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                        wx.TE_READONLY)
        gbSizer2.Add(self.bm_textCtrl6, wx.GBPosition(4, 3), wx.GBSpan(1, 1),
                     wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.bm_textCtrl7 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                        wx.TE_READONLY)
        gbSizer2.Add(self.bm_textCtrl7, wx.GBPosition(3, 3), wx.GBSpan(1, 1),
                     wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.bm_textCtrl17 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                         wx.TE_READONLY)
        gbSizer2.Add(self.bm_textCtrl17, wx.GBPosition(6, 3), wx.GBSpan(1, 1), wx.ALL, 5)

        self.bm_button4 = wx.Button(self, wx.ID_ANY, u"计算花费", wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer2.Add(self.bm_button4, wx.GBPosition(8, 6), wx.GBSpan(2, 1),
                     wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL | wx.ALL | wx.EXPAND, 5)

        self.bm_staticText6 = wx.StaticText(self, wx.ID_ANY, u"强化药水", wx.DefaultPosition, wx.DefaultSize, 0)
        self.bm_staticText6.Wrap(-1)
        gbSizer2.Add(self.bm_staticText6, wx.GBPosition(3, 2), wx.GBSpan(1, 1),
                     wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.bm_staticText13 = wx.StaticText(self, wx.ID_ANY, u"成功率", wx.DefaultPosition, wx.DefaultSize, 0)
        self.bm_staticText13.Wrap(-1)
        gbSizer2.Add(self.bm_staticText13, wx.GBPosition(1, 4), wx.GBSpan(1, 1),
                     wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.bm_textCtrl16 = wx.TextCtrl(self, wx.ID_ANY, u"表面成功率", wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY)
        gbSizer2.Add(self.bm_textCtrl16, wx.GBPosition(1, 6), wx.GBSpan(1, 1), wx.ALL, 5)

        self.bm_textCtrl151 = wx.TextCtrl(self, wx.ID_ANY, u"真成功率", wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY)
        gbSizer2.Add(self.bm_textCtrl151, wx.GBPosition(1, 5), wx.GBSpan(1, 1), wx.ALL, 5)

        self.bm_staticText17 = wx.StaticText(self, wx.ID_ANY, u"原谅石", wx.DefaultPosition, wx.DefaultSize, 0)
        self.bm_staticText17.Wrap(-1)
        gbSizer2.Add(self.bm_staticText17, wx.GBPosition(5, 2), wx.GBSpan(1, 1),
                     wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.bm_textCtrl161 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                          wx.TE_READONLY)
        gbSizer2.Add(self.bm_textCtrl161, wx.GBPosition(5, 3), wx.GBSpan(1, 1), wx.ALL, 5)

        self.bm_staticText16 = wx.StaticText(self, wx.ID_ANY, u"强化次数", wx.DefaultPosition, wx.DefaultSize, 0)
        self.bm_staticText16.Wrap(-1)
        gbSizer2.Add(self.bm_staticText16, wx.GBPosition(0, 4), wx.GBSpan(1, 1),
                     wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.bm_staticText12 = wx.StaticText(self, wx.ID_ANY, u"总花费", wx.DefaultPosition, wx.DefaultSize, 0)
        self.bm_staticText12.Wrap(-1)
        gbSizer2.Add(self.bm_staticText12, wx.GBPosition(9, 2), wx.GBSpan(1, 1),
                     wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 5)

        self.bm_textCtrl15 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                         wx.TE_READONLY)
        gbSizer2.Add(self.bm_textCtrl15, wx.GBPosition(9, 4), wx.GBSpan(1, 1), wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.bm_textCtrl14 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                         wx.TE_READONLY)
        gbSizer2.Add(self.bm_textCtrl14, wx.GBPosition(9, 3), wx.GBSpan(1, 1),
                     wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        m_radiobox2choices = [u"%s 贵族单手剑" % level[0][0], u"%s 末日单手剑" % level[0][0],
                              u"%s 骸骨单手剑" % level[0][0], u"%s 雷吉纳单手剑" % level[0][0],
                              u"%s 布拉哈单手剑" % level[0][0], u"%s 境界的守护者单手剑" % level[0][0],
                              u"%s 鲁拉巴达单手剑" % level[0][0], u"%s 哈维登特单手剑" % level[0][0],
                              u"%s 图拉汗单手剑1" % level[0][0], u"%s 图拉汗单手剑2" % level[0][0],
                              u"%s 图拉汗单手剑3" % level[0][0], u"..."]
        self.m_radiobox2 = wx.RadioBox(self, wx.ID_ANY, u"武器选择", wx.DefaultPosition, wx.DefaultSize,
                                       m_radiobox2choices, 1, wx.RA_SPECIFY_COLS)
        self.m_radiobox2.SetSelection(0)
        self.m_radiobox2.ShowItem(11, False)
        gbSizer2.Add(self.m_radiobox2, wx.GBPosition(0, 0), wx.GBSpan(11, 2), wx.ALL, 5)

        m_radiobox3choices = [u"强化保护石", u"原谅石", u"11保护石", u"自动选择", u"不使用"]
        self.m_radiobox3 = wx.RadioBox(self, wx.ID_ANY, u"wxRadioBox", wx.DefaultPosition, wx.DefaultSize,
                                       m_radiobox3choices, 1, wx.RA_SPECIFY_COLS)
        self.m_radiobox3.SetSelection(4)
        gbSizer2.Add(self.m_radiobox3, wx.GBPosition(2, 4), wx.GBSpan(5, 1), wx.ALL, 5)

        self.bm_checkBox1 = wx.CheckBox(self, wx.ID_ANY, u"凯波乃强化石", wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer2.Add(self.bm_checkBox1, wx.GBPosition(3, 5), wx.GBSpan(1, 1), wx.ALL, 5)

        self.SetSizer(gbSizer2)
        self.Layout()

        # Connect Events
        self.bm_button1.Bind(wx.EVT_BUTTON, self.click_bbb)
        self.bm_button2.Bind(wx.EVT_BUTTON, self.init_init)
        self.bm_button4.Bind(wx.EVT_BUTTON, self.calculate)
        self.m_radiobox3.Bind(wx.EVT_RADIOBOX, self.protornot)
        self.m_radiobox2.Bind(wx.EVT_RADIOBOX, self.head_check)
        self.bm_checkBox1.Bind(wx.EVT_CHECKBOX, self.bonChecked)

    def __del__(self):
        pass

        # Virtual event handlers, overide them in your derived class

    def click_bbb(self, event):

        cd = self.m_radiobox2.GetStringSelection()
        cu = self.m_radiobox2.FindString(str(cd))
        if cu == 11:
            dlg = wx.MessageDialog(None, u"您的武器碎掉了，请重新选择武器", u"错误", wx.OK | wx.ICON_QUESTION)
            if dlg.ShowModal() == wx.ID_YES:
                self.Close(True)
            dlg.Destroy()
        else:
            global level
            global b_count
            global judge_bx
            global b_prot
            global b_damage
            global stone_bx
            global potion_bx
            global prot_stone_bx
            global rate_badd
            global bcount_yes
            global surface_s_brate
            global bprot_stone_gx
            global bind_able_bx
            bcd = self.m_radiobox2.GetStringSelection()   # 找到选定标签的名字
            bcd = str(bcd)
            b_level = self.m_radiobox2.FindString(bcd)     # 找到标签对应的flag
            judge_bx = level[b_level][0]
            bind_able_bx = level[b_level][1]
            bs_rate, b_stone, b_potion = judge(judge_bx)
            bs_rate1 = bs_rate
            bs_rate = bs_rate + rate_badd
            b_a = successornot()
            btrue_s_rate = str(int(b_a))+'/'+str(int(bs_rate))
            self.bm_textCtrl151.SetValue(btrue_s_rate)
            b_b = strengthen(bs_rate, b_a)
            judge_bx, b_destruction, bprot_stone, bprot_stone_g, bbind_able, brebound = protectornot(judge_bx, b_prot, b_b)
            bprot_stone_gx = bprot_stone_gx + bprot_stone_g
            self.bm_textCtrl161.SetValue(str(bprot_stone_gx))
            bind_able_bx = bind_able_bx - bbind_able
            self.bm_textCtrl17.SetValue(str(bind_able_bx))
            level[b_level][1] = bind_able_bx
            level[b_level][0] = judge_bx
            if bind_able_bx == 0:
                self.m_radiobox3.EnableItem(1, False)
                self.m_radiobox3.EnableItem(3, False)
                self.m_radiobox3.SetSelection(0)
                b_prot = 0
            self.bm_textCtrl2.SetValue('+'+str(judge_bx))
            stone_bx = stone_bx + b_stone
            potion_bx = potion_bx + b_potion
            prot_stone_bx = prot_stone_bx +bprot_stone
            self.bm_textCtrl6.SetValue(str(prot_stone_bx))
            self.bm_textCtrl5.SetValue(str(stone_bx))
            self.bm_textCtrl7.SetValue(str(potion_bx))
            b_count = b_count + 1
            if b_b == 1:
                bcount_yes = bcount_yes + 1
            surface_s_brate = bcount_yes/b_count
            self.bm_textCtrl16.SetValue(str(surface_s_brate*100)+'%')
            if b_destruction == 1:
                b_damage = b_damage + 1
                bind_able_bx = 3
                self.m_radiobox3.EnableItem(1, True)
                self.m_radiobox3.EnableItem(3, True)
                cd = self.m_radiobox2.GetStringSelection()
                cu = self.m_radiobox2.FindString(str(cd))
                self.m_radiobox2.EnableItem(cu, False)
                self.m_radiobox2.SetSelection(11)
            self.bm_textCtrl4.SetValue(str(b_damage))
            self.bm_textCtrl1.SetValue(str(b_count))
            cd = self.m_radiobox2.GetStringSelection()
            cu = self.m_radiobox2.FindString(str(cd))
            if cu != 11:
                clevel = level[cu][0]
                cd = str(cd).split()[1]
                self.m_radiobox2.SetString(cu, u"%s %s" % (str(clevel), cd))
        event.Skip()

    def init_init(self, event):
        global b_i
        global b_c
        global level
        global b_count
        global judge_bx
        global b_prot
        global b_damage
        global stone_bx
        global potion_bx
        global prot_stone_bx
        global bcount_yes
        global surface_s_brate
        global bprot_stone_gx
        global bind_able_bx
        b_damage = 0
        judge_bx = 0
        b_i = 1
        b_c = 0
        b_count = 0
        stone_bx = 0
        potion_bx = 0
        prot_stone_bx = 0
        surface_s_brate = 0
        bcount_yes = 0
        bind_able_bx = 3
        bprot_stone_gx = 0
        level = [[0, 3], [0, 3], [0, 3], [0, 3], [0, 3], [0, 3], [0, 3], [0, 3], [0, 3], [0, 3], [0, 3]]
        self.bm_textCtrl161.SetValue(str(bprot_stone_gx))  # 输出到界面
        self.bm_textCtrl161.Update()
        self.bm_textCtrl17.SetValue(str(bind_able_bx))  # 输出解绑次数到界面
        self.m_radiobox3.EnableItem(1, True)  # 原谅石可以使用
        self.m_radiobox3.EnableItem(3, True)  # 可以自动选择
        self.bm_textCtrl16.SetValue('表面成功率')
        self.bm_textCtrl151.SetValue('当前成功率')
        self.bm_textCtrl4.SetValue(str(b_damage))
        self.bm_textCtrl1.SetValue(str(0))
        self.bm_textCtrl2.SetValue('+' + str(judge_bx))
        self.bm_textCtrl5.SetValue(str(stone_bx))
        self.bm_textCtrl6.SetValue(str(prot_stone_bx))
        self.bm_textCtrl7.SetValue(str(potion_bx))
        self.bm_textCtrl14.SetValue(str(0))
        self.bm_textCtrl15.SetValue(str(0) + '元')
        self.m_radiobox3.SetSelection(4)
        b_prot = 4
        for ii in range(11):
            cd = self.m_radiobox2.GetString(ii)
            clevel = level[ii][0]
            cd = str(cd).split()[1]
            self.m_radiobox2.SetString(ii, u"%s %s" % (str(clevel), cd))
            self.m_radiobox2.EnableItem(ii, True)
        event.Skip()

    def calculate(self, event):
        global stone_bx
        global potion_bx
        global prot_stone_bx
        bmoney_stone = int(self.bm_textCtrl11.GetValue())
        bmoney_potion = int(self.bm_textCtrl12.GetValue())
        bmoney_protstonex = int(self.bm_textCtrl13.GetValue())
        bmoney1 = stone_bx * bmoney_stone + potion_bx * bmoney_potion
        bmoney2 = prot_stone_bx * bmoney_protstonex
        self.bm_textCtrl14.SetValue(str(bmoney1))
        self.bm_textCtrl15.SetValue(str(bmoney2) + '元')
        event.Skip()

    def protornot(self, event):
        global b_prot
        cd = self.m_radiobox3.GetStringSelection()  # 找到选定标签的名字
        cd = str(cd)
        b_prot = self.m_radiobox3.FindString(cd)  # 找到标签对应的flag（0-4）
        event.Skip()

    def bonChecked(self, event):
        global rate_badd
        cu = event.GetEventObject()
        a = cu.GetValue()
        if a is True:
            rate_badd = 10
        else:
            rate_badd = 0
        return rate_badd

    def head_check(self, event):
        global level
        global b_prot
        cd = self.m_radiobox2.GetStringSelection()
        cu = self.m_radiobox2.FindString(str(cd))
        if cu != 11:
            clevel = level[cu][0]
            cd = str(cd).split()[1]
            self.m_radiobox2.SetString(cu, u"%s %s" % (str(clevel), cd))
            if level[cu][1] == 0:
                self.m_radiobox3.EnableItem(1, False)
                self.m_radiobox3.EnableItem(3, False)
                self.m_radiobox3.SetSelection(0)
                b_prot = 0
            else:
                self.m_radiobox3.EnableItem(1, True)
                self.m_radiobox3.EnableItem(3, True)
                self.m_radiobox3.SetSelection(0)
                b_prot = 0
        event.Skip()


class Simulation(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(900, 600),
                          style=wx.TAB_TRAVERSAL)

        gbSizer3 = wx.GridBagSizer(0, 0)
        gbSizer3.SetFlexibleDirection(wx.BOTH)
        gbSizer3.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        global attack
        global defence
        global crit
        global balance
        global speed
        global resistance
        global hp
        self.cm_staticText34 = wx.StaticText(self, wx.ID_ANY, u"Now", wx.DefaultPosition, wx.DefaultSize, 0)
        self.cm_staticText34.Wrap(-1)
        gbSizer3.Add(self.cm_staticText34, wx.GBPosition(0, 1), wx.GBSpan(1, 1),
                     wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.cm_staticText36 = wx.StaticText(self, wx.ID_ANY, u"攻击", wx.DefaultPosition, wx.DefaultSize, 0)
        self.cm_staticText36.Wrap(-1)
        gbSizer3.Add(self.cm_staticText36, wx.GBPosition(1, 0), wx.GBSpan(1, 1),
                     wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.cm_textCtrl34 = wx.TextCtrl(self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer3.Add(self.cm_textCtrl34, wx.GBPosition(1, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        self.cm_textCtrl35 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                        wx.TE_READONLY)
        gbSizer3.Add(self.cm_textCtrl35, wx.GBPosition(1, 2), wx.GBSpan(1, 1), wx.ALL, 5)

        self.cm_staticText43 = wx.StaticText(self, wx.ID_ANY, u"武器", wx.DefaultPosition, wx.DefaultSize, 0)
        self.cm_staticText43.Wrap(-1)
        gbSizer3.Add(self.cm_staticText43, wx.GBPosition(1, 4), wx.GBSpan(1, 1),
                     wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        cm_choice1Choices = [u"不义的", u"正义的", u"混沌的", u"曙光般的", u"富饶的", u"确凿的", u"猎豹", wx.EmptyString]
        self.cm_choice1 = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, cm_choice1Choices, 0)
        self.cm_choice1.SetSelection(7)
        gbSizer3.Add(self.cm_choice1, wx.GBPosition(1, 5), wx.GBSpan(1, 1),
                     wx.ALL | wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        cm_choice2Choices = [u"审判", u"断罪", u"花瓣", u"勇猛", u"天诛", u"野心", u"挑战", u"信念", wx.EmptyString]
        self.cm_choice2 = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, cm_choice2Choices, 0)
        self.cm_choice2.SetSelection(8)
        gbSizer3.Add(self.cm_choice2, wx.GBPosition(1, 6), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        self.cm_choice271 = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, cm_choice1Choices, 0)
        self.cm_choice271.SetSelection(1)
        gbSizer3.Add(self.cm_choice271, wx.GBPosition(1, 7), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        self.cm_choice281 = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, cm_choice2Choices, 0)
        self.cm_choice281.SetSelection(7)
        gbSizer3.Add(self.cm_choice281, wx.GBPosition(1, 8), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        self.cm_staticText37 = wx.StaticText(self, wx.ID_ANY, u"防御", wx.DefaultPosition, wx.DefaultSize, 0)
        self.cm_staticText37.Wrap(-1)
        gbSizer3.Add(self.cm_staticText37, wx.GBPosition(2, 0), wx.GBSpan(1, 1),
                     wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.cm_textCtrl36 = wx.TextCtrl(self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer3.Add(self.cm_textCtrl36, wx.GBPosition(2, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        self.cm_textCtrl37 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                        wx.TE_READONLY)
        gbSizer3.Add(self.cm_textCtrl37, wx.GBPosition(2, 2), wx.GBSpan(1, 1), wx.ALL, 5)

        self.cm_staticText44 = wx.StaticText(self, wx.ID_ANY, u"头部防具", wx.DefaultPosition, wx.DefaultSize, 0)
        self.cm_staticText44.Wrap(-1)
        gbSizer3.Add(self.cm_staticText44, wx.GBPosition(2, 4), wx.GBSpan(1, 1),
                     wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        cm_choice3Choices = [u"冷静的", u"记忆的", u"保持平衡的", u"努力地", wx.EmptyString]
        self.cm_choice3 = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, cm_choice3Choices, 0)
        self.cm_choice3.SetSelection(4)
        gbSizer3.Add(self.cm_choice3, wx.GBPosition(2, 5), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        cm_choice4Choices = [u"远征", u"热忱", u"落叶", u"茉莉花", u"致命", u"抵抗", u"犰狳", u"私掠", wx.EmptyString]
        self.cm_choice4 = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, cm_choice4Choices, 0)
        self.cm_choice4.SetSelection(8)
        gbSizer3.Add(self.cm_choice4, wx.GBPosition(2, 6), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        self.cm_choice29 = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, cm_choice3Choices, 0)
        self.cm_choice29.SetSelection(0)
        gbSizer3.Add(self.cm_choice29, wx.GBPosition(2, 7), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        self.cm_choice30 = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, cm_choice4Choices, 0)
        self.cm_choice30.SetSelection(7)
        gbSizer3.Add(self.cm_choice30, wx.GBPosition(2, 8), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        self.cm_staticText38 = wx.StaticText(self, wx.ID_ANY, u"暴击", wx.DefaultPosition, wx.DefaultSize, 0)
        self.cm_staticText38.Wrap(-1)
        gbSizer3.Add(self.cm_staticText38, wx.GBPosition(3, 0), wx.GBSpan(1, 1),
                     wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.cm_textCtrl38 = wx.TextCtrl(self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer3.Add(self.cm_textCtrl38, wx.GBPosition(3, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        self.cm_textCtrl39 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                        wx.TE_READONLY)
        gbSizer3.Add(self.cm_textCtrl39, wx.GBPosition(3, 2), wx.GBSpan(1, 1), wx.ALL, 5)

        self.cm_staticText45 = wx.StaticText(self, wx.ID_ANY, u"胸部防具", wx.DefaultPosition, wx.DefaultSize, 0)
        self.cm_staticText45.Wrap(-1)
        gbSizer3.Add(self.cm_staticText45, wx.GBPosition(3, 4), wx.GBSpan(1, 1),
                     wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        cm_choice5Choices = [u"时间的", u"保持平衡的", u"努力地", u"无尽的", wx.EmptyString]
        self.cm_choice5 = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, cm_choice5Choices, 0)
        self.cm_choice5.SetSelection(4)
        gbSizer3.Add(self.cm_choice5, wx.GBPosition(3, 5), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        cm_choice6Choices = [u"烙印", u"保护", u"茉莉花", u"热忱", u"落叶", u"致命", u"结界", wx.EmptyString]
        self.cm_choice6 = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, cm_choice6Choices, 0)
        self.cm_choice6.SetSelection(7)
        gbSizer3.Add(self.cm_choice6, wx.GBPosition(3, 6), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        self.cm_choice31 = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, cm_choice5Choices, 0)
        self.cm_choice31.SetSelection(3)
        gbSizer3.Add(self.cm_choice31, wx.GBPosition(3, 7), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        self.cm_choice32 = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, cm_choice6Choices, 0)
        self.cm_choice32.SetSelection(6)
        gbSizer3.Add(self.cm_choice32, wx.GBPosition(3, 8), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        self.cm_staticText39 = wx.StaticText(self, wx.ID_ANY, u"平衡", wx.DefaultPosition, wx.DefaultSize, 0)
        self.cm_staticText39.Wrap(-1)
        gbSizer3.Add(self.cm_staticText39, wx.GBPosition(4, 0), wx.GBSpan(1, 1),
                     wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.cm_textCtrl40 = wx.TextCtrl(self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer3.Add(self.cm_textCtrl40, wx.GBPosition(4, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        self.cm_textCtrl41 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                        wx.TE_READONLY)
        gbSizer3.Add(self.cm_textCtrl41, wx.GBPosition(4, 2), wx.GBSpan(1, 1), wx.ALL, 5)

        self.cm_staticText46 = wx.StaticText(self, wx.ID_ANY, u"腿部防具", wx.DefaultPosition, wx.DefaultSize, 0)
        self.cm_staticText46.Wrap(-1)
        gbSizer3.Add(self.cm_staticText46, wx.GBPosition(4, 4), wx.GBSpan(1, 1),
                     wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        cm_choice7Choices = [u"冷静的", u"记忆的", u"保持平衡的", u"努力地", wx.EmptyString]
        self.cm_choice7 = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, cm_choice7Choices, 0)
        self.cm_choice7.SetSelection(4)
        gbSizer3.Add(self.cm_choice7, wx.GBPosition(4, 5), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        cm_choice8Choices = [u"远征", u"热忱", u"落叶", u"茉莉花", u"致命", u"抵抗", u"犰狳", u"私掠", wx.EmptyString]
        self.cm_choice8 = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, cm_choice8Choices, 0)
        self.cm_choice8.SetSelection(8)
        gbSizer3.Add(self.cm_choice8, wx.GBPosition(4, 6), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        self.cm_choice33 = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, cm_choice7Choices, 0)
        self.cm_choice33.SetSelection(3)
        gbSizer3.Add(self.cm_choice33, wx.GBPosition(4, 7), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        self.cm_choice34 = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, cm_choice8Choices, 0)
        self.cm_choice34.SetSelection(7)
        gbSizer3.Add(self.cm_choice34, wx.GBPosition(4, 8), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        self.cm_staticText40 = wx.StaticText(self, wx.ID_ANY, u"攻速", wx.DefaultPosition, wx.DefaultSize, 0)
        self.cm_staticText40.Wrap(-1)
        gbSizer3.Add(self.cm_staticText40, wx.GBPosition(5, 0), wx.GBSpan(1, 1),
                     wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.cm_textCtrl42 = wx.TextCtrl(self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer3.Add(self.cm_textCtrl42, wx.GBPosition(5, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        self.cm_textCtrl43 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                        wx.TE_READONLY)
        gbSizer3.Add(self.cm_textCtrl43, wx.GBPosition(5, 2), wx.GBSpan(1, 1), wx.ALL, 5)

        self.cm_staticText47 = wx.StaticText(self, wx.ID_ANY, u"手部防具", wx.DefaultPosition, wx.DefaultSize, 0)
        self.cm_staticText47.Wrap(-1)
        gbSizer3.Add(self.cm_staticText47, wx.GBPosition(5, 4), wx.GBSpan(1, 1),
                     wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        cm_choice9Choices = [u"哭泣的", u"重述的", u"保持平衡的", u"努力地", wx.EmptyString]
        self.cm_choice9 = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, cm_choice9Choices, 0)
        self.cm_choice9.SetSelection(4)
        gbSizer3.Add(self.cm_choice9, wx.GBPosition(5, 5), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        cm_choice10Choices = [u"回音", u"热忱", u"落叶", u"茉莉花", u"致命", u"抵抗", u"犰狳", u"灵魂", wx.EmptyString]
        self.cm_choice10 = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, cm_choice10Choices, 0)
        self.cm_choice10.SetSelection(8)
        gbSizer3.Add(self.cm_choice10, wx.GBPosition(5, 6), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        self.cm_choice35 = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, cm_choice9Choices, 0)
        self.cm_choice35.SetSelection(0)
        gbSizer3.Add(self.cm_choice35, wx.GBPosition(5, 7), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        self.cm_choice36 = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, cm_choice10Choices, 0)
        self.cm_choice36.SetSelection(7)
        gbSizer3.Add(self.cm_choice36, wx.GBPosition(5, 8), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        self.cm_staticText41 = wx.StaticText(self, wx.ID_ANY, u"爆抗", wx.DefaultPosition, wx.DefaultSize, 0)
        self.cm_staticText41.Wrap(-1)
        gbSizer3.Add(self.cm_staticText41, wx.GBPosition(6, 0), wx.GBSpan(1, 1),
                     wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.cm_textCtrl44 = wx.TextCtrl(self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer3.Add(self.cm_textCtrl44, wx.GBPosition(6, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        self.cm_textCtrl45 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                        wx.TE_READONLY)
        gbSizer3.Add(self.cm_textCtrl45, wx.GBPosition(6, 2), wx.GBSpan(1, 1), wx.ALL, 5)

        self.cm_staticText48 = wx.StaticText(self, wx.ID_ANY, u"脚部防具", wx.DefaultPosition, wx.DefaultSize, 0)
        self.cm_staticText48.Wrap(-1)
        gbSizer3.Add(self.cm_staticText48, wx.GBPosition(6, 4), wx.GBSpan(1, 1),
                     wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.cm_choice11 = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, cm_choice9Choices, 0)
        self.cm_choice11.SetSelection(4)
        gbSizer3.Add(self.cm_choice11, wx.GBPosition(6, 5), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        self.cm_choice12 = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, cm_choice10Choices, 0)
        self.cm_choice12.SetSelection(8)
        gbSizer3.Add(self.cm_choice12, wx.GBPosition(6, 6), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        self.cm_choice37 = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, cm_choice9Choices, 0)
        self.cm_choice37.SetSelection(0)
        gbSizer3.Add(self.cm_choice37, wx.GBPosition(6, 7), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        self.cm_choice38 = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, cm_choice10Choices, 0)
        self.cm_choice38.SetSelection(7)
        gbSizer3.Add(self.cm_choice38, wx.GBPosition(6, 8), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        self.cm_staticText42 = wx.StaticText(self, wx.ID_ANY, u"生命", wx.DefaultPosition, wx.DefaultSize, 0)
        self.cm_staticText42.Wrap(-1)
        gbSizer3.Add(self.cm_staticText42, wx.GBPosition(7, 0), wx.GBSpan(1, 1),
                     wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.cm_staticText55 = wx.StaticText(self, wx.ID_ANY, u"副手", wx.DefaultPosition, wx.DefaultSize, 0)
        self.cm_staticText55.Wrap(-1)
        gbSizer3.Add(self.cm_staticText55, wx.GBPosition(11, 4), wx.GBSpan(1, 1),
                     wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.cm_staticText60 = wx.StaticText(self, wx.ID_ANY, u"腰带", wx.DefaultPosition, wx.DefaultSize, 0)
        self.cm_staticText60.Wrap(-1)
        gbSizer3.Add(self.cm_staticText60, wx.GBPosition(12, 4), wx.GBSpan(1, 1),
                     wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        cm_choice25Choices = [u"隐隐的", u"小巧的", u"迅速的", u"有意义的", wx.EmptyString]
        self.cm_choice25 = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, cm_choice25Choices, 0)
        self.cm_choice25.SetSelection(4)
        gbSizer3.Add(self.cm_choice25, wx.GBPosition(12, 5), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        cm_choice14Choices = [u"热情", u"心灵", u"活力", wx.EmptyString]
        self.cm_choice26 = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, cm_choice14Choices, 0)
        self.cm_choice26.SetSelection(3)
        gbSizer3.Add(self.cm_choice26, wx.GBPosition(12, 6), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        self.cm_choice49 = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, cm_choice25Choices, 0)
        self.cm_choice49.SetSelection(4)
        gbSizer3.Add(self.cm_choice49, wx.GBPosition(12, 7), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        self.cm_choice50 = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, cm_choice14Choices, 0)
        self.cm_choice50.SetSelection(3)
        gbSizer3.Add(self.cm_choice50, wx.GBPosition(12, 8), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        self.cm_staticText61 = wx.StaticText(self, wx.ID_ANY, u"工艺品", wx.DefaultPosition, wx.DefaultSize, 0)
        self.cm_staticText61.Wrap(-1)
        gbSizer3.Add(self.cm_staticText61, wx.GBPosition(13, 4), wx.GBSpan(1, 1),
                     wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.cm_staticText64 = wx.StaticText(self, wx.ID_ANY, u"商城胸针", wx.DefaultPosition, wx.DefaultSize, 0)
        self.cm_staticText64.Wrap(-1)
        gbSizer3.Add(self.cm_staticText64, wx.GBPosition(14, 4), wx.GBSpan(1, 1),
                     wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        cm_choice53Choices = [u"迅速的", u"有意义的", u"多疑的", wx.EmptyString]
        self.cm_choice53 = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, cm_choice53Choices, 0)
        self.cm_choice53.SetSelection(3)
        gbSizer3.Add(self.cm_choice53, wx.GBPosition(14, 5), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        self.cm_choice54 = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, cm_choice14Choices, 0)
        self.cm_choice54.SetSelection(3)
        gbSizer3.Add(self.cm_choice54, wx.GBPosition(14, 6), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        self.cm_choice55 = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, cm_choice53Choices, 0)
        self.cm_choice55.SetSelection(3)
        gbSizer3.Add(self.cm_choice55, wx.GBPosition(14, 7), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        self.cm_choice56 = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, cm_choice14Choices, 0)
        self.cm_choice56.SetSelection(3)
        gbSizer3.Add(self.cm_choice56, wx.GBPosition(14, 8), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        cm_choice27Choices = [u"迅速的", u"有意义的", u"多疑的", wx.EmptyString]
        self.cm_choice27 = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, cm_choice27Choices, 0)
        self.cm_choice27.SetSelection(3)
        gbSizer3.Add(self.cm_choice27, wx.GBPosition(13, 5), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        self.cm_choice28 = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, cm_choice14Choices, 0)
        self.cm_choice28.SetSelection(3)
        gbSizer3.Add(self.cm_choice28, wx.GBPosition(13, 6), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        self.cm_choice51 = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, cm_choice27Choices, 0)
        self.cm_choice51.SetSelection(3)
        gbSizer3.Add(self.cm_choice51, wx.GBPosition(13, 7), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        self.cm_choice52 = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, cm_choice14Choices, 0)
        self.cm_choice52.SetSelection(3)
        gbSizer3.Add(self.cm_choice52, wx.GBPosition(13, 8), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        self.cm_staticline3 = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        gbSizer3.Add(self.cm_staticline3, wx.GBPosition(15, 0), wx.GBSpan(1, 9), wx.EXPAND | wx.ALL, 5)

        self.cm_staticline2 = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        gbSizer3.Add(self.cm_staticline2, wx.GBPosition(8, 0), wx.GBSpan(1, 3), wx.EXPAND | wx.ALL, 5)

        self.cm_staticText56 = wx.StaticText(self, wx.ID_ANY, u"其他增益", wx.DefaultPosition, wx.DefaultSize, 0)
        self.cm_staticText56.Wrap(-1)
        gbSizer3.Add(self.cm_staticText56, wx.GBPosition(9, 0), wx.GBSpan(1, 1),
                     wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.cm_staticText65 = wx.StaticText(self, wx.ID_ANY, u"包括商城道具精灵石等", wx.DefaultPosition, wx.DefaultSize, 0)
        self.cm_staticText65.Wrap(-1)
        gbSizer3.Add(self.cm_staticText65, wx.GBPosition(9, 1), wx.GBSpan(1, 2), wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.cm_staticText57 = wx.StaticText(self, wx.ID_ANY, u"暴击", wx.DefaultPosition, wx.DefaultSize, 0)
        self.cm_staticText57.Wrap(-1)
        gbSizer3.Add(self.cm_staticText57, wx.GBPosition(10, 0), wx.GBSpan(1, 1),
                     wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.cm_textCtrl49 = wx.TextCtrl(self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer3.Add(self.cm_textCtrl49, wx.GBPosition(10, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        self.cm_staticText58 = wx.StaticText(self, wx.ID_ANY, u"平衡", wx.DefaultPosition, wx.DefaultSize, 0)
        self.cm_staticText58.Wrap(-1)
        gbSizer3.Add(self.cm_staticText58, wx.GBPosition(11, 0), wx.GBSpan(1, 1),
                     wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.cm_textCtrl50 = wx.TextCtrl(self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer3.Add(self.cm_textCtrl50, wx.GBPosition(11, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        self.cm_staticText59 = wx.StaticText(self, wx.ID_ANY, u"攻速", wx.DefaultPosition, wx.DefaultSize, 0)
        self.cm_staticText59.Wrap(-1)
        gbSizer3.Add(self.cm_staticText59, wx.GBPosition(12, 0), wx.GBSpan(1, 1),
                     wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.cm_staticText66 = wx.StaticText(self, wx.ID_ANY, u"攻击", wx.DefaultPosition, wx.DefaultSize, 0)
        self.cm_staticText66.Wrap(-1)
        gbSizer3.Add(self.cm_staticText66, wx.GBPosition(13, 0), wx.GBSpan(1, 1), wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.cm_textCtrl52 = wx.TextCtrl(self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer3.Add(self.cm_textCtrl52, wx.GBPosition(13, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        self.cm_button9 = wx.Button(self, wx.ID_ANY, u"初始化", wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer3.Add(self.cm_button9, wx.GBPosition(13, 2), wx.GBSpan(2, 1), wx.ALL | wx.EXPAND, 5)

        self.cm_staticText67 = wx.StaticText(self, wx.ID_ANY, u"防御", wx.DefaultPosition, wx.DefaultSize, 0)
        self.cm_staticText67.Wrap(-1)
        gbSizer3.Add(self.cm_staticText67, wx.GBPosition(14, 0), wx.GBSpan(1, 1), wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.cm_textCtrl511 = wx.TextCtrl(self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer3.Add(self.cm_textCtrl511, wx.GBPosition(14, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        self.cm_textCtrl51 = wx.TextCtrl(self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer3.Add(self.cm_textCtrl51, wx.GBPosition(12, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        self.cm_button8 = wx.Button(self, wx.ID_ANY, u"计算", wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer3.Add(self.cm_button8, wx.GBPosition(10, 2), wx.GBSpan(3, 1), wx.ALL | wx.EXPAND, 5)

        cm_choice23Choices = [u"洒脱的", u"惊心动魄的", u"贤者的", u"封印的", wx.EmptyString]
        self.cm_choice23 = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, cm_choice23Choices, 0)
        self.cm_choice23.SetSelection(4)
        gbSizer3.Add(self.cm_choice23, wx.GBPosition(11, 5), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        cm_choice24Choices = [u"金刚石", u"倾盆大雨", u"真实", wx.EmptyString]
        self.cm_choice24 = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, cm_choice24Choices, 0)
        self.cm_choice24.SetSelection(3)
        gbSizer3.Add(self.cm_choice24, wx.GBPosition(11, 6), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        self.cm_choice47 = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, cm_choice23Choices, 0)
        self.cm_choice47.SetSelection(4)
        gbSizer3.Add(self.cm_choice47, wx.GBPosition(11, 7), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        self.cm_choice48 = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, cm_choice24Choices, 0)
        self.cm_choice48.SetSelection(3)
        gbSizer3.Add(self.cm_choice48, wx.GBPosition(11, 8), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        self.cm_textCtrl46 = wx.TextCtrl(self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer3.Add(self.cm_textCtrl46, wx.GBPosition(7, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        self.cm_textCtrl47 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                        wx.TE_READONLY)
        gbSizer3.Add(self.cm_textCtrl47, wx.GBPosition(7, 2), wx.GBSpan(1, 1), wx.ALL, 5)

        self.cm_staticText49 = wx.StaticText(self, wx.ID_ANY, u"戒指1", wx.DefaultPosition, wx.DefaultSize, 0)
        self.cm_staticText49.Wrap(-1)
        gbSizer3.Add(self.cm_staticText49, wx.GBPosition(7, 4), wx.GBSpan(1, 1),
                     wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.cm_staticText50 = wx.StaticText(self, wx.ID_ANY, u"戒指2", wx.DefaultPosition, wx.DefaultSize, 0)
        self.cm_staticText50.Wrap(-1)
        gbSizer3.Add(self.cm_staticText50, wx.GBPosition(8, 4), wx.GBSpan(1, 1),
                     wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        cm_choice13Choices = [u"亡者的", u"闪亮的", u"迅速的", u"有意义的", u"多疑的", wx.EmptyString]
        self.cm_choice15 = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, cm_choice13Choices, 0)
        self.cm_choice15.SetSelection(5)
        gbSizer3.Add(self.cm_choice15, wx.GBPosition(8, 5), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        self.cm_choice16 = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, cm_choice14Choices, 0)
        self.cm_choice16.SetSelection(3)
        gbSizer3.Add(self.cm_choice16, wx.GBPosition(8, 6), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        self.cm_choice41 = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, cm_choice13Choices, 0)
        self.cm_choice41.SetSelection(5)
        gbSizer3.Add(self.cm_choice41, wx.GBPosition(8, 7), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        self.cm_choice42 = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, cm_choice14Choices, 0)
        self.cm_choice42.SetSelection(3)
        gbSizer3.Add(self.cm_choice42, wx.GBPosition(8, 8), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        self.cm_staticText51 = wx.StaticText(self, wx.ID_ANY, u"耳环", wx.DefaultPosition, wx.DefaultSize, 0)
        self.cm_staticText51.Wrap(-1)
        gbSizer3.Add(self.cm_staticText51, wx.GBPosition(9, 4), wx.GBSpan(1, 1),
                     wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        cm_choice17Choices = [u"迅速的", u"有意义的", u"多疑的", wx.EmptyString]
        self.cm_choice17 = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, cm_choice17Choices, 0)
        self.cm_choice17.SetSelection(3)
        gbSizer3.Add(self.cm_choice17, wx.GBPosition(9, 5), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        self.cm_choice18 = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, cm_choice14Choices, 0)
        self.cm_choice18.SetSelection(3)
        gbSizer3.Add(self.cm_choice18, wx.GBPosition(9, 6), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        self.cm_choice43 = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, cm_choice17Choices, 0)
        self.cm_choice43.SetSelection(3)
        gbSizer3.Add(self.cm_choice43, wx.GBPosition(9, 7), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        self.cm_choice44 = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, cm_choice14Choices, 0)
        self.cm_choice44.SetSelection(3)
        gbSizer3.Add(self.cm_choice44, wx.GBPosition(9, 8), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        self.cm_staticText52 = wx.StaticText(self, wx.ID_ANY, u"胸针", wx.DefaultPosition, wx.DefaultSize, 0)
        self.cm_staticText52.Wrap(-1)
        gbSizer3.Add(self.cm_staticText52, wx.GBPosition(10, 4), wx.GBSpan(1, 1),
                     wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        cm_choice19Choices = [u"星光", u"宝物猎人的", u"迅速的", u"有意义的", u"多疑的", wx.EmptyString]
        self.cm_choice19 = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, cm_choice19Choices, 0)
        self.cm_choice19.SetSelection(5)
        gbSizer3.Add(self.cm_choice19, wx.GBPosition(10, 5), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        cm_choice20Choices = [u"高尚的", u"热情", u"心灵", u"活力", wx.EmptyString]
        self.cm_choice20 = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, cm_choice20Choices, 0)
        self.cm_choice20.SetSelection(4)
        gbSizer3.Add(self.cm_choice20, wx.GBPosition(10, 6), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        self.cm_choice45 = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, cm_choice19Choices, 0)
        self.cm_choice45.SetSelection(5)
        gbSizer3.Add(self.cm_choice45, wx.GBPosition(10, 7), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        self.cm_choice46 = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, cm_choice20Choices, 0)
        self.cm_choice46.SetSelection(4)
        gbSizer3.Add(self.cm_choice46, wx.GBPosition(10, 8), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        self.cm_choice13 = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, cm_choice13Choices, 0)
        self.cm_choice13.SetSelection(5)
        gbSizer3.Add(self.cm_choice13, wx.GBPosition(7, 5), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        self.cm_choice14 = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, cm_choice14Choices, 0)
        self.cm_choice14.SetSelection(3)
        gbSizer3.Add(self.cm_choice14, wx.GBPosition(7, 6), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        self.cm_choice39 = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, cm_choice13Choices, 0)
        self.cm_choice39.SetSelection(5)
        gbSizer3.Add(self.cm_choice39, wx.GBPosition(7, 7), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        self.cm_choice40 = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, cm_choice14Choices, 0)
        self.cm_choice40.SetSelection(3)
        gbSizer3.Add(self.cm_choice40, wx.GBPosition(7, 8), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        self.cm_staticline1 = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL)
        gbSizer3.Add(self.cm_staticline1, wx.GBPosition(0, 3), wx.GBSpan(15, 1), wx.EXPAND | wx.ALL, 5)

        self.cm_staticText35 = wx.StaticText(self, wx.ID_ANY, u"After", wx.DefaultPosition, wx.DefaultSize, 0)
        self.cm_staticText35.Wrap(-1)
        gbSizer3.Add(self.cm_staticText35, wx.GBPosition(0, 2), wx.GBSpan(1, 1),
                     wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.cm_staticText53 = wx.StaticText(self, wx.ID_ANY, u"前缀当前", wx.DefaultPosition, wx.DefaultSize, 0)
        self.cm_staticText53.Wrap(-1)
        gbSizer3.Add(self.cm_staticText53, wx.GBPosition(0, 5), wx.GBSpan(1, 1),
                     wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.cm_staticText54 = wx.StaticText(self, wx.ID_ANY, u"后缀当前", wx.DefaultPosition, wx.DefaultSize, 0)
        self.cm_staticText54.Wrap(-1)
        gbSizer3.Add(self.cm_staticText54, wx.GBPosition(0, 6), wx.GBSpan(1, 1),
                     wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.cm_staticText62 = wx.StaticText(self, wx.ID_ANY, u"前缀更改", wx.DefaultPosition, wx.DefaultSize, 0)
        self.cm_staticText62.Wrap(-1)
        gbSizer3.Add(self.cm_staticText62, wx.GBPosition(0, 7), wx.GBSpan(1, 1),
                     wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.cm_staticText63 = wx.StaticText(self, wx.ID_ANY, u"后缀更改", wx.DefaultPosition, wx.DefaultSize, 0)
        self.cm_staticText63.Wrap(-1)
        gbSizer3.Add(self.cm_staticText63, wx.GBPosition(0, 8), wx.GBSpan(1, 1),
                     wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.SetSizer(gbSizer3)
        self.Layout()

        # Connect Events
        # self.cm_choice271.Bind(wx.EVT_CHOICE, self.choice271)
        # self.cm_choice281.Bind(wx.EVT_CHOICE, self.choice281)
        # self.cm_choice29.Bind(wx.EVT_CHOICE, self.choice29)
        # self.cm_choice30.Bind(wx.EVT_CHOICE, self.choice30)
        # self.cm_choice31.Bind(wx.EVT_CHOICE, self.choice31)
        # self.cm_choice32.Bind(wx.EVT_CHOICE, self.choice32)
        # self.cm_choice33.Bind(wx.EVT_CHOICE, self.choice33)
        # self.cm_choice34.Bind(wx.EVT_CHOICE, self.choice34)
        # self.cm_choice35.Bind(wx.EVT_CHOICE, self.choice35)
        # self.cm_choice36.Bind(wx.EVT_CHOICE, self.choice36)
        # self.cm_choice37.Bind(wx.EVT_CHOICE, self.choice37)
        # self.cm_choice38.Bind(wx.EVT_CHOICE, self.choice38)
        # self.cm_choice39.Bind(wx.EVT_CHOICE, self.choice39)
        # self.cm_choice40.Bind(wx.EVT_CHOICE, self.choice40)
        # self.cm_choice41.Bind(wx.EVT_CHOICE, self.choice41)
        # self.cm_choice42.Bind(wx.EVT_CHOICE, self.choice42)
        # self.cm_choice42.Bind(wx.EVT_CHOICE, self.choice43)
        # self.cm_choice42.Bind(wx.EVT_CHOICE, self.choice44)
        # self.cm_choice42.Bind(wx.EVT_CHOICE, self.choice45)
        # self.cm_choice42.Bind(wx.EVT_CHOICE, self.choice46)
        # self.cm_choice42.Bind(wx.EVT_CHOICE, self.choice47)
        # self.cm_choice42.Bind(wx.EVT_CHOICE, self.choice48)
        # self.cm_choice42.Bind(wx.EVT_CHOICE, self.choice49)
        # self.cm_choice42.Bind(wx.EVT_CHOICE, self.choice50)
        # self.cm_choice42.Bind(wx.EVT_CHOICE, self.choice51)
        # self.cm_choice42.Bind(wx.EVT_CHOICE, self.choice52)
        # self.cm_choice42.Bind(wx.EVT_CHOICE, self.choice55)
        # self.cm_choice42.Bind(wx.EVT_CHOICE, self.choice56)
        self.cm_button8.Bind(wx.EVT_BUTTON, self.calculate)
        self.cm_button9.Bind(wx.EVT_BUTTON, self.init_cal)
        self.cm_textCtrl34.Bind(wx.EVT_TEXT, self.textctrl34)
        self.cm_textCtrl36.Bind(wx.EVT_TEXT, self.textctrl36)
        self.cm_textCtrl38.Bind(wx.EVT_TEXT, self.textctrl38)
        self.cm_textCtrl40.Bind(wx.EVT_TEXT, self.textctrl40)
        self.cm_textCtrl42.Bind(wx.EVT_TEXT, self.textctrl42)
        self.cm_textCtrl44.Bind(wx.EVT_TEXT, self.textctrl44)
        self.cm_textCtrl46.Bind(wx.EVT_TEXT, self.textctrl46)

        # 定义全局变量 增量与减量并初始化为0
        global attack_mall
        global defence_mall
        global crit_mall
        global balance_mall
        global speed_mall
        global resistance_mall
        global hp_mall
        global hp_pall
        global attack_pall
        global defence_pall
        global crit_pall
        global balance_pall
        global speed_pall
        global resistance_pall
        global hp_now
        global attack_now
        global defence_now
        global crit_now
        global balance_now
        global speed_now
        global resistance_now
        global hp_other
        global attack_other
        global defence_other
        global crit_other
        global balance_other
        global speed_other
        global resistance_other
        attack_mall = 0
        defence_mall = 0
        crit_mall = 0
        balance_mall = 0
        speed_mall = 0
        resistance_mall = 0
        hp_mall = 0
        hp_pall = 0
        attack_pall = 0
        defence_pall = 0
        crit_pall = 0
        balance_pall = 0
        speed_pall = 0
        resistance_pall = 0
        hp_now = 0
        attack_now = 0
        defence_now = 0
        crit_now = 0
        balance_now = 0
        speed_now = 0
        resistance_now = 0
        hp_other = 0
        attack_other = 0
        defence_other = 0
        crit_other = 0
        balance_other = 0
        speed_other = 0
        resistance_other = 0

    def textctrl34(self, event):
        global attack_now
        attack_now = int(self.cm_textCtrl34.GetValue())
        if attack_now > 48000:
            dlg = wx.MessageDialog(None, u"您的输入超过最大值，请检查", u"错误", wx.OK | wx.ICON_QUESTION)
            if dlg.ShowModal() == wx.ID_YES:
                self.Close(True)
            dlg.Destroy()
            self.cm_textCtrl34.SetValue('')
            attack_now = 0
        event.Skip()

    def textctrl36(self, event):
        global defence_now
        defence_now = int(self.cm_textCtrl36.GetValue())
        if defence_now > 35000:
            dlg = wx.MessageDialog(None, u"您的输入超过最大值，请检查", u"错误", wx.OK | wx.ICON_QUESTION)
            if dlg.ShowModal() == wx.ID_YES:
                self.Close(True)
            dlg.Destroy()
            self.cm_textCtrl36.SetValue('')
            defence_now = 0
        event.Skip()

    def textctrl38(self, event):
        global crit_now
        crit_now = int(self.cm_textCtrl38.GetValue())
        if crit_now > 200:
            dlg = wx.MessageDialog(None, u"您的输入超过最大值，请检查", u"错误", wx.OK | wx.ICON_QUESTION)
            if dlg.ShowModal() == wx.ID_YES:
                self.Close(True)
            dlg.Destroy()
            self.cm_textCtrl38.SetValue('')
            crit_now = 0
        event.Skip()

    def textctrl40(self, event):
        global balance_now
        balance_now = int(self.cm_textCtrl40.GetValue())
        if balance_now > 150:
            dlg = wx.MessageDialog(None, u"您的输入超过最大值，请检查", u"错误", wx.OK | wx.ICON_QUESTION)
            if dlg.ShowModal() == wx.ID_YES:
                self.Close(True)
            dlg.Destroy()
            self.cm_textCtrl40.SetValue('')
            balance_now = 0
        event.Skip()

    def textctrl42(self, event):
        global speed_now
        speed_now = int(self.cm_textCtrl42.GetValue())
        if speed_now > 150:
            dlg = wx.MessageDialog(None, u"您的输入超过最大值，请检查", u"错误", wx.OK | wx.ICON_QUESTION)
            if dlg.ShowModal() == wx.ID_YES:
                self.Close(True)
            dlg.Destroy()
            self.cm_textCtrl42.SetValue('')
            speed_now = 0
        event.Skip()

    def textctrl44(self, event):
        global resistance_now
        resistance_now = int(self.cm_textCtrl44.GetValue())
        if resistance_now > 200:
            dlg = wx.MessageDialog(None, u"您的输入超过最大值，请检查", u"错误", wx.OK | wx.ICON_QUESTION)
            if dlg.ShowModal() == wx.ID_YES:
                self.Close(True)
            dlg.Destroy()
            self.cm_textCtrl44.SetValue('')
            resistance_now = 0
        event.Skip()

    def textctrl46(self, event):
        global hp_now
        hp_now = int(self.cm_textCtrl46.GetValue())
        if hp_now > 200000:
            dlg = wx.MessageDialog(None, u"您的输入超过最大值，请检查", u"错误", wx.OK | wx.ICON_QUESTION)
            if dlg.ShowModal() == wx.ID_YES:
                self.Close(True)
            dlg.Destroy()
            self.cm_textCtrl46.SetValue('')
            hp_now = 0
        event.Skip()

    def init_cal(self, event):
        self.cm_choice1.SetSelection(8)
        self.cm_choice2.SetSelection(8)
        self.cm_choice3.SetSelection(4)
        self.cm_choice4.SetSelection(8)
        self.cm_choice5.SetSelection(4)
        self.cm_choice6.SetSelection(7)
        self.cm_choice7.SetSelection(4)
        self.cm_choice8.SetSelection(8)
        self.cm_choice9.SetSelection(4)
        self.cm_choice10.SetSelection(8)
        self.cm_choice11.SetSelection(4)
        self.cm_choice12.SetSelection(8)
        self.cm_choice13.SetSelection(5)
        self.cm_choice14.SetSelection(3)
        self.cm_choice15.SetSelection(5)
        self.cm_choice16.SetSelection(3)
        self.cm_choice17.SetSelection(3)
        self.cm_choice18.SetSelection(3)
        self.cm_choice19.SetSelection(5)
        self.cm_choice20.SetSelection(4)
        self.cm_choice23.SetSelection(4)
        self.cm_choice24.SetSelection(3)
        self.cm_choice25.SetSelection(4)
        self.cm_choice26.SetSelection(3)
        self.cm_choice27.SetSelection(3)
        self.cm_choice28.SetSelection(3)
        self.cm_choice53.SetSelection(3)
        self.cm_choice54.SetSelection(3)
        self.cm_choice271.SetSelection(8)
        self.cm_choice281.SetSelection(8)
        self.cm_choice29.SetSelection(4)
        self.cm_choice30.SetSelection(8)
        self.cm_choice31.SetSelection(4)
        self.cm_choice32.SetSelection(7)
        self.cm_choice33.SetSelection(4)
        self.cm_choice34.SetSelection(8)
        self.cm_choice35.SetSelection(4)
        self.cm_choice36.SetSelection(8)
        self.cm_choice37.SetSelection(4)
        self.cm_choice38.SetSelection(8)
        self.cm_choice39.SetSelection(5)
        self.cm_choice40.SetSelection(3)
        self.cm_choice41.SetSelection(5)
        self.cm_choice42.SetSelection(3)
        self.cm_choice43.SetSelection(3)
        self.cm_choice44.SetSelection(3)
        self.cm_choice45.SetSelection(5)
        self.cm_choice46.SetSelection(4)
        self.cm_choice47.SetSelection(4)
        self.cm_choice48.SetSelection(3)
        self.cm_choice49.SetSelection(4)
        self.cm_choice50.SetSelection(3)
        self.cm_choice51.SetSelection(3)
        self.cm_choice52.SetSelection(3)
        self.cm_choice55.SetSelection(3)
        self.cm_choice56.SetSelection(3)
        event.Skip()

    def calculate(self, event):
        global attack_now
        global defence_now
        global crit_now
        global balance_now
        global speed_now
        global resistance_now
        global hp_now
        global attack_mall
        global defence_mall
        global crit_mall
        global balance_mall
        global speed_mall
        global resistance_mall
        global hp_mall
        global hp_pall
        global attack_pall
        global defence_pall
        global crit_pall
        global balance_pall
        global speed_pall
        global resistance_pall
        global hp_other
        global attack_other
        global defence_other
        global crit_other
        global balance_other
        global speed_other
        global resistance_other

        # 获取其他增量
        attack_other = int(self.cm_textCtrl52.GetValue())
        defence_other = int(self.cm_textCtrl511.GetValue())
        crit_other = int(self.cm_textCtrl49.GetValue())
        balance_other = int(self.cm_textCtrl50.GetValue())
        speed_other = int(self.cm_textCtrl51.GetValue())

        # 武器首次
        n = self.cm_choice1.GetSelection()
        attack_minus, defence_minus, crit_minus, balance_minus, speed_minus, resistance_minus = enchant_weapon0(n)
        n1 = self.cm_choice271.GetSelection()
        attack_plus, defence_plus, crit_plus, balance_plus, speed_plus, resistance_plus = enchant_weapon0(n1)
        attack_mall = attack_mall + attack_minus
        defence_mall = defence_mall + defence_minus
        crit_mall = crit_mall + crit_minus
        balance_mall = balance_mall + balance_minus
        speed_mall = speed_mall + speed_minus
        resistance_mall = resistance_mall + resistance_minus
        attack_pall = attack_pall + attack_plus
        defence_pall = defence_pall + defence_plus
        crit_pall = crit_pall + crit_plus
        balance_pall = balance_pall + balance_plus
        speed_pall = speed_pall + speed_plus
        resistance_pall = resistance_pall + resistance_plus

        # 武器后缀
        n = self.cm_choice2.GetSelection()
        attack_minus, defence_minus, crit_minus, balance_minus, speed_minus, resistance_minus = enchant_weapon1(n)
        n1 = self.cm_choice281.GetSelection()
        attack_plus, defence_plus, crit_plus, balance_plus, speed_plus, resistance_plus = enchant_weapon1(n1)
        attack_mall = attack_mall + attack_minus
        defence_mall = defence_mall + defence_minus
        crit_mall = crit_mall + crit_minus
        balance_mall = balance_mall + balance_minus
        speed_mall = speed_mall + speed_minus
        resistance_mall = resistance_mall + resistance_minus
        attack_pall = attack_pall + attack_plus
        defence_pall = defence_pall + defence_plus
        crit_pall = crit_pall + crit_plus
        balance_pall = balance_pall + balance_plus
        speed_pall = speed_pall + speed_plus
        resistance_pall = resistance_pall + resistance_plus

        # 头部防具首次
        nn = self.cm_choice3.GetSelection()
        if nn == 1:
            n = 2
        elif nn == 2 or nn == 3 or nn == 4:
            n = nn + 3
        else:
            n = nn
        attack_minus, defence_minus, crit_minus, balance_minus, \
            speed_minus, resistance_minus, hp_minus = enchant_armor0(n)
        nn1 = self.cm_choice29.GetSelection()
        if nn1 == 1:
            n1 = 2
        elif nn1 == 2 or nn1 == 3 or nn1 == 4:
            n1 = nn1 + 3
        else:
            n1 = nn1
        attack_plus, defence_plus, crit_plus, balance_plus, \
            speed_plus, resistance_plus, hp_plus = enchant_armor0(n1)
        attack_mall = attack_mall + attack_minus
        defence_mall = defence_mall + defence_minus
        crit_mall = crit_mall + crit_minus
        balance_mall = balance_mall + balance_minus
        speed_mall = speed_mall + speed_minus
        resistance_mall = resistance_mall + resistance_minus
        hp_mall = hp_mall + hp_minus
        attack_pall = attack_pall + attack_plus
        defence_pall = defence_pall + defence_plus
        crit_pall = crit_pall + crit_plus
        balance_pall = balance_pall + balance_plus
        speed_pall = speed_pall + speed_plus
        resistance_pall = resistance_pall + resistance_plus
        hp_pall = hp_pall + hp_plus

        # 头部防具后缀
        nn = self.cm_choice4.GetSelection()
        if (nn <= 4) & (nn > 0):
            n = nn + 1
        elif nn == 7:
            n = 11
        elif nn == 0:
            n = 1
        elif nn == 8:
            n = 100
        else:
            n = nn + 3

        attack_minus, defence_minus, crit_minus, balance_minus, speed_minus, resistance_minus = enchant_armor1(n)

        nn1 = self.cm_choice30.GetSelection()
        if (nn1 <= 4) & (nn1 > 0):
            n1 = nn1 + 1
        elif nn1 == 0:
            n1 = 1
        elif nn1 == 7:
            n1 = 11
        elif nn1 == 8:
            n1 = 100
        else:
            n1 = nn1 + 3


        attack_plus, defence_plus, crit_plus, balance_plus, speed_plus, resistance_plus = enchant_armor1(n1)

        attack_mall = attack_mall + attack_minus
        defence_mall = defence_mall + defence_minus
        crit_mall = crit_mall + crit_minus
        balance_mall = balance_mall + balance_minus
        speed_mall = speed_mall + speed_minus
        resistance_mall = resistance_mall + resistance_minus
        attack_pall = attack_pall + attack_plus
        defence_pall = defence_pall + defence_plus
        crit_pall = crit_pall + crit_plus
        balance_pall = balance_pall + balance_plus
        speed_pall = speed_pall + speed_plus
        resistance_pall = resistance_pall + resistance_plus

        # 胸部防具首次
        nn = self.cm_choice5.GetSelection()
        n = nn + 4
        attack_minus, defence_minus, crit_minus, balance_minus, \
            speed_minus, resistance_minus, hp_minus = enchant_armor0(n)
        nn1 = self.cm_choice31.GetSelection()
        n1 = nn1 + 4
        attack_plus, defence_plus, crit_plus, balance_plus, \
            speed_plus, resistance_plus, hp_plus = enchant_armor0(n1)
        attack_mall = attack_mall + attack_minus
        defence_mall = defence_mall + defence_minus
        crit_mall = crit_mall + crit_minus
        balance_mall = balance_mall + balance_minus
        speed_mall = speed_mall + speed_minus
        resistance_mall = resistance_mall + resistance_minus
        hp_mall = hp_mall + hp_minus
        hp_pall = hp_pall + hp_plus
        attack_pall = attack_pall + attack_plus
        defence_pall = defence_pall + defence_plus
        crit_pall = crit_pall + crit_plus
        balance_pall = balance_pall + balance_plus
        speed_pall = speed_pall + speed_plus
        resistance_pall = resistance_pall + resistance_plus

        # 胸部防具后缀
        nn = self.cm_choice6.GetSelection()
        if (nn == 0) or (nn == 1):
            n = nn + 6
        elif nn == 2:
            n = 4
        elif nn == 3 or nn == 4:
            n = nn - 1
        elif nn == 5:
            n = nn
        elif nn == 6:
            n = 12
        else:
            n = 100
        attack_minus, defence_minus, crit_minus, balance_minus, speed_minus, resistance_minus = enchant_armor1(n)
        nn1 = self.cm_choice32.GetSelection()
        if (nn1 == 0) or (nn1 == 1):
            n1 = nn1 + 6
        elif nn1 == 2:
            n1 = 4
        elif nn1 == 3 or nn1 == 4:
            n1 = nn1 - 1
        elif nn1 == 5:
            n1 = nn1
        elif nn1 == 6:
            n1 = 12
        else:
            n1 = 100
        attack_plus, defence_plus, crit_plus, balance_plus, speed_plus, resistance_plus = enchant_armor1(n1)
        attack_mall = attack_mall + attack_minus
        defence_mall = defence_mall + defence_minus
        crit_mall = crit_mall + crit_minus
        balance_mall = balance_mall + balance_minus
        speed_mall = speed_mall + speed_minus
        resistance_mall = resistance_mall + resistance_minus
        attack_pall = attack_pall + attack_plus
        defence_pall = defence_pall + defence_plus
        crit_pall = crit_pall + crit_plus
        balance_pall = balance_pall + balance_plus
        speed_pall = speed_pall + speed_plus
        resistance_pall = resistance_pall + resistance_plus

        # 腿部防具首次
        nn = self.cm_choice7.GetSelection()
        if nn == 1:
            n = 2
        elif nn == 2 or nn == 3 or nn == 4:
            n = nn + 3
        else:
            n = nn
        attack_minus, defence_minus, crit_minus, balance_minus, \
            speed_minus, resistance_minus, hp_minus = enchant_armor0(n)
        nn1 = self.cm_choice33.GetSelection()
        if nn1 == 1:
            n1 = 2
        elif nn1 == 2 or nn1 == 3 or nn1 == 4:
            n1 = nn1 + 3
        else:
            n1 = nn1
        attack_plus, defence_plus, crit_plus, balance_plus, speed_plus, resistance_plus, hp_plus = enchant_armor0(n1)
        attack_mall = attack_mall + attack_minus
        defence_mall = defence_mall + defence_minus
        crit_mall = crit_mall + crit_minus
        balance_mall = balance_mall + balance_minus
        speed_mall = speed_mall + speed_minus
        resistance_mall = resistance_mall + resistance_minus
        hp_mall = hp_mall + hp_minus
        hp_pall = hp_pall + hp_plus
        attack_pall = attack_pall + attack_plus
        defence_pall = defence_pall + defence_plus
        crit_pall = crit_pall + crit_plus
        balance_pall = balance_pall + balance_plus
        speed_pall = speed_pall + speed_plus
        resistance_pall = resistance_pall + resistance_plus

        # 腿部防具后缀
        nn = self.cm_choice8.GetSelection()
        if (nn <= 4) & (nn > 0):
            n = nn + 1
        elif nn == 7:
            n = 11
        elif nn == 0:
            n = 100
        elif nn == 8:
            n = 100
        else:
            n = nn + 3
        attack_minus, defence_minus, crit_minus, balance_minus, speed_minus, resistance_minus = enchant_armor1(n)
        nn1 = self.cm_choice34.GetSelection()
        if (nn1 <= 4) & (nn1 > 0):
            n1 = nn1 + 1
        elif nn1 == 0:
            n1 = 1
        elif nn1 == 7:
            n1 = 11
        elif nn1 == 8:
            n1 = 100
        else:
            n1 = nn1 + 3
        attack_plus, defence_plus, crit_plus, balance_plus, speed_plus, resistance_plus = enchant_armor1(n1)
        attack_mall = attack_mall + attack_minus
        defence_mall = defence_mall + defence_minus
        crit_mall = crit_mall + crit_minus
        balance_mall = balance_mall + balance_minus
        speed_mall = speed_mall + speed_minus
        resistance_mall = resistance_mall + resistance_minus
        attack_pall = attack_pall + attack_plus
        defence_pall = defence_pall + defence_plus
        crit_pall = crit_pall + crit_plus
        balance_pall = balance_pall + balance_plus
        speed_pall = speed_pall + speed_plus
        resistance_pall = resistance_pall + resistance_plus

        # 手部防具首次
        nn = self.cm_choice9.GetSelection()
        if nn == 1:
            n = 3
        elif nn == 2 or nn == 3 or nn == 4:
            n = nn + 3
        else:
            n = nn + 1
        attack_minus, defence_minus, crit_minus, balance_minus, \
            speed_minus, resistance_minus, hp_minus = enchant_armor0(n)
        nn1 = self.cm_choice35.GetSelection()
        if nn1 == 1:
            n1 = 3
        elif nn1 == 2 or nn1 == 3 or nn1 == 4:
            n1 = nn1 + 3
        else:
            n1 = nn1 + 1
        attack_plus, defence_plus, crit_plus, balance_plus, \
            speed_plus, resistance_plus, hp_plus = enchant_armor0(n1)
        attack_mall = attack_mall + attack_minus
        defence_mall = defence_mall + defence_minus
        crit_mall = crit_mall + crit_minus
        balance_mall = balance_mall + balance_minus
        speed_mall = speed_mall + speed_minus
        resistance_mall = resistance_mall + resistance_minus
        hp_mall = hp_mall + hp_minus
        hp_pall = hp_pall + hp_plus
        attack_pall = attack_pall + attack_plus
        defence_pall = defence_pall + defence_plus
        crit_pall = crit_pall + crit_plus
        balance_pall = balance_pall + balance_plus
        speed_pall = speed_pall + speed_plus
        resistance_pall = resistance_pall + resistance_plus

        # 手部防具后缀
        nn = self.cm_choice10.GetSelection()
        if (nn <= 4) & (nn > 0):
            n = nn + 1
        elif nn == 0:
            n = 0
        elif nn == 7:
            n = 10
        elif nn == 8:
            n = 100
        else:
            n = nn + 3
        attack_minus, defence_minus, crit_minus, balance_minus, speed_minus, resistance_minus = enchant_armor1(n)
        nn1 = self.cm_choice36.GetSelection()
        if (nn1 <= 4) & (nn1 > 0):
            n1 = nn1 + 1
        elif nn1 == 0:
            n1 = 0
        elif nn1 == 7:
            n1 = 10
        elif nn1 == 8:
            n1 = 100
        else:
            n1 = nn1 + 3
        attack_plus, defence_plus, crit_plus, balance_plus, speed_plus, resistance_plus = enchant_armor1(n1)
        attack_mall = attack_mall + attack_minus
        defence_mall = defence_mall + defence_minus
        crit_mall = crit_mall + crit_minus
        balance_mall = balance_mall + balance_minus
        speed_mall = speed_mall + speed_minus
        resistance_mall = resistance_mall + resistance_minus
        attack_pall = attack_pall + attack_plus
        defence_pall = defence_pall + defence_plus
        crit_pall = crit_pall + crit_plus
        balance_pall = balance_pall + balance_plus
        speed_pall = speed_pall + speed_plus
        resistance_pall = resistance_pall + resistance_plus

        # 脚部防具首次
        nn = self.cm_choice11.GetSelection()
        if nn == 1:
            n = 3
        elif nn == 2 or nn == 3 or nn == 4:
            n = nn + 3
        else:
            n = nn + 1
        attack_minus, defence_minus, crit_minus, balance_minus, \
            speed_minus, resistance_minus, hp_minus = enchant_armor0(n)
        nn1 = self.cm_choice37.GetSelection()
        if nn1 == 1:
            n1 = 3
        elif nn1 == 2 or nn1 == 3 or nn1 == 4:
            n1 = nn1 + 3
        else:
            n1 = nn1 + 1
        attack_plus, defence_plus, crit_plus, balance_plus, \
            speed_plus, resistance_plus, hp_plus = enchant_armor0(n1)
        attack_mall = attack_mall + attack_minus
        defence_mall = defence_mall + defence_minus
        crit_mall = crit_mall + crit_minus
        balance_mall = balance_mall + balance_minus
        speed_mall = speed_mall + speed_minus
        resistance_mall = resistance_mall + resistance_minus
        hp_mall = hp_mall + hp_minus
        hp_pall = hp_pall + hp_plus
        attack_pall = attack_pall + attack_plus
        defence_pall = defence_pall + defence_plus
        crit_pall = crit_pall + crit_plus
        balance_pall = balance_pall + balance_plus
        speed_pall = speed_pall + speed_plus
        resistance_pall = resistance_pall + resistance_plus

        # 脚部防具后缀
        nn = self.cm_choice12.GetSelection()
        if (nn <= 4) & (nn > 0):
            n = nn + 1
        elif nn == 0:
            n = 0
        elif nn == 7:
            n = 10
        elif nn == 8:
            n = 100
        else:
            n = nn + 3
        attack_minus, defence_minus, crit_minus, balance_minus, speed_minus, resistance_minus = enchant_armor1(n)
        nn1 = self.cm_choice38.GetSelection()
        if (nn1 <= 4) & (nn1 > 0):
            n1 = nn1 + 1
        elif nn1 == 0:
            n1 = 0
        elif nn1 == 7:
            n1 = 10
        elif nn1 == 8:
            n1 = 100
        else:
            n1 = nn1 + 3
        attack_plus, defence_plus, crit_plus, balance_plus, speed_plus, resistance_plus = enchant_armor1(n1)
        attack_mall = attack_mall + attack_minus
        defence_mall = defence_mall + defence_minus
        crit_mall = crit_mall + crit_minus
        balance_mall = balance_mall + balance_minus
        speed_mall = speed_mall + speed_minus
        resistance_mall = resistance_mall + resistance_minus
        attack_pall = attack_pall + attack_plus
        defence_pall = defence_pall + defence_plus
        crit_pall = crit_pall + crit_plus
        balance_pall = balance_pall + balance_plus
        speed_pall = speed_pall + speed_plus
        resistance_pall = resistance_pall + resistance_plus

        # 戒指1首次
        nn = self.cm_choice13.GetSelection()
        if nn == 1:
            n = 2
        elif nn == 2 or nn == 3 or nn == 4:
            n = nn + 2
        elif nn == 0:
            n = nn
        else:
            n = 100
        attack_minus, defence_minus, crit_minus, balance_minus, \
            speed_minus, resistance_minus, hp_minus = enchant_jewelry0(n)
        nn1 = self.cm_choice39.GetSelection()
        if nn1 == 1:
            n1 = 2
        elif nn1 == 2 or nn1 == 3 or nn1 == 4:
            n1 = nn1 + 2
        elif nn1 == 0:
            n1 = nn1
        else:
            n1 = 100
        attack_plus, defence_plus, crit_plus, balance_plus, \
            speed_plus, resistance_plus, hp_plus = enchant_jewelry0(n1)
        attack_mall = attack_mall + attack_minus
        defence_mall = defence_mall + defence_minus
        crit_mall = crit_mall + crit_minus
        balance_mall = balance_mall + balance_minus
        speed_mall = speed_mall + speed_minus
        resistance_mall = resistance_mall + resistance_minus
        hp_mall = hp_mall + hp_minus
        hp_pall = hp_pall + hp_plus
        attack_pall = attack_pall + attack_plus
        defence_pall = defence_pall + defence_plus
        crit_pall = crit_pall + crit_plus
        balance_pall = balance_pall + balance_plus
        speed_pall = speed_pall + speed_plus
        resistance_pall = resistance_pall + resistance_plus

        # 戒指1后缀
        nn = self.cm_choice14.GetSelection()
        if nn != 3:
            n = nn + 1
        else:
            n = 100
        attack_minus, defence_minus, crit_minus, balance_minus, \
            speed_minus, resistance_minus, hp_minus = enchant_jewelry1(n)
        nn1 = self.cm_choice40.GetSelection()
        if nn1 != 3:
            n1 = nn1 + 1
        else:
            n1 = 100
        attack_plus, defence_plus, crit_plus, balance_plus, \
            speed_plus, resistance_plus, hp_plus = enchant_jewelry1(n1)
        attack_mall = attack_mall + attack_minus
        defence_mall = defence_mall + defence_minus
        crit_mall = crit_mall + crit_minus
        balance_mall = balance_mall + balance_minus
        speed_mall = speed_mall + speed_minus
        resistance_mall = resistance_mall + resistance_minus
        hp_mall = hp_mall + hp_minus
        hp_pall = hp_pall + hp_plus
        attack_pall = attack_pall + attack_plus
        defence_pall = defence_pall + defence_plus
        crit_pall = crit_pall + crit_plus
        balance_pall = balance_pall + balance_plus
        speed_pall = speed_pall + speed_plus
        resistance_pall = resistance_pall + resistance_plus

        # 戒指2首次
        nn = self.cm_choice15.GetSelection()
        if nn == 1:
            n = 2
        elif nn == 2 or nn == 3 or nn == 4:
            n = nn + 2
        elif nn == 0:
            n = nn
        else:
            n = 100
        attack_minus, defence_minus, crit_minus, balance_minus, \
            speed_minus, resistance_minus, hp_minus = enchant_jewelry0(n)
        nn1 = self.cm_choice41.GetSelection()
        if nn1 == 1:
            n1 = 2
        elif nn1 == 2 or nn1 == 3 or nn1 == 4:
            n1 = nn1 + 2
        elif nn1 == 0:
            n1 = nn1
        else:
            n1 = 100
        attack_plus, defence_plus, crit_plus, balance_plus, \
            speed_plus, resistance_plus, hp_plus = enchant_jewelry0(n1)
        attack_mall = attack_mall + attack_minus
        defence_mall = defence_mall + defence_minus
        crit_mall = crit_mall + crit_minus
        balance_mall = balance_mall + balance_minus
        speed_mall = speed_mall + speed_minus
        resistance_mall = resistance_mall + resistance_minus
        hp_mall = hp_mall + hp_minus
        hp_pall = hp_pall + hp_plus
        attack_pall = attack_pall + attack_plus
        defence_pall = defence_pall + defence_plus
        crit_pall = crit_pall + crit_plus
        balance_pall = balance_pall + balance_plus
        speed_pall = speed_pall + speed_plus
        resistance_pall = resistance_pall + resistance_plus

        # 戒指2后缀
        nn = self.cm_choice16.GetSelection()
        if nn != 3:
            n = nn + 1
        else:
            n = 100
        attack_minus, defence_minus, crit_minus, balance_minus, \
            speed_minus, resistance_minus, hp_minus = enchant_jewelry1(n)
        nn1 = self.cm_choice42.GetSelection()
        if nn1 != 3:
            n1 = nn1 + 1
        else:
            n1 = 100
        attack_plus, defence_plus, crit_plus, balance_plus, \
            speed_plus, resistance_plus, hp_plus = enchant_jewelry1(n1)
        attack_mall = attack_mall + attack_minus
        defence_mall = defence_mall + defence_minus
        crit_mall = crit_mall + crit_minus
        balance_mall = balance_mall + balance_minus
        speed_mall = speed_mall + speed_minus
        resistance_mall = resistance_mall + resistance_minus
        hp_mall = hp_mall + hp_minus
        hp_pall = hp_pall + hp_plus
        attack_pall = attack_pall + attack_plus
        defence_pall = defence_pall + defence_plus
        crit_pall = crit_pall + crit_plus
        balance_pall = balance_pall + balance_plus
        speed_pall = speed_pall + speed_plus
        resistance_pall = resistance_pall + resistance_plus

        # 耳环首次
        nn = self.cm_choice17.GetSelection()
        if nn != 3:
            n = nn + 4
        else:
            n = 100
        attack_minus, defence_minus, crit_minus, balance_minus, \
            speed_minus, resistance_minus, hp_minus = enchant_jewelry0(n)
        nn1 = self.cm_choice43.GetSelection()
        if nn1 != 3:
            n1 = nn1 + 4
        else:
            n1 = 100
        attack_plus, defence_plus, crit_plus, balance_plus, \
            speed_plus, resistance_plus, hp_plus = enchant_jewelry0(n1)
        attack_mall = attack_mall + attack_minus
        defence_mall = defence_mall + defence_minus
        crit_mall = crit_mall + crit_minus
        balance_mall = balance_mall + balance_minus
        speed_mall = speed_mall + speed_minus
        resistance_mall = resistance_mall + resistance_minus
        hp_mall = hp_mall + hp_minus
        hp_pall = hp_pall + hp_plus
        attack_pall = attack_pall + attack_plus
        defence_pall = defence_pall + defence_plus
        crit_pall = crit_pall + crit_plus
        balance_pall = balance_pall + balance_plus
        speed_pall = speed_pall + speed_plus
        resistance_pall = resistance_pall + resistance_plus

        # 耳环后缀
        nn = self.cm_choice18.GetSelection()
        if nn != 3:
            n = nn + 1
        else:
            n = 100
        attack_minus, defence_minus, crit_minus, balance_minus, \
            speed_minus, resistance_minus, hp_minus = enchant_jewelry1(n)
        nn1 = self.cm_choice44.GetSelection()
        if nn1 != 3:
            n1 = nn1 + 1
        else:
            n1 = 100
        attack_plus, defence_plus, crit_plus, balance_plus, \
            speed_plus, resistance_plus, hp_plus = enchant_jewelry1(n1)
        attack_mall = attack_mall + attack_minus
        defence_mall = defence_mall + defence_minus
        crit_mall = crit_mall + crit_minus
        balance_mall = balance_mall + balance_minus
        speed_mall = speed_mall + speed_minus
        resistance_mall = resistance_mall + resistance_minus
        hp_mall = hp_mall + hp_minus
        hp_pall = hp_pall + hp_plus
        attack_pall = attack_pall + attack_plus
        defence_pall = defence_pall + defence_plus
        crit_pall = crit_pall + crit_plus
        balance_pall = balance_pall + balance_plus
        speed_pall = speed_pall + speed_plus
        resistance_pall = resistance_pall + resistance_plus

        # 胸针首次
        nn = self.cm_choice19.GetSelection()
        if nn == 0:
            n = 10
        elif nn == 1:
            n = 9
        elif (nn >= 2) & (nn <= 4):
            n = nn + 2
        else:
            n = 100
        attack_minus, defence_minus, crit_minus, balance_minus, \
            speed_minus, resistance_minus, hp_minus = enchant_jewelry0(n)
        nn1 = self.cm_choice45.GetSelection()
        if nn1 == 0:
            n1 = 10
        elif nn1 == 1:
            n1 = 9
        elif (nn1 >= 2) & (nn1 <= 4):
            n1 = nn1 + 2
        else:
            n1 = 100
        attack_plus, defence_plus, crit_plus, balance_plus, \
            speed_plus, resistance_plus, hp_plus = enchant_jewelry0(n1)
        attack_mall = attack_mall + attack_minus
        defence_mall = defence_mall + defence_minus
        crit_mall = crit_mall + crit_minus
        balance_mall = balance_mall + balance_minus
        speed_mall = speed_mall + speed_minus
        resistance_mall = resistance_mall + resistance_minus
        hp_mall = hp_mall + hp_minus
        hp_pall = hp_pall + hp_plus
        attack_pall = attack_pall + attack_plus
        defence_pall = defence_pall + defence_plus
        crit_pall = crit_pall + crit_plus
        balance_pall = balance_pall + balance_plus
        speed_pall = speed_pall + speed_plus
        resistance_pall = resistance_pall + resistance_plus

        # 胸针后缀
        nn = self.cm_choice20.GetSelection()
        if nn != 4:
            n = nn
        else:
            n = 100
        attack_minus, defence_minus, crit_minus, balance_minus, \
            speed_minus, resistance_minus, hp_minus = enchant_jewelry1(n)
        nn1 = self.cm_choice46.GetSelection()
        if nn1 != 4:
            n1 = nn1
        else:
            n1 = 100
        attack_plus, defence_plus, crit_plus, balance_plus, \
            speed_plus, resistance_plus, hp_plus = enchant_jewelry1(n1)
        attack_mall = attack_mall + attack_minus
        defence_mall = defence_mall + defence_minus
        crit_mall = crit_mall + crit_minus
        balance_mall = balance_mall + balance_minus
        speed_mall = speed_mall + speed_minus
        resistance_mall = resistance_mall + resistance_minus
        hp_mall = hp_mall + hp_minus
        hp_pall = hp_pall + hp_plus
        attack_pall = attack_pall + attack_plus
        defence_pall = defence_pall + defence_plus
        crit_pall = crit_pall + crit_plus
        balance_pall = balance_pall + balance_plus
        speed_pall = speed_pall + speed_plus
        resistance_pall = resistance_pall + resistance_plus

        # 副手首次
        nn = self.cm_choice23.GetSelection()
        if nn == 0 or nn == 1:
            n = nn + 7
        elif nn == 3:
            n = 11
        else:
            n = 100
        attack_minus, defence_minus, crit_minus, balance_minus, \
            speed_minus, resistance_minus, hp_minus = enchant_jewelry0(n)
        nn1 = self.cm_choice47.GetSelection()
        if nn1 == 0 or nn1 == 1:
            n1 = nn1 + 7
        elif nn1 == 3:
            n1 = 11
        else:
            n1 = 100
        attack_plus, defence_plus, crit_plus, balance_plus, \
            speed_plus, resistance_plus, hp_plus = enchant_jewelry0(n1)
        attack_mall = attack_mall + attack_minus
        defence_mall = defence_mall + defence_minus
        crit_mall = crit_mall + crit_minus
        balance_mall = balance_mall + balance_minus
        speed_mall = speed_mall + speed_minus
        resistance_mall = resistance_mall + resistance_minus
        hp_mall = hp_mall + hp_minus
        hp_pall = hp_pall + hp_plus
        attack_pall = attack_pall + attack_plus
        defence_pall = defence_pall + defence_plus
        crit_pall = crit_pall + crit_plus
        balance_pall = balance_pall + balance_plus
        speed_pall = speed_pall + speed_plus
        resistance_pall = resistance_pall + resistance_plus

        # 副手后缀
        nn = self.cm_choice24.GetSelection()
        if nn == 0:
            n = 4
        elif nn == 2:
            n = 5
        else:
            n = 100
        attack_minus, defence_minus, crit_minus, balance_minus, \
            speed_minus, resistance_minus, hp_minus = enchant_jewelry1(n)
        nn1 = self.cm_choice48.GetSelection()
        if nn1 == 0:
            n1 = 4
        elif nn1 == 2:
            n1 = 5
        else:
            n1 = 100
        attack_plus, defence_plus, crit_plus, balance_plus, \
            speed_plus, resistance_plus, hp_plus = enchant_jewelry1(n1)
        attack_mall = attack_mall + attack_minus
        defence_mall = defence_mall + defence_minus
        crit_mall = crit_mall + crit_minus
        balance_mall = balance_mall + balance_minus
        speed_mall = speed_mall + speed_minus
        resistance_mall = resistance_mall + resistance_minus
        hp_mall = hp_mall + hp_minus
        hp_pall = hp_pall + hp_plus
        attack_pall = attack_pall + attack_plus
        defence_pall = defence_pall + defence_plus
        crit_pall = crit_pall + crit_plus
        balance_pall = balance_pall + balance_plus
        speed_pall = speed_pall + speed_plus
        resistance_pall = resistance_pall + resistance_plus

        # 腰带首次
        nn = self.cm_choice25.GetSelection()
        if nn == 0:
            n = 1
        elif (nn >= 1) & (nn <= 3):
            n = nn + 2
        else:
            n = 100
        attack_minus, defence_minus, crit_minus, balance_minus, \
            speed_minus, resistance_minus, hp_minus = enchant_jewelry0(n)
        nn1 = self.cm_choice49.GetSelection()
        if nn1 == 0:
            n1 = 1
        elif (nn1 >= 1) & (nn1 <= 3):
            n1 = nn1 + 2
        else:
            n1 = 100
        attack_plus, defence_plus, crit_plus, balance_plus, \
            speed_plus, resistance_plus, hp_plus = enchant_jewelry0(n1)
        attack_mall = attack_mall + attack_minus
        defence_mall = defence_mall + defence_minus
        crit_mall = crit_mall + crit_minus
        balance_mall = balance_mall + balance_minus
        speed_mall = speed_mall + speed_minus
        resistance_mall = resistance_mall + resistance_minus
        hp_mall = hp_mall + hp_minus
        hp_pall = hp_pall + hp_plus
        attack_pall = attack_pall + attack_plus
        defence_pall = defence_pall + defence_plus
        crit_pall = crit_pall + crit_plus
        balance_pall = balance_pall + balance_plus
        speed_pall = speed_pall + speed_plus
        resistance_pall = resistance_pall + resistance_plus

        # 腰带后缀
        nn = self.cm_choice26.GetSelection()
        if nn != 3:
            n = nn+1
        else:
            n = 100
        attack_minus, defence_minus, crit_minus, balance_minus, \
            speed_minus, resistance_minus, hp_minus = enchant_jewelry1(n)
        nn1 = self.cm_choice50.GetSelection()
        if nn1 != 3:
            n1 = nn1+1
        else:
            n1 = 100
        attack_plus, defence_plus, crit_plus, balance_plus, \
            speed_plus, resistance_plus, hp_plus = enchant_jewelry1(n1)
        attack_mall = attack_mall + attack_minus
        defence_mall = defence_mall + defence_minus
        crit_mall = crit_mall + crit_minus
        balance_mall = balance_mall + balance_minus
        speed_mall = speed_mall + speed_minus
        resistance_mall = resistance_mall + resistance_minus
        hp_mall = hp_mall + hp_minus
        hp_pall = hp_pall + hp_plus
        attack_pall = attack_pall + attack_plus
        defence_pall = defence_pall + defence_plus
        crit_pall = crit_pall + crit_plus
        balance_pall = balance_pall + balance_plus
        speed_pall = speed_pall + speed_plus
        resistance_pall = resistance_pall + resistance_plus

        # 工艺品首次
        nn = self.cm_choice27.GetSelection()
        if nn != 3:
            n = nn + 4
        else:
            n = 100
        attack_minus, defence_minus, crit_minus, balance_minus, \
            speed_minus, resistance_minus, hp_minus = enchant_jewelry0(n)
        nn1 = self.cm_choice51.GetSelection()
        if nn1 != 3:
            n1 = nn1 + 4
        else:
            n1 = 100
        attack_plus, defence_plus, crit_plus, balance_plus, \
            speed_plus, resistance_plus, hp_plus = enchant_jewelry0(n1)
        attack_mall = attack_mall + attack_minus
        defence_mall = defence_mall + defence_minus
        crit_mall = crit_mall + crit_minus
        balance_mall = balance_mall + balance_minus
        speed_mall = speed_mall + speed_minus
        resistance_mall = resistance_mall + resistance_minus
        hp_mall = hp_mall + hp_minus
        hp_pall = hp_pall + hp_plus
        attack_pall = attack_pall + attack_plus
        defence_pall = defence_pall + defence_plus
        crit_pall = crit_pall + crit_plus
        balance_pall = balance_pall + balance_plus
        speed_pall = speed_pall + speed_plus
        resistance_pall = resistance_pall + resistance_plus

        # 工艺品后缀
        nn = self.cm_choice28.GetSelection()
        if nn != 3:
            n = nn+1
        else:
            n = 100
        attack_minus, defence_minus, crit_minus, balance_minus, \
            speed_minus, resistance_minus, hp_minus = enchant_jewelry1(n)
        nn1 = self.cm_choice52.GetSelection()
        if nn1 != 3:
            n1 = nn1+1
        else:
            n1 = 100
        attack_plus, defence_plus, crit_plus, balance_plus, \
            speed_plus, resistance_plus, hp_plus = enchant_jewelry1(n1)
        attack_mall = attack_mall + attack_minus
        defence_mall = defence_mall + defence_minus
        crit_mall = crit_mall + crit_minus
        balance_mall = balance_mall + balance_minus
        speed_mall = speed_mall + speed_minus
        resistance_mall = resistance_mall + resistance_minus
        hp_mall = hp_mall + hp_minus
        hp_pall = hp_pall + hp_plus
        attack_pall = attack_pall + attack_plus
        defence_pall = defence_pall + defence_plus
        crit_pall = crit_pall + crit_plus
        balance_pall = balance_pall + balance_plus
        speed_pall = speed_pall + speed_plus
        resistance_pall = resistance_pall + resistance_plus

        # 商城胸针首次
        nn = self.cm_choice53.GetSelection()
        if nn != 3:
            n = nn + 4
        else:
            n = 100
        attack_minus, defence_minus, crit_minus, balance_minus, \
            speed_minus, resistance_minus, hp_minus = enchant_jewelry0(n)
        nn1 = self.cm_choice55.GetSelection()
        if nn1 != 3:
            n1 = nn1 + 4
        else:
            n1 = 100
        attack_plus, defence_plus, crit_plus, balance_plus, \
            speed_plus, resistance_plus, hp_plus = enchant_jewelry0(n1)
        attack_mall = attack_mall + attack_minus
        defence_mall = defence_mall + defence_minus
        crit_mall = crit_mall + crit_minus
        balance_mall = balance_mall + balance_minus
        speed_mall = speed_mall + speed_minus
        resistance_mall = resistance_mall + resistance_minus
        hp_mall = hp_mall + hp_minus
        hp_pall = hp_pall + hp_plus
        attack_pall = attack_pall + attack_plus
        defence_pall = defence_pall + defence_plus
        crit_pall = crit_pall + crit_plus
        balance_pall = balance_pall + balance_plus
        speed_pall = speed_pall + speed_plus
        resistance_pall = resistance_pall + resistance_plus

        # 商城工艺品后缀
        nn = self.cm_choice54.GetSelection()
        if nn != 3:
            n = nn+1
        else:
            n = 100
        attack_minus, defence_minus, crit_minus, balance_minus, \
            speed_minus, resistance_minus, hp_minus = enchant_jewelry1(n)
        nn1 = self.cm_choice56.GetSelection()
        if nn1 != 3:
            n1 = nn1+1
        else:
            n1 = 100
        attack_plus, defence_plus, crit_plus, balance_plus, \
            speed_plus, resistance_plus, hp_plus = enchant_jewelry1(n1)
        attack_mall = attack_mall + attack_minus
        defence_mall = defence_mall + defence_minus
        crit_mall = crit_mall + crit_minus
        balance_mall = balance_mall + balance_minus
        speed_mall = speed_mall + speed_minus
        resistance_mall = resistance_mall + resistance_minus
        hp_mall = hp_mall + hp_minus
        hp_pall = hp_pall + hp_plus
        attack_pall = attack_pall + attack_plus
        defence_pall = defence_pall + defence_plus
        crit_pall = crit_pall + crit_plus
        balance_pall = balance_pall + balance_plus
        speed_pall = speed_pall + speed_plus
        resistance_pall = resistance_pall + resistance_plus

        # 计算最终结果
        attack_after = attack_now - attack_mall + attack_pall + attack_other
        defence_after = defence_now - defence_mall + defence_pall + defence_other
        crit_after = crit_now - crit_mall + crit_pall + crit_other
        balance_after = balance_now - balance_mall + balance_pall + balance_other
        speed_after = speed_now - speed_mall + speed_pall + speed_other
        resistance_after = resistance_now - resistance_mall + resistance_pall
        hp_after = hp_now - hp_mall + hp_pall
        self.cm_textCtrl35.SetValue(str(attack_after))
        self.cm_textCtrl37.SetValue(str(defence_after))
        self.cm_textCtrl39.SetValue(str(crit_after))
        self.cm_textCtrl41.SetValue(str(balance_after))
        self.cm_textCtrl43.SetValue(str(speed_after))
        self.cm_textCtrl45.SetValue(str(resistance_after))
        self.cm_textCtrl47.SetValue(str(hp_after))

        # 所有的增加 减少量归0
        attack_mall = 0
        defence_mall = 0
        crit_mall = 0
        balance_mall = 0
        speed_mall = 0
        resistance_mall = 0
        hp_mall = 0
        hp_pall = 0
        attack_pall = 0
        defence_pall = 0
        crit_pall = 0
        balance_pall = 0
        speed_pall = 0
        resistance_pall = 0
        event.Skip()

    # def choice271(self, event):
    #     global attack_mall
    #     global defence_mall
    #     global crit_mall
    #     global balance_mall
    #     global speed_mall
    #     global resistance_mall
    #     global attack_pall
    #     global defence_pall
    #     global crit_pall
    #     global balance_pall
    #     global speed_pall
    #     global resistance_pall
    #     n = self.cm_choice1.GetSelection()
    #     attack_minus, defence_minus, crit_minus, balance_minus, speed_minus, resistance_minus = enchant_head0(n)
    #     n1 = self.cm_choice271.GetSelection()
    #     attack_plus, defence_plus, crit_plus, balance_plus, speed_plus, resistance_plus = enchant_head0(n1)
    #     attack_mall = attack_mall + attack_minus
    #     defence_mall = defence_mall + defence_minus
    #     crit_mall = crit_mall + crit_minus
    #     balance_mall = balance_mall + balance_minus
    #     speed_mall = speed_mall + speed_minus
    #     resistance_mall = resistance_mall + resistance_minus
    #     attack_pall = attack_pall + attack_plus
    #     defence_pall = defence_pall + defence_plus
    #     crit_pall = crit_pall + crit_plus
    #     balance_pall = balance_pall + balance_plus
    #     speed_pall = speed_pall + speed_plus
    #     resistance_pall = resistance_pall + resistance_plus
    #     event.Skip()

    # def choice281(self, event):
    #     global attack_mall
    #     global defence_mall
    #     global crit_mall
    #     global balance_mall
    #     global speed_mall
    #     global resistance_mall
    #     global attack_pall
    #     global defence_pall
    #     global crit_pall
    #     global balance_pall
    #     global speed_pall
    #     global resistance_pall
    #     n = self.cm_choice2.GetSelection()
    #     attack_minus, defence_minus, crit_minus, balance_minus, speed_minus, resistance_minus = enchant_head1(n)
    #     n1 = self.cm_choice281.GetSelection()
    #     attack_plus, defence_plus, crit_plus, balance_plus, speed_plus, resistance_plus = enchant_head1(n1)
    #     attack_mall = attack_mall + attack_minus
    #     defence_mall = defence_mall + defence_minus
    #     crit_mall = crit_mall + crit_minus
    #     balance_mall = balance_mall + balance_minus
    #     speed_mall = speed_mall + speed_minus
    #     resistance_mall = resistance_mall + resistance_minus
    #     attack_pall = attack_pall + attack_plus
    #     defence_pall = defence_pall + defence_plus
    #     crit_pall = crit_pall + crit_plus
    #     balance_pall = balance_pall + balance_plus
    #     speed_pall = speed_pall + speed_plus
    #     resistance_pall = resistance_pall + resistance_plus
    #     event.Skip()

    # def choice29(self, event):
    #     global attack_mall
    #     global defence_mall
    #     global crit_mall
    #     global balance_mall
    #     global speed_mall
    #     global resistance_mall
    #     global hp_mall
    #     global attack_pall
    #     global defence_pall
    #     global crit_pall
    #     global balance_pall
    #     global speed_pall
    #     global resistance_pall
    #     global hp_pall
    #     nn = self.cm_choice3.GetSelection()
    #     if nn == 1:
    #         n = 2
    #     elif nn == 2 or nn == 3 or nn == 4:
    #         n = nn + 3
    #     else:
    #         n = nn
    #     attack_minus, defence_minus, crit_minus, balance_minus,\
    #         speed_minus, resistance_minus, hp_minus = enchant_armor0(n)
    #     nn1 = self.cm_choice29.GetSelection()
    #     if nn1 == 1:
    #         n1 = 2
    #     elif nn1 == 2 or nn1 == 3 or nn1 == 4:
    #         n1 = nn1 + 3
    #     else:
    #         n1 = nn1
    #     attack_plus, defence_plus, crit_plus, balance_plus,\
    #         speed_plus, resistance_plus, hp_plus = enchant_armor0(n1)
    #     attack_mall = attack_mall + attack_minus
    #     defence_mall = defence_mall + defence_minus
    #     crit_mall = crit_mall + crit_minus
    #     balance_mall = balance_mall + balance_minus
    #     speed_mall = speed_mall + speed_minus
    #     resistance_mall = resistance_mall + resistance_minus
    #     hp_mall = hp_mall + hp_minus
    #     attack_pall = attack_pall + attack_plus
    #     defence_pall = defence_pall + defence_plus
    #     crit_pall = crit_pall + crit_plus
    #     balance_pall = balance_pall + balance_plus
    #     speed_pall = speed_pall + speed_plus
    #     resistance_pall = resistance_pall + resistance_plus
    #     hp_pall = hp_pall + hp_plus
    #     event.Skip()

    # def choice30(self, event):
    #     global attack_mall
    #     global defence_mall
    #     global crit_mall
    #     global balance_mall
    #     global speed_mall
    #     global resistance_mall
    #     global attack_pall
    #     global defence_pall
    #     global crit_pall
    #     global balance_pall
    #     global speed_pall
    #     global resistance_pall
    #     nn = self.cm_choice4.GetSelection()
    #     if nn <= 4 & nn > 0:
    #         n = nn + 1
    #     elif nn == 0:
    #         n = 100
    #     else:
    #         n = nn + 3
    #     attack_minus, defence_minus, crit_minus, balance_minus, speed_minus, resistance_minus = enchant_armor1(n)
    #     nn1 = self.cm_choice30.GetSelection()
    #     if nn1 <= 4 & nn1 > 0:
    #         n1 = nn1 + 1
    #     elif nn1 == 0:
    #         n1 = 100
    #     else:
    #         n1 = nn1 + 3
    #     attack_plus, defence_plus, crit_plus, balance_plus, speed_plus, resistance_plus = enchant_armor1(n1)
    #     attack_mall = attack_mall + attack_minus
    #     defence_mall = defence_mall + defence_minus
    #     crit_mall = crit_mall + crit_minus
    #     balance_mall = balance_mall + balance_minus
    #     speed_mall = speed_mall + speed_minus
    #     resistance_mall = resistance_mall + resistance_minus
    #     attack_pall = attack_pall + attack_plus
    #     defence_pall = defence_pall + defence_plus
    #     crit_pall = crit_pall + crit_plus
    #     balance_pall = balance_pall + balance_plus
    #     speed_pall = speed_pall + speed_plus
    #     resistance_pall = resistance_pall + resistance_plus
    #     event.Skip()
    #
    # def choice31(self, event):
    #     global attack_mall
    #     global defence_mall
    #     global crit_mall
    #     global balance_mall
    #     global speed_mall
    #     global resistance_mall
    #     global hp_mall
    #     global attack_pall
    #     global defence_pall
    #     global crit_pall
    #     global balance_pall
    #     global speed_pall
    #     global resistance_pall
    #     global hp_pall
    #     nn = self.cm_choice5.GetSelection()
    #     n = nn + 4
    #     attack_minus, defence_minus, crit_minus, balance_minus,\
    #         speed_minus, resistance_minus, hp_minus = enchant_armor0(n)
    #     nn1 = self.cm_choice31.GetSelection()
    #     n1 = nn1 + 4
    #     attack_plus, defence_plus, crit_plus, balance_plus,\
    #         speed_plus, resistance_plus, hp_plus = enchant_armor0(n1)
    #     attack_mall = attack_mall + attack_minus
    #     defence_mall = defence_mall + defence_minus
    #     crit_mall = crit_mall + crit_minus
    #     balance_mall = balance_mall + balance_minus
    #     speed_mall = speed_mall + speed_minus
    #     resistance_mall = resistance_mall + resistance_minus
    #     hp_mall = hp_mall + hp_minus
    #     hp_pall = hp_pall + hp_plus
    #     attack_pall = attack_pall + attack_plus
    #     defence_pall = defence_pall + defence_plus
    #     crit_pall = crit_pall + crit_plus
    #     balance_pall = balance_pall + balance_plus
    #     speed_pall = speed_pall + speed_plus
    #     resistance_pall = resistance_pall + resistance_plus
    #     event.Skip()
    #
    # def choice32(self, event):
    #     global attack_mall
    #     global defence_mall
    #     global crit_mall
    #     global balance_mall
    #     global speed_mall
    #     global resistance_mall
    #     global attack_pall
    #     global defence_pall
    #     global crit_pall
    #     global balance_pall
    #     global speed_pall
    #     global resistance_pall
    #     nn = self.cm_choice6.GetSelection()
    #     if nn == 0 & nn == 1:
    #         n = nn + 6
    #     elif nn == 2:
    #         n = 4
    #     elif nn == 3 or nn == 4:
    #         n = nn - 1
    #     elif nn == 5:
    #         n = nn
    #     else:
    #         n = 100
    #     attack_minus, defence_minus, crit_minus, balance_minus, speed_minus, resistance_minus = enchant_armor1(n)
    #     nn1 = self.cm_choice32.GetSelection()
    #     if nn1 == 0 & nn1 == 1:
    #         n1 = nn1 + 6
    #     elif nn1 == 2:
    #         n1 = 4
    #     elif nn1 == 3 or nn1 == 4:
    #         n1 = nn1 - 1
    #     elif nn1 == 5:
    #         n1 = nn1
    #     else:
    #         n1 = 100
    #     attack_plus, defence_plus, crit_plus, balance_plus, speed_plus, resistance_plus = enchant_armor1(n1)
    #     attack_mall = attack_mall + attack_minus
    #     defence_mall = defence_mall + defence_minus
    #     crit_mall = crit_mall + crit_minus
    #     balance_mall = balance_mall + balance_minus
    #     speed_mall = speed_mall + speed_minus
    #     resistance_mall = resistance_mall + resistance_minus
    #     attack_pall = attack_pall + attack_plus
    #     defence_pall = defence_pall + defence_plus
    #     crit_pall = crit_pall + crit_plus
    #     balance_pall = balance_pall + balance_plus
    #     speed_pall = speed_pall + speed_plus
    #     resistance_pall = resistance_pall + resistance_plus
    #     event.Skip()
    #
    # def choice33(self, event):
    #     global attack_mall
    #     global defence_mall
    #     global crit_mall
    #     global balance_mall
    #     global speed_mall
    #     global resistance_mall
    #     global hp_mall
    #     global hp_pall
    #     global attack_pall
    #     global defence_pall
    #     global crit_pall
    #     global balance_pall
    #     global speed_pall
    #     global resistance_pall
    #     nn = self.cm_choice7.GetSelection()
    #     if nn == 1:
    #         n = 2
    #     elif nn == 2 or nn == 3 or nn == 4:
    #         n = nn + 3
    #     else:
    #         n = nn
    #     attack_minus, defence_minus, crit_minus, balance_minus, \
    #         speed_minus, resistance_minus, hp_minus = enchant_armor0(n)
    #     nn1 = self.cm_choice33.GetSelection()
    #     if nn1 == 1:
    #         n1 = 2
    #     elif nn1 == 2 or nn1 == 3 or nn1 == 4:
    #         n1 = nn1 + 3
    #     else:
    #         n1 = nn1
    #     attack_plus, defence_plus, crit_plus, balance_plus, speed_plus, resistance_plus, hp_plus = enchant_armor0(n1)
    #     attack_mall = attack_mall + attack_minus
    #     defence_mall = defence_mall + defence_minus
    #     crit_mall = crit_mall + crit_minus
    #     balance_mall = balance_mall + balance_minus
    #     speed_mall = speed_mall + speed_minus
    #     resistance_mall = resistance_mall + resistance_minus
    #     hp_mall = hp_mall + hp_minus
    #     hp_pall = hp_pall + hp_plus
    #     attack_pall = attack_pall + attack_plus
    #     defence_pall = defence_pall + defence_plus
    #     crit_pall = crit_pall + crit_plus
    #     balance_pall = balance_pall + balance_plus
    #     speed_pall = speed_pall + speed_plus
    #     resistance_pall = resistance_pall + resistance_plus
    #     event.Skip()
    #
    # def choice34(self, event):
    #     global attack_mall
    #     global defence_mall
    #     global crit_mall
    #     global balance_mall
    #     global speed_mall
    #     global resistance_mall
    #     global attack_pall
    #     global defence_pall
    #     global crit_pall
    #     global balance_pall
    #     global speed_pall
    #     global resistance_pall
    #     nn = self.cm_choice8.GetSelection()
    #     if nn <= 4 & nn > 0:
    #         n = nn + 1
    #     elif nn == 0:
    #         n = 100
    #     else:
    #         n = nn + 3
    #     attack_minus, defence_minus, crit_minus, balance_minus, speed_minus, resistance_minus = enchant_armor1(n)
    #     nn1 = self.cm_choice34.GetSelection()
    #     if nn1 <= 4 & nn1 > 0:
    #         n1 = nn1 + 1
    #     elif nn1 == 0:
    #         n1 = 100
    #     else:
    #         n1 = nn1 + 3
    #     attack_plus, defence_plus, crit_plus, balance_plus, speed_plus, resistance_plus = enchant_armor1(n1)
    #     attack_mall = attack_mall + attack_minus
    #     defence_mall = defence_mall + defence_minus
    #     crit_mall = crit_mall + crit_minus
    #     balance_mall = balance_mall + balance_minus
    #     speed_mall = speed_mall + speed_minus
    #     resistance_mall = resistance_mall + resistance_minus
    #     attack_pall = attack_pall + attack_plus
    #     defence_pall = defence_pall + defence_plus
    #     crit_pall = crit_pall + crit_plus
    #     balance_pall = balance_pall + balance_plus
    #     speed_pall = speed_pall + speed_plus
    #     resistance_pall = resistance_pall + resistance_plus
    #     event.Skip()
    #
    # def choice35(self, event):
    #     global attack_mall
    #     global defence_mall
    #     global crit_mall
    #     global balance_mall
    #     global speed_mall
    #     global resistance_mall
    #     global hp_mall
    #     global hp_pall
    #     global attack_pall
    #     global defence_pall
    #     global crit_pall
    #     global balance_pall
    #     global speed_pall
    #     global resistance_pall
    #     nn = self.cm_choice9.GetSelection()
    #     if nn == 1:
    #         n = 3
    #     elif nn == 2 or nn == 3 or nn == 4:
    #         n = nn + 3
    #     else:
    #         n = nn + 1
    #     attack_minus, defence_minus, crit_minus, balance_minus,\
    #         speed_minus, resistance_minus, hp_minus = enchant_armor0(n)
    #     nn1 = self.cm_choice35.GetSelection()
    #     if nn1 == 1:
    #         n1 = 3
    #     elif nn1 == 2 or nn1 == 3 or nn1 == 4:
    #         n1 = nn1 + 3
    #     else:
    #         n1 = nn1 + 1
    #     attack_plus, defence_plus, crit_plus, balance_plus,\
    #         speed_plus, resistance_plus, hp_plus = enchant_armor0(n1)
    #     attack_mall = attack_mall + attack_minus
    #     defence_mall = defence_mall + defence_minus
    #     crit_mall = crit_mall + crit_minus
    #     balance_mall = balance_mall + balance_minus
    #     speed_mall = speed_mall + speed_minus
    #     resistance_mall = resistance_mall + resistance_minus
    #     hp_mall = hp_mall + hp_minus
    #     hp_pall = hp_pall + hp_plus
    #     attack_pall = attack_pall + attack_plus
    #     defence_pall = defence_pall + defence_plus
    #     crit_pall = crit_pall + crit_plus
    #     balance_pall = balance_pall + balance_plus
    #     speed_pall = speed_pall + speed_plus
    #     resistance_pall = resistance_pall + resistance_plus
    #     event.Skip()
    #
    # def choice36(self, event):
    #     global attack_mall
    #     global defence_mall
    #     global crit_mall
    #     global balance_mall
    #     global speed_mall
    #     global resistance_mall
    #     global attack_pall
    #     global defence_pall
    #     global crit_pall
    #     global balance_pall
    #     global speed_pall
    #     global resistance_pall
    #     nn = self.cm_choice10.GetSelection()
    #     if nn <= 4 & nn > 0:
    #         n = nn + 1
    #     elif nn == 0:
    #         n = 0
    #     else:
    #         n = nn + 3
    #     attack_minus, defence_minus, crit_minus, balance_minus, speed_minus, resistance_minus = enchant_armor1(n)
    #     nn1 = self.cm_choice36.GetSelection()
    #     if nn1 <= 4 & nn1 > 0:
    #         n1 = nn1 + 1
    #     elif nn1 == 0:
    #         n1 = 0
    #     else:
    #         n1 = nn1 + 3
    #     attack_plus, defence_plus, crit_plus, balance_plus, speed_plus, resistance_plus = enchant_armor1(n1)
    #     attack_mall = attack_mall + attack_minus
    #     defence_mall = defence_mall + defence_minus
    #     crit_mall = crit_mall + crit_minus
    #     balance_mall = balance_mall + balance_minus
    #     speed_mall = speed_mall + speed_minus
    #     resistance_mall = resistance_mall + resistance_minus
    #     attack_pall = attack_pall + attack_plus
    #     defence_pall = defence_pall + defence_plus
    #     crit_pall = crit_pall + crit_plus
    #     balance_pall = balance_pall + balance_plus
    #     speed_pall = speed_pall + speed_plus
    #     resistance_pall = resistance_pall + resistance_plus
    #     event.Skip()
    #
    # def choice37(self, event):
    #     global attack_mall
    #     global defence_mall
    #     global crit_mall
    #     global balance_mall
    #     global speed_mall
    #     global resistance_mall
    #     global hp_mall
    #     global hp_pall
    #     global attack_pall
    #     global defence_pall
    #     global crit_pall
    #     global balance_pall
    #     global speed_pall
    #     global resistance_pall
    #     nn = self.cm_choice11.GetSelection()
    #     if nn == 1:
    #         n = 3
    #     elif nn == 2 or nn == 3 or nn == 4:
    #         n = nn + 3
    #     else:
    #         n = nn + 1
    #     attack_minus, defence_minus, crit_minus, balance_minus,\
    #         speed_minus, resistance_minus, hp_minus = enchant_armor0(n)
    #     nn1 = self.cm_choice37.GetSelection()
    #     if nn1 == 1:
    #         n1 = 3
    #     elif nn1 == 2 or nn1 == 3 or nn1 == 4:
    #         n1 = nn1 + 3
    #     else:
    #         n1 = nn1 + 1
    #     attack_plus, defence_plus, crit_plus, balance_plus,\
    #         speed_plus, resistance_plus, hp_plus = enchant_armor0(n1)
    #     attack_mall = attack_mall + attack_minus
    #     defence_mall = defence_mall + defence_minus
    #     crit_mall = crit_mall + crit_minus
    #     balance_mall = balance_mall + balance_minus
    #     speed_mall = speed_mall + speed_minus
    #     resistance_mall = resistance_mall + resistance_minus
    #     hp_mall = hp_mall + hp_minus
    #     hp_pall = hp_pall + hp_plus
    #     attack_pall = attack_pall + attack_plus
    #     defence_pall = defence_pall + defence_plus
    #     crit_pall = crit_pall + crit_plus
    #     balance_pall = balance_pall + balance_plus
    #     speed_pall = speed_pall + speed_plus
    #     resistance_pall = resistance_pall + resistance_plus
    #     event.Skip()
    #
    # def choice38(self, event):
    #     global attack_mall
    #     global defence_mall
    #     global crit_mall
    #     global balance_mall
    #     global speed_mall
    #     global resistance_mall
    #     global attack_pall
    #     global defence_pall
    #     global crit_pall
    #     global balance_pall
    #     global speed_pall
    #     global resistance_pall
    #     nn = self.cm_choice12.GetSelection()
    #     if nn <= 4 & nn > 0:
    #         n = nn + 1
    #     elif nn == 0:
    #         n = 0
    #     else:
    #         n = nn + 3
    #     attack_minus, defence_minus, crit_minus, balance_minus, speed_minus, resistance_minus = enchant_armor1(n)
    #     nn1 = self.cm_choice38.GetSelection()
    #     if nn1 <= 4 & nn1 > 0:
    #         n1 = nn1 + 1
    #     elif nn1 == 0:
    #         n1 = 0
    #     else:
    #         n1 = nn1 + 3
    #     attack_plus, defence_plus, crit_plus, balance_plus, speed_plus, resistance_plus = enchant_armor1(n1)
    #     attack_mall = attack_mall + attack_minus
    #     defence_mall = defence_mall + defence_minus
    #     crit_mall = crit_mall + crit_minus
    #     balance_mall = balance_mall + balance_minus
    #     speed_mall = speed_mall + speed_minus
    #     resistance_mall = resistance_mall + resistance_minus
    #     attack_pall = attack_pall + attack_plus
    #     defence_pall = defence_pall + defence_plus
    #     crit_pall = crit_pall + crit_plus
    #     balance_pall = balance_pall + balance_plus
    #     speed_pall = speed_pall + speed_plus
    #     resistance_pall = resistance_pall + resistance_plus
    #     event.Skip()
    #
    # def choice39(self, event):
    #     global attack_mall
    #     global defence_mall
    #     global crit_mall
    #     global balance_mall
    #     global speed_mall
    #     global resistance_mall
    #     global hp_mall
    #     global hp_pall
    #     global attack_pall
    #     global defence_pall
    #     global crit_pall
    #     global balance_pall
    #     global speed_pall
    #     global resistance_pall
    #     nn = self.cm_choice13.GetSelection()
    #     if nn == 1:
    #         n = 2
    #     elif nn == 2 or nn == 3 or nn == 4:
    #         n = nn + 2
    #     elif nn == 0:
    #         n = nn
    #     else:
    #         n = 100
    #     attack_minus, defence_minus, crit_minus, balance_minus,\
    #         speed_minus, resistance_minus, hp_minus = enchant_jewelry0(n)
    #     nn1 = self.cm_choice39.GetSelection()
    #     if nn1 == 1:
    #         n1 = 2
    #     elif nn1 == 2 or nn1 == 3 or nn1 == 4:
    #         n1 = nn1 + 2
    #     elif nn == 0:
    #         n1 = nn
    #     else:
    #         n1 = 100
    #     attack_plus, defence_plus, crit_plus, balance_plus,\
    #         speed_plus, resistance_plus, hp_plus = enchant_jewelry0(n1)
    #     attack_mall = attack_mall + attack_minus
    #     defence_mall = defence_mall + defence_minus
    #     crit_mall = crit_mall + crit_minus
    #     balance_mall = balance_mall + balance_minus
    #     speed_mall = speed_mall + speed_minus
    #     resistance_mall = resistance_mall + resistance_minus
    #     hp_mall = hp_mall + hp_minus
    #     hp_pall = hp_pall + hp_plus
    #     attack_pall = attack_pall + attack_plus
    #     defence_pall = defence_pall + defence_plus
    #     crit_pall = crit_pall + crit_plus
    #     balance_pall = balance_pall + balance_plus
    #     speed_pall = speed_pall + speed_plus
    #     resistance_pall = resistance_pall + resistance_plus
    #     event.Skip()
    #
    # def choice40(self, event):
    #     global attack_mall
    #     global defence_mall
    #     global crit_mall
    #     global balance_mall
    #     global speed_mall
    #     global resistance_mall
    #     global hp_mall
    #     global hp_pall
    #     global attack_pall
    #     global defence_pall
    #     global crit_pall
    #     global balance_pall
    #     global speed_pall
    #     global resistance_pall
    #     nn = self.cm_choice14.GetSelection()
    #     if nn != 3:
    #         n = nn + 1
    #     else:
    #         n = 100
    #     attack_minus, defence_minus, crit_minus, balance_minus, \
    #         speed_minus, resistance_minus, hp_minus = enchant_jewelry1(n)
    #     nn1 = self.cm_choice40.GetSelection()
    #     if nn1 != 3:
    #         n1 = nn1 + 1
    #     else:
    #         n1 = 100
    #     attack_plus, defence_plus, crit_plus, balance_plus,\
    #         speed_plus, resistance_plus, hp_plus = enchant_jewelry1(n1)
    #     attack_mall = attack_mall + attack_minus
    #     defence_mall = defence_mall + defence_minus
    #     crit_mall = crit_mall + crit_minus
    #     balance_mall = balance_mall + balance_minus
    #     speed_mall = speed_mall + speed_minus
    #     resistance_mall = resistance_mall + resistance_minus
    #     hp_mall = hp_mall + hp_minus
    #     hp_pall = hp_pall + hp_plus
    #     attack_pall = attack_pall + attack_plus
    #     defence_pall = defence_pall + defence_plus
    #     crit_pall = crit_pall + crit_plus
    #     balance_pall = balance_pall + balance_plus
    #     speed_pall = speed_pall + speed_plus
    #     resistance_pall = resistance_pall + resistance_plus
    #     event.Skip()
    #
    # def choice41(self, event):
    #     global attack_mall
    #     global defence_mall
    #     global crit_mall
    #     global balance_mall
    #     global speed_mall
    #     global resistance_mall
    #     global hp_mall
    #     global hp_pall
    #     global attack_pall
    #     global defence_pall
    #     global crit_pall
    #     global balance_pall
    #     global speed_pall
    #     global resistance_pall
    #     nn = self.cm_choice15.GetSelection()
    #     if nn == 1:
    #         n = 2
    #     elif nn == 2 or nn == 3 or nn == 4:
    #         n = nn + 2
    #     elif nn == 0:
    #         n = nn
    #     else:
    #         n = 100
    #     attack_minus, defence_minus, crit_minus, balance_minus,\
    #         speed_minus, resistance_minus,  hp_minus = enchant_jewelry0(n)
    #     nn1 = self.cm_choice41.GetSelection()
    #     if nn1 == 1:
    #         n1 = 2
    #     elif nn1 == 2 or nn1 == 3 or nn1 == 4:
    #         n1 = nn1 + 2
    #     elif nn == 0:
    #         n1 = nn1
    #     else:
    #         n1 = 100
    #     attack_plus, defence_plus, crit_plus, balance_plus,\
    #         speed_plus, resistance_plus, hp_plus = enchant_jewelry0(n1)
    #     attack_mall = attack_mall + attack_minus
    #     defence_mall = defence_mall + defence_minus
    #     crit_mall = crit_mall + crit_minus
    #     balance_mall = balance_mall + balance_minus
    #     speed_mall = speed_mall + speed_minus
    #     resistance_mall = resistance_mall + resistance_minus
    #     hp_mall = hp_mall + hp_minus
    #     hp_pall = hp_pall + hp_plus
    #     attack_pall = attack_pall + attack_plus
    #     defence_pall = defence_pall + defence_plus
    #     crit_pall = crit_pall + crit_plus
    #     balance_pall = balance_pall + balance_plus
    #     speed_pall = speed_pall + speed_plus
    #     resistance_pall = resistance_pall + resistance_plus
    #     event.Skip()
    #
    # def choice42(self, event):
    #     global attack_mall
    #     global defence_mall
    #     global crit_mall
    #     global balance_mall
    #     global speed_mall
    #     global resistance_mall
    #     global hp_mall
    #     global hp_pall
    #     global attack_pall
    #     global defence_pall
    #     global crit_pall
    #     global balance_pall
    #     global speed_pall
    #     global resistance_pall
    #     nn = self.cm_choice16.GetSelection()
    #     if nn != 3:
    #         n = nn + 1
    #     else:
    #         n = 100
    #     attack_minus, defence_minus, crit_minus, balance_minus,\
    #         speed_minus, resistance_minus, hp_minus = enchant_jewelry1(n)
    #     nn1 = self.cm_choice42.GetSelection()
    #     if nn1 != 3:
    #         n1 = nn1 + 1
    #     else:
    #         n1 = 100
    #     attack_plus, defence_plus, crit_plus, balance_plus,\
    #         speed_plus, resistance_plus, hp_plus = enchant_jewelry1(n1)
    #     attack_mall = attack_mall + attack_minus
    #     defence_mall = defence_mall + defence_minus
    #     crit_mall = crit_mall + crit_minus
    #     balance_mall = balance_mall + balance_minus
    #     speed_mall = speed_mall + speed_minus
    #     resistance_mall = resistance_mall + resistance_minus
    #     hp_mall = hp_mall + hp_minus
    #     hp_pall = hp_pall + hp_plus
    #     attack_pall = attack_pall + attack_plus
    #     defence_pall = defence_pall + defence_plus
    #     crit_pall = crit_pall + crit_plus
    #     balance_pall = balance_pall + balance_plus
    #     speed_pall = speed_pall + speed_plus
    #     resistance_pall = resistance_pall + resistance_plus
    #     event.Skip()
    #
    # def choice43(self, event):
    #     global attack_mall
    #     global defence_mall
    #     global crit_mall
    #     global balance_mall
    #     global speed_mall
    #     global resistance_mall
    #     global hp_mall
    #     global hp_pall
    #     global attack_pall
    #     global defence_pall
    #     global crit_pall
    #     global balance_pall
    #     global speed_pall
    #     global resistance_pall
    #     nn = self.cm_choice17.GetSelection()
    #     if nn != 3:
    #         n = nn + 4
    #     else:
    #         n = 100
    #     attack_minus, defence_minus, crit_minus, balance_minus, \
    #         speed_minus, resistance_minus, hp_minus = enchant_jewelry0(n)
    #     nn1 = self.cm_choice43.GetSelection()
    #     if nn1 != 3:
    #         n1 = nn1 + 4
    #     else:
    #         n1 = 100
    #     attack_plus, defence_plus, crit_plus, balance_plus,\
    #         speed_plus, resistance_plus, hp_plus = enchant_jewelry0(n1)
    #     attack_mall = attack_mall + attack_minus
    #     defence_mall = defence_mall + defence_minus
    #     crit_mall = crit_mall + crit_minus
    #     balance_mall = balance_mall + balance_minus
    #     speed_mall = speed_mall + speed_minus
    #     resistance_mall = resistance_mall + resistance_minus
    #     hp_mall = hp_mall + hp_minus
    #     hp_pall = hp_pall + hp_plus
    #     attack_pall = attack_pall + attack_plus
    #     defence_pall = defence_pall + defence_plus
    #     crit_pall = crit_pall + crit_plus
    #     balance_pall = balance_pall + balance_plus
    #     speed_pall = speed_pall + speed_plus
    #     resistance_pall = resistance_pall + resistance_plus
    #     event.Skip()
    #
    # def choice44(self, event):
    #     global attack_mall
    #     global defence_mall
    #     global crit_mall
    #     global balance_mall
    #     global speed_mall
    #     global resistance_mall
    #     global hp_mall
    #     global hp_pall
    #     global attack_pall
    #     global defence_pall
    #     global crit_pall
    #     global balance_pall
    #     global speed_pall
    #     global resistance_pall
    #     nn = self.cm_choice18.GetSelection()
    #     if nn != 3:
    #         n = nn + 1
    #     else:
    #         n = 100
    #     attack_minus, defence_minus, crit_minus, balance_minus,\
    #         speed_minus, resistance_minus, hp_minus = enchant_jewelry1(n)
    #     nn1 = self.cm_choice44.GetSelection()
    #     if nn1 != 3:
    #         n1 = nn1 + 1
    #     else:
    #         n1 = 100
    #     attack_plus, defence_plus, crit_plus, balance_plus,\
    #         speed_plus, resistance_plus, hp_plus = enchant_jewelry1(n1)
    #     attack_mall = attack_mall + attack_minus
    #     defence_mall = defence_mall + defence_minus
    #     crit_mall = crit_mall + crit_minus
    #     balance_mall = balance_mall + balance_minus
    #     speed_mall = speed_mall + speed_minus
    #     resistance_mall = resistance_mall + resistance_minus
    #     hp_mall = hp_mall + hp_minus
    #     hp_pall = hp_pall + hp_plus
    #     attack_pall = attack_pall + attack_plus
    #     defence_pall = defence_pall + defence_plus
    #     crit_pall = crit_pall + crit_plus
    #     balance_pall = balance_pall + balance_plus
    #     speed_pall = speed_pall + speed_plus
    #     resistance_pall = resistance_pall + resistance_plus
    #     event.Skip()
    #
    # def choice45(self, event):
    #     global attack_mall
    #     global defence_mall
    #     global crit_mall
    #     global balance_mall
    #     global speed_mall
    #     global resistance_mall
    #     global hp_mall
    #     global hp_pall
    #     global attack_pall
    #     global defence_pall
    #     global crit_pall
    #     global balance_pall
    #     global speed_pall
    #     global resistance_pall
    #     nn = self.cm_choice19.GetSelection()
    #     if nn == 0:
    #         n = 10
    #     elif nn == 1:
    #         n = 9
    #     elif nn >= 2 & nn <= 4:
    #         n = nn + 2
    #     else:
    #         n = 100
    #     attack_minus, defence_minus, crit_minus, balance_minus,\
    #         speed_minus, resistance_minus, hp_minus = enchant_jewelry0(n)
    #     nn1 = self.cm_choice45.GetSelection()
    #     if nn1 == 0:
    #         n1 = 10
    #     elif nn1 == 1:
    #         n1 = 9
    #     elif nn1 >= 2 & nn1 <= 4:
    #         n1 = nn1 + 2
    #     else:
    #         n1 = 100
    #     attack_plus, defence_plus, crit_plus, balance_plus, \
    #         speed_plus, resistance_plus, hp_plus = enchant_jewelry0(n1)
    #     attack_mall = attack_mall + attack_minus
    #     defence_mall = defence_mall + defence_minus
    #     crit_mall = crit_mall + crit_minus
    #     balance_mall = balance_mall + balance_minus
    #     speed_mall = speed_mall + speed_minus
    #     resistance_mall = resistance_mall + resistance_minus
    #     hp_mall = hp_mall + hp_minus
    #     hp_pall = hp_pall + hp_plus
    #     attack_pall = attack_pall + attack_plus
    #     defence_pall = defence_pall + defence_plus
    #     crit_pall = crit_pall + crit_plus
    #     balance_pall = balance_pall + balance_plus
    #     speed_pall = speed_pall + speed_plus
    #     resistance_pall = resistance_pall + resistance_plus
    #     event.Skip()
    #
    # def choice46(self, event):
    #     global attack_mall
    #     global defence_mall
    #     global crit_mall
    #     global balance_mall
    #     global speed_mall
    #     global resistance_mall
    #     global hp_mall
    #     global hp_pall
    #     global attack_pall
    #     global defence_pall
    #     global crit_pall
    #     global balance_pall
    #     global speed_pall
    #     global resistance_pall
    #     nn = self.cm_choice20.GetSelection()
    #     if nn != 4:
    #         n = nn
    #     else:
    #         n = 100
    #     attack_minus, defence_minus, crit_minus, balance_minus,\
    #         speed_minus, resistance_minus, hp_minus = enchant_jewelry1(n)
    #     nn1 = self.cm_choice46.GetSelection()
    #     if nn1 != 4:
    #         n1 = nn1
    #     else:
    #         n1 = 100
    #     attack_plus, defence_plus, crit_plus, balance_plus, \
    #         speed_plus, resistance_plus, hp_plus = enchant_jewelry1(n1)
    #     attack_mall = attack_mall + attack_minus
    #     defence_mall = defence_mall + defence_minus
    #     crit_mall = crit_mall + crit_minus
    #     balance_mall = balance_mall + balance_minus
    #     speed_mall = speed_mall + speed_minus
    #     resistance_mall = resistance_mall + resistance_minus
    #     hp_mall = hp_mall + hp_minus
    #     hp_pall = hp_pall + hp_plus
    #     attack_pall = attack_pall + attack_plus
    #     defence_pall = defence_pall + defence_plus
    #     crit_pall = crit_pall + crit_plus
    #     balance_pall = balance_pall + balance_plus
    #     speed_pall = speed_pall + speed_plus
    #     resistance_pall = resistance_pall + resistance_plus
    #     event.Skip()
    #
    # def choice47(self, event):
    #     global attack_mall
    #     global defence_mall
    #     global crit_mall
    #     global balance_mall
    #     global speed_mall
    #     global resistance_mall
    #     global hp_mall
    #     global hp_pall
    #     global attack_pall
    #     global defence_pall
    #     global crit_pall
    #     global balance_pall
    #     global speed_pall
    #     global resistance_pall
    #     nn = self.cm_choice23.GetSelection()
    #     if nn == 0 or nn == 1:
    #         n = nn + 7
    #     else:
    #         n = 100
    #     attack_minus, defence_minus, crit_minus, balance_minus,\
    #         speed_minus, resistance_minus, hp_minus = enchant_jewelry0(n)
    #     nn1 = self.cm_choice47.GetSelection()
    #     if nn1 == 0 or nn1 == 1:
    #         n1 = nn1 + 7
    #     else:
    #         n1 = 100
    #     attack_plus, defence_plus, crit_plus, balance_plus, \
    #         speed_plus, resistance_plus, hp_plus = enchant_jewelry0(n1)
    #     attack_mall = attack_mall + attack_minus
    #     defence_mall = defence_mall + defence_minus
    #     crit_mall = crit_mall + crit_minus
    #     balance_mall = balance_mall + balance_minus
    #     speed_mall = speed_mall + speed_minus
    #     resistance_mall = resistance_mall + resistance_minus
    #     hp_mall = hp_mall + hp_minus
    #     hp_pall = hp_pall + hp_plus
    #     attack_pall = attack_pall + attack_plus
    #     defence_pall = defence_pall + defence_plus
    #     crit_pall = crit_pall + crit_plus
    #     balance_pall = balance_pall + balance_plus
    #     speed_pall = speed_pall + speed_plus
    #     resistance_pall = resistance_pall + resistance_plus
    #     event.Skip()
    #
    # def choice48(self, event):
    #     global attack_mall
    #     global defence_mall
    #     global crit_mall
    #     global balance_mall
    #     global speed_mall
    #     global resistance_mall
    #     global hp_mall
    #     global hp_pall
    #     global attack_pall
    #     global defence_pall
    #     global crit_pall
    #     global balance_pall
    #     global speed_pall
    #     global resistance_pall
    #     nn = self.cm_choice24.GetSelection()
    #     if nn == 0:
    #         n = 4
    #     else:
    #         n = 100
    #     attack_minus, defence_minus, crit_minus, balance_minus,\
    #         speed_minus, resistance_minus, hp_minus = enchant_jewelry1(n)
    #     nn1 = self.cm_choice48.GetSelection()
    #     if nn1 == 0:
    #         n1 = 4
    #     else:
    #         n1 = 100
    #     attack_plus, defence_plus, crit_plus, balance_plus,\
    #         speed_plus, resistance_plus, hp_plus = enchant_jewelry1(n1)
    #     attack_mall = attack_mall + attack_minus
    #     defence_mall = defence_mall + defence_minus
    #     crit_mall = crit_mall + crit_minus
    #     balance_mall = balance_mall + balance_minus
    #     speed_mall = speed_mall + speed_minus
    #     resistance_mall = resistance_mall + resistance_minus
    #     hp_mall = hp_mall + hp_minus
    #     hp_pall = hp_pall + hp_plus
    #     attack_pall = attack_pall + attack_plus
    #     defence_pall = defence_pall + defence_plus
    #     crit_pall = crit_pall + crit_plus
    #     balance_pall = balance_pall + balance_plus
    #     speed_pall = speed_pall + speed_plus
    #     resistance_pall = resistance_pall + resistance_plus
    #     event.Skip()
    #
    # def choice49(self, event):
    #     global attack_mall
    #     global defence_mall
    #     global crit_mall
    #     global balance_mall
    #     global speed_mall
    #     global resistance_mall
    #     global hp_mall
    #     global hp_pall
    #     global attack_pall
    #     global defence_pall
    #     global crit_pall
    #     global balance_pall
    #     global speed_pall
    #     global resistance_pall
    #     nn = self.cm_choice25.GetSelection()
    #     if nn == 0:
    #         n = 1
    #     elif nn >= 1 & nn <= 3:
    #         n = nn + 2
    #     else:
    #         n = 100
    #     attack_minus, defence_minus, crit_minus, balance_minus,\
    #         speed_minus, resistance_minus, hp_minus = enchant_jewelry0(n)
    #     nn1 = self.cm_choice49.GetSelection()
    #     if nn1 == 0:
    #         n1 = 1
    #     elif nn1 >= 1 & nn1 <= 3:
    #         n1 = nn1 + 2
    #     else:
    #         n1 = 100
    #     attack_plus, defence_plus, crit_plus, balance_plus,\
    #         speed_plus, resistance_plus, hp_plus = enchant_jewelry0(n1)
    #     attack_mall = attack_mall + attack_minus
    #     defence_mall = defence_mall + defence_minus
    #     crit_mall = crit_mall + crit_minus
    #     balance_mall = balance_mall + balance_minus
    #     speed_mall = speed_mall + speed_minus
    #     resistance_mall = resistance_mall + resistance_minus
    #     hp_mall = hp_mall + hp_minus
    #     hp_pall = hp_pall + hp_plus
    #     attack_pall = attack_pall + attack_plus
    #     defence_pall = defence_pall + defence_plus
    #     crit_pall = crit_pall + crit_plus
    #     balance_pall = balance_pall + balance_plus
    #     speed_pall = speed_pall + speed_plus
    #     resistance_pall = resistance_pall + resistance_plus
    #     event.Skip()
    #
    # def choice50(self, event):
    #     global attack_mall
    #     global defence_mall
    #     global crit_mall
    #     global balance_mall
    #     global speed_mall
    #     global resistance_mall
    #     global hp_mall
    #     global hp_pall
    #     global attack_pall
    #     global defence_pall
    #     global crit_pall
    #     global balance_pall
    #     global speed_pall
    #     global resistance_pall
    #     nn = self.cm_choice26.GetSelection()
    #     if nn != 4:
    #         n = nn
    #     else:
    #         n = 100
    #     attack_minus, defence_minus, crit_minus, balance_minus,\
    #         speed_minus, resistance_minus, hp_minus = enchant_jewelry1(n)
    #     nn1 = self.cm_choice50.GetSelection()
    #     if nn1 != 4:
    #         n1 = nn1
    #     else:
    #         n1 = 100
    #     attack_plus, defence_plus, crit_plus, balance_plus,\
    #         speed_plus, resistance_plus, hp_plus = enchant_jewelry1(n1)
    #     attack_mall = attack_mall + attack_minus
    #     defence_mall = defence_mall + defence_minus
    #     crit_mall = crit_mall + crit_minus
    #     balance_mall = balance_mall + balance_minus
    #     speed_mall = speed_mall + speed_minus
    #     resistance_mall = resistance_mall + resistance_minus
    #     hp_mall = hp_mall + hp_minus
    #     hp_pall = hp_pall + hp_plus
    #     attack_pall = attack_pall + attack_plus
    #     defence_pall = defence_pall + defence_plus
    #     crit_pall = crit_pall + crit_plus
    #     balance_pall = balance_pall + balance_plus
    #     speed_pall = speed_pall + speed_plus
    #     resistance_pall = resistance_pall + resistance_plus
    #     event.Skip()
    #
    # def choice51(self, event):
    #     global attack_mall
    #     global defence_mall
    #     global crit_mall
    #     global balance_mall
    #     global speed_mall
    #     global resistance_mall
    #     global hp_mall
    #     global hp_pall
    #     global attack_pall
    #     global defence_pall
    #     global crit_pall
    #     global balance_pall
    #     global speed_pall
    #     global resistance_pall
    #     nn = self.cm_choice27.GetSelection()
    #     if nn != 3:
    #         n = nn + 4
    #     else:
    #         n = 100
    #     attack_minus, defence_minus, crit_minus, balance_minus,\
    #         speed_minus, resistance_minus, hp_minus = enchant_jewelry0(n)
    #     nn1 = self.cm_choice51.GetSelection()
    #     if nn1 != 3:
    #         n1 = nn1 + 4
    #     else:
    #         n1 = 100
    #     attack_plus, defence_plus, crit_plus, balance_plus, \
    #         speed_plus, resistance_plus, hp_plus = enchant_jewelry0(n1)
    #     attack_mall = attack_mall + attack_minus
    #     defence_mall = defence_mall + defence_minus
    #     crit_mall = crit_mall + crit_minus
    #     balance_mall = balance_mall + balance_minus
    #     speed_mall = speed_mall + speed_minus
    #     resistance_mall = resistance_mall + resistance_minus
    #     hp_mall = hp_mall + hp_minus
    #     hp_pall = hp_pall + hp_plus
    #     attack_pall = attack_pall + attack_plus
    #     defence_pall = defence_pall + defence_plus
    #     crit_pall = crit_pall + crit_plus
    #     balance_pall = balance_pall + balance_plus
    #     speed_pall = speed_pall + speed_plus
    #     resistance_pall = resistance_pall + resistance_plus
    #     event.Skip()
    #
    # def choice52(self, event):
    #     global attack_mall
    #     global defence_mall
    #     global crit_mall
    #     global balance_mall
    #     global speed_mall
    #     global resistance_mall
    #     global hp_mall
    #     global hp_pall
    #     global attack_pall
    #     global defence_pall
    #     global crit_pall
    #     global balance_pall
    #     global speed_pall
    #     global resistance_pall
    #     nn = self.cm_choice28.GetSelection()
    #     if nn != 4:
    #         n = nn
    #     else:
    #         n = 100
    #     attack_minus, defence_minus, crit_minus, balance_minus,\
    #         speed_minus, resistance_minus, hp_minus = enchant_jewelry1(n)
    #     nn1 = self.cm_choice52.GetSelection()
    #     if nn1 != 4:
    #         n1 = nn1
    #     else:
    #         n1 = 100
    #     attack_plus, defence_plus, crit_plus, balance_plus,\
    #         speed_plus, resistance_plus, hp_plus = enchant_jewelry1(n1)
    #     attack_mall = attack_mall + attack_minus
    #     defence_mall = defence_mall + defence_minus
    #     crit_mall = crit_mall + crit_minus
    #     balance_mall = balance_mall + balance_minus
    #     speed_mall = speed_mall + speed_minus
    #     resistance_mall = resistance_mall + resistance_minus
    #     hp_mall = hp_mall + hp_minus
    #     hp_pall = hp_pall + hp_plus
    #     attack_pall = attack_pall + attack_plus
    #     defence_pall = defence_pall + defence_plus
    #     crit_pall = crit_pall + crit_plus
    #     balance_pall = balance_pall + balance_plus
    #     speed_pall = speed_pall + speed_plus
    #     resistance_pall = resistance_pall + resistance_plus
    #     event.Skip()
    #
    # def choice55(self, event):
    #     global attack_mall
    #     global defence_mall
    #     global crit_mall
    #     global balance_mall
    #     global speed_mall
    #     global resistance_mall
    #     global hp_mall
    #     global hp_pall
    #     global attack_pall
    #     global defence_pall
    #     global crit_pall
    #     global balance_pall
    #     global speed_pall
    #     global resistance_pall
    #     nn = self.cm_choice53.GetSelection()
    #     if nn != 3:
    #         n = nn + 4
    #     else:
    #         n = 100
    #     attack_minus, defence_minus, crit_minus, balance_minus,\
    #         speed_minus, resistance_minus, hp_minus = enchant_jewelry0(n)
    #     nn1 = self.cm_choice55.GetSelection()
    #     if nn1 != 3:
    #         n1 = nn1 + 4
    #     else:
    #         n1 = 100
    #     attack_plus, defence_plus, crit_plus, balance_plus,\
    #         speed_plus, resistance_plus, hp_plus = enchant_jewelry0(n1)
    #     attack_mall = attack_mall + attack_minus
    #     defence_mall = defence_mall + defence_minus
    #     crit_mall = crit_mall + crit_minus
    #     balance_mall = balance_mall + balance_minus
    #     speed_mall = speed_mall + speed_minus
    #     resistance_mall = resistance_mall + resistance_minus
    #     hp_mall = hp_mall + hp_minus
    #     hp_pall = hp_pall + hp_plus
    #     attack_pall = attack_pall + attack_plus
    #     defence_pall = defence_pall + defence_plus
    #     crit_pall = crit_pall + crit_plus
    #     balance_pall = balance_pall + balance_plus
    #     speed_pall = speed_pall + speed_plus
    #     resistance_pall = resistance_pall + resistance_plus
    #     event.Skip()
    #
    # def choice56(self, event):
    #     global attack_mall
    #     global defence_mall
    #     global crit_mall
    #     global balance_mall
    #     global speed_mall
    #     global resistance_mall
    #     global hp_mall
    #     global hp_pall
    #     global attack_pall
    #     global defence_pall
    #     global crit_pall
    #     global balance_pall
    #     global speed_pall
    #     global resistance_pall
    #     nn = self.cm_choice54.GetSelection()
    #     if nn != 4:
    #         n = nn
    #     else:
    #         n = 100
    #     attack_minus, defence_minus, crit_minus, balance_minus, \
    #         speed_minus, resistance_minus, hp_minus = enchant_jewelry1(n)
    #     nn1 = self.cm_choice56.GetSelection()
    #     if nn1 != 4:
    #         n1 = nn1
    #     else:
    #         n1 = 100
    #     attack_plus, defence_plus, crit_plus, balance_plus,\
    #         speed_plus, resistance_plus, hp_plus = enchant_jewelry1(n1)
    #     attack_mall = attack_mall + attack_minus
    #     defence_mall = defence_mall + defence_minus
    #     crit_mall = crit_mall + crit_minus
    #     balance_mall = balance_mall + balance_minus
    #     speed_mall = speed_mall + speed_minus
    #     resistance_mall = resistance_mall + resistance_minus
    #     hp_mall = hp_mall + hp_minus
    #     hp_pall = hp_pall + hp_plus
    #     attack_pall = attack_pall + attack_plus
    #     defence_pall = defence_pall + defence_plus
    #     crit_pall = crit_pall + crit_plus
    #     balance_pall = balance_pall + balance_plus
    #     speed_pall = speed_pall + speed_plus
    #     resistance_pall = resistance_pall + resistance_plus
    #     event.Skip()

    def __del__(self):
        pass


class Others(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(831, 530),
                          style=wx.TAB_TRAVERSAL)

        bSizer1 = wx.BoxSizer(wx.HORIZONTAL)

        sbSizer1 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"附魔出处"), wx.HORIZONTAL)

        gbSizer5 = wx.GridBagSizer(0, 0)
        gbSizer5.SetFlexibleDirection(wx.BOTH)
        gbSizer5.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.dm_textCtrl66 = wx.TextCtrl(sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                         wx.DefaultSize, 0)
        gbSizer5.Add(self.dm_textCtrl66, wx.GBPosition(0, 0), wx.GBSpan(1, 1),
                     wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.dm_button15 = wx.Button(sbSizer1.GetStaticBox(), wx.ID_ANY, u"查询", wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer5.Add(self.dm_button15, wx.GBPosition(0, 1), wx.GBSpan(1, 1),
                     wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.dm_textCtrl67 = wx.TextCtrl(sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                         wx.DefaultSize, wx.TE_MULTILINE | wx.TE_READONLY)
        gbSizer5.Add(self.dm_textCtrl67, wx.GBPosition(1, 0), wx.GBSpan(9, 2), wx.ALL | wx.EXPAND, 5)

        self.dm_staticText87 = wx.StaticText(sbSizer1.GetStaticBox(), wx.ID_ANY, u"攻击", wx.DefaultPosition,
                                             wx.DefaultSize, 0)
        self.dm_staticText87.Wrap(-1)
        gbSizer5.Add(self.dm_staticText87, wx.GBPosition(10, 0), wx.GBSpan(1, 2), wx.ALL | wx.EXPAND, 5)

        self.dm_staticText88 = wx.StaticText(sbSizer1.GetStaticBox(), wx.ID_ANY, u"防御", wx.DefaultPosition,
                                             wx.DefaultSize, 0)
        self.dm_staticText88.Wrap(-1)
        gbSizer5.Add(self.dm_staticText88, wx.GBPosition(11, 0), wx.GBSpan(1, 2), wx.ALL | wx.EXPAND, 5)

        self.dm_staticText89 = wx.StaticText(sbSizer1.GetStaticBox(), wx.ID_ANY, u"暴击", wx.DefaultPosition,
                                             wx.DefaultSize, 0)
        self.dm_staticText89.Wrap(-1)
        gbSizer5.Add(self.dm_staticText89, wx.GBPosition(12, 0), wx.GBSpan(1, 2), wx.ALL | wx.EXPAND, 5)

        self.dm_staticText90 = wx.StaticText(sbSizer1.GetStaticBox(), wx.ID_ANY, u"平衡", wx.DefaultPosition,
                                             wx.DefaultSize, 0)
        self.dm_staticText90.Wrap(-1)
        gbSizer5.Add(self.dm_staticText90, wx.GBPosition(13, 0), wx.GBSpan(1, 2), wx.ALL | wx.EXPAND, 5)

        self.dm_staticText91 = wx.StaticText(sbSizer1.GetStaticBox(), wx.ID_ANY, u"攻速", wx.DefaultPosition,
                                             wx.DefaultSize, 0)
        self.dm_staticText91.Wrap(-1)
        gbSizer5.Add(self.dm_staticText91, wx.GBPosition(14, 0), wx.GBSpan(1, 2), wx.ALL | wx.EXPAND, 5)

        self.dm_staticText92 = wx.StaticText(sbSizer1.GetStaticBox(), wx.ID_ANY, u"爆抗", wx.DefaultPosition,
                                             wx.DefaultSize, 0)
        self.dm_staticText92.Wrap(-1)
        gbSizer5.Add(self.dm_staticText92, wx.GBPosition(15, 0), wx.GBSpan(1, 2), wx.ALL | wx.EXPAND, 5)

        self.dm_staticText74 = wx.StaticText(sbSizer1.GetStaticBox(), wx.ID_ANY, u"其他", wx.DefaultPosition,
                                             wx.DefaultSize, 0)
        self.dm_staticText74.Wrap(-1)
        gbSizer5.Add(self.dm_staticText74, wx.GBPosition(16, 0), wx.GBSpan(1, 2), wx.ALL | wx.EXPAND, 5)

        sbSizer1.Add(gbSizer5, 1, wx.EXPAND, 5)

        bSizer1.Add(sbSizer1, 1, wx.EXPAND, 5)

        sbSizer2 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"武器强化概率一览"), wx.HORIZONTAL)

        gbSizer51 = wx.GridBagSizer(0, 0)
        gbSizer51.SetFlexibleDirection(wx.BOTH)
        gbSizer51.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        str_rate = "    +1 ------------100%\r\n    +2 ------------100%\r\n    +3 ------------100%\r\n" \
                   "    +4 ------------ 90%\r\n    +5 ------------ 90%\r\n" \
                   "----------------------------\r\n" \
                   "    +6 ------------ 80%\r\n    +7 ------------ 70%\r\n    +8 ------------ 60%\r\n" \
                   "----------------------------\r\n" \
                   "    +9 ------------ 55%\r\n    +10------------ 50%\r\n" \
                   "----------------------------\r\n" \
                   "    +11------------ 45%\r\n    +12------------ 40%\r\n" \
                   "----------------------------\r\n" \
                   "    +13------------ 20%\r\n    +14------------ 16%\r\n    +15------------ 15%\r\n" \
                   "----------------------------\r\n" \
                   "    +16------------ 14%\r\n    +17------------ 13%\r\n    +18------------ 10%\r\n" \
                   "----------------------------\r\n" \
                   "    +19------------ 8%\r\n    +20------------ 1%\r\n"
        self.dm_staticText75 = wx.StaticText(sbSizer2.GetStaticBox(), wx.ID_ANY, str_rate, wx.DefaultPosition,
                                             wx.DefaultSize, 0)
        self.dm_staticText75.Wrap(-1)
        gbSizer51.Add(self.dm_staticText75, wx.GBPosition(0, 0), wx.GBSpan(19, 2), wx.ALL | wx.EXPAND, 5)

        sbSizer2.Add(gbSizer51, 1, wx.EXPAND, 5)

        bSizer1.Add(sbSizer2, 1, wx.EXPAND, 5)

        sbSizer3 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"附魔相关"), wx.HORIZONTAL)

        gbSizer6 = wx.GridBagSizer(0, 0)
        gbSizer6.SetFlexibleDirection(wx.BOTH)
        gbSizer6.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.dm_staticText76 = wx.StaticText(sbSizer3.GetStaticBox(), wx.ID_ANY, u"附魔失败多少次将不如直接购买碎片",
                                             wx.DefaultPosition, wx.DefaultSize, 0)
        self.dm_staticText76.Wrap(-1)
        gbSizer6.Add(self.dm_staticText76, wx.GBPosition(0, 0), wx.GBSpan(1, 2), wx.ALL | wx.EXPAND, 5)

        self.dm_staticText77 = wx.StaticText(sbSizer3.GetStaticBox(), wx.ID_ANY, u"附魔价格", wx.DefaultPosition,
                                             wx.DefaultSize, 0)
        self.dm_staticText77.Wrap(-1)
        gbSizer6.Add(self.dm_staticText77, wx.GBPosition(1, 0), wx.GBSpan(1, 1),
                     wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.dm_textCtrl55 = wx.TextCtrl(sbSizer3.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                         wx.DefaultSize, 0)
        gbSizer6.Add(self.dm_textCtrl55, wx.GBPosition(1, 1), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        self.dm_staticText78 = wx.StaticText(sbSizer3.GetStaticBox(), wx.ID_ANY, u"碎片价格", wx.DefaultPosition,
                                             wx.DefaultSize, 0)
        self.dm_staticText78.Wrap(-1)
        gbSizer6.Add(self.dm_staticText78, wx.GBPosition(2, 0), wx.GBSpan(1, 1),
                     wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.dm_textCtrl56 = wx.TextCtrl(sbSizer3.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                         wx.DefaultSize, 0)
        gbSizer6.Add(self.dm_textCtrl56, wx.GBPosition(2, 1), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        self.dm_staticText79 = wx.StaticText(sbSizer3.GetStaticBox(), wx.ID_ANY, u"金价比例", wx.DefaultPosition,
                                             wx.DefaultSize, 0)
        self.dm_staticText79.Wrap(-1)
        gbSizer6.Add(self.dm_staticText79, wx.GBPosition(3, 0), wx.GBSpan(1, 1),
                     wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.dm_button11 = wx.Button(sbSizer3.GetStaticBox(), wx.ID_ANY, u"计算", wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer6.Add(self.dm_button11, wx.GBPosition(4, 0), wx.GBSpan(1, 2), wx.ALL | wx.EXPAND, 5)

        self.dm_staticText80 = wx.StaticText(sbSizer3.GetStaticBox(), wx.ID_ANY,
                                             u"------------------------------------\r\n", wx.DefaultPosition,
                                             wx.DefaultSize, 0)
        self.dm_staticText80.Wrap(-1)
        gbSizer6.Add(self.dm_staticText80, wx.GBPosition(5, 0), wx.GBSpan(3, 2),
                     wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL | wx.EXPAND, 5)

        self.dm_staticText82 = wx.StaticText(sbSizer3.GetStaticBox(), wx.ID_ANY,
                                             u"------------------------------------\r\n", wx.DefaultPosition,
                                             wx.DefaultSize, 0)
        self.dm_staticText82.Wrap(-1)
        gbSizer6.Add(self.dm_staticText82, wx.GBPosition(8, 0), wx.GBSpan(3, 2),
                     wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL | wx.EXPAND, 5)

        mind = u"------------------------------------\r\n该小程序可以用来计算\r\n你多少次附魔失败之后的总花费\r\n" \
               u"将超过直接购买4个碎片合成的花费\r\n" \
               u"在上面的框中填入价格,单位:W\r\n比例为1RMB兑换多少游戏币\r\n由于采用了四舍五入的方法\r\n" \
               u"所以与实际可能有一点点的差距"
        self.dm_staticText81 = wx.StaticText(sbSizer3.GetStaticBox(), wx.ID_ANY, mind, wx.DefaultPosition,
                                             wx.DefaultSize, 0)
        self.dm_staticText81.Wrap(-1)
        gbSizer6.Add(self.dm_staticText81, wx.GBPosition(11, 0), wx.GBSpan(3, 2),
                     wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL | wx.EXPAND, 5)

        self.dm_textCtrl57 = wx.TextCtrl(sbSizer3.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                         wx.DefaultSize, 0)
        gbSizer6.Add(self.dm_textCtrl57, wx.GBPosition(3, 1), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        sbSizer3.Add(gbSizer6, 1, wx.EXPAND, 5)

        bSizer1.Add(sbSizer3, 1, wx.EXPAND, 5)

        self.SetSizer(bSizer1)
        self.Layout()

        self.dm_button15.Bind(wx.EVT_BUTTON, self.button15)
        self.dm_button11.Bind(wx.EVT_BUTTON, self.button11)

        pub.subscribe(self.updatejoke, "joker")
        pub.subscribe(self.enable_find, "joker1")

    def __del__(self):
        pass

    def button15(self, event):  # 附魔查找
        global autojoke
        fumo = self.dm_textCtrl66.GetValue()
        jewelry_list = ['亡者', '隐隐', '闪亮', '小巧', '迅速', '有意义', '多疑', '洒脱', '惊心动魄', '宝物猎人', '星光',
                      'wz', 'yy', 'sl', 'xq', 'xs', 'yyy', 'dy', 'st', 'jxdp', 'bwlr', 'xg',
                      'WZ', 'YY', 'SL', 'XQ', 'XS', 'YYY', 'DY', 'ST', 'JXDP', 'BWLR', 'XG']
        jewelry_list1 = ['高尚的', '热情', '心灵', '活力', '金刚石',
                         'gsd', 'rq', 'xl', 'hl', 'jgs',
                         'GSD', 'RQ', 'XL', 'HL', 'JGS']
        armor_list = ['冷静', '哭泣', '记忆', '重述', '时间', '保持平衡', '努力',
                      'lj', 'kq', 'jy', 'cs', 'sj', 'bcph', 'nl',
                      'LJ', 'KQ', 'JY', 'CS', 'SJ', 'BCPH', 'NL']
        armor_list1 = ['回音', '远征', '热忱', '落叶', '茉莉花', '致命', '烙印', '保护', '抵抗', '犰狳',
                       'hy', 'yz', 'rc', 'ly', 'mlh', 'zm', 'ly', 'bh', 'dk',
                       'HY', 'YZ', 'RC', 'LY', 'MLH', 'ZM', 'LY', 'BH', 'DK']
        head_list = ['不义', '正义', '混沌', '曙光', '富饶', '确凿', '猎豹',
                       'by', 'zy', 'hd', 'sg', 'fr', 'qz', 'lb',
                       'BY', 'ZY', 'HD', 'SG', 'FR', 'QZ', 'LB']
        head_list1 = ['审判', '断罪', '花瓣', '勇猛', '天诛', '野心', '挑战',
                        'sp', 'dz', 'hb', 'ym', 'tz', 'yx', 'tz',
                        'SP', 'DZ', 'HB', 'YM', 'TZ', 'YX', 'TZ']
        if fumo in jewelry_list:
            afu = jewelry_list.index(fumo)
            if afu > 21:
                afu = afu - 22
            elif (afu > 10) & (afu < 22):
                afu = afu - 11
            attack, defence, crit, balance, speed, resistance, hp = enchant_jewelry0(afu)
            self.dm_staticText87.SetLabelText('攻击:   %d' % attack)
            self.dm_staticText88.SetLabelText('防御:   %d' % defence)
            self.dm_staticText89.SetLabelText('暴击:   %d' % crit)
            self.dm_staticText90.SetLabelText('平衡:   %d' % balance)
            self.dm_staticText91.SetLabelText('攻速:   %d' % speed)
            self.dm_staticText92.SetLabelText('爆抗:   %d' % resistance)
            score = (crit + balance + speed)*300 + resistance*50 + attack + defence
            self.dm_staticText74.SetLabelText('其他:   评分:%d' % score)
            self.dm_textCtrl67.SetValue('')
            if afu == 0:
                self.dm_textCtrl67.SetValue('S3所有Raid副本有一定几率掉落\r\n可附魔在戒指上\r\n最大成功率40%'
                                            '\r\n简化版:闪亮的 附魔卷轴')
            elif afu == 1:
                self.dm_textCtrl67.SetValue('S3所有Raid副本有一定几率掉落\r\n可附魔在腰带上\r\n最大成功率40%'
                                            '\r\n简化版:小巧的 附魔卷轴')
            elif afu == 2:
                self.dm_textCtrl67.SetValue('公主:沙漠公主\r\n哈盘:流逝的记忆\r\n小死神:死亡暗影\r\n坦克:奇异的机器\r\n'
                                            '捡肥皂:深处深渊\r\n小光头:破败的莫乐班\r\n生死神:死神\r\n可附魔在戒指上\r\n'
                                            '最大成功率50%\r\n增强版:亡者的 附魔卷轴')
            elif afu == 3:
                self.dm_textCtrl67.SetValue('大蛇:支配者的安息处\r\n没完没了的提问\r\n地下城市\r\n坦克:奇异的机器\r\n'
                                            '捡肥皂:深处深渊\r\n小光头:破败的莫乐班\r\n生死神:死神\r\n可附魔在腰带上\r\n'
                                            '最大成功率50%\r\n增强版:隐隐的 附魔卷轴')
            elif afu == 4:
                self.dm_textCtrl67.SetValue('生存者\r\n章鱼:大海之恶魔\r\n公主:沙漠公主\r\n哈盘:流逝的记忆\r\n'
                                            '小死神:死亡暗影\r\n小光头:破败的莫乐班\r\n生死神:死神\r\n可附魔在全部饰品上\r\n'
                                            '最大成功率50%\r\n迅速的大量减少平衡还请注意')
            elif afu == 5:
                self.dm_textCtrl67.SetValue('生存者\r\n寻觅宝物\r\n章鱼:大海之恶魔\r\n公主:沙漠公主\r\n'
                                            '哈盘:流逝的记忆\r\n小光头:破败的莫乐班\r\n生死神:死神\r\n可附魔在全部饰品上\r\n'
                                            '最大成功率50%\r\n一点攻速,平衡不够时使用')
            elif afu == 6:
                self.dm_textCtrl67.SetValue('没有什么特别的地方\r\n升级就会出\r\n没有价值不建议使用')
            elif afu == 7:
                self.dm_textCtrl67.SetValue('S3所有Raid副本有一定几率掉落\r\n可附魔在盾牌魂器上\r\n最大成功率40%'
                                            '\r\n建议直接买碎片合成100%')
            elif afu == 8:
                self.dm_textCtrl67.SetValue('没有特别的地方\r\n可附魔在盾牌魂器上\r\n最大成功率50%')
            elif afu == 9:
                self.dm_textCtrl67.SetValue('已绝版\r\n可附魔在宝物胸针上')
            elif afu == 10:
                self.dm_textCtrl67.SetValue('已绝版\r\n可附魔在月光蓝宝石胸针上')
        elif fumo in jewelry_list1:
            afu = jewelry_list1.index(fumo)
            if afu > 9:
                afu = afu - 10
            elif (afu > 4) & (afu < 10):
                afu = afu - 5
            attack, defence, crit, balance, speed, resistance, hp = enchant_jewelry1(afu)
            self.dm_staticText87.SetLabelText('攻击:   %d' % attack)
            self.dm_staticText88.SetLabelText('防御:   %d' % defence)
            self.dm_staticText89.SetLabelText('暴击:   %d' % crit)
            self.dm_staticText90.SetLabelText('平衡:   %d' % balance)
            self.dm_staticText91.SetLabelText('攻速:   %d' % speed)
            self.dm_staticText92.SetLabelText('爆抗:   %d' % resistance)
            score = (crit + balance + speed) * 300 + resistance * 50 + attack + defence
            self.dm_staticText74.SetLabelText('其他:   评分:%d' % score)
            self.dm_textCtrl67.SetValue('')
            if afu == 0:
                self.dm_textCtrl67.SetValue('已绝版\r\n可附魔在月光蓝宝石胸针上')
            elif afu == 1:
                self.dm_textCtrl67.SetValue('生存者\r\n寻觅宝物\r\n章鱼:大海之恶魔\r\n火牛:地狱守门人\r\n'
                                            '德鲁伊:燃烧的神殿\r\n可附魔在所有饰品上\r\n搬砖神物')
            elif afu == 2:
                self.dm_textCtrl67.SetValue('生存者\r\n寻觅宝物\r\n章鱼:大海之恶魔\r\n德鲁伊:燃烧的神殿\r\n'
                                            '可附魔在所有饰品上\r\n最大成功率50%\r\n最多只适用一个')
            elif afu == 3:
                self.dm_textCtrl67.SetValue('不建议使用的附魔\r\n热情多好')
            elif afu == 4:
                self.dm_textCtrl67.SetValue('可附魔在盾牌魂器上')

        elif fumo in armor_list:
            afu = armor_list.index(fumo)
            if afu > 13:
                afu = afu - 14
            elif (afu > 6) & (afu < 14):
                afu = afu - 7
            attack, defence, crit, balance, speed, resistance, hp = enchant_armor0(afu)
            self.dm_staticText87.SetLabelText('攻击:   %d' % attack)
            self.dm_staticText88.SetLabelText('防御:   %d' % defence)
            self.dm_staticText89.SetLabelText('暴击:   %d' % crit)
            self.dm_staticText90.SetLabelText('平衡:   %d' % balance)
            self.dm_staticText91.SetLabelText('攻速:   %d' % speed)
            self.dm_staticText92.SetLabelText('爆抗:   %d' % resistance)
            score = (crit + balance + speed) * 300 + resistance * 50 + attack + defence
            self.dm_staticText74.SetLabelText('其他:   评分:%d' % score)
            self.dm_textCtrl67.SetValue('')
            if afu == 0:
                self.dm_textCtrl67.SetValue('S3除无头阿凡达之外所有R均本可掉落\r\n可附魔在头部和腿部防具上\r\n'
                                            '不可附魔在90级防具上')
            elif afu == 1:
                self.dm_textCtrl67.SetValue('S3除无头阿凡达之外所有R均本可掉落\r\n可附魔在手部和脚部防具上\r\n'
                                            '不可附魔在90级防具上')
            elif afu == 2:
                self.dm_textCtrl67.SetValue('S3除无头阿凡达之外所有R均本可掉落\r\n可附魔在头部和腿部防具上\r\n'
                                            '不建议附魔在95级防具上\r\n95防具有更好的附魔')
            elif afu == 3:
                self.dm_textCtrl67.SetValue('S3除无头阿凡达之外所有R均本可掉落\r\n可附魔在手部和脚部防具上\r\n'
                                            '不建议附魔在95级防具上\r\n95防具有更好的附魔')
            elif afu == 4:
                self.dm_textCtrl67.SetValue('S3除无头阿凡达之外所有R均本可掉落\r\n可附魔在上衣防具上\r\n'
                                            '拥有更高的暴击')
            elif afu == 5:
                self.dm_textCtrl67.SetValue('大蛇:支配者的安息处\r\n公主:沙漠公主\r\n哈盘:流逝的记忆\r\n'
                                            '小死神:死亡暗影\r\n小光头:破败的莫乐班\r\n生死神:死神'
                                            '可附魔在所有防具上\r\n新手过渡必备')
            elif afu == 6:
                self.dm_textCtrl67.SetValue('哇塞！你居然能找到这儿\r\n太不可思议了！\r\n然而这儿并没有什么特殊说明\r\n'
                                            '惊不惊喜！意不意外！')
        elif fumo in armor_list1:
            afu = armor_list1.index(fumo)
            if afu > 19:
                afu = afu - 20
            elif (afu > 9) & (afu < 20):
                afu = afu - 10
            attack, defence, crit, balance, speed, resistance = enchant_armor1(afu)
            self.dm_staticText87.SetLabelText('攻击:   %d' % attack)
            self.dm_staticText88.SetLabelText('防御:   %d' % defence)
            self.dm_staticText89.SetLabelText('暴击:   %d' % crit)
            self.dm_staticText90.SetLabelText('平衡:   %d' % balance)
            self.dm_staticText91.SetLabelText('攻速:   %d' % speed)
            self.dm_staticText92.SetLabelText('爆抗:   %d' % resistance)
            score = (crit + balance + speed) * 300 + resistance * 50 + attack + defence
            self.dm_staticText74.SetLabelText('其他:   评分:%d' % score)
            self.dm_textCtrl67.SetValue('')
            if afu == 0:
                self.dm_textCtrl67.SetValue('S3除无头阿凡达之外所有R均本可掉落\r\n可附魔在手部和脚部防具上\r\n'
                                            '托！你居然出回音了！')
            elif afu == 1:
                self.dm_textCtrl67.SetValue('S3除无头阿凡达之外所有R均本可掉落\r\n可附魔在头部和腿部防具上\r\n'
                                            '有比较高的爆抗与防御')
            elif afu == 2:
                self.dm_textCtrl67.SetValue('女族长克耶鲁\r\n大蛇:支配者的安息处\r\n火牛:地狱守门人\r\n'
                                            '德鲁伊:燃烧的神殿\r\n可附魔在所有防具上\r\n过渡必备但是比较减防御\r\n')
            elif afu == 3:
                self.dm_textCtrl67.SetValue('大蛇:支配者的安息处\r\n火牛:地狱守门人\r\n德鲁伊:燃烧的神殿\r\n'
                                            '可附魔在所有防具上\r\n单个调整使用,价值不大')
            elif afu == 4:
                self.dm_textCtrl67.SetValue('据说有茉莉花强化大法哦~~')
            elif afu == 5:
                self.dm_textCtrl67.SetValue('拥有暴击的\r\n极限堆暴击可以使用')
            elif afu == 6:
                self.dm_textCtrl67.SetValue('S3除无头阿凡达之外所有R均本可掉落\r\n可附魔在上衣防具上\r\n'
                                            '是一个很好的堆暴击方法\r\n削弱版:保护 附魔卷轴')
            elif afu == 7:
                self.dm_textCtrl67.SetValue('火牛:地狱守门人\r\n德鲁伊:燃烧的神殿\r\n可以代替烙印过渡使用'
                                            '\r\n增强版:烙印 附魔卷轴')
            elif afu == 8:
                self.dm_textCtrl67.SetValue('拥有很高的防御和爆抗\r\n可以附魔在所有防具上\r\n极限堆爆抗可以使用')
            elif afu == 9:
                self.dm_textCtrl67.SetValue('这个也没什么可以特别说的呀')
        elif fumo in head_list:
            afu = head_list.index(fumo)
            if afu > 13:
                afu = afu - 14
            elif (afu > 6) & (afu < 14):
                afu = afu - 7
            attack, defence, crit, balance, speed, resistance = enchant_weapon0(afu)
            self.dm_staticText87.SetLabelText('攻击:   %d' % attack)
            self.dm_staticText88.SetLabelText('防御:   %d' % defence)
            self.dm_staticText89.SetLabelText('暴击:   %d' % crit)
            self.dm_staticText90.SetLabelText('平衡:   %d' % balance)
            self.dm_staticText91.SetLabelText('攻速:   %d' % speed)
            self.dm_staticText92.SetLabelText('爆抗:   %d' % resistance)
            score = (crit + balance + speed) * 300 + resistance * 50 + attack + defence
            self.dm_staticText74.SetLabelText('其他:   评分:%d' % score)
            self.dm_textCtrl67.SetValue('')
            if afu == 0:
                self.dm_textCtrl67.SetValue('S3除无头阿凡达之外所有R均本可掉落\r\n可附魔在武器上\r\n高暴击\r\n'
                                            '增强版:混沌的 附魔卷轴')
            elif afu == 1:
                self.dm_textCtrl67.SetValue('S3除无头阿凡达之外所有R均本可掉落\r\n可附魔在武器上\r\n相对高攻速')
            elif afu == 2:
                self.dm_textCtrl67.SetValue('S3除无头阿凡达之外所有R均本可掉落\r\n可附魔在武器上\r\n高暴击\r\n'
                                            '不可以附魔在90级武器上')
            elif afu == 3:
                self.dm_textCtrl67.SetValue('找不到啦,我叫豆子,你呢？')
            elif afu == 4:
                self.dm_textCtrl67.SetValue('小光头:破败的莫乐班\r\n可附魔在武器上\r\n三围不错')
            elif afu == 5:
                self.dm_textCtrl67.SetValue('小光头:破败的莫乐班\r\n可附魔在武器上\r\n三围不错')
            elif afu == 6:
                self.dm_textCtrl67.SetValue('小光头:破败的莫乐班\r\n生死神:死神\r\n可附魔在武器上\r\n攻击不错')
        elif fumo in head_list1:
            afu = head_list1.index(fumo)
            if afu > 13:
                afu = afu - 14
            elif (afu > 6) & (afu < 14):
                afu = afu - 7
            attack, defence, crit, balance, speed, resistance = enchant_weapon1(afu)
            self.dm_staticText87.SetLabelText('攻击:   %d' % attack)
            self.dm_staticText88.SetLabelText('防御:   %d' % defence)
            self.dm_staticText89.SetLabelText('暴击:   %d' % crit)
            self.dm_staticText90.SetLabelText('平衡:   %d' % balance)
            self.dm_staticText91.SetLabelText('攻速:   %d' % speed)
            self.dm_staticText92.SetLabelText('爆抗:   %d' % resistance)
            score = (crit + balance + speed) * 300 + resistance * 50 + attack + defence
            self.dm_staticText74.SetLabelText('其他:   评分:%d' % score)
            self.dm_textCtrl67.SetValue('')
            if afu == 0:
                self.dm_textCtrl67.SetValue('S3除无头阿凡达之外所有R均本可掉落\r\n可附魔在武器上\r\n相对高攻速\r\n')
            elif afu == 1:
                self.dm_textCtrl67.SetValue('S3除无头阿凡达之外所有R均本可掉落\r\n可附魔在武器上\r\n高暴击')
            elif afu == 2:
                self.dm_textCtrl67.SetValue('坦克:奇异的机器\r\n扔肥皂:身处深渊\r\n火牛:地狱守门人\r\n'
                                            '德鲁伊:燃烧的神殿\r\n过渡可用,三围较高')
            elif afu == 3:
                self.dm_textCtrl67.SetValue('大蛇:支配者的安息处\r\n坦克:奇异的机器\r\n扔肥皂:身处深渊\r\n'
                                            '火牛:地狱守门人\r\n德鲁伊:燃烧的神殿\r\n过渡可用,三围较高')
            elif afu == 4:
                self.dm_textCtrl67.SetValue('坦克:奇异的机器\r\n扔肥皂:身处深渊\r\n'
                                            '火牛:地狱守门人\r\n德鲁伊:燃烧的神殿\r\n过渡可用,攻击还不错')
            elif afu == 5:
                self.dm_textCtrl67.SetValue('找不到啦\r\n用这个有什么意义呢\r\n我是谁\r\n我从哪儿来\r\n我要做什么')
            elif afu == 6:
                self.dm_textCtrl67.SetValue('我只是一个萌新啊')
        else:
            self.dm_staticText87.SetLabelText('                    您')
            self.dm_staticText88.SetLabelText('                    可')
            self.dm_staticText89.SetLabelText('                    能')
            self.dm_staticText90.SetLabelText('                    输')
            self.dm_staticText91.SetLabelText('                    入')
            self.dm_staticText92.SetLabelText('                    错')
            self.dm_staticText74.SetLabelText('                    了')
            self.dm_button15.Enable(False)
            self.dm_textCtrl66.Enable(False)
            JustJoke()

            event.Skip()

    def updatejoke(self, msg2):
        self.dm_textCtrl67.SetValue(msg2)

    def enable_find(self, msg3):
        self.dm_button15.Enable(True)
        self.dm_textCtrl66.Enable(True)

    def button11(self, event):
        value_fumo = int(self.dm_textCtrl55.GetValue())
        value_debris = int(self.dm_textCtrl56.GetValue())
        value_gold = int(self.dm_textCtrl57.GetValue())
        count_a = round(-4*value_debris/(value_debris - 10*value_gold/3 - value_fumo))
        value_loss = round(value_fumo + value_gold*5 - value_debris - value_gold*5/3)
        self.dm_staticText82.SetLabelText('------------------------------------\r\n'
                                          '一次失败您将损失%dW的金币' % value_loss)
        self.dm_staticText80.SetLabelText('------------------------------------\r\n'
                                          '%d次附魔失败之后将不如直接购买碎片' % count_a)
        event.Skip()


# class MyPanel5(wx.Panel):
#     global data_equipment
#     global data_inital
#     data_equipment = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#     data_inital = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#
#     def __init__(self, parent):
#         wx.Panel.__init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(712, 510),
#                           style=wx.TAB_TRAVERSAL)
#
#         bSizer2 = wx.BoxSizer(wx.HORIZONTAL)
#
#         sbSizer4 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"装备栏"), wx.HORIZONTAL)
#
#         gSizer3 = wx.GridSizer(0, 3, 0, 0)
#
#         self.att_bpButton3 = wx.BitmapButton(sbSizer4.GetStaticBox(), wx.ID_ANY,
#                                              wx.Bitmap(u"C:\\Users\\lyf18\\Pictures\\work_UI\\btn_game_start.bmp",
#                                              wx.BITMAP_TYPE_ANY), wx.DefaultPosition, wx.DefaultSize,
#                                              wx.BU_AUTODRAW)
#         gSizer3.Add(self.att_bpButton3, 0, wx.ALL, 5)
#
#         self.att_bpButton4 = wx.BitmapButton(sbSizer4.GetStaticBox(), wx.ID_ANY,
#                                              wx.Bitmap(u"C:\\Users\\lyf18\\Pictures\\work_UI\\btn_game_start.bmp",
#                                              wx.BITMAP_TYPE_ANY), wx.DefaultPosition, wx.DefaultSize,
#                                              wx.BU_AUTODRAW)
#         gSizer3.Add(self.att_bpButton4, 0, wx.ALL, 5)
#
#         self.att_bpButton5 = wx.BitmapButton(sbSizer4.GetStaticBox(), wx.ID_ANY,
#                                            wx.Bitmap(u"C:\\Users\\lyf18\\Pictures\\work_UI\\btn_game_start.bmp",
#                                                      wx.BITMAP_TYPE_ANY), wx.DefaultPosition, wx.DefaultSize,
#                                            wx.BU_AUTODRAW)
#         gSizer3.Add(self.att_bpButton5, 0, wx.ALL, 5)
#
#         self.att_bpButton6 = wx.BitmapButton(sbSizer4.GetStaticBox(), wx.ID_ANY,
#                                            wx.Bitmap(u"C:\\Users\\lyf18\\Pictures\\work_UI\\btn_game_start.bmp",
#                                                      wx.BITMAP_TYPE_ANY), wx.DefaultPosition, wx.DefaultSize,
#                                            wx.BU_AUTODRAW)
#         gSizer3.Add(self.att_bpButton6, 0, wx.ALL, 5)
#
#         self.att_bpButton7 = wx.BitmapButton(sbSizer4.GetStaticBox(), wx.ID_ANY,
#                                            wx.Bitmap(u"C:\\Users\\lyf18\\Pictures\\work_UI\\btn_game_start.bmp",
#                                                      wx.BITMAP_TYPE_ANY), wx.DefaultPosition, wx.DefaultSize,
#                                            wx.BU_AUTODRAW)
#         gSizer3.Add(self.att_bpButton7, 0, wx.ALL, 5)
#
#         self.att_bpButton8 = wx.BitmapButton(sbSizer4.GetStaticBox(), wx.ID_ANY,
#                                            wx.Bitmap(u"C:\\Users\\lyf18\\Pictures\\work_UI\\btn_game_start.bmp",
#                                                      wx.BITMAP_TYPE_ANY), wx.DefaultPosition, wx.DefaultSize,
#                                            wx.BU_AUTODRAW)
#         gSizer3.Add(self.att_bpButton8, 0, wx.ALL, 5)
#
#         self.att_bpButton9 = wx.BitmapButton(sbSizer4.GetStaticBox(), wx.ID_ANY,
#                                            wx.Bitmap(u"C:\\Users\\lyf18\\Pictures\\work_UI\\btn_game_start.bmp",
#                                                      wx.BITMAP_TYPE_ANY), wx.DefaultPosition, wx.DefaultSize,
#                                            wx.BU_AUTODRAW)
#         gSizer3.Add(self.att_bpButton9, 0, wx.ALL, 5)
#
#         self.att_bpButton10 = wx.BitmapButton(sbSizer4.GetStaticBox(), wx.ID_ANY,
#                                             wx.Bitmap(u"C:\\Users\\lyf18\\Pictures\\work_UI\\btn_game_start.bmp",
#                                                       wx.BITMAP_TYPE_ANY), wx.DefaultPosition, wx.DefaultSize,
#                                             wx.BU_AUTODRAW)
#         gSizer3.Add(self.att_bpButton10, 0, wx.ALL, 5)
#
#         self.att_bpButton11 = wx.BitmapButton(sbSizer4.GetStaticBox(), wx.ID_ANY,
#                                             wx.Bitmap(u"C:\\Users\\lyf18\\Pictures\\work_UI\\btn_game_start.bmp",
#                                                       wx.BITMAP_TYPE_ANY), wx.DefaultPosition, wx.DefaultSize,
#                                             wx.BU_AUTODRAW)
#         gSizer3.Add(self.att_bpButton11, 0, wx.ALL, 5)
#
#         self.att_bpButton12 = wx.BitmapButton(sbSizer4.GetStaticBox(), wx.ID_ANY,
#                                             wx.Bitmap(u"C:\\Users\\lyf18\\Pictures\\work_UI\\btn_game_start.bmp",
#                                                       wx.BITMAP_TYPE_ANY), wx.DefaultPosition, wx.DefaultSize,
#                                             wx.BU_AUTODRAW)
#         gSizer3.Add(self.att_bpButton12, 0, wx.ALL, 5)
#
#         self.att_bpButton13 = wx.BitmapButton(sbSizer4.GetStaticBox(), wx.ID_ANY,
#                                             wx.Bitmap(u"C:\\Users\\lyf18\\Pictures\\work_UI\\btn_game_start.bmp",
#                                                       wx.BITMAP_TYPE_ANY), wx.DefaultPosition, wx.DefaultSize,
#                                             wx.BU_AUTODRAW)
#         gSizer3.Add(self.att_bpButton13, 0, wx.ALL, 5)
#
#         self.att_bpButton14 = wx.BitmapButton(sbSizer4.GetStaticBox(), wx.ID_ANY,
#                                             wx.Bitmap(u"C:\\Users\\lyf18\\Pictures\\work_UI\\btn_game_start.bmp",
#                                                       wx.BITMAP_TYPE_ANY), wx.DefaultPosition, wx.DefaultSize,
#                                             wx.BU_AUTODRAW)
#         gSizer3.Add(self.att_bpButton14, 0, wx.ALL, 5)
#
#         self.att_bpButton15 = wx.BitmapButton(sbSizer4.GetStaticBox(), wx.ID_ANY,
#                                             wx.Bitmap(u"C:\\Users\\lyf18\\Pictures\\work_UI\\btn_game_start.bmp",
#                                                       wx.BITMAP_TYPE_ANY), wx.DefaultPosition, wx.DefaultSize,
#                                             wx.BU_AUTODRAW)
#         gSizer3.Add(self.att_bpButton15, 0, wx.ALL, 5)
#
#         self.att_bpButton16 = wx.BitmapButton(sbSizer4.GetStaticBox(), wx.ID_ANY,
#                                             wx.Bitmap(u"C:\\Users\\lyf18\\Pictures\\work_UI\\btn_game_start.bmp",
#                                                       wx.BITMAP_TYPE_ANY), wx.DefaultPosition, wx.DefaultSize,
#                                             wx.BU_AUTODRAW)
#         gSizer3.Add(self.att_bpButton16, 0, wx.ALL, 5)
#
#         self.att_bpButton17 = wx.BitmapButton(sbSizer4.GetStaticBox(), wx.ID_ANY,
#                                             wx.Bitmap(u"C:\\Users\\lyf18\\Pictures\\work_UI\\btn_game_start.bmp",
#                                                       wx.BITMAP_TYPE_ANY), wx.DefaultPosition, wx.DefaultSize,
#                                             wx.BU_AUTODRAW)
#         gSizer3.Add(self.att_bpButton17, 0, wx.ALL, 5)
#
#         sbSizer4.Add(gSizer3, 1, wx.EXPAND, 5)
#
#         bSizer2.Add(sbSizer4, 1, wx.EXPAND, 5)
#
#         sbSizer6 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"属性栏"), wx.VERTICAL)
#
#         sbSizer7 = wx.StaticBoxSizer(wx.StaticBox(sbSizer6.GetStaticBox(), wx.ID_ANY, u"空白属性"), wx.VERTICAL)
#
#         gbSizer24 = wx.GridBagSizer(0, 0)
#         gbSizer24.SetFlexibleDirection(wx.BOTH)
#         gbSizer24.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)
#
#         self.att_textCtrl228 = wx.TextCtrl(sbSizer7.GetStaticBox(), wx.ID_ANY, u"力量:", wx.DefaultPosition,
#                                          wx.DefaultSize, 0)
#         gbSizer24.Add(self.att_textCtrl228, wx.GBPosition(0, 0), wx.GBSpan(1, 1), wx.ALL, 5)
#
#         self.att_textCtrl229 = wx.TextCtrl(sbSizer7.GetStaticBox(), wx.ID_ANY, u"攻击力:", wx.DefaultPosition,
#                                          wx.DefaultSize, 0)
#         gbSizer24.Add(self.att_textCtrl229, wx.GBPosition(0, 1), wx.GBSpan(1, 1), wx.ALL, 5)
#
#         self.att_textCtrl230 = wx.TextCtrl(sbSizer7.GetStaticBox(), wx.ID_ANY, u"敏捷:", wx.DefaultPosition,
#                                          wx.DefaultSize, 0)
#         gbSizer24.Add(self.att_textCtrl230, wx.GBPosition(1, 0), wx.GBSpan(1, 1), wx.ALL, 5)
#
#         self.att_textCtrl233 = wx.TextCtrl(sbSizer7.GetStaticBox(), wx.ID_ANY, u"防御力:", wx.DefaultPosition,
#                                          wx.DefaultSize, 0)
#         gbSizer24.Add(self.att_textCtrl233, wx.GBPosition(1, 1), wx.GBSpan(1, 1), wx.ALL, 5)
#
#         self.att_textCtrl234 = wx.TextCtrl(sbSizer7.GetStaticBox(), wx.ID_ANY, u"智力:", wx.DefaultPosition,
#                                          wx.DefaultSize, 0)
#         gbSizer24.Add(self.att_textCtrl234, wx.GBPosition(2, 0), wx.GBSpan(1, 1), wx.ALL, 5)
#
#         self.att_textCtrl235 = wx.TextCtrl(sbSizer7.GetStaticBox(), wx.ID_ANY, u"暴击:", wx.DefaultPosition,
#                                          wx.DefaultSize, 0)
#         gbSizer24.Add(self.att_textCtrl235, wx.GBPosition(2, 1), wx.GBSpan(1, 1), wx.ALL, 5)
#
#         self.att_textCtrl236 = wx.TextCtrl(sbSizer7.GetStaticBox(), wx.ID_ANY, u"意志:", wx.DefaultPosition,
#                                          wx.DefaultSize, 0)
#         gbSizer24.Add(self.att_textCtrl236, wx.GBPosition(3, 0), wx.GBSpan(1, 1), wx.ALL, 5)
#
#         self.att_textCtrl237 = wx.TextCtrl(sbSizer7.GetStaticBox(), wx.ID_ANY, u"平衡:", wx.DefaultPosition,
#                                          wx.DefaultSize, 0)
#         gbSizer24.Add(self.att_textCtrl237, wx.GBPosition(3, 1), wx.GBSpan(1, 1), wx.ALL, 5)
#
#         self.att_textCtrl238 = wx.TextCtrl(sbSizer7.GetStaticBox(), wx.ID_ANY, u"攻速:", wx.DefaultPosition,
#                                          wx.DefaultSize, 0)
#         gbSizer24.Add(self.att_textCtrl238, wx.GBPosition(4, 0), wx.GBSpan(1, 1), wx.ALL, 5)
#
#         self.att_textCtrl239 = wx.TextCtrl(sbSizer7.GetStaticBox(), wx.ID_ANY, u"爆抗:", wx.DefaultPosition,
#                                          wx.DefaultSize, 0)
#         gbSizer24.Add(self.att_textCtrl239, wx.GBPosition(4, 1), wx.GBSpan(1, 1), wx.ALL, 5)
#
#         self.att_textCtrl240 = wx.TextCtrl(sbSizer7.GetStaticBox(), wx.ID_ANY, u"解禁:", wx.DefaultPosition,
#                                            wx.DefaultSize, 0)
#         gbSizer24.Add(self.att_textCtrl240, wx.GBPosition(5, 0), wx.GBSpan(1, 1), wx.ALL, 5)
#
#         self.att_textCtrl241 = wx.TextCtrl(sbSizer7.GetStaticBox(), wx.ID_ANY, u"追伤:", wx.DefaultPosition,
#                                            wx.DefaultSize, 0)
#         gbSizer24.Add(self.att_textCtrl241, wx.GBPosition(5, 1), wx.GBSpan(1, 1), wx.ALL, 5)
#
#         self.att_textCtrl260 = wx.TextCtrl(sbSizer7.GetStaticBox(), wx.ID_ANY, u"等级:", wx.DefaultPosition,
#                                            wx.DefaultSize, 0)
#         gbSizer24.Add(self.att_textCtrl260, wx.GBPosition(0, 2), wx.GBSpan(1, 1), wx.ALL, 5)
#
#         m_choice115Choices = [u"物理职业", u"魔法职业"]
#         self.att_choice115 = wx.Choice(sbSizer7.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
#                                      m_choice115Choices, 0)
#         self.att_choice115.SetSelection(0)
#         gbSizer24.Add(self.att_choice115, wx.GBPosition(1, 2), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)
#
#         self.att_button12 = wx.Button(sbSizer7.GetStaticBox(), wx.ID_ANY, u"确定", wx.DefaultPosition, wx.DefaultSize, 0)
#         gbSizer24.Add(self.att_button12, wx.GBPosition(2, 2), wx.GBSpan(3, 1),
#                       wx.ALL | wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)
#
#         sbSizer7.Add(gbSizer24, 1, wx.EXPAND, 5)
#
#         sbSizer6.Add(sbSizer7, 1, wx.EXPAND, 5)
#
#         sbSizer8 = wx.StaticBoxSizer(wx.StaticBox(sbSizer6.GetStaticBox(), wx.ID_ANY, u"总属性"), wx.VERTICAL)
#
#         gbSizer241 = wx.GridBagSizer(0, 0)
#         gbSizer241.SetFlexibleDirection(wx.BOTH)
#         gbSizer241.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)
#
#         self.att_textCtrl2281 = wx.TextCtrl(sbSizer8.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
#                                           wx.DefaultSize, wx.TE_READONLY)
#         gbSizer241.Add(self.att_textCtrl2281, wx.GBPosition(0, 0), wx.GBSpan(1, 1), wx.ALL, 5)
#
#         self.att_textCtrl2291 = wx.TextCtrl(sbSizer8.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
#                                           wx.DefaultSize, wx.TE_READONLY)
#         gbSizer241.Add(self.att_textCtrl2291, wx.GBPosition(0, 1), wx.GBSpan(1, 1), wx.ALL, 5)
#
#         self.att_textCtrl2301 = wx.TextCtrl(sbSizer8.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
#                                           wx.DefaultSize, wx.TE_READONLY)
#         gbSizer241.Add(self.att_textCtrl2301, wx.GBPosition(1, 0), wx.GBSpan(1, 1), wx.ALL, 5)
#
#         self.att_textCtrl2331 = wx.TextCtrl(sbSizer8.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
#                                           wx.DefaultSize, wx.TE_READONLY)
#         gbSizer241.Add(self.att_textCtrl2331, wx.GBPosition(1, 1), wx.GBSpan(1, 1), wx.ALL, 5)
#
#         self.att_textCtrl2341 = wx.TextCtrl(sbSizer8.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
#                                           wx.DefaultSize, wx.TE_READONLY)
#         gbSizer241.Add(self.att_textCtrl2341, wx.GBPosition(2, 0), wx.GBSpan(1, 1), wx.ALL, 5)
#
#         self.att_textCtrl2351 = wx.TextCtrl(sbSizer8.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
#                                           wx.DefaultSize, wx.TE_READONLY)
#         gbSizer241.Add(self.att_textCtrl2351, wx.GBPosition(2, 1), wx.GBSpan(1, 1), wx.ALL, 5)
#
#         self.att_textCtrl2361 = wx.TextCtrl(sbSizer8.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
#                                           wx.DefaultSize, wx.TE_READONLY)
#         gbSizer241.Add(self.att_textCtrl2361, wx.GBPosition(3, 0), wx.GBSpan(1, 1), wx.ALL, 5)
#
#         self.att_textCtrl2371 = wx.TextCtrl(sbSizer8.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
#                                           wx.DefaultSize, wx.TE_READONLY)
#         gbSizer241.Add(self.att_textCtrl2371, wx.GBPosition(3, 1), wx.GBSpan(1, 1), wx.ALL, 5)
#
#         self.att_textCtrl2381 = wx.TextCtrl(sbSizer8.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
#                                           wx.DefaultSize, wx.TE_READONLY)
#         gbSizer241.Add(self.att_textCtrl2381, wx.GBPosition(4, 0), wx.GBSpan(1, 1), wx.ALL, 5)
#
#         self.att_textCtrl2391 = wx.TextCtrl(sbSizer8.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
#                                           wx.DefaultSize, wx.TE_READONLY)
#         gbSizer241.Add(self.att_textCtrl2391, wx.GBPosition(4, 1), wx.GBSpan(1, 1), wx.ALL, 5)
#
#         self.att_textCtrl2401 = wx.TextCtrl(sbSizer8.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
#                                             wx.DefaultSize, wx.TE_READONLY)
#         gbSizer241.Add(self.att_textCtrl2401, wx.GBPosition(5, 0), wx.GBSpan(1, 1), wx.ALL, 5)
#
#         self.att_textCtrl2411 = wx.TextCtrl(sbSizer8.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
#                                             wx.DefaultSize, wx.TE_READONLY)
#         gbSizer241.Add(self.att_textCtrl2411, wx.GBPosition(5, 1), wx.GBSpan(1, 1), wx.ALL, 5)
#
#         sbSizer8.Add(gbSizer241, 1, wx.EXPAND, 5)
#
#         sbSizer6.Add(sbSizer8, 1, wx.EXPAND, 5)
#
#         bSizer2.Add(sbSizer6, 1, wx.EXPAND, 5)
#
#         self.SetSizer(bSizer2)
#         self.Layout()
#
#         # Connect Events
#         self.att_bpButton6.Bind(wx.EVT_BUTTON, self.find_weapon)
#         self.att_bpButton4.Bind(wx.EVT_BUTTON, self.find_head)
#         self.att_bpButton7.Bind(wx.EVT_BUTTON, self.find_coat)
#         self.att_bpButton8.Bind(wx.EVT_BUTTON, self.find_hand)
#         self.att_bpButton10.Bind(wx.EVT_BUTTON, self.find_leg)
#         self.att_bpButton13.Bind(wx.EVT_BUTTON, self.find_foot)
#         self.att_bpButton9.Bind(wx.EVT_BUTTON, self.find_belt)
#         self.att_bpButton11.Bind(wx.EVT_BUTTON, self.find_brooch)
#         self.att_bpButton3.Bind(wx.EVT_BUTTON, self.find_earring)
#         self.att_bpButton5.Bind(wx.EVT_BUTTON, self.find_store)
#         self.att_bpButton12.Bind(wx.EVT_BUTTON, self.find_ring1)
#         self.att_bpButton14.Bind(wx.EVT_BUTTON, self.find_ring2)
#         self.att_bpButton15.Bind(wx.EVT_BUTTON, self.find_bracelet1)
#         self.att_bpButton16.Bind(wx.EVT_BUTTON, self.find_craft)
#         self.att_bpButton17.Bind(wx.EVT_BUTTON, self.find_DeputyW)
#         self.att_choice115.Bind(wx.EVT_CHOICE, self.update_choice)
#         self.att_button12.Bind(wx.EVT_BUTTON, self.getinit)
#         self.att_choice115.Bind(wx.EVT_CHOICE, self.getinit)
#
#         # create a pub receiver
#         pub.subscribe(self.equipment, "equipment")
#         DataThread()
#
#     def __del__(self):
#         pass
#
#     # Virtual event handlers, overide them in your derived class
#     def find_weapon(self, event):
#         Weapon(self, "武器").ShowModal()
#         event.Skip()
#
#     def find_head(self, event):
#         a = Head(self, "头部防具").ShowModal()
#         event.Skip()
#
#     def find_coat(self, event):
#         a = Coat(self, "上衣防具").ShowModal()
#         event.Skip()
#
#     def find_hand(self, event):
#         a = Hand(self, "手部防具").ShowModal()
#         event.Skip()
#
#     def find_leg(self, event):
#         a = Leg(self, "腿部防具").ShowModal()
#         event.Skip()
#
#     def find_foot(self, event):
#         a = Foot(self, "脚部防具").ShowModal()
#         event.Skip()
#
#     def find_belt(self, event):
#         a = Belt(self, "腰带").ShowModal()
#         event.Skip()
#
#     def find_brooch(self, event):
#         a = Brooch(self, "胸针").ShowModal()
#         event.Skip()
#
#     def find_earring(self, event):
#         a = Earring(self, "耳环").ShowModal()
#         event.Skip()
#
#     def find_store(self, event):
#         a = Store(self, "商城物品").ShowModal()
#         event.Skip()
#
#     def find_ring1(self, event):
#         a = Ring1(self, "戒指1").ShowModal()
#         event.Skip()
#
#     def find_ring2(self, event):
#         a = Ring2(self, "戒指2").ShowModal()
#         event.Skip()
#
#     def find_bracelet1(self, event):
#         a = Bracelet1(self, "手镯1").ShowModal()
#         event.Skip()
#
#     def find_craft(self, event):
#         a = Craft(self).ShowModal()
#         event.Skip()
#
#     def find_DeputyW(self, event):
#         a = DeputyW(self, "副手武器").ShowModal()
#         event.Skip()
#
#     def getinit(self, event):
#         global data_inital
#         datainital = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#         datainital[0] = intplus(self.att_textCtrl229.GetValue())
#         datainital[1] = intplus(self.att_textCtrl237.GetValue())
#         datainital[2] = intplus(self.att_textCtrl235.GetValue())
#         datainital[3] = intplus(self.att_textCtrl238.GetValue())
#         datainital[4] = intplus(self.att_textCtrl241.GetValue())
#         datainital[5] = intplus(self.att_textCtrl228.GetValue())
#         datainital[6] = intplus(self.att_textCtrl230.GetValue())
#         datainital[7] = intplus(self.att_textCtrl234.GetValue())
#         datainital[8] = intplus(self.att_textCtrl236.GetValue())
#         datainital[9] = intplus(self.att_textCtrl240.GetValue())
#         datainital[10] = intplus(self.att_textCtrl239.GetValue())
#         datainital[11] = intplus(self.att_textCtrl233.GetValue())
#         if self.att_choice115.GetSelection() == 0:
#             datainital[0] = datainital[0] - math.floor(datainital[5] * 2.7)
#         else:
#             datainital[0] = datainital[0] - math.floor(datainital[7] * 2)
#         datainital[11] = datainital[11] - math.floor(datainital[6]/2)
#         datainital[2] = datainital[2] - math.floor(datainital[8]/2000)
#         data_inital = datainital
#         DataThread()
#         event.Skip()
#
#     def update_choice(self, event):
#         DataThread()
#         event.Skip()
#
#     def equipment(self, msge):
#         self.att_textCtrl2281.SetValue(u"力量:" + str(msge[5]))
#         if self.att_choice115.GetSelection() == 0:
#             self.att_textCtrl2291.SetValue(u"攻击力:" + str(msge[0] + math.floor(msge[5] * 2.7)))
#         else:
#             self.att_textCtrl2291.SetValue(u"攻击力:" + str(msge[0] + math.floor(msge[7] * 2)))
#         self.att_textCtrl2331.SetValue(u"防御力:" + str(msge[11] + math.floor(msge[6]/2)))
#         self.att_textCtrl2371.SetValue(u"平衡:" + str(msge[1]))
#         self.att_textCtrl2351.SetValue(u"暴击:" + str(msge[2] + math.floor(msge[8]/2000)))
#         self.att_textCtrl2381.SetValue(u"攻速:" + str(msge[3]))
#         self.att_textCtrl2411.SetValue(u"追伤:" + str(msge[4]))
#         self.att_textCtrl2391.SetValue(u"爆抗:" + str(msge[10]))
#         self.att_textCtrl2301.SetValue(u"敏捷:" + str(msge[6]))
#         self.att_textCtrl2341.SetValue(u"智力:" + str(msge[7]))
#         self.att_textCtrl2361.SetValue(u"意志:" + str(msge[8]))
#         self.att_textCtrl2401.SetValue(u"解禁:" + str(msge[9]))
#

class Weapon(wx.Dialog):
    global weapon_data
    global weapon_att
    weapon_data = [[0, '', '', ''],
                   [1, '', '', ''],
                   [1, '', '', '', '', '', ''],
                   [1, '', '', ''],
                   [1, '', '', '', '', '', ''],
                   [9, ''],
                   ['', 8, 7]]
    weapon_att = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    # weapon_att 分别是[攻击力，平衡，暴击，攻速，追伤，力量，敏捷，智力，意志，解禁，爆抗]

    def __init__(self, parent, title):
        super(Weapon, self).__init__(parent, title=title, size=(600, 450))

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        gbSizer9 = wx.GridBagSizer(0, 0)
        gbSizer9.SetFlexibleDirection(wx.BOTH)
        gbSizer9.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        wm_choice57Choices = [u"橙色核心", u"紫色核心"]
        self.weapon_core = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wm_choice57Choices, 0)
        self.weapon_core.SetSelection(weapon_data[0][0])
        gbSizer9.Add(self.weapon_core, wx.GBPosition(0, 0), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        self.wm_textCtrl58 = wx.TextCtrl(self, wx.ID_ANY, weapon_data[0][1], wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer9.Add(self.wm_textCtrl58, wx.GBPosition(0, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        self.wm_textCtrl59 = wx.TextCtrl(self, wx.ID_ANY, weapon_data[0][2], wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer9.Add(self.wm_textCtrl59, wx.GBPosition(0, 2), wx.GBSpan(1, 1), wx.ALL, 5)

        self.wm_textCtrl81 = wx.TextCtrl(self, wx.ID_ANY, weapon_data[0][3], wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer9.Add(self.wm_textCtrl81, wx.GBPosition(0, 3), wx.GBSpan(1, 1), wx.ALL, 5)

        wm_choice58Choices = [u"橙色锐利", u"紫色锐利"]
        self.weapon_sharp = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wm_choice58Choices, 0)
        self.weapon_sharp.SetSelection(weapon_data[1][0])
        gbSizer9.Add(self.weapon_sharp, wx.GBPosition(1, 0), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        self.wm_textCtrl61 = wx.TextCtrl(self, wx.ID_ANY, weapon_data[1][1], wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer9.Add(self.wm_textCtrl61, wx.GBPosition(1, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        self.wm_textCtrl62 = wx.TextCtrl(self, wx.ID_ANY, weapon_data[1][2], wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer9.Add(self.wm_textCtrl62, wx.GBPosition(1, 2), wx.GBSpan(1, 1), wx.ALL, 5)

        self.wm_textCtrl82 = wx.TextCtrl(self, wx.ID_ANY, weapon_data[1][3], wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer9.Add(self.wm_textCtrl82, wx.GBPosition(1, 3), wx.GBSpan(1, 1), wx.ALL, 5)

        wm_choice59Choices = [u"橙色稳定", u"紫色稳定"]
        self.weapon_stable = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wm_choice59Choices, 0)
        self.weapon_stable.SetSelection(weapon_data[2][0])
        gbSizer9.Add(self.weapon_stable, wx.GBPosition(2, 0), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        self.wm_textCtrl66 = wx.TextCtrl(self, wx.ID_ANY, weapon_data[2][1], wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer9.Add(self.wm_textCtrl66, wx.GBPosition(2, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        self.wm_textCtrl67 = wx.TextCtrl(self, wx.ID_ANY, weapon_data[2][2], wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer9.Add(self.wm_textCtrl67, wx.GBPosition(2, 2), wx.GBSpan(1, 1), wx.ALL, 5)

        self.wm_textCtrl68 = wx.TextCtrl(self, wx.ID_ANY, weapon_data[2][3], wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer9.Add(self.wm_textCtrl68, wx.GBPosition(2, 3), wx.GBSpan(1, 1), wx.ALL, 5)

        self.wm_textCtrl71 = wx.TextCtrl(self, wx.ID_ANY, weapon_data[2][4], wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer9.Add(self.wm_textCtrl71, wx.GBPosition(3, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        self.wm_textCtrl72 = wx.TextCtrl(self, wx.ID_ANY, weapon_data[2][5], wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer9.Add(self.wm_textCtrl72, wx.GBPosition(3, 2), wx.GBSpan(1, 1), wx.ALL, 5)

        self.wm_textCtrl83 = wx.TextCtrl(self, wx.ID_ANY, weapon_data[2][6], wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer9.Add(self.wm_textCtrl83, wx.GBPosition(3, 3), wx.GBSpan(1, 1), wx.ALL, 5)

        wm_choice60Choices = [u"橙色轻盈", u"紫色轻盈"]
        self.weapon_light = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wm_choice60Choices, 0)
        self.weapon_light.SetSelection(weapon_data[3][0])
        gbSizer9.Add(self.weapon_light, wx.GBPosition(4, 0), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        self.wm_textCtrl73 = wx.TextCtrl(self, wx.ID_ANY, weapon_data[3][1], wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer9.Add(self.wm_textCtrl73, wx.GBPosition(4, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        self.wm_textCtrl74 = wx.TextCtrl(self, wx.ID_ANY, weapon_data[3][2], wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer9.Add(self.wm_textCtrl74, wx.GBPosition(4, 2), wx.GBSpan(1, 1), wx.ALL, 5)

        self.wm_textCtrl84 = wx.TextCtrl(self, wx.ID_ANY, weapon_data[3][3], wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer9.Add(self.wm_textCtrl84, wx.GBPosition(4, 3), wx.GBSpan(1, 1), wx.ALL, 5)

        wm_choice61Choices = [u"橙色完美", u"紫色完美"]
        self.weapon_perfect = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wm_choice61Choices, 0)
        self.weapon_perfect.SetSelection(weapon_data[4][0])
        gbSizer9.Add(self.weapon_perfect, wx.GBPosition(5, 0), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        self.wm_textCtrl75 = wx.TextCtrl(self, wx.ID_ANY, weapon_data[4][1], wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer9.Add(self.wm_textCtrl75, wx.GBPosition(5, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        self.wm_textCtrl76 = wx.TextCtrl(self, wx.ID_ANY, weapon_data[4][2], wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer9.Add(self.wm_textCtrl76, wx.GBPosition(5, 2), wx.GBSpan(1, 1), wx.ALL, 5)

        self.wm_textCtrl77 = wx.TextCtrl(self, wx.ID_ANY, weapon_data[4][3], wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer9.Add(self.wm_textCtrl77, wx.GBPosition(5, 3), wx.GBSpan(1, 1), wx.ALL, 5)

        self.wm_textCtrl78 = wx.TextCtrl(self, wx.ID_ANY, weapon_data[4][4], wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer9.Add(self.wm_textCtrl78, wx.GBPosition(6, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        self.wm_textCtrl79 = wx.TextCtrl(self, wx.ID_ANY, weapon_data[4][5], wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer9.Add(self.wm_textCtrl79, wx.GBPosition(6, 2), wx.GBSpan(1, 1), wx.ALL, 5)

        self.wm_textCtrl85 = wx.TextCtrl(self, wx.ID_ANY, weapon_data[4][6], wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer9.Add(self.wm_textCtrl85, wx.GBPosition(6, 3), wx.GBSpan(1, 1), wx.ALL, 5)

        wm_choice62Choices = [u"暴击", u"平衡", u"攻速", u"攻击力", u"防御", u"力量", u"敏捷", u"智力", u"意志", u"无"]
        self.weapon_add = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wm_choice62Choices, 0)
        self.weapon_add.SetSelection(weapon_data[5][0])
        gbSizer9.Add(self.weapon_add, wx.GBPosition(7, 0), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        self.wm_textCtrl80 = wx.TextCtrl(self, wx.ID_ANY, weapon_data[5][1], wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer9.Add(self.wm_textCtrl80, wx.GBPosition(7, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        wm_choice64Choices = [u"不义的", u"正义的", u"混沌的", u"曙光般的", u"富饶的", u"确凿的", u"猎豹", wx.EmptyString]
        self.weapon_enchant0 = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wm_choice64Choices, 0)
        self.weapon_enchant0.SetSelection(weapon_data[6][1])
        gbSizer9.Add(self.weapon_enchant0, wx.GBPosition(8, 2), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        self.wm_staticText85 = wx.StaticText(self, wx.ID_ANY, u"强化等级", wx.DefaultPosition, wx.DefaultSize, 0)
        self.wm_staticText85.Wrap(-1)
        gbSizer9.Add(self.wm_staticText85, wx.GBPosition(8, 0), wx.GBSpan(1, 1),
                     wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.wm_textCtrl86 = wx.TextCtrl(self, wx.ID_ANY, weapon_data[6][0], wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer9.Add(self.wm_textCtrl86, wx.GBPosition(8, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        wm_choice65Choices = [u"审判", u"断罪", u"花瓣", u"勇猛", u"天诛", u"野心", u"挑战", wx.EmptyString]
        self.weapon_enchant1 = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wm_choice65Choices, 0)
        self.weapon_enchant1.SetSelection(weapon_data[6][2])
        gbSizer9.Add(self.weapon_enchant1, wx.GBPosition(8, 3), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        self.wm_staticText173 = wx.StaticText(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                              wx.ALIGN_CENTRE)
        self.wm_staticText173.Wrap(-1)
        gbSizer9.Add(self.wm_staticText173, wx.GBPosition(9, 0), wx.GBSpan(2, 4), wx.ALL | wx.EXPAND, 5)

        wm_sdbSizer2 = wx.StdDialogButtonSizer()
        self.wm_sdbSizer2OK = wx.Button(self, wx.ID_OK)
        wm_sdbSizer2.AddButton(self.wm_sdbSizer2OK)
        self.wm_sdbSizer2Cancel = wx.Button(self, wx.ID_CANCEL)
        wm_sdbSizer2.AddButton(self.wm_sdbSizer2Cancel)
        wm_sdbSizer2.Realize()
        gbSizer9.Add(wm_sdbSizer2, wx.GBPosition(12, 2), wx.GBSpan(1, 2), wx.EXPAND, 5)

        self.weapon_core.Bind(wx.EVT_CHOICE, self.core_weapon)
        self.weapon_light.Bind(wx.EVT_CHOICE, self.light_weapon)
        self.weapon_perfect.Bind(wx.EVT_CHOICE, self.perfect_weapon)
        self.weapon_sharp.Bind(wx.EVT_CHOICE, self.sharp_weapon)
        self.weapon_stable.Bind(wx.EVT_CHOICE, self.stable_weapon)
        self.weapon_add.Bind(wx.EVT_CHOICE, self.update_att)
        self.wm_sdbSizer2OK.Bind(wx.EVT_BUTTON, self.dateupdate)
        self.wm_textCtrl58.Bind(wx.EVT_TEXT, self.update_att)
        self.wm_textCtrl81.Bind(wx.EVT_TEXT, self.update_att)
        self.wm_textCtrl75.Bind(wx.EVT_TEXT, self.update_att)
        self.wm_textCtrl76.Bind(wx.EVT_TEXT, self.update_att)
        self.wm_textCtrl77.Bind(wx.EVT_TEXT, self.update_att)
        self.wm_textCtrl78.Bind(wx.EVT_TEXT, self.update_att)
        self.wm_textCtrl79.Bind(wx.EVT_TEXT, self.update_att)
        self.wm_textCtrl85.Bind(wx.EVT_TEXT, self.update_att)
        self.wm_textCtrl59.Bind(wx.EVT_TEXT, self.update_att)
        self.wm_textCtrl66.Bind(wx.EVT_TEXT, self.update_att)
        self.wm_textCtrl67.Bind(wx.EVT_TEXT, self.update_att)
        self.wm_textCtrl68.Bind(wx.EVT_TEXT, self.update_att)
        self.wm_textCtrl71.Bind(wx.EVT_TEXT, self.update_att)
        self.wm_textCtrl72.Bind(wx.EVT_TEXT, self.update_att)
        self.wm_textCtrl83.Bind(wx.EVT_TEXT, self.update_att)
        self.wm_textCtrl61.Bind(wx.EVT_TEXT, self.update_att)
        self.wm_textCtrl62.Bind(wx.EVT_TEXT, self.update_att)
        self.wm_textCtrl82.Bind(wx.EVT_TEXT, self.update_att)
        self.wm_textCtrl73.Bind(wx.EVT_TEXT, self.update_att)
        self.wm_textCtrl74.Bind(wx.EVT_TEXT, self.update_att)
        self.wm_textCtrl84.Bind(wx.EVT_TEXT, self.update_att)
        self.wm_textCtrl80.Bind(wx.EVT_TEXT, self.update_att)
        self.weapon_enchant0.Bind(wx.EVT_CHOICE, self.update_att)
        self.weapon_enchant1.Bind(wx.EVT_CHOICE, self.update_att)
        self.wm_textCtrl86.Bind(wx.EVT_TEXT, self.update_att)

        self.SetSizer(gbSizer9)
        self.Layout()

        self.Centre(wx.BOTH)

    def __del__(self):
        pass

    def core_weapon(self, event):
        cw_choice = self.weapon_core.GetSelection()
        if cw_choice == 0:
            self.wm_textCtrl58.SetValue('8880')
            self.wm_textCtrl59.SetValue('3')
            self.wm_textCtrl81.SetValue('0')
        else:
            self.wm_textCtrl58.SetValue('3456')
            self.wm_textCtrl59.SetValue('3')
            self.wm_textCtrl81.SetValue('0')

        event.Skip()

    def light_weapon(self, event):
        lw_choice = self.weapon_light.GetSelection()
        if lw_choice == 1:
            self.wm_textCtrl73.SetValue('24')
            self.wm_textCtrl74.SetValue('4')
            self.wm_textCtrl84.SetValue('0')
        else:
            self.wm_textCtrl73.SetValue('3')
            self.wm_textCtrl74.SetValue('4')
            self.wm_textCtrl84.SetValue('0')
        event.Skip()

    def perfect_weapon(self, event):
        pw_choice = self.weapon_perfect.GetSelection()
        if pw_choice == 0:
            self.wm_textCtrl75.SetValue('5446')
            self.wm_textCtrl76.SetValue('52')
            self.wm_textCtrl77.SetValue('28')
            self.wm_textCtrl78.SetValue('70')
            self.wm_textCtrl79.SetValue('38')
            self.wm_textCtrl85.SetValue('0')
        else:
            self.wm_textCtrl75.SetValue('1')
            self.wm_textCtrl76.SetValue('1')
            self.wm_textCtrl77.SetValue('1')
            self.wm_textCtrl78.SetValue('1')
            self.wm_textCtrl79.SetValue('1')
            self.wm_textCtrl85.SetValue('0')
        event.Skip()

    def sharp_weapon(self, event):
        sw_choice = self.weapon_sharp.GetSelection()
        if sw_choice == 0:
            self.wm_textCtrl61.SetValue('24')
            self.wm_textCtrl62.SetValue('36')
            self.wm_textCtrl82.SetValue('0')
        else:
            self.wm_textCtrl61.SetValue('24')
            self.wm_textCtrl62.SetValue('36')
            self.wm_textCtrl82.SetValue('0')
        event.Skip()

    def stable_weapon(self, event):
        stw_choice = self.weapon_stable.GetSelection()
        if stw_choice == 0:
            self.wm_textCtrl66.SetValue('36')
            self.wm_textCtrl67.SetValue('35')
            self.wm_textCtrl68.SetValue('19')
            self.wm_textCtrl71.SetValue('47')
            self.wm_textCtrl72.SetValue('25')
            self.wm_textCtrl83.SetValue('0')
        else:
            self.wm_textCtrl66.SetValue('1')
            self.wm_textCtrl67.SetValue('1')
            self.wm_textCtrl68.SetValue('1')
            self.wm_textCtrl71.SetValue('1')
            self.wm_textCtrl72.SetValue('1')
            self.wm_textCtrl83.SetValue('0')
        event.Skip()

    def update_att(self, event):
        global weapon_att
        enchant_att0 = [0]
        enchant_att1 = [0]
        addw_x = [0]
        n0 = int(self.weapon_enchant0.GetSelection())
        n1 = int(self.weapon_enchant1.GetSelection())
        enchant_att0 = enchant_weapon0(n0)
        enchant_att1 = enchant_weapon1(n1)
        addw_choice = self.weapon_add.GetSelection()
        addw_x = alladd(1, addw_choice)
        add_att = intplus(self.wm_textCtrl80.GetValue())
        strength_data = data_strengthen(0, intplus(self.wm_textCtrl86.GetValue()))
        weapon_att[0] = intplus(self.wm_textCtrl58.GetValue()) + intplus(self.wm_textCtrl75.GetValue()) +\
                        enchant_att0[0] + enchant_att1[0] + addw_x[0]*add_att + strength_data[0]
        weapon_att[1] = intplus(self.wm_textCtrl61.GetValue()) + intplus(self.wm_textCtrl66.GetValue()) +\
                        enchant_att0[3] + enchant_att1[3] + addw_x[3]*add_att
        weapon_att[2] = intplus(self.wm_textCtrl62.GetValue()) + intplus(self.wm_textCtrl73.GetValue()) +\
                        enchant_att0[2] + enchant_att1[2] + addw_x[2]*add_att
        weapon_att[3] = intplus(self.wm_textCtrl59.GetValue()) + intplus(self.wm_textCtrl74.GetValue()) +\
                        enchant_att0[4] + enchant_att1[4] + addw_x[4]*add_att + strength_data[2]
        weapon_att[4] = strength_data[1]
        weapon_att[5] = intplus(self.wm_textCtrl67.GetValue()) + intplus(self.wm_textCtrl76.GetValue()) + addw_x[5]*add_att
        weapon_att[6] = intplus(self.wm_textCtrl68.GetValue()) + intplus(self.wm_textCtrl77.GetValue()) + addw_x[6]*add_att
        weapon_att[7] = intplus(self.wm_textCtrl71.GetValue()) + intplus(self.wm_textCtrl78.GetValue()) + addw_x[7]*add_att
        weapon_att[8] = intplus(self.wm_textCtrl72.GetValue()) + intplus(self.wm_textCtrl79.GetValue()) + addw_x[8]*add_att
        weapon_att[9] = intplus(self.wm_textCtrl81.GetValue()) + intplus(self.wm_textCtrl82.GetValue()) + \
                        intplus(self.wm_textCtrl83.GetValue()) + intplus(self.wm_textCtrl84.GetValue()) + \
                        intplus(self.wm_textCtrl85.GetValue())
        weapon_att[10] = enchant_att0[5] + enchant_att1[5] + addw_x[9]*add_att

        self.wm_staticText173.SetLabelText('攻击力: %d  平衡: %d  暴击: %d  攻速: %d  追伤: %d  力量: %d\r\n  '
                                           '敏捷: %d  智力: %d  意志: %d  解禁: %d  爆抗: %d'
                                           % (weapon_att[0], weapon_att[1], weapon_att[2], weapon_att[3], weapon_att[4],
                                              weapon_att[5], weapon_att[6], weapon_att[7], weapon_att[8], weapon_att[9],
                                              weapon_att[10]))
        event.Skip()

    def dateupdate(self, event):
        global weapon_data
        weapon_data = [[self.weapon_core.GetSelection(), self.wm_textCtrl58.GetValue(), self.wm_textCtrl59.GetValue(),
                        self.wm_textCtrl81.GetValue()],
                       [self.weapon_sharp.GetSelection(), self.wm_textCtrl61.GetValue(), self.wm_textCtrl62.GetValue(),
                        self.wm_textCtrl82.GetValue()],
                       [self.weapon_stable.GetSelection(), self.wm_textCtrl66.GetValue(), self.wm_textCtrl67.GetValue(),
                        self.wm_textCtrl68.GetValue(), self.wm_textCtrl71.GetValue(), self.wm_textCtrl72.GetValue(),
                        self.wm_textCtrl83.GetValue()],
                       [self.weapon_light.GetSelection(), self.wm_textCtrl73.GetValue(), self.wm_textCtrl74.GetValue(),
                        self.wm_textCtrl84.GetValue()],
                       [self.weapon_perfect.GetSelection(), self.wm_textCtrl75.GetValue(),
                        self.wm_textCtrl76.GetValue(), self.wm_textCtrl77.GetValue(), self.wm_textCtrl78.GetValue(),
                        self.wm_textCtrl79.GetValue(), self.wm_textCtrl85.GetValue()],
                       [self.weapon_add.GetSelection(), self.wm_textCtrl80.GetValue()],
                       [self.wm_textCtrl86.GetValue(), self.weapon_enchant0.GetSelection(),
                        self.weapon_enchant1.GetSelection()]]
        DataThread()
        event.Skip()


class Head(wx.Dialog):
    global head_data
    global head_att
    head_data = [[0, '', '', ''],
                 [1, '', '', '', '', '', ''],
                 [7, ''],
                 ['', 4, 7]]
    head_att = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    
    def __init__(self, parent, title):
        super(Head, self).__init__(parent, title=title, size=(600, 400))

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        gbSizerHead = wx.GridBagSizer(0, 0)
        gbSizerHead.SetFlexibleDirection(wx.BOTH)
        gbSizerHead.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        head_choice65Choices = [u"橙色核心", u"紫色核心"]
        self.head_core = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, head_choice65Choices, 0)
        self.head_core.SetSelection(0)
        gbSizerHead.Add(self.head_core, wx.GBPosition(0, 0), wx.GBSpan(1, 1),
                        wx.ALL | wx.EXPAND | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.head_textCtrl81 = wx.TextCtrl(self, wx.ID_ANY, head_data[0][1], wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizerHead.Add(self.head_textCtrl81, wx.GBPosition(0, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        self.head_textCtrl82 = wx.TextCtrl(self, wx.ID_ANY, head_data[0][2], wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizerHead.Add(self.head_textCtrl82, wx.GBPosition(0, 2), wx.GBSpan(1, 1), wx.ALL, 5)

        self.head_textCtrl83 = wx.TextCtrl(self, wx.ID_ANY, head_data[0][3], wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizerHead.Add(self.head_textCtrl83, wx.GBPosition(0, 3), wx.GBSpan(1, 1), wx.ALL, 5)

        head_choice66Choices = [u"橙色结实", u"紫色结实"]
        self.head_strong = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, head_choice66Choices, 0)
        self.head_strong.SetSelection(1)
        gbSizerHead.Add(self.head_strong, wx.GBPosition(1, 0), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        self.head_textCtrl84 = wx.TextCtrl(self, wx.ID_ANY, head_data[1][1], wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizerHead.Add(self.head_textCtrl84, wx.GBPosition(1, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        self.head_textCtrl85 = wx.TextCtrl(self, wx.ID_ANY, head_data[1][2], wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizerHead.Add(self.head_textCtrl85, wx.GBPosition(1, 2), wx.GBSpan(1, 1), wx.ALL, 5)

        self.head_textCtrl86 = wx.TextCtrl(self, wx.ID_ANY, head_data[1][3], wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizerHead.Add(self.head_textCtrl86, wx.GBPosition(1, 3), wx.GBSpan(1, 1), wx.ALL, 5)

        self.head_textCtrl87 = wx.TextCtrl(self, wx.ID_ANY, head_data[1][4], wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizerHead.Add(self.head_textCtrl87, wx.GBPosition(2, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        self.head_textCtrl88 = wx.TextCtrl(self, wx.ID_ANY, head_data[1][5], wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizerHead.Add(self.head_textCtrl88, wx.GBPosition(2, 2), wx.GBSpan(1, 1), wx.ALL, 5)

        self.head_textCtrl89 = wx.TextCtrl(self, wx.ID_ANY, head_data[1][6], wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizerHead.Add(self.head_textCtrl89, wx.GBPosition(2, 3), wx.GBSpan(1, 1), wx.ALL, 5)

        head_choice67Choices = [u"爆抗", u"防御力", u"意志", u"敏捷", u"生命力", u"智力", u"力量", u"无"]
        self.head_add = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, head_choice67Choices, 0)
        self.head_add.SetSelection(head_data[2][0])
        gbSizerHead.Add(self.head_add, wx.GBPosition(4, 0), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        self.head_textCtrl90 = wx.TextCtrl(self, wx.ID_ANY, head_data[2][1], wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizerHead.Add(self.head_textCtrl90, wx.GBPosition(4, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        self.head_staticText83 = wx.StaticText(self, wx.ID_ANY, u"强化等级", wx.DefaultPosition, wx.DefaultSize,
                                               wx.ALIGN_CENTRE)
        self.head_staticText83.Wrap(-1)
        gbSizerHead.Add(self.head_staticText83, wx.GBPosition(5, 0), wx.GBSpan(1, 1),
                        wx.ALL | wx.EXPAND | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.head_textCtrl91 = wx.TextCtrl(self, wx.ID_ANY, head_data[3][0], wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizerHead.Add(self.head_textCtrl91, wx.GBPosition(5, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        head_choice68Choices = [u"冷静的", u"记忆的", u"保持平衡的", u"努力地", wx.EmptyString]
        self.head_enchant0 = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, head_choice68Choices, 0)
        self.head_enchant0.SetSelection(head_data[3][1])
        gbSizerHead.Add(self.head_enchant0, wx.GBPosition(5, 2), wx.GBSpan(1, 1), wx.ALL, 5)

        head_choice69Choices = [u"远征", u"热忱", u"落叶", u"茉莉花", u"致命", u"抵抗", u"犰狳", wx.EmptyString]
        self.head_enchant1 = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, head_choice69Choices, 0)
        self.head_enchant1.SetSelection(head_data[3][2])
        gbSizerHead.Add(self.head_enchant1, wx.GBPosition(5, 3), wx.GBSpan(1, 1), wx.ALL, 5)

        self.head_staticText173 = wx.StaticText(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                                wx.ALIGN_CENTRE)
        self.head_staticText173.Wrap(-1)
        gbSizerHead.Add(self.head_staticText173, wx.GBPosition(6, 0), wx.GBSpan(2, 4), wx.ALL | wx.EXPAND, 5)

        head_sdbSizer3 = wx.StdDialogButtonSizer()
        self.head_sdbSizer3OK = wx.Button(self, wx.ID_OK)
        head_sdbSizer3.AddButton(self.head_sdbSizer3OK)
        self.head_sdbSizer3Cancel = wx.Button(self, wx.ID_CANCEL)
        head_sdbSizer3.AddButton(self.head_sdbSizer3Cancel)
        head_sdbSizer3.Realize()

        gbSizerHead.Add(head_sdbSizer3, wx.GBPosition(9, 3), wx.GBSpan(1, 1), wx.EXPAND, 5)

        self.SetSizer(gbSizerHead)
        self.Layout()

        self.Centre(wx.BOTH)

        self.head_core.Bind(wx.EVT_CHOICE, self.core_head)
        self.head_strong.Bind(wx.EVT_CHOICE, self.strong_head)
        self.head_sdbSizer3OK.Bind(wx.EVT_BUTTON, self.updata_head)
        self.head_textCtrl81.Bind(wx.EVT_TEXT, self.update_watt)
        self.head_textCtrl82.Bind(wx.EVT_TEXT, self.update_watt)
        self.head_textCtrl83.Bind(wx.EVT_TEXT, self.update_watt)
        self.head_textCtrl84.Bind(wx.EVT_TEXT, self.update_watt)
        self.head_textCtrl85.Bind(wx.EVT_TEXT, self.update_watt)
        self.head_textCtrl86.Bind(wx.EVT_TEXT, self.update_watt)
        self.head_textCtrl87.Bind(wx.EVT_TEXT, self.update_watt)
        self.head_textCtrl88.Bind(wx.EVT_TEXT, self.update_watt)
        self.head_textCtrl89.Bind(wx.EVT_TEXT, self.update_watt)
        self.head_textCtrl90.Bind(wx.EVT_TEXT, self.update_watt)
        self.head_add.Bind(wx.EVT_CHOICE, self.update_watt)
        self.head_enchant0.Bind(wx.EVT_CHOICE, self.update_watt)
        self.head_enchant1.Bind(wx.EVT_CHOICE, self.update_watt)
        self.head_textCtrl91.Bind(wx.EVT_TEXT, self.update_watt)

    def __del__(self):
        pass

    def core_head(self, event):
        ch_choice = self.head_core.GetSelection()
        if ch_choice == 0:
            self.head_textCtrl81.SetValue('1856')
            self.head_textCtrl82.SetValue('4')
            self.head_textCtrl83.SetValue('0')
        else:
            self.head_textCtrl81.SetValue('1578')
            self.head_textCtrl82.SetValue('3')
            self.head_textCtrl83.SetValue('0')
        event.Skip()

    def strong_head(self, event):
        sh_choice = self.head_strong.GetSelection()
        if sh_choice == 0:
            self.head_textCtrl84.SetValue('180')
            self.head_textCtrl85.SetValue('90')
            self.head_textCtrl86.SetValue('243')
            self.head_textCtrl87.SetValue('80')
            self.head_textCtrl88.SetValue('13')
            self.head_textCtrl89.SetValue('0')
        else:
            self.head_textCtrl84.SetValue('144')
            self.head_textCtrl85.SetValue('72')
            self.head_textCtrl86.SetValue('194')
            self.head_textCtrl87.SetValue('64')
            self.head_textCtrl88.SetValue('11')
            self.head_textCtrl89.SetValue('0')
        event.Skip()

    def update_watt(self, event):
        global head_att
        enchant_att0 = [0]
        enchant_att1 = [0]
        addw_x = [0]
        nn0 = int(self.head_enchant0.GetSelection())
        if nn0 == 1:
            n0 = 2
        elif nn0 == 2 or nn0 == 3 or nn0 == 4:
            n0 = nn0 + 3
        else:
            n0 = nn0
        enchant_att0 = enchant_armor0(n0)
        nn1 = int(self.head_enchant1.GetSelection())
        if (nn1 <= 4) & (nn1 > 0):
            n1 = nn1 + 1
        elif nn1 == 0:
            n1 = 1
        else:
            n1 = nn1 + 3
        enchant_att1 = enchant_armor1(n1)
        addw_choice = self.head_add.GetSelection()
        addw_x = alladd(2, addw_choice)
        add_att = intplus(self.head_textCtrl90.GetValue())
        streng_data = data_strengthen(1, intplus(self.head_textCtrl91.GetValue()))
        head_att[0] = enchant_att0[0] + enchant_att1[0]
        head_att[1] = enchant_att0[3] + enchant_att1[3]
        head_att[2] = enchant_att0[2] + enchant_att1[2]
        head_att[3] = enchant_att0[4] + enchant_att1[4]
        head_att[4] = streng_data[1]
        head_att[5] = intplus(self.head_textCtrl84.GetValue()) + addw_x[5] * add_att
        head_att[6] = intplus(self.head_textCtrl85.GetValue()) + addw_x[6] * add_att
        head_att[7] = intplus(self.head_textCtrl86.GetValue()) + addw_x[7] * add_att
        head_att[8] = intplus(self.head_textCtrl87.GetValue()) + addw_x[8] * add_att
        head_att[9] = intplus(self.head_textCtrl83.GetValue()) + intplus(self.head_textCtrl89.GetValue())
        head_att[10] = intplus(self.head_textCtrl82.GetValue()) + intplus(self.head_textCtrl88.GetValue()) +\
                       enchant_att0[5] + enchant_att1[5] + addw_x[9] * add_att
        head_att[11] = intplus(self.head_textCtrl81.GetValue()) + enchant_att0[1] + enchant_att1[1] +\
                       addw_x[1] * add_att + streng_data[0]

        self.head_staticText173.SetLabelText('攻击力: %d  防御力: %d  平衡: %d  暴击: %d  攻速: %d  追伤: %d\r\n  '
                                             '  力量: %d  敏捷: %d  智力: %d  意志: %d  解禁: %d  爆抗: %d'
                                           % (head_att[0], head_att[11], head_att[1], head_att[2], head_att[3],
                                              head_att[4], head_att[5], head_att[6], head_att[7], head_att[8],
                                              head_att[9], head_att[10]))
        event.Skip()
        
    def updata_head(self, event):
        global head_data
        head_data = [[self.head_core.GetSelection(), self.head_textCtrl81.GetValue(), self.head_textCtrl82.GetValue(),
                      self.head_textCtrl83.GetValue()],
                     [self.head_strong.GetSelection(), self.head_textCtrl84.GetValue(), self.head_textCtrl85.GetValue(),
                      self.head_textCtrl86.GetValue(), self.head_textCtrl87.GetValue(), self.head_textCtrl88.GetValue(),
                      self.head_textCtrl89.GetValue()],
                     [self.head_add.GetSelection(), self.head_textCtrl90.GetValue()],
                     [self.head_textCtrl91.GetValue(), self.head_enchant0.GetSelection(),
                      self.head_enchant1.GetSelection()]]
        DataThread()
        event.Skip()
        

class Hand(wx.Dialog):
    global hand_data
    global hand_att
    hand_data = [[0, '', '', ''],
                 [1, '', '', '', '', '', ''],
                 [7, ''],
                 ['', 4, 7]]
    hand_att = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    
    def __init__(self, parent, title):
        super(Hand, self).__init__(parent, title=title, size=(600, 400))

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        gbSizerHand = wx.GridBagSizer(0, 0)
        gbSizerHand.SetFlexibleDirection(wx.BOTH)
        gbSizerHand.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        hand_choice65Choices = [u"橙色核心", u"紫色核心"]
        self.hand_core = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, hand_choice65Choices, 0)
        self.hand_core.SetSelection(hand_data[0][0])
        gbSizerHand.Add(self.hand_core, wx.GBPosition(0, 0), wx.GBSpan(1, 1),
                        wx.ALL | wx.EXPAND | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.hand_textCtrl81 = wx.TextCtrl(self, wx.ID_ANY, hand_data[0][1], wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizerHand.Add(self.hand_textCtrl81, wx.GBPosition(0, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        self.hand_textCtrl82 = wx.TextCtrl(self, wx.ID_ANY, hand_data[0][2], wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizerHand.Add(self.hand_textCtrl82, wx.GBPosition(0, 2), wx.GBSpan(1, 1), wx.ALL, 5)

        self.hand_textCtrl83 = wx.TextCtrl(self, wx.ID_ANY, hand_data[0][3], wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizerHand.Add(self.hand_textCtrl83, wx.GBPosition(0, 3), wx.GBSpan(1, 1), wx.ALL, 5)

        hand_choice66Choices = [u"橙色结实", u"紫色结实"]
        self.hand_strong = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, hand_choice66Choices, 0)
        self.hand_strong.SetSelection(hand_data[1][0])
        gbSizerHand.Add(self.hand_strong, wx.GBPosition(1, 0), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        self.hand_textCtrl84 = wx.TextCtrl(self, wx.ID_ANY, hand_data[1][1], wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizerHand.Add(self.hand_textCtrl84, wx.GBPosition(1, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        self.hand_textCtrl85 = wx.TextCtrl(self, wx.ID_ANY, hand_data[1][2], wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizerHand.Add(self.hand_textCtrl85, wx.GBPosition(1, 2), wx.GBSpan(1, 1), wx.ALL, 5)

        self.hand_textCtrl86 = wx.TextCtrl(self, wx.ID_ANY, hand_data[1][3], wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizerHand.Add(self.hand_textCtrl86, wx.GBPosition(1, 3), wx.GBSpan(1, 1), wx.ALL, 5)

        self.hand_textCtrl87 = wx.TextCtrl(self, wx.ID_ANY, hand_data[1][4], wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizerHand.Add(self.hand_textCtrl87, wx.GBPosition(2, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        self.hand_textCtrl88 = wx.TextCtrl(self, wx.ID_ANY, hand_data[1][5], wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizerHand.Add(self.hand_textCtrl88, wx.GBPosition(2, 2), wx.GBSpan(1, 1), wx.ALL, 5)

        self.hand_textCtrl89 = wx.TextCtrl(self, wx.ID_ANY, hand_data[1][6], wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizerHand.Add(self.hand_textCtrl89, wx.GBPosition(2, 3), wx.GBSpan(1, 1), wx.ALL, 5)

        hand_choice67Choices = [u"爆抗", u"防御力", u"意志", u"敏捷", u"生命力", u"智力", u"力量", u"无"]
        self.hand_add = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, hand_choice67Choices, 0)
        self.hand_add.SetSelection(hand_data[2][0])
        gbSizerHand.Add(self.hand_add, wx.GBPosition(4, 0), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        self.hand_textCtrl90 = wx.TextCtrl(self, wx.ID_ANY, hand_data[2][1], wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizerHand.Add(self.hand_textCtrl90, wx.GBPosition(4, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        self.hand_staticText83 = wx.StaticText(self, wx.ID_ANY, u"强化等级", wx.DefaultPosition, wx.DefaultSize,
                                            wx.ALIGN_CENTRE)
        self.hand_staticText83.Wrap(-1)
        gbSizerHand.Add(self.hand_staticText83, wx.GBPosition(5, 0), wx.GBSpan(1, 1),
                        wx.ALL | wx.EXPAND | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.hand_textCtrl91 = wx.TextCtrl(self, wx.ID_ANY, hand_data[3][0], wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizerHand.Add(self.hand_textCtrl91, wx.GBPosition(5, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        hand_choice68Choices = [u"哭泣的", u"重述的", u"保持平衡的", u"努力地", wx.EmptyString]
        self.hand_enchant0 = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, hand_choice68Choices, 0)
        self.hand_enchant0.SetSelection(hand_data[3][1])
        gbSizerHand.Add(self.hand_enchant0, wx.GBPosition(5, 2), wx.GBSpan(1, 1), wx.ALL, 5)

        hand_choice69Choices = [u"回音", u"热忱", u"落叶", u"茉莉花", u"致命", u"抵抗", u"犰狳", wx.EmptyString]
        self.hand_enchant1 = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, hand_choice69Choices, 0)
        self.hand_enchant1.SetSelection(hand_data[3][2])
        gbSizerHand.Add(self.hand_enchant1, wx.GBPosition(5, 3), wx.GBSpan(1, 1), wx.ALL, 5)

        self.hand_staticText173 = wx.StaticText(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                                wx.ALIGN_CENTRE)
        self.hand_staticText173.Wrap(-1)
        gbSizerHand.Add(self.hand_staticText173, wx.GBPosition(6, 0), wx.GBSpan(2, 4), wx.ALL | wx.EXPAND, 5)

        hand_sdbSizer3 = wx.StdDialogButtonSizer()
        self.hand_sdbSizer3OK = wx.Button(self, wx.ID_OK)
        hand_sdbSizer3.AddButton(self.hand_sdbSizer3OK)
        self.hand_sdbSizer3Cancel = wx.Button(self, wx.ID_CANCEL)
        hand_sdbSizer3.AddButton(self.hand_sdbSizer3Cancel)
        hand_sdbSizer3.Realize()

        gbSizerHand.Add(hand_sdbSizer3, wx.GBPosition(9, 3), wx.GBSpan(1, 1), wx.EXPAND, 5)

        self.SetSizer(gbSizerHand)
        self.Layout()

        self.Centre(wx.BOTH)

        self.hand_core.Bind(wx.EVT_CHOICE, self.core_hand)
        self.hand_strong.Bind(wx.EVT_CHOICE, self.strong_hand)
        self.hand_sdbSizer3OK.Bind(wx.EVT_BUTTON, self.updata_hand)
        self.hand_textCtrl81.Bind(wx.EVT_TEXT, self.update_watt)
        self.hand_textCtrl82.Bind(wx.EVT_TEXT, self.update_watt)
        self.hand_textCtrl83.Bind(wx.EVT_TEXT, self.update_watt)
        self.hand_textCtrl84.Bind(wx.EVT_TEXT, self.update_watt)
        self.hand_textCtrl85.Bind(wx.EVT_TEXT, self.update_watt)
        self.hand_textCtrl86.Bind(wx.EVT_TEXT, self.update_watt)
        self.hand_textCtrl87.Bind(wx.EVT_TEXT, self.update_watt)
        self.hand_textCtrl88.Bind(wx.EVT_TEXT, self.update_watt)
        self.hand_textCtrl89.Bind(wx.EVT_TEXT, self.update_watt)
        self.hand_textCtrl90.Bind(wx.EVT_TEXT, self.update_watt)
        self.hand_add.Bind(wx.EVT_CHOICE, self.update_watt)
        self.hand_enchant0.Bind(wx.EVT_CHOICE, self.update_watt)
        self.hand_enchant1.Bind(wx.EVT_CHOICE, self.update_watt)
        self.hand_textCtrl91.Bind(wx.EVT_TEXT, self.update_watt)

    def __del__(self):
        pass

    def core_hand(self, event):
        ch1_choice = self.hand_core.GetSelection()
        if ch1_choice == 0:
            self.hand_textCtrl81.SetValue('1856')
            self.hand_textCtrl82.SetValue('4')
            self.hand_textCtrl83.SetValue('0')
        else:
            self.hand_textCtrl81.SetValue('1578')
            self.hand_textCtrl82.SetValue('3')
            self.hand_textCtrl83.SetValue('0')
        event.Skip()

    def strong_hand(self, event):
        sh_choice = self.hand_strong.GetSelection()
        if sh_choice == 0:
            self.hand_textCtrl84.SetValue('180')
            self.hand_textCtrl85.SetValue('90')
            self.hand_textCtrl86.SetValue('243')
            self.hand_textCtrl87.SetValue('80')
            self.hand_textCtrl88.SetValue('13')
            self.hand_textCtrl89.SetValue('0')
        else:
            self.hand_textCtrl84.SetValue('144')
            self.hand_textCtrl85.SetValue('72')
            self.hand_textCtrl86.SetValue('194')
            self.hand_textCtrl87.SetValue('64')
            self.hand_textCtrl88.SetValue('11')
            self.hand_textCtrl89.SetValue('0')
        event.Skip()

    def update_watt(self, event):
        global hand_att
        enchant_att0 = [0]
        enchant_att1 = [0]
        addw_x = [0]
        nn0 = self.hand_enchant0.GetSelection()
        if nn0 == 1:
            n0 = 3
        elif nn0 == 2 or nn0 == 3 or nn0 == 4:
            n0 = nn0 + 3
        else:
            n0 = nn0 + 1
        enchant_att0 = enchant_armor0(n0)
        nn1 = int(self.hand_enchant1.GetSelection())
        if (nn1 <= 4) & (nn1 > 0):
            n1 = nn1 + 1
        elif nn1 == 0:
            n1 = 0
        else:
            n1 = nn1 + 3
        enchant_att1 = enchant_armor1(n1)
        addw_choice = self.hand_add.GetSelection()
        addw_x = alladd(2, addw_choice)
        add_att = intplus(self.hand_textCtrl90.GetValue())
        streng_data = data_strengthen(1, intplus(self.hand_textCtrl91.GetValue()))
        hand_att[0] = enchant_att0[0] + enchant_att1[0]
        hand_att[1] = enchant_att0[3] + enchant_att1[3]
        hand_att[2] = enchant_att0[2] + enchant_att1[2]
        hand_att[3] = enchant_att0[4] + enchant_att1[4]
        hand_att[4] = streng_data[1]
        hand_att[5] = intplus(self.hand_textCtrl84.GetValue()) + addw_x[5] * add_att
        hand_att[6] = intplus(self.hand_textCtrl85.GetValue()) + addw_x[6] * add_att
        hand_att[7] = intplus(self.hand_textCtrl86.GetValue()) + addw_x[7] * add_att
        hand_att[8] = intplus(self.hand_textCtrl87.GetValue()) + addw_x[8] * add_att
        hand_att[9] = intplus(self.hand_textCtrl83.GetValue()) + intplus(self.hand_textCtrl89.GetValue())
        hand_att[10] = intplus(self.hand_textCtrl82.GetValue()) + intplus(self.hand_textCtrl88.GetValue()) +\
                       enchant_att0[5] + enchant_att1[5] + addw_x[9] * add_att
        hand_att[11] = intplus(self.hand_textCtrl81.GetValue()) + enchant_att0[1] + enchant_att1[1] +\
                       addw_x[1] * add_att + streng_data[0]

        self.hand_staticText173.SetLabelText('攻击力: %d  防御力: %d  平衡: %d  暴击: %d  攻速: %d  追伤: %d\r\n  '
                                             '  力量: %d  敏捷: %d  智力: %d  意志: %d  解禁: %d  爆抗: %d'
                                           % (hand_att[0], hand_att[11], hand_att[1], hand_att[2], hand_att[3],
                                              hand_att[4], hand_att[5], hand_att[6], hand_att[7], hand_att[8],
                                              hand_att[9], hand_att[10]))
        event.Skip()

    def updata_hand(self, event):
        global hand_data
        hand_data = [[self.hand_core.GetSelection(), self.hand_textCtrl81.GetValue(), self.hand_textCtrl82.GetValue(),
                      self.hand_textCtrl83.GetValue()],
                     [self.hand_strong.GetSelection(), self.hand_textCtrl84.GetValue(), self.hand_textCtrl85.GetValue(),
                      self.hand_textCtrl86.GetValue(), self.hand_textCtrl87.GetValue(), self.hand_textCtrl88.GetValue(),
                      self.hand_textCtrl89.GetValue()],
                     [self.hand_add.GetSelection(), self.hand_textCtrl90.GetValue()],
                     [self.hand_textCtrl91.GetValue(), self.hand_enchant0.GetSelection(),
                      self.hand_enchant1.GetSelection()]]
        DataThread()
        event.Skip()
        

class Foot(wx.Dialog):
    global foot_data
    global foot_att
    foot_data = [[0, '', '', ''],
                 [1, '', '', '', '', '', ''],
                 [7, ''],
                 ['', 4, 7]]
    foot_att = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    def __init__(self, parent, title):
        super(Foot, self).__init__(parent, title=title, size=(600, 400))

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        gbSizerfoot = wx.GridBagSizer(0, 0)
        gbSizerfoot.SetFlexibleDirection(wx.BOTH)
        gbSizerfoot.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        foot_choice65Choices = [u"橙色核心", u"紫色核心"]
        self.foot_core = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, foot_choice65Choices, 0)
        self.foot_core.SetSelection(foot_data[0][0])
        gbSizerfoot.Add(self.foot_core, wx.GBPosition(0, 0), wx.GBSpan(1, 1),
                        wx.ALL | wx.EXPAND | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.foot_textCtrl81 = wx.TextCtrl(self, wx.ID_ANY, foot_data[0][1], wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizerfoot.Add(self.foot_textCtrl81, wx.GBPosition(0, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        self.foot_textCtrl82 = wx.TextCtrl(self, wx.ID_ANY, foot_data[0][2], wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizerfoot.Add(self.foot_textCtrl82, wx.GBPosition(0, 2), wx.GBSpan(1, 1), wx.ALL, 5)

        self.foot_textCtrl83 = wx.TextCtrl(self, wx.ID_ANY, foot_data[0][3], wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizerfoot.Add(self.foot_textCtrl83, wx.GBPosition(0, 3), wx.GBSpan(1, 1), wx.ALL, 5)

        foot_choice66Choices = [u"橙色结实", u"紫色结实"]
        self.foot_strong = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, foot_choice66Choices, 0)
        self.foot_strong.SetSelection(foot_data[1][0])
        gbSizerfoot.Add(self.foot_strong, wx.GBPosition(1, 0), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        self.foot_textCtrl84 = wx.TextCtrl(self, wx.ID_ANY, foot_data[1][1], wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizerfoot.Add(self.foot_textCtrl84, wx.GBPosition(1, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        self.foot_textCtrl85 = wx.TextCtrl(self, wx.ID_ANY, foot_data[1][2], wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizerfoot.Add(self.foot_textCtrl85, wx.GBPosition(1, 2), wx.GBSpan(1, 1), wx.ALL, 5)

        self.foot_textCtrl86 = wx.TextCtrl(self, wx.ID_ANY, foot_data[1][3], wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizerfoot.Add(self.foot_textCtrl86, wx.GBPosition(1, 3), wx.GBSpan(1, 1), wx.ALL, 5)

        self.foot_textCtrl87 = wx.TextCtrl(self, wx.ID_ANY, foot_data[1][4], wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizerfoot.Add(self.foot_textCtrl87, wx.GBPosition(2, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        self.foot_textCtrl88 = wx.TextCtrl(self, wx.ID_ANY, foot_data[1][5], wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizerfoot.Add(self.foot_textCtrl88, wx.GBPosition(2, 2), wx.GBSpan(1, 1), wx.ALL, 5)

        self.foot_textCtrl89 = wx.TextCtrl(self, wx.ID_ANY, foot_data[1][6], wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizerfoot.Add(self.foot_textCtrl89, wx.GBPosition(2, 3), wx.GBSpan(1, 1), wx.ALL, 5)

        foot_choice67Choices = [u"爆抗", u"防御力", u"意志", u"敏捷", u"生命力", u"智力", u"力量", u"无"]
        self.foot_add = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, foot_choice67Choices, 0)
        self.foot_add.SetSelection(foot_data[2][0])
        gbSizerfoot.Add(self.foot_add, wx.GBPosition(4, 0), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        self.foot_textCtrl90 = wx.TextCtrl(self, wx.ID_ANY, foot_data[2][1], wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizerfoot.Add(self.foot_textCtrl90, wx.GBPosition(4, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        self.foot_staticText83 = wx.StaticText(self, wx.ID_ANY, u"强化等级", wx.DefaultPosition, wx.DefaultSize,
                                               wx.ALIGN_CENTRE)
        self.foot_staticText83.Wrap(-1)
        gbSizerfoot.Add(self.foot_staticText83, wx.GBPosition(5, 0), wx.GBSpan(1, 1),
                        wx.ALL | wx.EXPAND | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.foot_textCtrl91 = wx.TextCtrl(self, wx.ID_ANY, foot_data[3][0], wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizerfoot.Add(self.foot_textCtrl91, wx.GBPosition(5, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        foot_choice68Choices = [u"哭泣的", u"重述的", u"保持平衡的", u"努力地", wx.EmptyString]
        self.foot_enchant0 = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, foot_choice68Choices, 0)
        self.foot_enchant0.SetSelection(foot_data[3][1])
        gbSizerfoot.Add(self.foot_enchant0, wx.GBPosition(5, 2), wx.GBSpan(1, 1), wx.ALL, 5)

        foot_choice69Choices = [u"回音", u"热忱", u"落叶", u"茉莉花", u"致命", u"抵抗", u"犰狳", wx.EmptyString]
        self.foot_enchant1 = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, foot_choice69Choices, 0)
        self.foot_enchant1.SetSelection(foot_data[3][2])
        gbSizerfoot.Add(self.foot_enchant1, wx.GBPosition(5, 3), wx.GBSpan(1, 1), wx.ALL, 5)

        self.foot_staticText173 = wx.StaticText(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                                wx.ALIGN_CENTRE)
        self.foot_staticText173.Wrap(-1)
        gbSizerfoot.Add(self.foot_staticText173, wx.GBPosition(6, 0), wx.GBSpan(2, 4), wx.ALL | wx.EXPAND, 5)

        foot_sdbSizer3 = wx.StdDialogButtonSizer()
        self.foot_sdbSizer3OK = wx.Button(self, wx.ID_OK)
        foot_sdbSizer3.AddButton(self.foot_sdbSizer3OK)
        self.foot_sdbSizer3Cancel = wx.Button(self, wx.ID_CANCEL)
        foot_sdbSizer3.AddButton(self.foot_sdbSizer3Cancel)
        foot_sdbSizer3.Realize()

        gbSizerfoot.Add(foot_sdbSizer3, wx.GBPosition(9, 3), wx.GBSpan(1, 1), wx.EXPAND, 5)

        self.SetSizer(gbSizerfoot)
        self.Layout()

        self.Centre(wx.BOTH)

        self.foot_core.Bind(wx.EVT_CHOICE, self.core_foot)
        self.foot_strong.Bind(wx.EVT_CHOICE, self.strong_foot)
        self.foot_sdbSizer3OK.Bind(wx.EVT_BUTTON, self.updata_foot)
        self.foot_textCtrl81.Bind(wx.EVT_TEXT, self.update_watt)
        self.foot_textCtrl82.Bind(wx.EVT_TEXT, self.update_watt)
        self.foot_textCtrl83.Bind(wx.EVT_TEXT, self.update_watt)
        self.foot_textCtrl84.Bind(wx.EVT_TEXT, self.update_watt)
        self.foot_textCtrl85.Bind(wx.EVT_TEXT, self.update_watt)
        self.foot_textCtrl86.Bind(wx.EVT_TEXT, self.update_watt)
        self.foot_textCtrl87.Bind(wx.EVT_TEXT, self.update_watt)
        self.foot_textCtrl88.Bind(wx.EVT_TEXT, self.update_watt)
        self.foot_textCtrl89.Bind(wx.EVT_TEXT, self.update_watt)
        self.foot_textCtrl90.Bind(wx.EVT_TEXT, self.update_watt)
        self.foot_add.Bind(wx.EVT_CHOICE, self.update_watt)
        self.foot_enchant0.Bind(wx.EVT_CHOICE, self.update_watt)
        self.foot_enchant1.Bind(wx.EVT_CHOICE, self.update_watt)
        self.foot_textCtrl91.Bind(wx.EVT_TEXT, self.update_watt)

    def __del__(self):
        pass

    def core_foot(self, event):
        ch1_choice = self.foot_core.GetSelection()
        if ch1_choice == 0:
            self.foot_textCtrl81.SetValue('1856')
            self.foot_textCtrl82.SetValue('4')
            self.foot_textCtrl83.SetValue('0')
        else:
            self.foot_textCtrl81.SetValue('1578')
            self.foot_textCtrl82.SetValue('3')
            self.foot_textCtrl83.SetValue('0')
        event.Skip()

    def strong_foot(self, event):
        sh_choice = self.foot_strong.GetSelection()
        if sh_choice == 0:
            self.foot_textCtrl84.SetValue('180')
            self.foot_textCtrl85.SetValue('90')
            self.foot_textCtrl86.SetValue('243')
            self.foot_textCtrl87.SetValue('80')
            self.foot_textCtrl88.SetValue('13')
            self.foot_textCtrl89.SetValue('0')
        else:
            self.foot_textCtrl84.SetValue('144')
            self.foot_textCtrl85.SetValue('72')
            self.foot_textCtrl86.SetValue('194')
            self.foot_textCtrl87.SetValue('64')
            self.foot_textCtrl88.SetValue('11')
            self.foot_textCtrl89.SetValue('0')
        event.Skip()
        
    def update_watt(self, event):
        global foot_att
        enchant_att0 = [0]
        enchant_att1 = [0]
        addw_x = [0]
        nn0 = self.foot_enchant0.GetSelection()
        if nn0 == 1:
            n0 = 3
        elif nn0 == 2 or nn0 == 3 or nn0 == 4:
            n0 = nn0 + 3
        else:
            n0 = nn0 + 1
        enchant_att0 = enchant_armor0(n0)
        nn1 = int(self.foot_enchant1.GetSelection())
        if (nn1 <= 4) & (nn1 > 0):
            n1 = nn1 + 1
        elif nn1 == 0:
            n1 = 0
        else:
            n1 = nn1 + 3
        enchant_att1 = enchant_armor1(n1)
        addw_choice = self.foot_add.GetSelection()
        addw_x = alladd(2, addw_choice)
        add_att = intplus(self.foot_textCtrl90.GetValue())
        streng_data = data_strengthen(1, intplus(self.foot_textCtrl91.GetValue()))
        foot_att[0] = enchant_att0[0] + enchant_att1[0]
        foot_att[1] = enchant_att0[3] + enchant_att1[3]
        foot_att[2] = enchant_att0[2] + enchant_att1[2]
        foot_att[3] = enchant_att0[4] + enchant_att1[4]
        foot_att[4] = streng_data[1]
        foot_att[5] = intplus(self.foot_textCtrl84.GetValue()) + addw_x[5] * add_att
        foot_att[6] = intplus(self.foot_textCtrl85.GetValue()) + addw_x[6] * add_att
        foot_att[7] = intplus(self.foot_textCtrl86.GetValue()) + addw_x[7] * add_att
        foot_att[8] = intplus(self.foot_textCtrl87.GetValue()) + addw_x[8] * add_att
        foot_att[9] = intplus(self.foot_textCtrl83.GetValue()) + intplus(self.foot_textCtrl89.GetValue())
        foot_att[10] = intplus(self.foot_textCtrl82.GetValue()) + intplus(self.foot_textCtrl88.GetValue()) +\
                       enchant_att0[5] + enchant_att1[5] + addw_x[9] * add_att
        foot_att[11] = intplus(self.foot_textCtrl81.GetValue()) + enchant_att0[1] + enchant_att1[1] +\
                       addw_x[1] * add_att + streng_data[0]

        self.foot_staticText173.SetLabelText('攻击力: %d  防御力: %d  平衡: %d  暴击: %d  攻速: %d  追伤: %d\r\n  '
                                             '  力量: %d  敏捷: %d  智力: %d  意志: %d  解禁: %d  爆抗: %d'
                                           % (foot_att[0], foot_att[11], foot_att[1], foot_att[2], foot_att[3],
                                              foot_att[4], foot_att[5], foot_att[6], foot_att[7], foot_att[8],
                                              foot_att[9], foot_att[10]))
        event.Skip()

    def updata_foot(self, event):
        global foot_data
        foot_data = [[self.foot_core.GetSelection(), self.foot_textCtrl81.GetValue(), self.foot_textCtrl82.GetValue(),
                      self.foot_textCtrl83.GetValue()],
                     [self.foot_strong.GetSelection(), self.foot_textCtrl84.GetValue(), self.foot_textCtrl85.GetValue(),
                      self.foot_textCtrl86.GetValue(), self.foot_textCtrl87.GetValue(), self.foot_textCtrl88.GetValue(),
                      self.foot_textCtrl89.GetValue()],
                     [self.foot_add.GetSelection(), self.foot_textCtrl90.GetValue()],
                     [self.foot_textCtrl91.GetValue(), self.foot_enchant0.GetSelection(),
                      self.foot_enchant1.GetSelection()]]
        DataThread()
        event.Skip()


class Coat(wx.Dialog):
    global coat_data
    global coat_att
    coat_data = [[0, '', '', ''],
                 [1, '', '', '', '', '', ''],
                 [1, '', '', ''],
                 [7, ''],
                 ['', 3, 6]]
    coat_att = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    def __init__(self, parent, title):
        super(Coat, self).__init__(parent, title=title, size=(600, 400))

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        gbSizerHand = wx.GridBagSizer(0, 0)
        gbSizerHand.SetFlexibleDirection(wx.BOTH)
        gbSizerHand.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        coat_choice65Choices = [u"橙色核心", u"紫色核心"]
        self.coat_core = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, coat_choice65Choices, 0)
        self.coat_core.SetSelection(coat_data[0][0])
        gbSizerHand.Add(self.coat_core, wx.GBPosition(0, 0), wx.GBSpan(1, 1),
                        wx.ALL | wx.EXPAND | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.coat_textCtrl81 = wx.TextCtrl(self, wx.ID_ANY, coat_data[0][1], wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizerHand.Add(self.coat_textCtrl81, wx.GBPosition(0, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        self.coat_textCtrl82 = wx.TextCtrl(self, wx.ID_ANY, coat_data[0][2], wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizerHand.Add(self.coat_textCtrl82, wx.GBPosition(0, 2), wx.GBSpan(1, 1), wx.ALL, 5)

        self.coat_textCtrl83 = wx.TextCtrl(self, wx.ID_ANY, coat_data[0][3], wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizerHand.Add(self.coat_textCtrl83, wx.GBPosition(0, 3), wx.GBSpan(1, 1), wx.ALL, 5)

        coat_choice66Choices = [u"橙色结实", u"紫色结实"]
        self.coat_strong = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, coat_choice66Choices, 0)
        self.coat_strong.SetSelection(coat_data[1][0])
        gbSizerHand.Add(self.coat_strong, wx.GBPosition(1, 0), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        self.coat_textCtrl84 = wx.TextCtrl(self, wx.ID_ANY, coat_data[1][1], wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizerHand.Add(self.coat_textCtrl84, wx.GBPosition(1, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        self.coat_textCtrl85 = wx.TextCtrl(self, wx.ID_ANY, coat_data[1][2], wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizerHand.Add(self.coat_textCtrl85, wx.GBPosition(1, 2), wx.GBSpan(1, 1), wx.ALL, 5)

        self.coat_textCtrl86 = wx.TextCtrl(self, wx.ID_ANY, coat_data[1][3], wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizerHand.Add(self.coat_textCtrl86, wx.GBPosition(1, 3), wx.GBSpan(1, 1), wx.ALL, 5)

        self.coat_textCtrl87 = wx.TextCtrl(self, wx.ID_ANY, coat_data[1][4], wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizerHand.Add(self.coat_textCtrl87, wx.GBPosition(2, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        self.coat_textCtrl88 = wx.TextCtrl(self, wx.ID_ANY, coat_data[1][5], wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizerHand.Add(self.coat_textCtrl88, wx.GBPosition(2, 2), wx.GBSpan(1, 1), wx.ALL, 5)

        self.coat_textCtrl89 = wx.TextCtrl(self, wx.ID_ANY, coat_data[1][6], wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizerHand.Add(self.coat_textCtrl89, wx.GBPosition(2, 3), wx.GBSpan(1, 1), wx.ALL, 5)

        coat_choice100Choices = [u"橙色光滑", u"紫色光滑"]
        self.coat_smooth = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, coat_choice100Choices, 0)
        self.coat_smooth.SetSelection(coat_data[2][0])
        gbSizerHand.Add(self.coat_smooth, wx.GBPosition(3, 0), wx.GBSpan(1, 1), wx.ALL, 5)

        self.coat_textCtrl158 = wx.TextCtrl(self, wx.ID_ANY, coat_data[2][1], wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizerHand.Add(self.coat_textCtrl158, wx.GBPosition(3, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        self.coat_textCtrl159 = wx.TextCtrl(self, wx.ID_ANY, coat_data[2][2], wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizerHand.Add(self.coat_textCtrl159, wx.GBPosition(3, 2), wx.GBSpan(1, 1), wx.ALL, 5)

        self.coat_textCtrl160 = wx.TextCtrl(self, wx.ID_ANY, coat_data[2][3], wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizerHand.Add(self.coat_textCtrl160, wx.GBPosition(3, 3), wx.GBSpan(1, 1), wx.ALL, 5)

        coat_choice67Choices = [u"爆抗", u"防御力", u"意志", u"敏捷", u"生命力", u"智力", u"力量", u"无"]
        self.coat_add = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, coat_choice67Choices, 0)
        self.coat_add.SetSelection(coat_data[3][0])
        gbSizerHand.Add(self.coat_add, wx.GBPosition(5, 0), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        self.coat_textCtrl90 = wx.TextCtrl(self, wx.ID_ANY, coat_data[3][1], wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizerHand.Add(self.coat_textCtrl90, wx.GBPosition(5, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        self.coat_staticText83 = wx.StaticText(self, wx.ID_ANY, u"强化等级", wx.DefaultPosition, wx.DefaultSize,
                                               wx.ALIGN_CENTRE)
        self.coat_staticText83.Wrap(-1)
        gbSizerHand.Add(self.coat_staticText83, wx.GBPosition(6, 0), wx.GBSpan(1, 1),
                        wx.ALL | wx.EXPAND | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.coat_textCtrl91 = wx.TextCtrl(self, wx.ID_ANY, coat_data[4][0], wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizerHand.Add(self.coat_textCtrl91, wx.GBPosition(6, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        coat_choice68Choices = [u"时间的", u"保持平衡的", u"努力地", wx.EmptyString]
        self.coat_enchant0 = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, coat_choice68Choices, 0)
        self.coat_enchant0.SetSelection(coat_data[4][1])
        gbSizerHand.Add(self.coat_enchant0, wx.GBPosition(6, 2), wx.GBSpan(1, 1), wx.ALL, 5)

        coat_choice69Choices = [u"烙印", u"保护", u"茉莉花", u"热忱", u"落叶", u"致命", wx.EmptyString]
        self.coat_enchant1 = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, coat_choice69Choices, 0)
        self.coat_enchant1.SetSelection(coat_data[4][2])
        gbSizerHand.Add(self.coat_enchant1, wx.GBPosition(6, 3), wx.GBSpan(1, 1), wx.ALL, 5)

        self.coat_staticText173 = wx.StaticText(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                                wx.ALIGN_CENTRE)
        self.coat_staticText173.Wrap(-1)
        gbSizerHand.Add(self.coat_staticText173, wx.GBPosition(7, 0), wx.GBSpan(2, 4), wx.ALL | wx.EXPAND, 5)

        coat_sdbSizer3 = wx.StdDialogButtonSizer()
        self.coat_sdbSizer3OK = wx.Button(self, wx.ID_OK)
        coat_sdbSizer3.AddButton(self.coat_sdbSizer3OK)
        self.coat_sdbSizer3Cancel = wx.Button(self, wx.ID_CANCEL)
        coat_sdbSizer3.AddButton(self.coat_sdbSizer3Cancel)
        coat_sdbSizer3.Realize()

        gbSizerHand.Add(coat_sdbSizer3, wx.GBPosition(11, 3), wx.GBSpan(1, 1), wx.EXPAND, 5)

        self.SetSizer(gbSizerHand)
        self.Layout()

        self.Centre(wx.BOTH)

        self.coat_core.Bind(wx.EVT_CHOICE, self.core_coat)
        self.coat_strong.Bind(wx.EVT_CHOICE, self.strong_coat)
        self.coat_smooth.Bind(wx.EVT_CHOICE, self.smooth_coat)
        self.coat_sdbSizer3OK.Bind(wx.EVT_BUTTON, self.updata_coat)
        self.coat_textCtrl81.Bind(wx.EVT_TEXT, self.update_watt)
        self.coat_textCtrl82.Bind(wx.EVT_TEXT, self.update_watt)
        self.coat_textCtrl83.Bind(wx.EVT_TEXT, self.update_watt)
        self.coat_textCtrl84.Bind(wx.EVT_TEXT, self.update_watt)
        self.coat_textCtrl85.Bind(wx.EVT_TEXT, self.update_watt)
        self.coat_textCtrl86.Bind(wx.EVT_TEXT, self.update_watt)
        self.coat_textCtrl87.Bind(wx.EVT_TEXT, self.update_watt)
        self.coat_textCtrl88.Bind(wx.EVT_TEXT, self.update_watt)
        self.coat_textCtrl89.Bind(wx.EVT_TEXT, self.update_watt)
        self.coat_textCtrl90.Bind(wx.EVT_TEXT, self.update_watt)
        self.coat_textCtrl158.Bind(wx.EVT_TEXT, self.update_watt)
        self.coat_textCtrl159.Bind(wx.EVT_TEXT, self.update_watt)
        self.coat_textCtrl160.Bind(wx.EVT_TEXT, self.update_watt)
        self.coat_add.Bind(wx.EVT_CHOICE, self.update_watt)
        self.coat_enchant0.Bind(wx.EVT_CHOICE, self.update_watt)
        self.coat_enchant1.Bind(wx.EVT_CHOICE, self.update_watt)
        self.coat_textCtrl91.Bind(wx.EVT_TEXT, self.update_watt)

    def __del__(self):
        pass

    def core_coat(self, event):
        cc_choice = self.coat_core.GetSelection()
        if cc_choice == 0:
            self.coat_textCtrl81.SetValue('1172')
            self.coat_textCtrl82.SetValue('5')
            self.coat_textCtrl83.SetValue('0')
        else:
            self.coat_textCtrl81.SetValue('997')
            self.coat_textCtrl82.SetValue('4')
            self.coat_textCtrl83.SetValue('0')
        event.Skip()

    def strong_coat(self, event):
        sc_choice = self.coat_strong.GetSelection()
        if sc_choice == 0:
            self.coat_textCtrl84.SetValue('180')
            self.coat_textCtrl85.SetValue('90')
            self.coat_textCtrl86.SetValue('243')
            self.coat_textCtrl87.SetValue('80')
            self.coat_textCtrl88.SetValue('13')
            self.coat_textCtrl89.SetValue('0')
        else:
            self.coat_textCtrl84.SetValue('144')
            self.coat_textCtrl85.SetValue('72')
            self.coat_textCtrl86.SetValue('194')
            self.coat_textCtrl87.SetValue('64')
            self.coat_textCtrl88.SetValue('11')
            self.coat_textCtrl89.SetValue('0')
        event.Skip()

    def smooth_coat(self, event):
        sc1_choice = self.coat_smooth.GetSelection()
        if sc1_choice == 0:
            self.coat_textCtrl158.SetValue('840')
            self.coat_textCtrl159.SetValue('4')
            self.coat_textCtrl160.SetValue('0')
        else:
            self.coat_textCtrl158.SetValue('714')
            self.coat_textCtrl159.SetValue('3')
            self.coat_textCtrl160.SetValue('0')
        event.Skip()
        
    def update_watt(self, event):
        global coat_att
        enchant_att0 = [0]
        enchant_att1 = [0]
        addw_x = [0]
        nn0 = self.coat_enchant0.GetSelection()
        n0 = nn0 + 4
        enchant_att0 = enchant_armor0(n0)
        nn1 = int(self.coat_enchant1.GetSelection())
        if (nn1 == 0) or (nn1 == 1):
            n1 = nn1 + 6
        elif nn1 == 2:
            n1 = 4
        elif nn1 == 3 or nn1 == 4:
            n1 = nn1 - 1
        elif nn1 == 5:
            n1 = nn1
        else:
            n1 = 100
        enchant_att1 = enchant_armor1(n1)
        addw_choice = self.coat_add.GetSelection()
        addw_x = alladd(2, addw_choice)
        add_att = intplus(self.coat_textCtrl90.GetValue())
        streng_data = data_strengthen(1, intplus(self.coat_textCtrl91.GetValue()))
        coat_att[0] = enchant_att0[0] + enchant_att1[0]
        coat_att[1] = enchant_att0[3] + enchant_att1[3]
        coat_att[2] = enchant_att0[2] + enchant_att1[2]
        coat_att[3] = enchant_att0[4] + enchant_att1[4]
        coat_att[4] = streng_data[1]
        coat_att[5] = intplus(self.coat_textCtrl84.GetValue()) + addw_x[5] * add_att
        coat_att[6] = intplus(self.coat_textCtrl85.GetValue()) + addw_x[6] * add_att
        coat_att[7] = intplus(self.coat_textCtrl86.GetValue()) + addw_x[7] * add_att
        coat_att[8] = intplus(self.coat_textCtrl87.GetValue()) + addw_x[8] * add_att
        coat_att[9] = intplus(self.coat_textCtrl83.GetValue()) + intplus(self.coat_textCtrl89.GetValue()) +\
                      intplus(self.coat_textCtrl160.GetValue())
        coat_att[10] = intplus(self.coat_textCtrl82.GetValue()) + intplus(self.coat_textCtrl88.GetValue()) +\
                       intplus(self.coat_textCtrl159.GetValue()) + enchant_att0[5] + enchant_att1[5] +\
                       addw_x[9] * add_att
        coat_att[11] = intplus(self.coat_textCtrl81.GetValue()) + enchant_att0[1] + enchant_att1[1] +\
                       intplus(self.coat_textCtrl158.GetValue()) + addw_x[1] * add_att + streng_data[0]

        self.coat_staticText173.SetLabelText('攻击力: %d  防御力: %d  平衡: %d  暴击: %d  攻速: %d  追伤: %d\r\n  '
                                             '  力量: %d  敏捷: %d  智力: %d  意志: %d  解禁: %d  爆抗: %d'
                                           % (coat_att[0], coat_att[11], coat_att[1], coat_att[2], coat_att[3],
                                              coat_att[4], coat_att[5], coat_att[6], coat_att[7], coat_att[8],
                                              coat_att[9], coat_att[10]))
        event.Skip()

    def updata_coat(self, event):
        global coat_data
        coat_data = [[self.coat_core.GetSelection(), self.coat_textCtrl81.GetValue(), self.coat_textCtrl82.GetValue(),
                      self.coat_textCtrl83.GetValue()],
                     [self.coat_strong.GetSelection(), self.coat_textCtrl84.GetValue(), self.coat_textCtrl85.GetValue(),
                      self.coat_textCtrl86.GetValue(), self.coat_textCtrl87.GetValue(), self.coat_textCtrl88.GetValue(),
                      self.coat_textCtrl89.GetValue()],
                     [self.coat_smooth.GetSelection(), self.coat_textCtrl158.GetValue(),
                      self.coat_textCtrl159.GetValue(), self.coat_textCtrl160.GetValue()],
                     [self.coat_add.GetSelection(), self.coat_textCtrl90.GetValue()],
                     [self.coat_textCtrl91.GetValue(), self.coat_enchant0.GetSelection(),
                      self.coat_enchant1.GetSelection()]]
        DataThread()
        event.Skip()


class Leg(wx.Dialog):
    global leg_data
    global leg_att
    leg_data = [[0, '', '', ''],
                 [1, '', '', '', '', '', ''],
                 [1, '', '', ''],
                 [7, ''],
                 ['', 4, 7]]
    leg_att = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    def __init__(self, parent, title):
        super(Leg, self).__init__(parent, title=title, size=(600, 400))

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        gbSizerHand = wx.GridBagSizer(0, 0)
        gbSizerHand.SetFlexibleDirection(wx.BOTH)
        gbSizerHand.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        leg_choice65Choices = [u"橙色核心", u"紫色核心"]
        self.leg_core = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, leg_choice65Choices, 0)
        self.leg_core.SetSelection(leg_data[0][0])
        gbSizerHand.Add(self.leg_core, wx.GBPosition(0, 0), wx.GBSpan(1, 1),
                        wx.ALL | wx.EXPAND | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.leg_textCtrl81 = wx.TextCtrl(self, wx.ID_ANY, leg_data[0][1], wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizerHand.Add(self.leg_textCtrl81, wx.GBPosition(0, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        self.leg_textCtrl82 = wx.TextCtrl(self, wx.ID_ANY, leg_data[0][2], wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizerHand.Add(self.leg_textCtrl82, wx.GBPosition(0, 2), wx.GBSpan(1, 1), wx.ALL, 5)

        self.leg_textCtrl83 = wx.TextCtrl(self, wx.ID_ANY, leg_data[0][3], wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizerHand.Add(self.leg_textCtrl83, wx.GBPosition(0, 3), wx.GBSpan(1, 1), wx.ALL, 5)

        leg_choice66Choices = [u"橙色结实", u"紫色结实"]
        self.leg_strong = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, leg_choice66Choices, 0)
        self.leg_strong.SetSelection(leg_data[1][0])
        gbSizerHand.Add(self.leg_strong, wx.GBPosition(1, 0), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        self.leg_textCtrl84 = wx.TextCtrl(self, wx.ID_ANY, leg_data[1][1], wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizerHand.Add(self.leg_textCtrl84, wx.GBPosition(1, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        self.leg_textCtrl85 = wx.TextCtrl(self, wx.ID_ANY, leg_data[1][2], wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizerHand.Add(self.leg_textCtrl85, wx.GBPosition(1, 2), wx.GBSpan(1, 1), wx.ALL, 5)

        self.leg_textCtrl86 = wx.TextCtrl(self, wx.ID_ANY, leg_data[1][3], wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizerHand.Add(self.leg_textCtrl86, wx.GBPosition(1, 3), wx.GBSpan(1, 1), wx.ALL, 5)

        self.leg_textCtrl87 = wx.TextCtrl(self, wx.ID_ANY, leg_data[1][4], wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizerHand.Add(self.leg_textCtrl87, wx.GBPosition(2, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        self.leg_textCtrl88 = wx.TextCtrl(self, wx.ID_ANY, leg_data[1][5], wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizerHand.Add(self.leg_textCtrl88, wx.GBPosition(2, 2), wx.GBSpan(1, 1), wx.ALL, 5)

        self.leg_textCtrl89 = wx.TextCtrl(self, wx.ID_ANY, leg_data[1][6], wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizerHand.Add(self.leg_textCtrl89, wx.GBPosition(2, 3), wx.GBSpan(1, 1), wx.ALL, 5)

        leg_choice100Choices = [u"橙色光滑", u"紫色光滑"]
        self.leg_smooth = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, leg_choice100Choices, 0)
        self.leg_smooth.SetSelection(leg_data[2][0])
        gbSizerHand.Add(self.leg_smooth, wx.GBPosition(3, 0), wx.GBSpan(1, 1), wx.ALL, 5)

        self.leg_textCtrl158 = wx.TextCtrl(self, wx.ID_ANY, leg_data[2][1], wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizerHand.Add(self.leg_textCtrl158, wx.GBPosition(3, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        self.leg_textCtrl159 = wx.TextCtrl(self, wx.ID_ANY, leg_data[2][2], wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizerHand.Add(self.leg_textCtrl159, wx.GBPosition(3, 2), wx.GBSpan(1, 1), wx.ALL, 5)

        self.leg_textCtrl160 = wx.TextCtrl(self, wx.ID_ANY, leg_data[2][3], wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizerHand.Add(self.leg_textCtrl160, wx.GBPosition(3, 3), wx.GBSpan(1, 1), wx.ALL, 5)

        leg_choice67Choices = [u"爆抗", u"防御力", u"意志", u"敏捷", u"生命力", u"智力", u"力量", u"无"]
        self.leg_add = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, leg_choice67Choices, 0)
        self.leg_add.SetSelection(leg_data[3][0])
        gbSizerHand.Add(self.leg_add, wx.GBPosition(5, 0), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        self.leg_textCtrl90 = wx.TextCtrl(self, wx.ID_ANY, leg_data[3][1], wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizerHand.Add(self.leg_textCtrl90, wx.GBPosition(5, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        self.leg_staticText83 = wx.StaticText(self, wx.ID_ANY, u"强化等级", wx.DefaultPosition, wx.DefaultSize,
                                              wx.ALIGN_CENTRE)
        self.leg_staticText83.Wrap(-1)
        gbSizerHand.Add(self.leg_staticText83, wx.GBPosition(6, 0), wx.GBSpan(1, 1),
                        wx.ALL | wx.EXPAND | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.leg_textCtrl91 = wx.TextCtrl(self, wx.ID_ANY, leg_data[4][0], wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizerHand.Add(self.leg_textCtrl91, wx.GBPosition(6, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        leg_choice68Choices = [u"冷静的", u"记忆的", u"保持平衡的", u"努力地", wx.EmptyString]
        self.leg_enchant0 = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, leg_choice68Choices, 0)
        self.leg_enchant0.SetSelection(leg_data[4][1])
        gbSizerHand.Add(self.leg_enchant0, wx.GBPosition(6, 2), wx.GBSpan(1, 1), wx.ALL, 5)

        leg_choice69Choices = [u"远征", u"热忱", u"落叶", u"茉莉花", u"致命", u"抵抗", u"犰狳", wx.EmptyString]
        self.leg_enchant1 = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, leg_choice69Choices, 0)
        self.leg_enchant1.SetSelection(leg_data[4][2])
        gbSizerHand.Add(self.leg_enchant1, wx.GBPosition(6, 3), wx.GBSpan(1, 1), wx.ALL, 5)

        self.leg_staticText173 = wx.StaticText(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                                wx.ALIGN_CENTRE)
        self.leg_staticText173.Wrap(-1)
        gbSizerHand.Add(self.leg_staticText173, wx.GBPosition(7, 0), wx.GBSpan(2, 4), wx.ALL | wx.EXPAND, 5)

        leg_sdbSizer3 = wx.StdDialogButtonSizer()
        self.leg_sdbSizer3OK = wx.Button(self, wx.ID_OK)
        leg_sdbSizer3.AddButton(self.leg_sdbSizer3OK)
        self.leg_sdbSizer3Cancel = wx.Button(self, wx.ID_CANCEL)
        leg_sdbSizer3.AddButton(self.leg_sdbSizer3Cancel)
        leg_sdbSizer3.Realize()

        gbSizerHand.Add(leg_sdbSizer3, wx.GBPosition(10, 3), wx.GBSpan(1, 1), wx.EXPAND, 5)

        self.SetSizer(gbSizerHand)
        self.Layout()

        self.Centre(wx.BOTH)

        self.leg_core.Bind(wx.EVT_CHOICE, self.core_leg)
        self.leg_strong.Bind(wx.EVT_CHOICE, self.strong_leg)
        self.leg_smooth.Bind(wx.EVT_CHOICE, self.smooth_leg)
        self.leg_sdbSizer3OK.Bind(wx.EVT_BUTTON, self.updata_leg)
        self.leg_textCtrl81.Bind(wx.EVT_TEXT, self.update_watt)
        self.leg_textCtrl82.Bind(wx.EVT_TEXT, self.update_watt)
        self.leg_textCtrl83.Bind(wx.EVT_TEXT, self.update_watt)
        self.leg_textCtrl84.Bind(wx.EVT_TEXT, self.update_watt)
        self.leg_textCtrl85.Bind(wx.EVT_TEXT, self.update_watt)
        self.leg_textCtrl86.Bind(wx.EVT_TEXT, self.update_watt)
        self.leg_textCtrl87.Bind(wx.EVT_TEXT, self.update_watt)
        self.leg_textCtrl88.Bind(wx.EVT_TEXT, self.update_watt)
        self.leg_textCtrl89.Bind(wx.EVT_TEXT, self.update_watt)
        self.leg_textCtrl90.Bind(wx.EVT_TEXT, self.update_watt)
        self.leg_textCtrl158.Bind(wx.EVT_TEXT, self.update_watt)
        self.leg_textCtrl159.Bind(wx.EVT_TEXT, self.update_watt)
        self.leg_textCtrl160.Bind(wx.EVT_TEXT, self.update_watt)
        self.leg_add.Bind(wx.EVT_CHOICE, self.update_watt)
        self.leg_enchant0.Bind(wx.EVT_CHOICE, self.update_watt)
        self.leg_enchant1.Bind(wx.EVT_CHOICE, self.update_watt)
        self.leg_textCtrl91.Bind(wx.EVT_TEXT, self.update_watt)

    def __del__(self):
        pass

    def core_leg(self, event):
        cl_choice = self.leg_core.GetSelection()
        if cl_choice == 0:
            self.leg_textCtrl81.SetValue('1075')
            self.leg_textCtrl82.SetValue('8')
            self.leg_textCtrl83.SetValue('0')
        else:
            self.leg_textCtrl81.SetValue('913')
            self.leg_textCtrl82.SetValue('6')
            self.leg_textCtrl83.SetValue('0')
        event.Skip()

    def strong_leg(self, event):
        sl_choice = self.leg_strong.GetSelection()
        if sl_choice == 0:
            self.leg_textCtrl84.SetValue('180')
            self.leg_textCtrl85.SetValue('90')
            self.leg_textCtrl86.SetValue('243')
            self.leg_textCtrl87.SetValue('80')
            self.leg_textCtrl88.SetValue('13')
            self.leg_textCtrl89.SetValue('0')
        else:
            self.leg_textCtrl84.SetValue('144')
            self.leg_textCtrl85.SetValue('72')
            self.leg_textCtrl86.SetValue('194')
            self.leg_textCtrl87.SetValue('64')
            self.leg_textCtrl88.SetValue('11')
            self.leg_textCtrl89.SetValue('0')
        event.Skip()

    def smooth_leg(self, event):
        sl1_choice = self.leg_smooth.GetSelection()
        if sl1_choice == 0:
            self.leg_textCtrl158.SetValue('840')
            self.leg_textCtrl159.SetValue('4')
            self.leg_textCtrl160.SetValue('0')
        else:
            self.leg_textCtrl158.SetValue('714')
            self.leg_textCtrl159.SetValue('3')
            self.leg_textCtrl160.SetValue('0')
        event.Skip()
        
    def update_watt(self, event):
        global leg_att
        enchant_att0 = [0]
        enchant_att1 = [0]
        addw_x = [0]
        nn0 = self.leg_enchant0.GetSelection()
        if nn0 == 1:
            n0 = 2
        elif nn0 == 2 or nn0 == 3 or nn0 == 4:
            n0 = nn0 + 3
        else:
            n0 = nn0
        enchant_att0 = enchant_armor0(n0)
        nn1 = int(self.leg_enchant1.GetSelection())
        if (nn1 <= 4) & (nn1 > 0):
            n1 = nn1 + 1
        elif nn1 == 0:
            n1 = 1
        else:
            n1 = nn1 + 3
        enchant_att1 = enchant_armor1(n1)
        addw_choice = self.leg_add.GetSelection()
        addw_x = alladd(2, addw_choice)
        add_att = intplus(self.leg_textCtrl90.GetValue())
        streng_data = data_strengthen(1, intplus(self.leg_textCtrl91.GetValue()))
        leg_att[0] = enchant_att0[0] + enchant_att1[0]
        leg_att[1] = enchant_att0[3] + enchant_att1[3]
        leg_att[2] = enchant_att0[2] + enchant_att1[2]
        leg_att[3] = enchant_att0[4] + enchant_att1[4]
        leg_att[4] = streng_data[1]
        leg_att[5] = intplus(self.leg_textCtrl84.GetValue()) + addw_x[5] * add_att
        leg_att[6] = intplus(self.leg_textCtrl85.GetValue()) + addw_x[6] * add_att
        leg_att[7] = intplus(self.leg_textCtrl86.GetValue()) + addw_x[7] * add_att
        leg_att[8] = intplus(self.leg_textCtrl87.GetValue()) + addw_x[8] * add_att
        leg_att[9] = intplus(self.leg_textCtrl83.GetValue()) + intplus(self.leg_textCtrl89.GetValue()) +\
                      intplus(self.leg_textCtrl160.GetValue())
        leg_att[10] = intplus(self.leg_textCtrl82.GetValue()) + intplus(self.leg_textCtrl88.GetValue()) +\
                       intplus(self.leg_textCtrl159.GetValue()) + enchant_att0[5] + enchant_att1[5] +\
                       addw_x[9] * add_att
        leg_att[11] = intplus(self.leg_textCtrl81.GetValue()) + enchant_att0[1] + enchant_att1[1] +\
                       intplus(self.leg_textCtrl158.GetValue()) + addw_x[1] * add_att + streng_data[0]

        self.leg_staticText173.SetLabelText('攻击力: %d  防御力: %d  平衡: %d  暴击: %d  攻速: %d  追伤: %d\r\n'
                                            '力量: %d  敏捷: %d  智力: %d  意志: %d  解禁: %d  爆抗: %d'
                                            % (leg_att[0], leg_att[11], leg_att[1], leg_att[2], leg_att[3],
                                              leg_att[4], leg_att[5], leg_att[6], leg_att[7], leg_att[8],
                                              leg_att[9], leg_att[10]))
        event.Skip()

    def updata_leg(self, event):
        global leg_data
        leg_data = [[self.leg_core.GetSelection(), self.leg_textCtrl81.GetValue(), self.leg_textCtrl82.GetValue(),
                     self.leg_textCtrl83.GetValue()],
                    [self.leg_strong.GetSelection(), self.leg_textCtrl84.GetValue(), self.leg_textCtrl85.GetValue(),
                     self.leg_textCtrl86.GetValue(), self.leg_textCtrl87.GetValue(), self.leg_textCtrl88.GetValue(),
                     self.leg_textCtrl89.GetValue()],
                    [self.leg_smooth.GetSelection(), self.leg_textCtrl158.GetValue(),
                     self.leg_textCtrl159.GetValue(), self.leg_textCtrl160.GetValue()],
                    [self.leg_add.GetSelection(), self.leg_textCtrl90.GetValue()],
                    [self.leg_textCtrl91.GetValue(), self.leg_enchant0.GetSelection(),
                     self.leg_enchant1.GetSelection()]]
        DataThread()
        event.Skip()


class Belt(wx.Dialog):
    global belt_data
    global belt_att
    belt_att = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    belt_data = [[2, 1],
                 [10, ''],
                 [4, 3],
                 ['', '', '', '', '', '', '', '', '', '']]

    def __init__(self, parent, title):
        super(Belt, self).__init__(parent, title=title, size=(600, 400))

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        gbSizer17 = wx.GridBagSizer(0, 0)
        gbSizer17.SetFlexibleDirection(wx.BOTH)
        gbSizer17.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        belt_radioBox4Choices = [u"绝望之腰带", u"悲痛之腰带", u"我没有腰带"]
        self.belt_radioBox4 = wx.RadioBox(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                          belt_radioBox4Choices, 1, wx.RA_SPECIFY_COLS)
        self.belt_radioBox4.SetSelection(belt_data[0][0])
        gbSizer17.Add(self.belt_radioBox4, wx.GBPosition(0, 0), wx.GBSpan(3, 1), wx.ALL, 5)

        belt_choice114Choices = [u"暴击", u"平衡", u"攻速", u"智力", u"力量", u"意志", u"敏捷", u"爆抗", u"防御",
                                 u"无"]
        self.belt_add = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, belt_choice114Choices, 0)
        self.belt_add.SetSelection(belt_data[1][0])
        gbSizer17.Add(self.belt_add, wx.GBPosition(2, 1), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        self.belt_textCtrl198 = wx.TextCtrl(self, wx.ID_ANY, belt_data[1][1], wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer17.Add(self.belt_textCtrl198, wx.GBPosition(2, 2), wx.GBSpan(1, 1), wx.ALL, 5)

        belt_choice115Choices = [u"隐隐的", u"小巧的", u"迅速的", u"有意义的", wx.EmptyString]
        self.belt_enchant0 = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, belt_choice115Choices, 0)
        self.belt_enchant0.SetSelection(belt_data[2][0])
        gbSizer17.Add(self.belt_enchant0, wx.GBPosition(2, 3), wx.GBSpan(1, 1), wx.ALL, 5)

        belt_choice116Choices = [u"热情", u"心灵", u"活力", wx.EmptyString]
        self.belt_enchant1 = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, belt_choice116Choices, 0)
        self.belt_enchant1.SetSelection(belt_data[2][1])
        gbSizer17.Add(self.belt_enchant1, wx.GBPosition(2, 4), wx.GBSpan(1, 1), wx.ALL, 5)

        # belt_radioBox5Choices = [u"1星", u"2星", u"3星", u"4星", u"5星"]
        # self.belt_radioBox5 = wx.RadioBox(self, wx.ID_ANY, u"品质", wx.DefaultPosition, wx.DefaultSize,
        #                                   belt_radioBox5Choices, 1, wx.RA_SPECIFY_ROWS)
        # self.belt_radioBox5.SetSelection(belt_data[0][1])
        # gbSizer17.Add(self.belt_radioBox5, wx.GBPosition(0, 1), wx.GBSpan(2, 6), wx.ALL, 5)

        belt_text189 = "伤害平衡:" + str(belt_data[3][0])
        self.belt_textCtrl189 = wx.TextCtrl(self, wx.ID_ANY, belt_text189, wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer17.Add(self.belt_textCtrl189, wx.GBPosition(3, 0), wx.GBSpan(1, 1), wx.ALL, 5)

        belt_text190 = "暴击:" + str(belt_data[3][1])
        self.belt_textCtrl190 = wx.TextCtrl(self, wx.ID_ANY, belt_text190, wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer17.Add(self.belt_textCtrl190, wx.GBPosition(3, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        belt_text191 = "攻击速度:" + str(belt_data[3][2])
        self.belt_textCtrl191 = wx.TextCtrl(self, wx.ID_ANY, belt_text191, wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer17.Add(self.belt_textCtrl191, wx.GBPosition(3, 2), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        belt_text192 = "防御力:" + str(belt_data[3][3])
        self.belt_textCtrl192 = wx.TextCtrl(self, wx.ID_ANY, belt_text192, wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer17.Add(self.belt_textCtrl192, wx.GBPosition(3, 3), wx.GBSpan(1, 1), wx.ALL, 5)

        belt_text193 = "力量:" + str(belt_data[3][4])
        self.belt_textCtrl193 = wx.TextCtrl(self, wx.ID_ANY, belt_text193, wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer17.Add(self.belt_textCtrl193, wx.GBPosition(3, 4), wx.GBSpan(1, 1), wx.ALL, 5)

        belt_text194 = "敏捷:" + str(belt_data[3][5])
        self.belt_textCtrl194 = wx.TextCtrl(self, wx.ID_ANY, belt_text194, wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer17.Add(self.belt_textCtrl194, wx.GBPosition(4, 0), wx.GBSpan(1, 1), wx.ALL, 5)

        belt_text195 = "智力:" + str(belt_data[3][6])
        self.belt_textCtrl195 = wx.TextCtrl(self, wx.ID_ANY, belt_text195, wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer17.Add(self.belt_textCtrl195, wx.GBPosition(4, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        belt_text196 = "意志:" + str(belt_data[3][7])
        self.belt_textCtrl196 = wx.TextCtrl(self, wx.ID_ANY, belt_text196, wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer17.Add(self.belt_textCtrl196, wx.GBPosition(4, 2), wx.GBSpan(1, 1), wx.ALL, 5)

        belt_text197 = "暴击抵抗:" + str(belt_data[3][8])
        self.belt_textCtrl197 = wx.TextCtrl(self, wx.ID_ANY, belt_text197, wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer17.Add(self.belt_textCtrl197, wx.GBPosition(4, 3), wx.GBSpan(1, 1), wx.ALL, 5)

        belt_text199 = "生命力:" + str(belt_data[3][9])
        self.belt_textCtrl199 = wx.TextCtrl(self, wx.ID_ANY, belt_text199, wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer17.Add(self.belt_textCtrl199, wx.GBPosition(4, 4), wx.GBSpan(1, 1), wx.ALL, 5)

        belt_sdbSizer12 = wx.StdDialogButtonSizer()
        self.belt_sdbSizer12OK = wx.Button(self, wx.ID_OK)
        belt_sdbSizer12.AddButton(self.belt_sdbSizer12OK)
        self.belt_sdbSizer12Cancel = wx.Button(self, wx.ID_CANCEL)
        belt_sdbSizer12.AddButton(self.belt_sdbSizer12Cancel)
        belt_sdbSizer12.Realize()

        gbSizer17.Add(belt_sdbSizer12, wx.GBPosition(6, 3), wx.GBSpan(1, 2), wx.EXPAND, 5)

        self.SetSizer(gbSizer17)
        self.Layout()

        self.Centre(wx.BOTH)

        self.belt_sdbSizer12OK.Bind(wx.EVT_BUTTON, self.updata_belt)
        self.belt_radioBox4.Bind(wx.EVT_RADIOBOX, self.update_att)
        # self.belt_radioBox5.Bind(wx.EVT_RADIOBOX, self.update_att)
        self.belt_enchant0.Bind(wx.EVT_CHOICE, self.update_att)
        self.belt_enchant1.Bind(wx.EVT_CHOICE, self.update_att)
        self.belt_radioBox4.Bind(wx.EVT_RADIOBOX, self.update_att)
        self.belt_textCtrl198.Bind(wx.EVT_TEXT, self.update_att)
        self.belt_add.Bind(wx.EVT_CHOICE, self.update_att)

    def __del__(self):
        pass

    def update_att(self, event):
        nn0 = self.belt_enchant0.GetSelection()
        if nn0 == 0:
            n0 = 1
        elif (nn0 >= 1) & (nn0 <= 3):
            n0 = nn0 + 2
        else:
            n0 = 100
        enchant_aat0 = enchant_jewelry0(n0)
        nn1 = self.belt_enchant1.GetSelection()
        if nn1 != 3:
            n1 = nn1 + 1
        else:
            n1 = 100
        enchant_aat1 = enchant_jewelry1(n1)

        belt_choice = self.belt_radioBox4.GetSelection()
        if belt_choice == 0:
            belt_init = [2, 0, 0, 0, 140, 90, 0, 100, 0, 0]
        elif belt_choice == 1:
            belt_init = [2, 0, 0, 0, 0, 90, 180, 100, 0, 0]
        else:
            belt_init = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        addw_choice = self.belt_add.GetSelection()
        addw_x = alladd(3, addw_choice)
        add_att = intplus(self.belt_textCtrl198.GetValue())
        all_add = [(enchant_aat0[3] + enchant_aat1[3] + addw_x[3]*add_att),
                   (enchant_aat0[2] + enchant_aat1[2] + addw_x[2] * add_att),
                   (enchant_aat0[4] + enchant_aat1[4] + addw_x[4] * add_att),
                   (enchant_aat0[1] + enchant_aat1[1] + addw_x[1] * add_att),
                   (addw_x[5] * add_att),
                   (addw_x[6] * add_att),
                   (addw_x[7] * add_att),
                   (addw_x[8] * add_att),
                   (enchant_aat0[5] + enchant_aat1[5] + addw_x[9] * add_att),
                   (enchant_aat0[6] + enchant_aat1[6] + addw_x[1] * add_att)]
        belt_data[3] = numpy.array(belt_init) + numpy.array(all_add)
        belt189 = "伤害平衡:" + str(belt_data[3][0])
        self.belt_textCtrl189.SetValue(belt189)
        belt_text190 = "暴击:" + str(belt_data[3][1])
        self.belt_textCtrl190.SetValue(belt_text190)
        belt_text191 = "攻击速度:" + str(belt_data[3][2])
        self.belt_textCtrl191.SetValue(belt_text191)
        belt_text192 = "防御力:" + str(belt_data[3][3])
        self.belt_textCtrl192.SetValue(belt_text192)
        belt_text193 = "力量:" + str(belt_data[3][4])
        self.belt_textCtrl193.SetValue(belt_text193)
        belt_text194 = "敏捷:" + str(belt_data[3][5])
        self.belt_textCtrl194.SetValue(belt_text194)
        belt_text195 = "智力:" + str(belt_data[3][6])
        self.belt_textCtrl195.SetValue(belt_text195)
        belt_text196 = "意志:" + str(belt_data[3][7])
        self.belt_textCtrl196.SetValue(belt_text196)
        belt_text197 = "暴击抵抗:" + str(belt_data[3][8])
        self.belt_textCtrl197.SetValue(belt_text197)
        belt_text199 = "生命力:" + str(belt_data[3][9])
        self.belt_textCtrl199.SetValue(belt_text199)
        event.Skip()

    def updata_belt(self, event):
        global belt_data
        global belt_att
        belt_data = [[self.belt_radioBox4.GetSelection()],   # self.belt_radioBox5.GetSelection()],
                     [self.belt_add.GetSelection(), self.belt_textCtrl198.GetValue()],
                     [self.belt_enchant0.GetSelection(), self.belt_enchant1.GetSelection()],
                     [intplus(self.belt_textCtrl189.GetValue()), intplus(self.belt_textCtrl190.GetValue()),
                      intplus(self.belt_textCtrl191.GetValue()), intplus(self.belt_textCtrl192.GetValue()),
                      intplus(self.belt_textCtrl193.GetValue()), intplus(self.belt_textCtrl194.GetValue()),
                      intplus(self.belt_textCtrl195.GetValue()), intplus(self.belt_textCtrl196.GetValue()),
                      intplus(self.belt_textCtrl197.GetValue()), intplus(self.belt_textCtrl199.GetValue())]]
        belt_att[1] = belt_data[3][0]
        belt_att[2] = belt_data[3][1]
        belt_att[3] = belt_data[3][2]
        belt_att[5] = belt_data[3][4]
        belt_att[6] = belt_data[3][5]
        belt_att[7] = belt_data[3][6]
        belt_att[8] = belt_data[3][7]
        belt_att[10] = belt_data[3][8]
        belt_att[11] = belt_data[3][3]
        DataThread()
        event.Skip()


class Earring(wx.Dialog):
    global earring_data
    global earring_att
    earring_att = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    earring_data = [[2, 1],
                    [10, ''],
                    [3, 3],
                    ['', '', '', '', '', '', '', '', '', '']]

    def __init__(self, parent, title):
        super(Earring, self).__init__(parent, title=title, size=(600, 400))

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        gbSizer17 = wx.GridBagSizer(0, 0)
        gbSizer17.SetFlexibleDirection(wx.BOTH)
        gbSizer17.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        earring_radioBox4Choices = [u"无罪者的眼泪", u"无罪者的哭泣", u"我没有耳环"]
        self.earring_radioBox4 = wx.RadioBox(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                             earring_radioBox4Choices, 1, wx.RA_SPECIFY_COLS)
        self.earring_radioBox4.SetSelection(earring_data[0][0])
        gbSizer17.Add(self.earring_radioBox4, wx.GBPosition(0, 0), wx.GBSpan(3, 1), wx.ALL, 5)

        earring_choice114Choices = [u"暴击", u"平衡", u"攻速", u"智力", u"力量", u"意志", u"敏捷", u"爆抗", u"防御",
                                    u"无"]
        self.earring_add = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, earring_choice114Choices, 0)
        self.earring_add.SetSelection(earring_data[1][0])
        gbSizer17.Add(self.earring_add, wx.GBPosition(2, 1), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        self.earring_textCtrl198 = wx.TextCtrl(self, wx.ID_ANY, earring_data[1][1], wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer17.Add(self.earring_textCtrl198, wx.GBPosition(2, 2), wx.GBSpan(1, 1), wx.ALL, 5)

        earring_choice115Choices = [u"迅速的", u"有意义的", u"多疑的", wx.EmptyString]
        self.earring_enchant0 = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                          earring_choice115Choices, 0)
        self.earring_enchant0.SetSelection(earring_data[2][0])
        gbSizer17.Add(self.earring_enchant0, wx.GBPosition(2, 3), wx.GBSpan(1, 1), wx.ALL, 5)

        earring_choice116Choices = [u"热情", u"心灵", u"活力", wx.EmptyString]
        self.earring_enchant1 = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                          earring_choice116Choices, 0)
        self.earring_enchant1.SetSelection(earring_data[2][1])
        gbSizer17.Add(self.earring_enchant1, wx.GBPosition(2, 4), wx.GBSpan(1, 1), wx.ALL, 5)

        # earring_radioBox5Choices = [u"1星", u"2星", u"3星", u"4星", u"5星"]
        # self.earring_radioBox5 = wx.RadioBox(self, wx.ID_ANY, u"品质", wx.DefaultPosition, wx.DefaultSize,
        #                                      earring_radioBox5Choices, 1, wx.RA_SPECIFY_ROWS)
        # self.earring_radioBox5.SetSelection(earring_data[0][1])
        # gbSizer17.Add(self.earring_radioBox5, wx.GBPosition(0, 1), wx.GBSpan(2, 6), wx.ALL, 5)

        earring_text189 = "伤害平衡:" + str(earring_data[3][0])
        self.earring_textCtrl189 = wx.TextCtrl(self, wx.ID_ANY, earring_text189, wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer17.Add(self.earring_textCtrl189, wx.GBPosition(3, 0), wx.GBSpan(1, 1), wx.ALL, 5)

        earring_text190 = "暴击:" + str(earring_data[3][1])
        self.earring_textCtrl190 = wx.TextCtrl(self, wx.ID_ANY, earring_text190, wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer17.Add(self.earring_textCtrl190, wx.GBPosition(3, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        earring_text191 = "攻击速度:" + str(earring_data[3][2])
        self.earring_textCtrl191 = wx.TextCtrl(self, wx.ID_ANY, earring_text191, wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer17.Add(self.earring_textCtrl191, wx.GBPosition(3, 2), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        earring_text192 = "防御力:" + str(earring_data[3][3])
        self.earring_textCtrl192 = wx.TextCtrl(self, wx.ID_ANY, earring_text192, wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer17.Add(self.earring_textCtrl192, wx.GBPosition(3, 3), wx.GBSpan(1, 1), wx.ALL, 5)

        earring_text193 = "力量/智力:" + str(earring_data[3][4])
        self.earring_textCtrl193 = wx.TextCtrl(self, wx.ID_ANY, earring_text193, wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer17.Add(self.earring_textCtrl193, wx.GBPosition(3, 4), wx.GBSpan(1, 1), wx.ALL, 5)

        earring_text194 = "敏捷:" + str(earring_data[3][5])
        self.earring_textCtrl194 = wx.TextCtrl(self, wx.ID_ANY, earring_text194, wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer17.Add(self.earring_textCtrl194, wx.GBPosition(4, 0), wx.GBSpan(1, 1), wx.ALL, 5)

        earring_text195 = "意志:" + str(earring_data[3][6])
        self.earring_textCtrl195 = wx.TextCtrl(self, wx.ID_ANY, earring_text195, wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer17.Add(self.earring_textCtrl195, wx.GBPosition(4, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        earring_text196 = "体力:" + str(earring_data[3][7])
        self.earring_textCtrl196 = wx.TextCtrl(self, wx.ID_ANY, earring_text196, wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer17.Add(self.earring_textCtrl196, wx.GBPosition(4, 2), wx.GBSpan(1, 1), wx.ALL, 5)

        earring_text197 = "暴击抵抗:" + str(earring_data[3][8])
        self.earring_textCtrl197 = wx.TextCtrl(self, wx.ID_ANY, earring_text197, wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer17.Add(self.earring_textCtrl197, wx.GBPosition(4, 3), wx.GBSpan(1, 1), wx.ALL, 5)

        earring_text199 = "生命力:" + str(earring_data[3][9])
        self.earring_textCtrl199 = wx.TextCtrl(self, wx.ID_ANY, earring_text199, wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer17.Add(self.earring_textCtrl199, wx.GBPosition(4, 4), wx.GBSpan(1, 1), wx.ALL, 5)

        earring_sdbSizer12 = wx.StdDialogButtonSizer()
        self.earring_sdbSizer12OK = wx.Button(self, wx.ID_OK)
        earring_sdbSizer12.AddButton(self.earring_sdbSizer12OK)
        self.earring_sdbSizer12Cancel = wx.Button(self, wx.ID_CANCEL)
        earring_sdbSizer12.AddButton(self.earring_sdbSizer12Cancel)
        earring_sdbSizer12.Realize()

        gbSizer17.Add(earring_sdbSizer12, wx.GBPosition(6, 3), wx.GBSpan(1, 2), wx.EXPAND, 5)

        self.SetSizer(gbSizer17)
        self.Layout()

        self.Centre(wx.BOTH)

        self.earring_sdbSizer12OK.Bind(wx.EVT_BUTTON, self.updata_earring)
        self.earring_radioBox4.Bind(wx.EVT_RADIOBOX, self.update_att)
        # self.earring_radioBox5.Bind(wx.EVT_RADIOBOX, self.update_att)
        self.earring_enchant0.Bind(wx.EVT_CHOICE, self.update_att)
        self.earring_enchant1.Bind(wx.EVT_CHOICE, self.update_att)
        self.earring_radioBox4.Bind(wx.EVT_RADIOBOX, self.update_att)
        self.earring_textCtrl198.Bind(wx.EVT_TEXT, self.update_att)
        self.earring_add.Bind(wx.EVT_CHOICE, self.update_att)

    def __del__(self):
        pass

    def update_att(self, event):
        nn0 = self.earring_enchant0.GetSelection()
        if nn0 != 3:
            n0 = nn0 + 4
        else:
            n0 = 100
        enchant_aat0 = enchant_jewelry0(n0)
        nn1 = self.earring_enchant1.GetSelection()
        if nn1 != 3:
            n1 = nn1 + 1
        else:
            n1 = 100
        enchant_aat1 = enchant_jewelry1(n1)

        earring_choice = self.earring_radioBox4.GetSelection()
        if earring_choice == 0:
            earring_init = [0, 1, 0, 0, 120, 45, 0, 53, 0, 0]
        elif earring_choice == 1:
            earring_init = [0, 1, 0, 0, 0, 45, 140, 53, 0, 0]
        else:
            earring_init = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        addw_choice = self.earring_add.GetSelection()
        addw_x = alladd(3, addw_choice)
        add_att = intplus(self.earring_textCtrl198.GetValue())
        all_add = [(enchant_aat0[3] + enchant_aat1[3] + addw_x[3]*add_att),
                   (enchant_aat0[2] + enchant_aat1[2] + addw_x[2] * add_att),
                   (enchant_aat0[4] + enchant_aat1[4] + addw_x[4] * add_att),
                   (enchant_aat0[1] + enchant_aat1[1] + addw_x[1] * add_att),
                   (addw_x[5] * add_att),
                   (addw_x[6] * add_att),
                   (addw_x[7] * add_att),
                   (addw_x[8] * add_att),
                   (enchant_aat0[5] + enchant_aat1[5] + addw_x[9] * add_att),
                   (enchant_aat0[6] + enchant_aat1[6] + addw_x[1] * add_att)]
        earring_data[3] = numpy.array(earring_init) + numpy.array(all_add)
        earring189 = "伤害平衡:" + str(earring_data[3][0])
        self.earring_textCtrl189.SetValue(earring189)
        earring_text190 = "暴击:" + str(earring_data[3][1])
        self.earring_textCtrl190.SetValue(earring_text190)
        earring_text191 = "攻击速度:" + str(earring_data[3][2])
        self.earring_textCtrl191.SetValue(earring_text191)
        earring_text192 = "防御力:" + str(earring_data[3][3])
        self.earring_textCtrl192.SetValue(earring_text192)
        earring_text193 = "力量:" + str(earring_data[3][4])
        self.earring_textCtrl193.SetValue(earring_text193)
        earring_text194 = "敏捷:" + str(earring_data[3][5])
        self.earring_textCtrl194.SetValue(earring_text194)
        earring_text195 = "智力:" + str(earring_data[3][6])
        self.earring_textCtrl195.SetValue(earring_text195)
        earring_text196 = "意志:" + str(earring_data[3][7])
        self.earring_textCtrl196.SetValue(earring_text196)
        earring_text197 = "暴击抵抗:" + str(earring_data[3][8])
        self.earring_textCtrl197.SetValue(earring_text197)
        earring_text199 = "生命力:" + str(earring_data[3][9])
        self.earring_textCtrl199.SetValue(earring_text199)
        event.Skip()

    def updata_earring(self, event):
        global earring_data
        global earring_att
        earring_data = [[self.earring_radioBox4.GetSelection()], # self.earring_radioBox5.GetSelection()],
                     [self.earring_add.GetSelection(), self.earring_textCtrl198.GetValue()],
                     [self.earring_enchant0.GetSelection(), self.earring_enchant1.GetSelection()],
                     [intplus(self.earring_textCtrl189.GetValue()), intplus(self.earring_textCtrl190.GetValue()),
                      intplus(self.earring_textCtrl191.GetValue()), intplus(self.earring_textCtrl192.GetValue()),
                      intplus(self.earring_textCtrl193.GetValue()), intplus(self.earring_textCtrl194.GetValue()),
                      intplus(self.earring_textCtrl195.GetValue()), intplus(self.earring_textCtrl196.GetValue()),
                      intplus(self.earring_textCtrl197.GetValue()), intplus(self.earring_textCtrl199.GetValue())]]
        earring_att[1] = earring_data[3][0]
        earring_att[2] = earring_data[3][1]
        earring_att[3] = earring_data[3][2]
        earring_att[5] = earring_data[3][4]
        earring_att[6] = earring_data[3][5]
        earring_att[7] = earring_data[3][6]
        earring_att[8] = earring_data[3][7]
        earring_att[10] = earring_data[3][8]
        earring_att[11] = earring_data[3][3]
        DataThread()
        event.Skip()


class Brooch(wx.Dialog):
    global brooch_data
    global brooch_att
    brooch_att = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    brooch_data = [[5, 1],
                   [10, ''],
                   [5, 4],
                   ['', '', '', '', '', '', '', '', '', '']]

    def __init__(self, parent, title):
        super(Brooch, self).__init__(parent, title=title, size=(600, 400))

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        gbSizer17 = wx.GridBagSizer(0, 0)
        gbSizer17.SetFlexibleDirection(wx.BOTH)
        gbSizer17.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        brooch_radioBox4Choices = [u"月光蓝宝石胸针", u"元素晶核胸针", u"白色小猫",
                                   u"蓝色小猫", u"古代水晶", u"我没有胸针"]
        self.brooch_radioBox4 = wx.RadioBox(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                            brooch_radioBox4Choices, 1, wx.RA_SPECIFY_COLS)
        self.brooch_radioBox4.SetSelection(brooch_data[0][0])
        gbSizer17.Add(self.brooch_radioBox4, wx.GBPosition(0, 0), wx.GBSpan(3, 1), wx.ALL, 5)

        brooch_choice114Choices = [u"暴击", u"平衡", u"攻速", u"智力", u"力量", u"意志", u"敏捷", u"爆抗", u"防御",
                                   u"生命力", u"无"]
        self.brooch_add = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, brooch_choice114Choices, 0)
        self.brooch_add.SetSelection(brooch_data[1][0])
        gbSizer17.Add(self.brooch_add, wx.GBPosition(2, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        self.brooch_textCtrl198 = wx.TextCtrl(self, wx.ID_ANY, brooch_data[1][1], wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer17.Add(self.brooch_textCtrl198, wx.GBPosition(2, 2), wx.GBSpan(1, 1), wx.ALL, 5)

        brooch_choice115Choices = [u"星光", u"宝物猎人的", u"迅速的", u"有意义的", u"多疑的", wx.EmptyString]
        self.brooch_enchant0 = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                         brooch_choice115Choices, 0)
        self.brooch_enchant0.SetSelection(brooch_data[2][0])
        gbSizer17.Add(self.brooch_enchant0, wx.GBPosition(2, 3), wx.GBSpan(1, 1), wx.ALL, 5)

        brooch_choice116Choices = [u"高尚的", u"热情", u"心灵", u"活力", wx.EmptyString]
        self.brooch_enchant1 = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                         brooch_choice116Choices, 0)
        self.brooch_enchant1.SetSelection(brooch_data[2][1])
        gbSizer17.Add(self.brooch_enchant1, wx.GBPosition(2, 4), wx.GBSpan(1, 1), wx.ALL, 5)

        # brooch_radioBox5Choices = [u"1星", u"2星", u"3星", u"4星", u"5星"]
        # self.brooch_radioBox5 = wx.RadioBox(self, wx.ID_ANY, u"品质", wx.DefaultPosition, wx.DefaultSize,
        #                                     brooch_radioBox5Choices, 1, wx.RA_SPECIFY_ROWS)
        # self.brooch_radioBox5.SetSelection(brooch_data[0][1])
        # gbSizer17.Add(self.brooch_radioBox5, wx.GBPosition(0, 1), wx.GBSpan(2, 6), wx.ALL, 5)

        brooch_text189 = "伤害平衡:" + str(brooch_data[3][0])
        self.brooch_textCtrl189 = wx.TextCtrl(self, wx.ID_ANY, brooch_text189, wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer17.Add(self.brooch_textCtrl189, wx.GBPosition(3, 0), wx.GBSpan(1, 1), wx.ALL, 5)

        brooch_text190 = "暴击:" + str(brooch_data[3][1])
        self.brooch_textCtrl190 = wx.TextCtrl(self, wx.ID_ANY, brooch_text190, wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer17.Add(self.brooch_textCtrl190, wx.GBPosition(3, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        brooch_text191 = "攻击速度:" + str(brooch_data[3][2])
        self.brooch_textCtrl191 = wx.TextCtrl(self, wx.ID_ANY, brooch_text191, wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer17.Add(self.brooch_textCtrl191, wx.GBPosition(3, 2), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        brooch_text192 = "防御力:" + str(brooch_data[3][3])
        self.brooch_textCtrl192 = wx.TextCtrl(self, wx.ID_ANY, brooch_text192, wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer17.Add(self.brooch_textCtrl192, wx.GBPosition(3, 3), wx.GBSpan(1, 1), wx.ALL, 5)

        brooch_text193 = "力量/智力:" + str(brooch_data[3][4])
        self.brooch_textCtrl193 = wx.TextCtrl(self, wx.ID_ANY, brooch_text193, wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer17.Add(self.brooch_textCtrl193, wx.GBPosition(3, 4), wx.GBSpan(1, 1), wx.ALL, 5)

        brooch_text194 = "敏捷:" + str(brooch_data[3][5])
        self.brooch_textCtrl194 = wx.TextCtrl(self, wx.ID_ANY, brooch_text194, wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer17.Add(self.brooch_textCtrl194, wx.GBPosition(4, 0), wx.GBSpan(1, 1), wx.ALL, 5)

        brooch_text195 = "意志:" + str(brooch_data[3][6])
        self.brooch_textCtrl195 = wx.TextCtrl(self, wx.ID_ANY, brooch_text195, wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer17.Add(self.brooch_textCtrl195, wx.GBPosition(4, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        brooch_text196 = "体力:" + str(brooch_data[3][7])
        self.brooch_textCtrl196 = wx.TextCtrl(self, wx.ID_ANY, brooch_text196, wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer17.Add(self.brooch_textCtrl196, wx.GBPosition(4, 2), wx.GBSpan(1, 1), wx.ALL, 5)

        brooch_text197 = "暴击抵抗:" + str(brooch_data[3][8])
        self.brooch_textCtrl197 = wx.TextCtrl(self, wx.ID_ANY, brooch_text197, wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer17.Add(self.brooch_textCtrl197, wx.GBPosition(4, 3), wx.GBSpan(1, 1), wx.ALL, 5)

        brooch_text199 = "生命力:" + str(brooch_data[3][9])
        self.brooch_textCtrl199 = wx.TextCtrl(self, wx.ID_ANY, brooch_text199, wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer17.Add(self.brooch_textCtrl199, wx.GBPosition(4, 4), wx.GBSpan(1, 1), wx.ALL, 5)

        brooch_sdbSizer12 = wx.StdDialogButtonSizer()
        self.brooch_sdbSizer12OK = wx.Button(self, wx.ID_OK)
        brooch_sdbSizer12.AddButton(self.brooch_sdbSizer12OK)
        self.brooch_sdbSizer12Cancel = wx.Button(self, wx.ID_CANCEL)
        brooch_sdbSizer12.AddButton(self.brooch_sdbSizer12Cancel)
        brooch_sdbSizer12.Realize()

        gbSizer17.Add(brooch_sdbSizer12, wx.GBPosition(6, 3), wx.GBSpan(1, 2), wx.EXPAND, 5)

        self.SetSizer(gbSizer17)
        self.Layout()

        self.Centre(wx.BOTH)

        self.brooch_sdbSizer12OK.Bind(wx.EVT_BUTTON, self.updata_brooch)
        self.brooch_radioBox4.Bind(wx.EVT_RADIOBOX, self.update_att)
        # self.brooch_radioBox5.Bind(wx.EVT_RADIOBOX, self.update_att)
        self.brooch_enchant0.Bind(wx.EVT_CHOICE, self.update_att)
        self.brooch_enchant1.Bind(wx.EVT_CHOICE, self.update_att)
        self.brooch_radioBox4.Bind(wx.EVT_RADIOBOX, self.update_att)
        self.brooch_textCtrl198.Bind(wx.EVT_TEXT, self.update_att)
        self.brooch_add.Bind(wx.EVT_CHOICE, self.update_att)

    def __del__(self):
        pass
    
    def update_att(self, event):
        nn0 = self.brooch_enchant0.GetSelection()
        if nn0 == 0:
            n0 = 10
        elif nn0 == 1:
            n0 = 9
        elif (nn0 >= 2) & (nn0 <= 4):
            n0 = nn0 + 2
        else:
            n0 = 100
        enchant_aat0 = enchant_jewelry0(n0)
        nn1 = self.brooch_enchant1.GetSelection()
        if nn1 != 4:
            n1 = nn1
        else:
            n1 = 100
        enchant_aat1 = enchant_jewelry1(n1)

        brooch_choice = self.brooch_radioBox4.GetSelection()
        if brooch_choice == 0:
            brooch_init = [2, 0, 0, 0, 140, 90, 0, 100, 0, 0]
        elif brooch_choice == 1:
            brooch_init = [2, 0, 0, 0, 0, 90, 180, 100, 0, 0]
        else:
            brooch_init = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        addw_choice = self.brooch_add.GetSelection()
        addw_x = alladd(3, addw_choice)
        add_att = intplus(self.brooch_textCtrl198.GetValue())
        all_add = [(enchant_aat0[3] + enchant_aat1[3] + addw_x[3]*add_att),
                   (enchant_aat0[2] + enchant_aat1[2] + addw_x[2] * add_att),
                   (enchant_aat0[4] + enchant_aat1[4] + addw_x[4] * add_att),
                   (enchant_aat0[1] + enchant_aat1[1] + addw_x[1] * add_att),
                   (addw_x[5] * add_att),
                   (addw_x[6] * add_att),
                   (addw_x[7] * add_att),
                   (addw_x[8] * add_att),
                   (enchant_aat0[5] + enchant_aat1[5] + addw_x[9] * add_att),
                   (enchant_aat0[6] + enchant_aat1[6] + addw_x[1] * add_att)]
        brooch_data[3] = numpy.array(brooch_init) + numpy.array(all_add)
        brooch189 = "伤害平衡:" + str(brooch_data[3][0])
        self.brooch_textCtrl189.SetValue(brooch189)
        brooch_text190 = "暴击:" + str(brooch_data[3][1])
        self.brooch_textCtrl190.SetValue(brooch_text190)
        brooch_text191 = "攻击速度:" + str(brooch_data[3][2])
        self.brooch_textCtrl191.SetValue(brooch_text191)
        brooch_text192 = "防御力:" + str(brooch_data[3][3])
        self.brooch_textCtrl192.SetValue(brooch_text192)
        brooch_text193 = "力量:" + str(brooch_data[3][4])
        self.brooch_textCtrl193.SetValue(brooch_text193)
        brooch_text194 = "敏捷:" + str(brooch_data[3][5])
        self.brooch_textCtrl194.SetValue(brooch_text194)
        brooch_text195 = "智力:" + str(brooch_data[3][6])
        self.brooch_textCtrl195.SetValue(brooch_text195)
        brooch_text196 = "意志:" + str(brooch_data[3][7])
        self.brooch_textCtrl196.SetValue(brooch_text196)
        brooch_text197 = "暴击抵抗:" + str(brooch_data[3][8])
        self.brooch_textCtrl197.SetValue(brooch_text197)
        brooch_text199 = "生命力:" + str(brooch_data[3][9])
        self.brooch_textCtrl199.SetValue(brooch_text199)
        event.Skip()

    def updata_brooch(self, event):
        global brooch_data
        global brooch_att
        brooch_data = [[self.brooch_radioBox4.GetSelection()], # self.brooch_radioBox5.GetSelection()],
                        [self.brooch_add.GetSelection(), self.brooch_textCtrl198.GetValue()],
                        [self.brooch_enchant0.GetSelection(), self.brooch_enchant1.GetSelection()],
                        [intplus(self.brooch_textCtrl189.GetValue()), intplus(self.brooch_textCtrl190.GetValue()),
                         intplus(self.brooch_textCtrl191.GetValue()), intplus(self.brooch_textCtrl192.GetValue()),
                         intplus(self.brooch_textCtrl193.GetValue()), intplus(self.brooch_textCtrl194.GetValue()),
                         intplus(self.brooch_textCtrl195.GetValue()), intplus(self.brooch_textCtrl196.GetValue()),
                         intplus(self.brooch_textCtrl197.GetValue()),
                         intplus(self.brooch_textCtrl199.GetValue())]]
        brooch_att[1] = brooch_data[3][0]
        brooch_att[2] = brooch_data[3][1]
        brooch_att[3] = brooch_data[3][2]
        brooch_att[5] = brooch_data[3][4]
        brooch_att[6] = brooch_data[3][5]
        brooch_att[7] = brooch_data[3][6]
        brooch_att[8] = brooch_data[3][7]
        brooch_att[10] = brooch_data[3][8]
        brooch_att[11] = brooch_data[3][3]
        DataThread()
        event.Skip()


class Ring1(wx.Dialog):
    global ring1_data
    global ring1_att
    ring1_att = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ring1_data = [[4, 1],
                    [10, ''],
                    [5, 3],
                    ['', '', '', '', '', '', '', '', '', '']]

    def __init__(self, parent, title):
        super(Ring1, self).__init__(parent, title=title, size=(600, 400))

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        gbSizer17 = wx.GridBagSizer(0, 0)
        gbSizer17.SetFlexibleDirection(wx.BOTH)
        gbSizer17.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        ring1_radioBox4Choices = [u"酷寒的意志", u"酷寒的怨念", u"酷寒的匕首", u"酷寒的刺", u"我没有戒指"]
        self.ring1_radioBox4 = wx.RadioBox(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                           ring1_radioBox4Choices, 1, wx.RA_SPECIFY_COLS)
        self.ring1_radioBox4.SetSelection(ring1_data[0][0])
        gbSizer17.Add(self.ring1_radioBox4, wx.GBPosition(0, 0), wx.GBSpan(3, 1), wx.ALL, 5)

        ring1_choice114Choices = [u"暴击", u"平衡", u"攻速", u"智力", u"力量", u"意志", u"敏捷", u"爆抗", u"防御",
                                  u"生命力", u"无"]
        self.ring1_add = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, ring1_choice114Choices, 0)
        self.ring1_add.SetSelection(ring1_data[1][0])
        gbSizer17.Add(self.ring1_add, wx.GBPosition(2, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        self.ring1_textCtrl198 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer17.Add(self.ring1_textCtrl198, wx.GBPosition(2, 2), wx.GBSpan(1, 1), wx.ALL, 5)

        ring1_choice115Choices = [u"亡者的", u"闪亮的", u"迅速的", u"有意义的", u"多疑的", wx.EmptyString]
        self.ring1_enchant0 = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                        ring1_choice115Choices, 0)
        self.ring1_enchant0.SetSelection(ring1_data[2][0])
        gbSizer17.Add(self.ring1_enchant0, wx.GBPosition(2, 3), wx.GBSpan(1, 1), wx.ALL, 5)

        ring1_choice116Choices = [u"热情", u"心灵", u"活力", wx.EmptyString]
        self.ring1_enchant1 = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                        ring1_choice116Choices, 0)
        self.ring1_enchant1.SetSelection(ring1_data[2][1])
        gbSizer17.Add(self.ring1_enchant1, wx.GBPosition(2, 4), wx.GBSpan(1, 1), wx.ALL, 5)

        # ring1_radioBox5Choices = [u"1星", u"2星", u"3星", u"4星", u"5星"]
        # self.ring1_radioBox5 = wx.RadioBox(self, wx.ID_ANY, u"品质", wx.DefaultPosition, wx.DefaultSize,
        #                                    ring1_radioBox5Choices, 1, wx.RA_SPECIFY_ROWS)
        # self.ring1_radioBox5.SetSelection(ring1_data[0][1])
        # gbSizer17.Add(self.ring1_radioBox5, wx.GBPosition(0, 1), wx.GBSpan(2, 6), wx.ALL, 5)

        ring1_text189 = "伤害平衡:" + str(ring1_data[3][0])
        self.ring1_textCtrl189 = wx.TextCtrl(self, wx.ID_ANY, ring1_text189, wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer17.Add(self.ring1_textCtrl189, wx.GBPosition(3, 0), wx.GBSpan(1, 1), wx.ALL, 5)

        ring1_text190 = "暴击:" + str(ring1_data[3][1])
        self.ring1_textCtrl190 = wx.TextCtrl(self, wx.ID_ANY, ring1_text190, wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer17.Add(self.ring1_textCtrl190, wx.GBPosition(3, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        ring1_text191 = "攻击速度:" + str(ring1_data[3][2])
        self.ring1_textCtrl191 = wx.TextCtrl(self, wx.ID_ANY, ring1_text191, wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer17.Add(self.ring1_textCtrl191, wx.GBPosition(3, 2), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        ring1_text192 = "防御力:" + str(ring1_data[3][3])
        self.ring1_textCtrl192 = wx.TextCtrl(self, wx.ID_ANY, ring1_text192, wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer17.Add(self.ring1_textCtrl192, wx.GBPosition(3, 3), wx.GBSpan(1, 1), wx.ALL, 5)

        ring1_text193 = "力量/智力:" + str(ring1_data[3][4])
        self.ring1_textCtrl193 = wx.TextCtrl(self, wx.ID_ANY, ring1_text193, wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer17.Add(self.ring1_textCtrl193, wx.GBPosition(3, 4), wx.GBSpan(1, 1), wx.ALL, 5)

        ring1_text194 = "敏捷:" + str(ring1_data[3][5])
        self.ring1_textCtrl194 = wx.TextCtrl(self, wx.ID_ANY, ring1_text194, wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer17.Add(self.ring1_textCtrl194, wx.GBPosition(4, 0), wx.GBSpan(1, 1), wx.ALL, 5)

        ring1_text195 = "意志:" + str(ring1_data[3][6])
        self.ring1_textCtrl195 = wx.TextCtrl(self, wx.ID_ANY, ring1_text195, wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer17.Add(self.ring1_textCtrl195, wx.GBPosition(4, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        ring1_text196 = "体力:" + str(ring1_data[3][7])
        self.ring1_textCtrl196 = wx.TextCtrl(self, wx.ID_ANY, ring1_text196, wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer17.Add(self.ring1_textCtrl196, wx.GBPosition(4, 2), wx.GBSpan(1, 1), wx.ALL, 5)

        ring1_text197 = "暴击抵抗:" + str(ring1_data[3][8])
        self.ring1_textCtrl197 = wx.TextCtrl(self, wx.ID_ANY, ring1_text197, wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer17.Add(self.ring1_textCtrl197, wx.GBPosition(4, 3), wx.GBSpan(1, 1), wx.ALL, 5)

        ring1_text199 = "生命力:" + str(ring1_data[3][9])
        self.ring1_textCtrl199 = wx.TextCtrl(self, wx.ID_ANY, ring1_text199, wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer17.Add(self.ring1_textCtrl199, wx.GBPosition(4, 4), wx.GBSpan(1, 1), wx.ALL, 5)

        ring1_sdbSizer12 = wx.StdDialogButtonSizer()
        self.ring1_sdbSizer12OK = wx.Button(self, wx.ID_OK)
        ring1_sdbSizer12.AddButton(self.ring1_sdbSizer12OK)
        self.ring1_sdbSizer12Cancel = wx.Button(self, wx.ID_CANCEL)
        ring1_sdbSizer12.AddButton(self.ring1_sdbSizer12Cancel)
        ring1_sdbSizer12.Realize()

        gbSizer17.Add(ring1_sdbSizer12, wx.GBPosition(6, 3), wx.GBSpan(1, 2), wx.EXPAND, 5)

        self.SetSizer(gbSizer17)
        self.Layout()

        self.Centre(wx.BOTH)

        self.ring1_sdbSizer12OK.Bind(wx.EVT_BUTTON, self.updata_ring1)
        self.ring1_radioBox4.Bind(wx.EVT_RADIOBOX, self.update_att)
        # self.ring1_radioBox5.Bind(wx.EVT_RADIOBOX, self.update_att)
        self.ring1_enchant0.Bind(wx.EVT_CHOICE, self.update_att)
        self.ring1_enchant1.Bind(wx.EVT_CHOICE, self.update_att)
        self.ring1_radioBox4.Bind(wx.EVT_RADIOBOX, self.update_att)
        self.ring1_textCtrl198.Bind(wx.EVT_TEXT, self.update_att)
        self.ring1_add.Bind(wx.EVT_CHOICE, self.update_att)

    def __del__(self):
        pass
    
    def update_att(self, event):
        nn0 = self.ring1_enchant0.GetSelection()
        if nn0 == 1:
            n0 = 2
        elif nn0 == 2 or nn0 == 3 or nn0 == 4:
            n0 = nn0 + 2
        elif nn0 == 0:
            n0 = nn0
        else:
            n0 = 100
        enchant_aat0 = enchant_jewelry0(n0)
        nn1 = self.ring1_enchant1.GetSelection()
        if nn1 != 3:
            n1 = nn1 + 1
        else:
            n1 = 100
        enchant_aat1 = enchant_jewelry1(n1)

        ring1_choice = self.ring1_radioBox4.GetSelection()
        if ring1_choice == 0:
            ring1_init = [2, 0, 0, 0, 140, 90, 0, 100, 0, 0]
        elif ring1_choice == 1:
            ring1_init = [2, 0, 0, 0, 0, 90, 180, 100, 0, 0]
        else:
            ring1_init = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        addw_choice = self.ring1_add.GetSelection()
        addw_x = alladd(3, addw_choice)
        add_att = intplus(self.ring1_textCtrl198.GetValue())
        all_add = [(enchant_aat0[3] + enchant_aat1[3] + addw_x[3]*add_att),
                   (enchant_aat0[2] + enchant_aat1[2] + addw_x[2] * add_att),
                   (enchant_aat0[4] + enchant_aat1[4] + addw_x[4] * add_att),
                   (enchant_aat0[1] + enchant_aat1[1] + addw_x[1] * add_att),
                   (addw_x[5] * add_att),
                   (addw_x[6] * add_att),
                   (addw_x[7] * add_att),
                   (addw_x[8] * add_att),
                   (enchant_aat0[5] + enchant_aat1[5] + addw_x[9] * add_att),
                   (enchant_aat0[6] + enchant_aat1[6] + addw_x[1] * add_att)]
        ring1_data[3] = numpy.array(ring1_init) + numpy.array(all_add)
        ring1189 = "伤害平衡:" + str(ring1_data[3][0])
        self.ring1_textCtrl189.SetValue(ring1189)
        ring1_text190 = "暴击:" + str(ring1_data[3][1])
        self.ring1_textCtrl190.SetValue(ring1_text190)
        ring1_text191 = "攻击速度:" + str(ring1_data[3][2])
        self.ring1_textCtrl191.SetValue(ring1_text191)
        ring1_text192 = "防御力:" + str(ring1_data[3][3])
        self.ring1_textCtrl192.SetValue(ring1_text192)
        ring1_text193 = "力量:" + str(ring1_data[3][4])
        self.ring1_textCtrl193.SetValue(ring1_text193)
        ring1_text194 = "敏捷:" + str(ring1_data[3][5])
        self.ring1_textCtrl194.SetValue(ring1_text194)
        ring1_text195 = "智力:" + str(ring1_data[3][6])
        self.ring1_textCtrl195.SetValue(ring1_text195)
        ring1_text196 = "意志:" + str(ring1_data[3][7])
        self.ring1_textCtrl196.SetValue(ring1_text196)
        ring1_text197 = "暴击抵抗:" + str(ring1_data[3][8])
        self.ring1_textCtrl197.SetValue(ring1_text197)
        ring1_text199 = "生命力:" + str(ring1_data[3][9])
        self.ring1_textCtrl199.SetValue(ring1_text199)
        event.Skip()

    def updata_ring1(self, event):
        global ring1_data
        global ring1_att
        ring1_data = [[self.ring1_radioBox4.GetSelection()],# self.ring1_radioBox5.GetSelection()],
                      [self.ring1_add.GetSelection(), self.ring1_textCtrl198.GetValue()],
                      [self.ring1_enchant0.GetSelection(), self.ring1_enchant1.GetSelection()],
                      [intplus(self.ring1_textCtrl189.GetValue()), intplus(self.ring1_textCtrl190.GetValue()),
                       intplus(self.ring1_textCtrl191.GetValue()), intplus(self.ring1_textCtrl192.GetValue()),
                       intplus(self.ring1_textCtrl193.GetValue()), intplus(self.ring1_textCtrl194.GetValue()),
                       intplus(self.ring1_textCtrl195.GetValue()), intplus(self.ring1_textCtrl196.GetValue()),
                       intplus(self.ring1_textCtrl197.GetValue()), intplus(self.ring1_textCtrl199.GetValue())]]
        ring1_att[1] = ring1_data[3][0]
        ring1_att[2] = ring1_data[3][1]
        ring1_att[3] = ring1_data[3][2]
        ring1_att[5] = ring1_data[3][4]
        ring1_att[6] = ring1_data[3][5]
        ring1_att[7] = ring1_data[3][6]
        ring1_att[8] = ring1_data[3][7]
        ring1_att[10] = ring1_data[3][8]
        ring1_att[11] = ring1_data[3][3]
        DataThread()
        event.Skip()


class Ring2(wx.Dialog):
    global ring2_data
    global ring2_att
    ring2_att = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ring2_data = [[4, 1],
                  [10, ''],
                  [5, 3],
                  ['', '', '', '', '', '', '', '', '', '']]

    def __init__(self, parent, title):
        super(Ring2, self).__init__(parent, title=title, size=(600, 400))

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        gbSizer17 = wx.GridBagSizer(0, 0)
        gbSizer17.SetFlexibleDirection(wx.BOTH)
        gbSizer17.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        ring2_radioBox4Choices = [u"酷寒的意志", u"酷寒的怨念", u"酷寒的匕首", u"酷寒的刺", u"我没有戒指"]
        self.ring2_radioBox4 = wx.RadioBox(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                           ring2_radioBox4Choices, 1, wx.RA_SPECIFY_COLS)
        self.ring2_radioBox4.SetSelection(ring2_data[0][0])
        gbSizer17.Add(self.ring2_radioBox4, wx.GBPosition(0, 0), wx.GBSpan(3, 1), wx.ALL, 5)

        ring2_choice114Choices = [u"暴击", u"平衡", u"攻速", u"智力", u"力量", u"意志", u"敏捷", u"爆抗", u"防御",
                                  u"生命力", u"无"]
        self.ring2_add = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, ring2_choice114Choices, 0)
        self.ring2_add.SetSelection(ring2_data[1][0])
        gbSizer17.Add(self.ring2_add, wx.GBPosition(2, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        self.ring2_textCtrl198 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer17.Add(self.ring2_textCtrl198, wx.GBPosition(2, 2), wx.GBSpan(1, 1), wx.ALL, 5)

        ring2_choice115Choices = [u"亡者的", u"闪亮的", u"迅速的", u"有意义的", u"多疑的", wx.EmptyString]
        self.ring2_enchant0 = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                        ring2_choice115Choices, 0)
        self.ring2_enchant0.SetSelection(ring2_data[2][0])
        gbSizer17.Add(self.ring2_enchant0, wx.GBPosition(2, 3), wx.GBSpan(1, 1), wx.ALL, 5)

        ring2_choice116Choices = [u"热情", u"心灵", u"活力", wx.EmptyString]
        self.ring2_enchant1 = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                        ring2_choice116Choices, 0)
        self.ring2_enchant1.SetSelection(ring2_data[2][1])
        gbSizer17.Add(self.ring2_enchant1, wx.GBPosition(2, 4), wx.GBSpan(1, 1), wx.ALL, 5)

        # ring2_radioBox5Choices = [u"1星", u"2星", u"3星", u"4星", u"5星"]
        # self.ring2_radioBox5 = wx.RadioBox(self, wx.ID_ANY, u"品质", wx.DefaultPosition, wx.DefaultSize,
        #                                    ring2_radioBox5Choices, 1, wx.RA_SPECIFY_ROWS)
        # self.ring2_radioBox5.SetSelection(ring2_data[0][1])
        # gbSizer17.Add(self.ring2_radioBox5, wx.GBPosition(0, 1), wx.GBSpan(2, 6), wx.ALL, 5)

        ring2_text189 = "伤害平衡:" + str(ring2_data[3][0])
        self.ring2_textCtrl189 = wx.TextCtrl(self, wx.ID_ANY, ring2_text189, wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer17.Add(self.ring2_textCtrl189, wx.GBPosition(3, 0), wx.GBSpan(1, 1), wx.ALL, 5)

        ring2_text190 = "暴击:" + str(ring2_data[3][1])
        self.ring2_textCtrl190 = wx.TextCtrl(self, wx.ID_ANY, ring2_text190, wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer17.Add(self.ring2_textCtrl190, wx.GBPosition(3, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        ring2_text191 = "攻击速度:" + str(ring2_data[3][2])
        self.ring2_textCtrl191 = wx.TextCtrl(self, wx.ID_ANY, ring2_text191, wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer17.Add(self.ring2_textCtrl191, wx.GBPosition(3, 2), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        ring2_text192 = "防御力:" + str(ring2_data[3][3])
        self.ring2_textCtrl192 = wx.TextCtrl(self, wx.ID_ANY, ring2_text192, wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer17.Add(self.ring2_textCtrl192, wx.GBPosition(3, 3), wx.GBSpan(1, 1), wx.ALL, 5)

        ring2_text193 = "力量/智力:" + str(ring2_data[3][4])
        self.ring2_textCtrl193 = wx.TextCtrl(self, wx.ID_ANY, ring2_text193, wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer17.Add(self.ring2_textCtrl193, wx.GBPosition(3, 4), wx.GBSpan(1, 1), wx.ALL, 5)

        ring2_text194 = "敏捷:" + str(ring2_data[3][5])
        self.ring2_textCtrl194 = wx.TextCtrl(self, wx.ID_ANY, ring2_text194, wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer17.Add(self.ring2_textCtrl194, wx.GBPosition(4, 0), wx.GBSpan(1, 1), wx.ALL, 5)

        ring2_text195 = "意志:" + str(ring2_data[3][6])
        self.ring2_textCtrl195 = wx.TextCtrl(self, wx.ID_ANY, ring2_text195, wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer17.Add(self.ring2_textCtrl195, wx.GBPosition(4, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        ring2_text196 = "体力:" + str(ring2_data[3][7])
        self.ring2_textCtrl196 = wx.TextCtrl(self, wx.ID_ANY, ring2_text196, wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer17.Add(self.ring2_textCtrl196, wx.GBPosition(4, 2), wx.GBSpan(1, 1), wx.ALL, 5)

        ring2_text197 = "暴击抵抗:" + str(ring2_data[3][8])
        self.ring2_textCtrl197 = wx.TextCtrl(self, wx.ID_ANY, ring2_text197, wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer17.Add(self.ring2_textCtrl197, wx.GBPosition(4, 3), wx.GBSpan(1, 1), wx.ALL, 5)

        ring2_text199 = "生命力:" + str(ring2_data[3][9])
        self.ring2_textCtrl199 = wx.TextCtrl(self, wx.ID_ANY, ring2_text199, wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer17.Add(self.ring2_textCtrl199, wx.GBPosition(4, 4), wx.GBSpan(1, 1), wx.ALL, 5)

        ring2_sdbSizer12 = wx.StdDialogButtonSizer()
        self.ring2_sdbSizer12OK = wx.Button(self, wx.ID_OK)
        ring2_sdbSizer12.AddButton(self.ring2_sdbSizer12OK)
        self.ring2_sdbSizer12Cancel = wx.Button(self, wx.ID_CANCEL)
        ring2_sdbSizer12.AddButton(self.ring2_sdbSizer12Cancel)
        ring2_sdbSizer12.Realize()

        gbSizer17.Add(ring2_sdbSizer12, wx.GBPosition(6, 3), wx.GBSpan(1, 2), wx.EXPAND, 5)

        self.SetSizer(gbSizer17)
        self.Layout()

        self.Centre(wx.BOTH)

        self.ring2_sdbSizer12OK.Bind(wx.EVT_BUTTON, self.updata_ring2)
        self.ring2_radioBox4.Bind(wx.EVT_RADIOBOX, self.update_att)
        # self.ring2_radioBox5.Bind(wx.EVT_RADIOBOX, self.update_att)
        self.ring2_enchant0.Bind(wx.EVT_CHOICE, self.update_att)
        self.ring2_enchant1.Bind(wx.EVT_CHOICE, self.update_att)
        self.ring2_radioBox4.Bind(wx.EVT_RADIOBOX, self.update_att)
        self.ring2_textCtrl198.Bind(wx.EVT_TEXT, self.update_att)
        self.ring2_add.Bind(wx.EVT_CHOICE, self.update_att)

    def __del__(self):
        pass
    
    def update_att(self, event):
        nn0 = self.ring2_enchant0.GetSelection()
        if nn0 == 1:
            n0 = 2
        elif nn0 == 2 or nn0 == 3 or nn0 == 4:
            n0 = nn0 + 2
        elif nn0 == 0:
            n0 = nn0
        else:
            n0 = 100
        enchant_aat0 = enchant_jewelry0(n0)
        nn1 = self.ring2_enchant1.GetSelection()
        if nn1 != 3:
            n1 = nn1 + 1
        else:
            n1 = 100
        enchant_aat1 = enchant_jewelry1(n1)

        ring2_choice = self.ring2_radioBox4.GetSelection()
        if ring2_choice == 0:
            ring2_init = [2, 0, 0, 0, 140, 90, 0, 100, 0, 0]
        elif ring2_choice == 1:
            ring2_init = [2, 0, 0, 0, 0, 90, 180, 100, 0, 0]
        else:
            ring2_init = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        addw_choice = self.ring2_add.GetSelection()
        addw_x = alladd(3, addw_choice)
        add_att = intplus(self.ring2_textCtrl198.GetValue())
        all_add = [(enchant_aat0[3] + enchant_aat1[3] + addw_x[3]*add_att),
                   (enchant_aat0[2] + enchant_aat1[2] + addw_x[2] * add_att),
                   (enchant_aat0[4] + enchant_aat1[4] + addw_x[4] * add_att),
                   (enchant_aat0[1] + enchant_aat1[1] + addw_x[1] * add_att),
                   (addw_x[5] * add_att),
                   (addw_x[6] * add_att),
                   (addw_x[7] * add_att),
                   (addw_x[8] * add_att),
                   (enchant_aat0[5] + enchant_aat1[5] + addw_x[9] * add_att),
                   (enchant_aat0[6] + enchant_aat1[6] + addw_x[1] * add_att)]
        ring2_data[3] = numpy.array(ring2_init) + numpy.array(all_add)
        ring2189 = "伤害平衡:" + str(ring2_data[3][0])
        self.ring2_textCtrl189.SetValue(ring2189)
        ring2_text190 = "暴击:" + str(ring2_data[3][1])
        self.ring2_textCtrl190.SetValue(ring2_text190)
        ring2_text191 = "攻击速度:" + str(ring2_data[3][2])
        self.ring2_textCtrl191.SetValue(ring2_text191)
        ring2_text192 = "防御力:" + str(ring2_data[3][3])
        self.ring2_textCtrl192.SetValue(ring2_text192)
        ring2_text193 = "力量:" + str(ring2_data[3][4])
        self.ring2_textCtrl193.SetValue(ring2_text193)
        ring2_text194 = "敏捷:" + str(ring2_data[3][5])
        self.ring2_textCtrl194.SetValue(ring2_text194)
        ring2_text195 = "智力:" + str(ring2_data[3][6])
        self.ring2_textCtrl195.SetValue(ring2_text195)
        ring2_text196 = "意志:" + str(ring2_data[3][7])
        self.ring2_textCtrl196.SetValue(ring2_text196)
        ring2_text197 = "暴击抵抗:" + str(ring2_data[3][8])
        self.ring2_textCtrl197.SetValue(ring2_text197)
        ring2_text199 = "生命力:" + str(ring2_data[3][9])
        self.ring2_textCtrl199.SetValue(ring2_text199)
        event.Skip()

    def updata_ring2(self, event):
        global ring2_data
        global ring2_att
        ring2_data = [[self.ring2_radioBox4.GetSelection()], # self.ring2_radioBox5.GetSelection()],
                      [self.ring2_add.GetSelection(), self.ring2_textCtrl198.GetValue()],
                      [self.ring2_enchant0.GetSelection(), self.ring2_enchant1.GetSelection()],
                      [intplus(self.ring2_textCtrl189.GetValue()), intplus(self.ring2_textCtrl190.GetValue()),
                       intplus(self.ring2_textCtrl191.GetValue()), intplus(self.ring2_textCtrl192.GetValue()),
                       intplus(self.ring2_textCtrl193.GetValue()), intplus(self.ring2_textCtrl194.GetValue()),
                       intplus(self.ring2_textCtrl195.GetValue()), intplus(self.ring2_textCtrl196.GetValue()),
                       intplus(self.ring2_textCtrl197.GetValue()), intplus(self.ring2_textCtrl199.GetValue())]]
        ring2_att[1] = ring2_data[3][0]
        ring2_att[2] = ring2_data[3][1]
        ring2_att[3] = ring2_data[3][2]
        ring2_att[5] = ring2_data[3][4]
        ring2_att[6] = ring2_data[3][5]
        ring2_att[7] = ring2_data[3][6]
        ring2_att[8] = ring2_data[3][7]
        ring2_att[10] = ring2_data[3][8]
        ring2_att[11] = ring2_data[3][3]
        DataThread()
        event.Skip()


class Bracelet1(wx.Dialog):
    global bcl_data
    global bcl_att
    bcl_att = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    bcl_data = ['', '', '', '', '', '']

    def __init__(self, parent, title):
        super(Bracelet1, self).__init__(parent, title=title, size=(600, 400))

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        gbSizer27 = wx.GridBagSizer(0, 0)
        gbSizer27.SetFlexibleDirection(wx.BOTH)
        gbSizer27.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.bcl1_staticText1 = wx.StaticText(self, wx.ID_ANY, u"手镯1", wx.DefaultPosition, wx.DefaultSize, 0)
        self.bcl1_staticText1.Wrap(-1)
        gbSizer27.Add(self.bcl1_staticText1, wx.GBPosition(4, 1), wx.GBSpan(1, 1),
                      wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.bcl1_staticText2 = wx.StaticText(self, wx.ID_ANY, u"手镯2", wx.DefaultPosition, wx.DefaultSize, 0)
        self.bcl1_staticText2.Wrap(-1)
        gbSizer27.Add(self.bcl1_staticText2, wx.GBPosition(5, 1), wx.GBSpan(1, 1),
                      wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.bcl1_staticText97 = wx.StaticText(self, wx.ID_ANY, u"攻击力", wx.DefaultPosition, wx.DefaultSize, 0)
        self.bcl1_staticText97.Wrap(-1)
        gbSizer27.Add(self.bcl1_staticText97, wx.GBPosition(2, 2), wx.GBSpan(1, 1),
                      wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.bcl1_staticText99 = wx.StaticText(self, wx.ID_ANY, u"防御力", wx.DefaultPosition, wx.DefaultSize, 0)
        self.bcl1_staticText99.Wrap(-1)
        gbSizer27.Add(self.bcl1_staticText99, wx.GBPosition(2, 4), wx.GBSpan(1, 1),
                      wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.bcl1_staticText100 = wx.StaticText(self, wx.ID_ANY, u"血量", wx.DefaultPosition, wx.DefaultSize, 0)
        self.bcl1_staticText100.Wrap(-1)
        gbSizer27.Add(self.bcl1_staticText100, wx.GBPosition(2, 5), wx.GBSpan(1, 1),
                      wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.bcl1_textCtrl294 = wx.TextCtrl(self, wx.ID_ANY, str(bcl_data[0]), wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer27.Add(self.bcl1_textCtrl294, wx.GBPosition(4, 2), wx.GBSpan(1, 1), wx.ALL, 5)

        self.bcl1_textCtrl296 = wx.TextCtrl(self, wx.ID_ANY, str(bcl_data[1]), wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer27.Add(self.bcl1_textCtrl296, wx.GBPosition(4, 4), wx.GBSpan(1, 1), wx.ALL, 5)

        self.bcl1_textCtrl297 = wx.TextCtrl(self, wx.ID_ANY, str(bcl_data[2]), wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer27.Add(self.bcl1_textCtrl297, wx.GBPosition(4, 5), wx.GBSpan(1, 1), wx.ALL, 5)

        self.bcl2_textCtrl294 = wx.TextCtrl(self, wx.ID_ANY, str(bcl_data[3]), wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer27.Add(self.bcl2_textCtrl294, wx.GBPosition(5, 2), wx.GBSpan(1, 1), wx.ALL, 5)

        self.bcl2_textCtrl296 = wx.TextCtrl(self, wx.ID_ANY, str(bcl_data[4]), wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer27.Add(self.bcl2_textCtrl296, wx.GBPosition(5, 4), wx.GBSpan(1, 1), wx.ALL, 5)

        self.bcl2_textCtrl297 = wx.TextCtrl(self, wx.ID_ANY, str(bcl_data[5]), wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer27.Add(self.bcl2_textCtrl297, wx.GBPosition(5, 5), wx.GBSpan(1, 1), wx.ALL, 5)

        bcl1_sdbSizer22 = wx.StdDialogButtonSizer()
        self.bcl1_sdbSizer22OK = wx.Button(self, wx.ID_OK)
        bcl1_sdbSizer22.AddButton(self.bcl1_sdbSizer22OK)
        self.bcl1_sdbSizer22Cancel = wx.Button(self, wx.ID_CANCEL)
        bcl1_sdbSizer22.AddButton(self.bcl1_sdbSizer22Cancel)
        bcl1_sdbSizer22.Realize()

        gbSizer27.Add(bcl1_sdbSizer22, wx.GBPosition(7, 4), wx.GBSpan(1, 2), wx.EXPAND, 5)

        self.SetSizer(gbSizer27)
        self.Layout()

        self.Centre(wx.BOTH)

        self.bcl1_sdbSizer22OK.Bind(wx.EVT_BUTTON, self.updata_bcl)

    def __del__(self):
        pass

    def updata_bcl(self, event):
        global bcl_data
        global bcl_att
        bcl_data = [intplus(self.bcl1_textCtrl294.GetValue()), intplus(self.bcl1_textCtrl296.GetValue()),
                    intplus(self.bcl1_textCtrl297.GetValue()), intplus(self.bcl2_textCtrl294.GetValue()),
                    intplus(self.bcl2_textCtrl296.GetValue()), intplus(self.bcl2_textCtrl297.GetValue())]
        bcl_att[0] = bcl_data[0] + bcl_data[3]
        bcl_att[11] = bcl_data[1] + bcl_data[4]
        DataThread()
        event.Skip()


class DeputyW(wx.Dialog):
    global dew_data
    global dew_att
    dew_att = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    dew_data = [[2],
                [4, 3],
                ['', 10, ''],
                ['', '', '', '', '', '', '', '', '', '']]

    def __init__(self, parent, title):
        super(DeputyW, self).__init__(parent, title=title, size=(600, 400))

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        gbSizer27 = wx.GridBagSizer(0, 0)
        gbSizer27.SetFlexibleDirection(wx.BOTH)
        gbSizer27.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        dew_radioBox15Choices = [u"魔法书", u"盾牌", u"魂器", u"无"]
        self.dew_radioBox15 = wx.RadioBox(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                          dew_radioBox15Choices, 1, wx.RA_SPECIFY_ROWS)
        self.dew_radioBox15.SetSelection(dew_data[0][0])
        gbSizer27.Add(self.dew_radioBox15, wx.GBPosition(0, 0), wx.GBSpan(1, 2), wx.ALL, 5)

        de_enchant0Choices = [u"洒脱的", u"惊心动魄的", u"贤者的", u"封印的", wx.EmptyString]
        self.de_enchant0 = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, de_enchant0Choices, 0)
        self.de_enchant0.SetSelection(dew_data[1][0])
        gbSizer27.Add(self.de_enchant0, wx.GBPosition(0, 2), wx.GBSpan(1, 1),
                      wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        de_enchant1Choices = [u"金刚石", u"倾盆大雨", u"真相", wx.EmptyString]
        self.de_enchant1 = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, de_enchant1Choices, 0)
        self.de_enchant1.SetSelection(dew_data[1][1])
        gbSizer27.Add(self.de_enchant1, wx.GBPosition(0, 3), wx.GBSpan(1, 1),
                      wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.dew_staticText118 = wx.StaticText(self, wx.ID_ANY, u"强化", wx.DefaultPosition, wx.DefaultSize, 0)
        self.dew_staticText118.Wrap(-1)
        gbSizer27.Add(self.dew_staticText118, wx.GBPosition(1, 0), wx.GBSpan(1, 1),
                      wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 5)

        self.dew_textCtrl274 = wx.TextCtrl(self, wx.ID_ANY, dew_data[2][0], wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer27.Add(self.dew_textCtrl274, wx.GBPosition(1, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        dew_choice114Choices = [u"暴击", u"平衡", u"攻速", u"智力", u"力量", u"意志", u"敏捷", u"爆抗", u"防御",
                                u"生命力", u"无"]
        self.dew_choice114 = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, dew_choice114Choices, 0)
        self.dew_choice114.SetSelection(dew_data[1][1])
        gbSizer27.Add(self.dew_choice114, wx.GBPosition(1, 2), wx.GBSpan(1, 1), wx.ALL | wx.ALIGN_RIGHT, 5)

        self.dew_textCtrl275 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer27.Add(self.dew_textCtrl275, wx.GBPosition(1, 3), wx.GBSpan(1, 1), wx.ALL, 5)

        dew_text264 = "攻击力:" + str(dew_data[3][0])
        self.dew_textCtrl264 = wx.TextCtrl(self, wx.ID_ANY, dew_text264, wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer27.Add(self.dew_textCtrl264, wx.GBPosition(2, 0), wx.GBSpan(1, 1), wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        dew_text265 = "防御力:" + str(dew_data[3][1])
        self.dew_textCtrl265 = wx.TextCtrl(self, wx.ID_ANY, dew_text265, wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer27.Add(self.dew_textCtrl265, wx.GBPosition(2, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        dew_text266 = "暴击:" + str(dew_data[3][2])
        self.dew_textCtrl266 = wx.TextCtrl(self, wx.ID_ANY, dew_text266, wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer27.Add(self.dew_textCtrl266, wx.GBPosition(2, 2), wx.GBSpan(1, 1), wx.ALL, 5)

        dew_text267 = "平衡:" + str(dew_data[3][3])
        self.dew_textCtrl267 = wx.TextCtrl(self, wx.ID_ANY, dew_text267, wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer27.Add(self.dew_textCtrl267, wx.GBPosition(2, 3), wx.GBSpan(1, 1), wx.ALL, 5)

        dew_sdbSizer16 = wx.StdDialogButtonSizer()
        self.dew_sdbSizer16OK = wx.Button(self, wx.ID_OK)
        dew_sdbSizer16.AddButton(self.dew_sdbSizer16OK)
        self.dew_sdbSizer16Cancel = wx.Button(self, wx.ID_CANCEL)
        dew_sdbSizer16.AddButton(self.dew_sdbSizer16Cancel)
        dew_sdbSizer16.Realize()

        gbSizer27.Add(dew_sdbSizer16, wx.GBPosition(6, 2), wx.GBSpan(1, 2), wx.EXPAND, 5)

        dew_text268 = "攻速:" + str(dew_data[3][4])
        self.dew_textCtrl268 = wx.TextCtrl(self, wx.ID_ANY, dew_text268, wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer27.Add(self.dew_textCtrl268, wx.GBPosition(3, 0), wx.GBSpan(1, 1), wx.ALL, 5)

        dew_text269 = "力量:" + str(dew_data[3][5])
        self.dew_textCtrl269 = wx.TextCtrl(self, wx.ID_ANY, dew_text269, wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer27.Add(self.dew_textCtrl269, wx.GBPosition(3, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        dew_text270 = "敏捷:" + str(dew_data[3][6])
        self.dew_textCtrl270 = wx.TextCtrl(self, wx.ID_ANY, dew_text270, wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer27.Add(self.dew_textCtrl270, wx.GBPosition(3, 2), wx.GBSpan(1, 1), wx.ALL, 5)

        dew_text271 = "智力:" + str(dew_data[3][7])
        self.dew_textCtrl271 = wx.TextCtrl(self, wx.ID_ANY, dew_text271, wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer27.Add(self.dew_textCtrl271, wx.GBPosition(3, 3), wx.GBSpan(1, 1), wx.ALL, 5)

        dew_text272 = "意志:" + str(dew_data[3][8])
        self.dew_textCtrl272 = wx.TextCtrl(self, wx.ID_ANY, dew_text272, wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer27.Add(self.dew_textCtrl272, wx.GBPosition(4, 0), wx.GBSpan(1, 1), wx.ALL, 5)

        dew_text273 = "爆抗:" + str(dew_data[3][9])
        self.dew_textCtrl273 = wx.TextCtrl(self, wx.ID_ANY, dew_text273, wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer27.Add(self.dew_textCtrl273, wx.GBPosition(4, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        self.SetSizer(gbSizer27)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.dew_radioBox15.Bind(wx.EVT_INIT_DIALOG, self.update_att)
        self.de_enchant0.Bind(wx.EVT_CHOICE, self.update_att)
        self.de_enchant1.Bind(wx.EVT_CHOICE, self.update_att)
        self.dew_textCtrl274.Bind(wx.EVT_TEXT, self.update_att)
        self.dew_choice114.Bind(wx.EVT_CHOICE, self.update_att)
        self.dew_textCtrl275.Bind(wx.EVT_TEXT, self.update_att)
        self.dew_textCtrl264.Bind(wx.EVT_TEXT, self.update_att)
        self.dew_textCtrl265.Bind(wx.EVT_TEXT, self.update_att)
        self.dew_textCtrl266.Bind(wx.EVT_TEXT, self.update_att)
        self.dew_textCtrl267.Bind(wx.EVT_TEXT, self.update_att)
        self.dew_sdbSizer16OK.Bind(wx.EVT_BUTTON, self.updata_deputy)
        self.dew_textCtrl268.Bind(wx.EVT_TEXT, self.update_att)
        self.dew_textCtrl269.Bind(wx.EVT_TEXT, self.update_att)
        self.dew_textCtrl270.Bind(wx.EVT_TEXT, self.update_att)
        self.dew_textCtrl271.Bind(wx.EVT_TEXT, self.update_att)
        self.dew_textCtrl272.Bind(wx.EVT_TEXT, self.update_att)
        self.dew_textCtrl273.Bind(wx.EVT_TEXT, self.update_att)

    def __del__(self):
        pass

        # Virtual event handlers, overide them in your derived class

    def update_att(self, event):
        dewc = self.dew_radioBox15.GetSelection()

        nn0 = self.de_enchant0.GetSelection()
        if nn0 == 0 or nn0 == 1:
            n0 = nn0 + 7
        elif nn0 == 3:
            n0 = 11
        else:
            n0 = 100
        enchant_aat0 = enchant_jewelry0(n0)
        nn1 = self.de_enchant1.GetSelection()
        if nn1 == 0:
            n1 = 4
        elif nn1 == 1:
            n1 = 5
        else:
            n1 = 100
        enchant_aat1 = enchant_jewelry1(n1)

        event.Skip()

    def updata_deputy(self, event):

        DataThread()
        event.Skip()


class Craft(wx.Dialog):
    global craft_data
    global craft_att
    craft_att = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    craft_data = [[3, 3],
                  ['', '', '', '']]
    
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=u"工艺品", pos=wx.DefaultPosition, size=wx.Size(351, 311),
                           style=wx.DEFAULT_DIALOG_STYLE)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        gbSizer30 = wx.GridBagSizer(0, 0)
        gbSizer30.SetFlexibleDirection(wx.BOTH)
        gbSizer30.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.craft_staticText109 = wx.StaticText(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        self.craft_staticText109.Wrap(-1)
        gbSizer30.Add(self.craft_staticText109, wx.GBPosition(0, 0), wx.GBSpan(1, 1),
                      wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        craft_choice141Choices = [u"迅速的", u"有意义的", u"多疑的", wx.EmptyString]
        self.craft_enchant0 = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, craft_choice141Choices, 0)
        self.craft_enchant0.SetSelection(craft_data[0][0])
        gbSizer30.Add(self.craft_enchant0, wx.GBPosition(2, 2), wx.GBSpan(1, 1), wx.ALL, 5)

        craft_choice142Choices = [u"热情", u"心灵", u"活力", wx.EmptyString]
        self.craft_enchant1 = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, craft_choice142Choices, 0)
        self.craft_enchant1.SetSelection(craft_data[0][1])
        gbSizer30.Add(self.craft_enchant1, wx.GBPosition(2, 3), wx.GBSpan(1, 1), wx.ALL, 5)

        craft_text306 = "攻速:" + str(craft_data[1][0])
        self.craft_textCtrl306 = wx.TextCtrl(self, wx.ID_ANY, craft_text306, wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer30.Add(self.craft_textCtrl306, wx.GBPosition(3, 2), wx.GBSpan(1, 1), wx.ALL, 5)

        craft_text307 = "平衡:" + str(craft_data[1][1])
        self.craft_textCtrl307 = wx.TextCtrl(self, wx.ID_ANY, craft_text307, wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer30.Add(self.craft_textCtrl307, wx.GBPosition(3, 3), wx.GBSpan(1, 1), wx.ALL, 5)

        craft_text308 = "攻击:" + str(craft_data[1][2])
        self.craft_textCtrl308 = wx.TextCtrl(self, wx.ID_ANY, craft_text308, wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer30.Add(self.craft_textCtrl308, wx.GBPosition(4, 2), wx.GBSpan(1, 1), wx.ALL, 5)

        craft_text309 = "防御:" + str(craft_data[1][3])
        self.craft_textCtrl309 = wx.TextCtrl(self, wx.ID_ANY, craft_text309, wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer30.Add(self.craft_textCtrl309, wx.GBPosition(4, 3), wx.GBSpan(1, 1), wx.ALL, 5)

        craft_sdbSizer25 = wx.StdDialogButtonSizer()
        self.craft_sdbSizer25OK = wx.Button(self, wx.ID_OK)
        craft_sdbSizer25.AddButton(self.craft_sdbSizer25OK)
        self.craft_sdbSizer25Cancel = wx.Button(self, wx.ID_CANCEL)
        craft_sdbSizer25.AddButton(self.craft_sdbSizer25Cancel)
        craft_sdbSizer25.Realize()

        gbSizer30.Add(craft_sdbSizer25, wx.GBPosition(6, 3), wx.GBSpan(1, 2), wx.EXPAND, 5)

        self.SetSizer(gbSizer30)
        self.Layout()

        self.Centre(wx.BOTH)
        
        self.craft_sdbSizer25OK.Bind(wx.EVT_BUTTON, self.updata_craft)
        self.craft_enchant0.Bind(wx.EVT_CHOICE, self.update_att)
        self.craft_enchant1.Bind(wx.EVT_CHOICE, self.update_att)

    def __del__(self):
        pass
    
    def update_att(self, event):
        nn0 = self.craft_enchant0.GetSelection()
        if nn0 != 3:
            n0 = nn0 + 4
        else:
            n0 = 100
        enchant_aat0 = enchant_jewelry0(n0)
        nn1 = self.craft_enchant1.GetSelection()
        if nn1 != 3:
            n1 = nn1 + 1
        else:
            n1 = 100
        enchant_aat1 = enchant_jewelry1(n1)

        craft_data[1] = [(enchant_aat0[4] + enchant_aat1[4]), (enchant_aat0[3] + enchant_aat1[3]),
                         (enchant_aat0[0] + enchant_aat1[0]), (enchant_aat0[1] + enchant_aat1[1])]
        craft189 = "攻速:" + str(craft_data[1][0])
        self.craft_textCtrl306.SetValue(craft189)
        craft_text190 = "平衡:" + str(craft_data[1][1])
        self.craft_textCtrl307.SetValue(craft_text190)
        craft_text191 = "攻击:" + str(craft_data[1][2])
        self.craft_textCtrl308.SetValue(craft_text191)
        craft_text192 = "防御:" + str(craft_data[1][3])
        self.craft_textCtrl309.SetValue(craft_text192)

        event.Skip()

    def updata_craft(self, event):
        global craft_data
        global craft_att
        craft_data = [[self.craft_enchant0.GetSelection(), self.craft_enchant1.GetSelection()],
                      [intplus(self.craft_textCtrl306.GetValue()), intplus(self.craft_textCtrl307.GetValue()),
                       intplus(self.craft_textCtrl308.GetValue()), intplus(self.craft_textCtrl309.GetValue())]]
        craft_att[0] = craft_data[1][2]
        craft_att[11] = craft_data[1][3]
        craft_att[3] = craft_data[1][0]
        craft_att[1] = craft_data[1][1]
        DataThread()
        event.Skip()


class Store(wx.Dialog):
    global store_data
    global store_att
    store_att = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    store_data = [['', '', '', '', ''],
                  ['', '', '', '', ''],
                  [['', '', '', '', '', '', '', '', ''], [8, ''], [3, 3]],
                  [2, '']]
    
    def __init__(self, parent, title):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=title, pos=wx.DefaultPosition,
                           size=wx.Size(697, 555), style=wx.DEFAULT_DIALOG_STYLE)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        bSizer3 = wx.BoxSizer(wx.VERTICAL)

        bSizer4 = wx.BoxSizer(wx.HORIZONTAL)

        sbSizer13 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"左肩章"), wx.VERTICAL)

        gbSizer40 = wx.GridBagSizer(0, 0)
        gbSizer40.SetFlexibleDirection(wx.BOTH)
        gbSizer40.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.store_staticText147 = wx.StaticText(sbSizer13.GetStaticBox(), wx.ID_ANY, u"攻击力", wx.DefaultPosition,
                                                 wx.DefaultSize, 0)
        self.store_staticText147.Wrap(-1)
        gbSizer40.Add(self.store_staticText147, wx.GBPosition(0, 0), wx.GBSpan(1, 1),
                      wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.store_textCtrl348 = wx.TextCtrl(sbSizer13.GetStaticBox(), wx.ID_ANY, str(store_data[0][0]), wx.DefaultPosition,
                                             wx.DefaultSize, 0)
        gbSizer40.Add(self.store_textCtrl348, wx.GBPosition(0, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        self.store_staticText148 = wx.StaticText(sbSizer13.GetStaticBox(), wx.ID_ANY, u"防御力", wx.DefaultPosition,
                                             wx.DefaultSize, 0)
        self.store_staticText148.Wrap(-1)
        gbSizer40.Add(self.store_staticText148, wx.GBPosition(0, 2), wx.GBSpan(1, 1),
                      wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.store_textCtrl349 = wx.TextCtrl(sbSizer13.GetStaticBox(), wx.ID_ANY, str(store_data[0][1]), wx.DefaultPosition,
                                         wx.DefaultSize, 0)
        gbSizer40.Add(self.store_textCtrl349, wx.GBPosition(0, 3), wx.GBSpan(1, 1), wx.ALL, 5)

        self.store_staticText149 = wx.StaticText(sbSizer13.GetStaticBox(), wx.ID_ANY, u"攻速", wx.DefaultPosition,
                                             wx.DefaultSize, 0)
        self.store_staticText149.Wrap(-1)
        gbSizer40.Add(self.store_staticText149, wx.GBPosition(1, 0), wx.GBSpan(1, 1),
                      wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.store_textCtrl350 = wx.TextCtrl(sbSizer13.GetStaticBox(), wx.ID_ANY, str(store_data[0][2]), wx.DefaultPosition,
                                         wx.DefaultSize, 0)
        gbSizer40.Add(self.store_textCtrl350, wx.GBPosition(1, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        self.store_staticText150 = wx.StaticText(sbSizer13.GetStaticBox(), wx.ID_ANY, u"暴击", wx.DefaultPosition,
                                             wx.DefaultSize, 0)
        self.store_staticText150.Wrap(-1)
        gbSizer40.Add(self.store_staticText150, wx.GBPosition(1, 2), wx.GBSpan(1, 1),
                      wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.store_textCtrl351 = wx.TextCtrl(sbSizer13.GetStaticBox(), wx.ID_ANY, str(store_data[0][3]), wx.DefaultPosition,
                                         wx.DefaultSize, 0)
        gbSizer40.Add(self.store_textCtrl351, wx.GBPosition(1, 3), wx.GBSpan(1, 1), wx.ALL, 5)

        self.store_staticText151 = wx.StaticText(sbSizer13.GetStaticBox(), wx.ID_ANY, u"平衡", wx.DefaultPosition,
                                             wx.DefaultSize, 0)
        self.store_staticText151.Wrap(-1)
        gbSizer40.Add(self.store_staticText151, wx.GBPosition(2, 0), wx.GBSpan(1, 1),
                      wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.store_textCtrl352 = wx.TextCtrl(sbSizer13.GetStaticBox(), wx.ID_ANY, str(store_data[0][4]), wx.DefaultPosition,
                                             wx.DefaultSize, 0)
        gbSizer40.Add(self.store_textCtrl352, wx.GBPosition(2, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        sbSizer13.Add(gbSizer40, 1, wx.EXPAND, 5)

        bSizer4.Add(sbSizer13, 1, wx.EXPAND, 5)

        sbSizer15 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"右肩章"), wx.VERTICAL)

        gbSizer401 = wx.GridBagSizer(0, 0)
        gbSizer401.SetFlexibleDirection(wx.BOTH)
        gbSizer401.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.store_staticText1471 = wx.StaticText(sbSizer15.GetStaticBox(), wx.ID_ANY, u"攻击力", wx.DefaultPosition,
                                              wx.DefaultSize, 0)
        self.store_staticText1471.Wrap(-1)
        gbSizer401.Add(self.store_staticText1471, wx.GBPosition(0, 0), wx.GBSpan(1, 1),
                       wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.store_textCtrl3481 = wx.TextCtrl(sbSizer15.GetStaticBox(), wx.ID_ANY, str(store_data[1][0]), wx.DefaultPosition,
                                          wx.DefaultSize, 0)
        gbSizer401.Add(self.store_textCtrl3481, wx.GBPosition(0, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        self.store_staticText1481 = wx.StaticText(sbSizer15.GetStaticBox(), wx.ID_ANY, u"防御力", wx.DefaultPosition,
                                              wx.DefaultSize, 0)
        self.store_staticText1481.Wrap(-1)
        gbSizer401.Add(self.store_staticText1481, wx.GBPosition(0, 2), wx.GBSpan(1, 1),
                       wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.store_textCtrl3491 = wx.TextCtrl(sbSizer15.GetStaticBox(), wx.ID_ANY, str(store_data[1][1]), wx.DefaultPosition,
                                          wx.DefaultSize, 0)
        gbSizer401.Add(self.store_textCtrl3491, wx.GBPosition(0, 3), wx.GBSpan(1, 1), wx.ALL, 5)

        self.store_staticText1491 = wx.StaticText(sbSizer15.GetStaticBox(), wx.ID_ANY, u"攻速", wx.DefaultPosition,
                                              wx.DefaultSize, 0)
        self.store_staticText1491.Wrap(-1)
        gbSizer401.Add(self.store_staticText1491, wx.GBPosition(1, 0), wx.GBSpan(1, 1),
                       wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.store_textCtrl3501 = wx.TextCtrl(sbSizer15.GetStaticBox(), wx.ID_ANY, str(store_data[1][2]), wx.DefaultPosition,
                                          wx.DefaultSize, 0)
        gbSizer401.Add(self.store_textCtrl3501, wx.GBPosition(1, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        self.store_staticText1501 = wx.StaticText(sbSizer15.GetStaticBox(), wx.ID_ANY, u"暴击", wx.DefaultPosition,
                                              wx.DefaultSize, 0)
        self.store_staticText1501.Wrap(-1)
        gbSizer401.Add(self.store_staticText1501, wx.GBPosition(1, 2), wx.GBSpan(1, 1),
                       wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.store_textCtrl3511 = wx.TextCtrl(sbSizer15.GetStaticBox(), wx.ID_ANY, str(store_data[1][3]), wx.DefaultPosition,
                                          wx.DefaultSize, 0)
        gbSizer401.Add(self.store_textCtrl3511, wx.GBPosition(1, 3), wx.GBSpan(1, 1), wx.ALL, 5)

        self.store_staticText1511 = wx.StaticText(sbSizer15.GetStaticBox(), wx.ID_ANY, u"平衡", wx.DefaultPosition,
                                              wx.DefaultSize, 0)
        self.store_staticText1511.Wrap(-1)
        gbSizer401.Add(self.store_staticText1511, wx.GBPosition(2, 0), wx.GBSpan(1, 1),
                       wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.store_textCtrl3521 = wx.TextCtrl(sbSizer15.GetStaticBox(), wx.ID_ANY, str(store_data[1][4]), wx.DefaultPosition,
                                          wx.DefaultSize, 0)
        gbSizer401.Add(self.store_textCtrl3521, wx.GBPosition(2, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        sbSizer15.Add(gbSizer401, 1, wx.EXPAND, 5)

        bSizer4.Add(sbSizer15, 1, wx.EXPAND, 5)

        bSizer3.Add(bSizer4, 1, wx.EXPAND, 5)

        sbSizer16 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"项链"), wx.VERTICAL)

        gbSizer44 = wx.GridBagSizer(0, 0)
        gbSizer44.SetFlexibleDirection(wx.BOTH)
        gbSizer44.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.store_staticText162 = wx.StaticText(sbSizer16.GetStaticBox(), wx.ID_ANY, u"力量", wx.DefaultPosition,
                                             wx.DefaultSize, 0)
        self.store_staticText162.Wrap(-1)
        gbSizer44.Add(self.store_staticText162, wx.GBPosition(0, 0), wx.GBSpan(1, 1),
                      wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.store_textCtrl363 = wx.TextCtrl(sbSizer16.GetStaticBox(), wx.ID_ANY, str(store_data[2][0][0]), wx.DefaultPosition,
                                         wx.DefaultSize, 0)
        gbSizer44.Add(self.store_textCtrl363, wx.GBPosition(0, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        self.store_staticText163 = wx.StaticText(sbSizer16.GetStaticBox(), wx.ID_ANY, u"敏捷", wx.DefaultPosition,
                                             wx.DefaultSize, 0)
        self.store_staticText163.Wrap(-1)
        gbSizer44.Add(self.store_staticText163, wx.GBPosition(0, 2), wx.GBSpan(1, 1),
                      wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.store_textCtrl364 = wx.TextCtrl(sbSizer16.GetStaticBox(), wx.ID_ANY, str(store_data[2][0][1]), wx.DefaultPosition,
                                         wx.DefaultSize, 0)
        gbSizer44.Add(self.store_textCtrl364, wx.GBPosition(0, 3), wx.GBSpan(1, 1), wx.ALL, 5)

        self.store_staticText164 = wx.StaticText(sbSizer16.GetStaticBox(), wx.ID_ANY, u"智力", wx.DefaultPosition,
                                             wx.DefaultSize, 0)
        self.store_staticText164.Wrap(-1)
        gbSizer44.Add(self.store_staticText164, wx.GBPosition(0, 4), wx.GBSpan(1, 1),
                      wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.store_textCtrl365 = wx.TextCtrl(sbSizer16.GetStaticBox(), wx.ID_ANY, str(store_data[2][0][2]), wx.DefaultPosition,
                                         wx.DefaultSize, 0)
        gbSizer44.Add(self.store_textCtrl365, wx.GBPosition(0, 5), wx.GBSpan(1, 1), wx.ALL, 5)

        self.store_staticText165 = wx.StaticText(sbSizer16.GetStaticBox(), wx.ID_ANY, u"意志", wx.DefaultPosition,
                                             wx.DefaultSize, 0)
        self.store_staticText165.Wrap(-1)
        gbSizer44.Add(self.store_staticText165, wx.GBPosition(0, 6), wx.GBSpan(1, 1),
                      wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.store_textCtrl366 = wx.TextCtrl(sbSizer16.GetStaticBox(), wx.ID_ANY, str(store_data[2][0][3]), wx.DefaultPosition,
                                         wx.DefaultSize, 0)
        gbSizer44.Add(self.store_textCtrl366, wx.GBPosition(0, 7), wx.GBSpan(1, 1), wx.ALL, 5)

        store_choice146Choices = [u"暴击", u"平衡", u"攻速", u"智力", u"力量", u"意志", u"敏捷",
                                  u"无"]
        self.store_add = wx.Choice(sbSizer16.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                     store_choice146Choices, 0)
        self.store_add.SetSelection(store_data[2][1][0])
        gbSizer44.Add(self.store_add, wx.GBPosition(1, 0), wx.GBSpan(1, 1), wx.ALL, 5)

        self.store_textCtrl367 = wx.TextCtrl(sbSizer16.GetStaticBox(), wx.ID_ANY, str(store_data[2][1][1]), wx.DefaultPosition,
                                         wx.DefaultSize, 0)
        gbSizer44.Add(self.store_textCtrl367, wx.GBPosition(1, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        self.store_staticText169 = wx.StaticText(sbSizer16.GetStaticBox(), wx.ID_ANY, u"前缀", wx.DefaultPosition,
                                             wx.DefaultSize, 0)
        self.store_staticText169.Wrap(-1)
        gbSizer44.Add(self.store_staticText169, wx.GBPosition(1, 2), wx.GBSpan(1, 1), wx.ALL, 5)

        store_choice147Choices = [u"迅速的", u"有意义的", u"多疑的", wx.EmptyString]
        self.store_enchant0 = wx.Choice(sbSizer16.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                     store_choice147Choices, 0)
        self.store_enchant0.SetSelection(store_data[2][2][0])
        gbSizer44.Add(self.store_enchant0, wx.GBPosition(1, 3), wx.GBSpan(1, 1), wx.ALL, 5)

        self.store_staticText170 = wx.StaticText(sbSizer16.GetStaticBox(), wx.ID_ANY, u"后缀", wx.DefaultPosition,
                                             wx.DefaultSize, 0)
        self.store_staticText170.Wrap(-1)
        gbSizer44.Add(self.store_staticText170, wx.GBPosition(1, 4), wx.GBSpan(1, 1), wx.ALL, 5)

        store_choice148Choices = [u"热情", u"心灵", u"活力", wx.EmptyString]
        self.store_enchant1 = wx.Choice(sbSizer16.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                     store_choice148Choices, 0)
        self.store_enchant1.SetSelection(store_data[2][2][1])
        gbSizer44.Add(self.store_enchant1, wx.GBPosition(1, 5), wx.GBSpan(1, 1), wx.ALL, 5)

        self.store_staticText116 = wx.StaticText(sbSizer16.GetStaticBox(), wx.ID_ANY, u"攻击", wx.DefaultPosition,
                                             wx.DefaultSize, 0)
        self.store_staticText116.Wrap(-1)
        gbSizer44.Add(self.store_staticText116, wx.GBPosition(1, 6), wx.GBSpan(1, 1),
                      wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.store_textCtrl260 = wx.TextCtrl(sbSizer16.GetStaticBox(), wx.ID_ANY, str(store_data[2][0][7]), wx.DefaultPosition,
                                         wx.DefaultSize, 0)
        gbSizer44.Add(self.store_textCtrl260, wx.GBPosition(1, 7), wx.GBSpan(1, 1), wx.ALL, 5)

        self.store_textCtrl370 = wx.TextCtrl(sbSizer16.GetStaticBox(), wx.ID_ANY, str(store_data[2][0][4]), wx.DefaultPosition,
                                         wx.DefaultSize, 0)
        gbSizer44.Add(self.store_textCtrl370, wx.GBPosition(2, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        self.store_staticText166 = wx.StaticText(sbSizer16.GetStaticBox(), wx.ID_ANY, u"平衡", wx.DefaultPosition,
                                             wx.DefaultSize, 0)
        self.store_staticText166.Wrap(-1)
        gbSizer44.Add(self.store_staticText166, wx.GBPosition(2, 2), wx.GBSpan(1, 1), wx.ALL, 5)

        self.store_textCtrl371 = wx.TextCtrl(sbSizer16.GetStaticBox(), wx.ID_ANY, str(store_data[2][0][5]), wx.DefaultPosition,
                                         wx.DefaultSize, 0)
        gbSizer44.Add(self.store_textCtrl371, wx.GBPosition(2, 3), wx.GBSpan(1, 1), wx.ALL, 5)

        self.store_staticText168 = wx.StaticText(sbSizer16.GetStaticBox(), wx.ID_ANY, u"攻速", wx.DefaultPosition,
                                             wx.DefaultSize, 0)
        self.store_staticText168.Wrap(-1)
        gbSizer44.Add(self.store_staticText168, wx.GBPosition(2, 4), wx.GBSpan(1, 1), wx.ALL, 5)

        self.store_textCtrl372 = wx.TextCtrl(sbSizer16.GetStaticBox(), wx.ID_ANY, str(store_data[2][0][6]), wx.DefaultPosition,
                                         wx.DefaultSize, 0)
        gbSizer44.Add(self.store_textCtrl372, wx.GBPosition(2, 5), wx.GBSpan(1, 1), wx.ALL, 5)

        self.store_staticText117 = wx.StaticText(sbSizer16.GetStaticBox(), wx.ID_ANY, u"防御", wx.DefaultPosition,
                                             wx.DefaultSize, 0)
        self.store_staticText117.Wrap(-1)
        gbSizer44.Add(self.store_staticText117, wx.GBPosition(2, 6), wx.GBSpan(1, 1), wx.ALL, 5)

        self.store_textCtrl261 = wx.TextCtrl(sbSizer16.GetStaticBox(), wx.ID_ANY, str(store_data[2][0][7]), wx.DefaultPosition,
                                         wx.DefaultSize, 0)
        gbSizer44.Add(self.store_textCtrl261, wx.GBPosition(2, 7), wx.GBSpan(1, 1), wx.ALL, 5)

        self.store_staticText167 = wx.StaticText(sbSizer16.GetStaticBox(), wx.ID_ANY, u"暴击", wx.DefaultPosition,
                                             wx.DefaultSize, 0)
        self.store_staticText167.Wrap(-1)
        gbSizer44.Add(self.store_staticText167, wx.GBPosition(2, 0), wx.GBSpan(1, 1),
                      wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        sbSizer16.Add(gbSizer44, 1, wx.EXPAND, 5)

        bSizer3.Add(sbSizer16, 1, wx.EXPAND, 5)

        sbSizer17 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"徽章"), wx.VERTICAL)

        store_radioBox22Choices = [u"勇士徽章", u"初级勇士徽章", u"我没有徽章"]
        self.store_radioBox22 = wx.RadioBox(sbSizer17.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                        wx.DefaultSize, store_radioBox22Choices, 1, wx.RA_SPECIFY_ROWS)
        self.store_radioBox22.SetSelection(store_data[3][0])
        sbSizer17.Add(self.store_radioBox22, 0, wx.ALL, 5)

        store_text375 = "防御:" + str(store_data[3][1])
        self.store_textCtrl375 = wx.TextCtrl(sbSizer17.GetStaticBox(), wx.ID_ANY, store_text375, wx.DefaultPosition,
                                             wx.DefaultSize, wx.TE_READONLY)
        sbSizer17.Add(self.store_textCtrl375, 0, wx.ALL, 5)

        bSizer3.Add(sbSizer17, 1, wx.EXPAND, 5)

        store_sdbSizer30 = wx.StdDialogButtonSizer()
        self.store_sdbSizer30OK = wx.Button(self, wx.ID_OK)
        store_sdbSizer30.AddButton(self.store_sdbSizer30OK)
        self.store_sdbSizer30Cancel = wx.Button(self, wx.ID_CANCEL)
        store_sdbSizer30.AddButton(self.store_sdbSizer30Cancel)
        store_sdbSizer30.Realize()

        bSizer3.Add(store_sdbSizer30, 1, wx.EXPAND, 5)

        self.SetSizer(bSizer3)
        self.Layout()

        self.Centre(wx.BOTH)

        self.store_sdbSizer30OK.Bind(wx.EVT_BUTTON, self.update_store)
        self.store_enchant0.Bind(wx.EVT_CHOICE, self.update_att)
        self.store_enchant1.Bind(wx.EVT_CHOICE, self.update_att)
        self.store_add.Bind(wx.EVT_CHOICE, self.update_att)
        self.store_textCtrl367.Bind(wx.EVT_TEXT, self.update_att)
        self.store_radioBox22.Bind(wx.EVT_RADIOBOX, self.update_att)

    def __del__(self):
        pass

    def update_att(self, event):
        badge = self.store_radioBox22.GetSelection()
        if badge == 0:
            self.store_textCtrl375.SetValue('防御:600')
        elif badge == 1:
            self.store_textCtrl375.SetValue('防御:200')
        else:
            self.store_textCtrl375.SetValue('防御:0')

        nn0 = self.store_enchant0.GetSelection()
        if nn0 != 3:
            n0 = nn0 + 4
        else:
            n0 = 100
        enchant_aat0 = enchant_jewelry0(n0)
        nn1 = self.store_enchant1.GetSelection()
        if nn1 != 3:
            n1 = nn1 + 1
        else:
            n1 = 100
        enchant_aat1 = enchant_jewelry1(n1)
        store_init = [0, 0, 0, 0, 0, 0, 0, 0, 0]

        addw_choice = self.store_add.GetSelection()
        addw_x = alladd(3, addw_choice)
        add_att = intplus(self.store_textCtrl367.GetValue())
        all_add = [(addw_x[5] * add_att + store_init[0]), (addw_x[6] * add_att + store_init[1]),
                   (addw_x[7] * add_att + store_init[2]), (addw_x[8] * add_att + store_init[3]),
                   (enchant_aat0[2] + enchant_aat1[2] + addw_x[2] * add_att + store_init[4]),
                   (enchant_aat0[3] + enchant_aat1[3] + addw_x[3] * add_att + store_init[5]),
                   (enchant_aat0[4] + enchant_aat1[4] + addw_x[4] * add_att + store_init[6]),
                   (enchant_aat0[0] + enchant_aat1[0] + addw_x[0] * add_att + store_init[7]),
                   (enchant_aat0[1] + enchant_aat1[1] + addw_x[1] * add_att + store_init[8])]
        self.store_textCtrl363.SetValue(str(all_add[0]))
        self.store_textCtrl364.SetValue(str(all_add[1]))
        self.store_textCtrl365.SetValue(str(all_add[2]))
        self.store_textCtrl366.SetValue(str(all_add[3]))
        self.store_textCtrl370.SetValue(str(all_add[4]))
        self.store_textCtrl371.SetValue(str(all_add[5]))
        self.store_textCtrl372.SetValue(str(all_add[6]))
        self.store_textCtrl260.SetValue(str(all_add[7]))
        self.store_textCtrl261.SetValue(str(all_add[8]))
        event.Skip()
        

    def update_store(self, event):
        global store_data
        global store_att
        store_data = [[intplus(self.store_textCtrl348.GetValue()), intplus(self.store_textCtrl349.GetValue()),
                       intplus(self.store_textCtrl350.GetValue()), intplus(self.store_textCtrl351.GetValue()),
                       intplus(self.store_textCtrl352.GetValue())],
                      [intplus(self.store_textCtrl3481.GetValue()), intplus(self.store_textCtrl3491.GetValue()),
                       intplus(self.store_textCtrl3501.GetValue()), intplus(self.store_textCtrl3511.GetValue()),
                       intplus(self.store_textCtrl3521.GetValue())],
                      [[intplus(self.store_textCtrl363.GetValue()), intplus(self.store_textCtrl364.GetValue()),
                        intplus(self.store_textCtrl365.GetValue()), intplus(self.store_textCtrl366.GetValue()),
                        intplus(self.store_textCtrl370.GetValue()), intplus(self.store_textCtrl371.GetValue()),
                        intplus(self.store_textCtrl372.GetValue()), intplus(self.store_textCtrl260.GetValue()),
                        intplus(self.store_textCtrl261.GetValue())],
                       [self.store_add.GetSelection(), intplus(self.store_textCtrl367.GetValue())],
                       [self.store_enchant0.GetSelection(), self.store_enchant1.GetSelection()]],
                      [self.store_radioBox22.GetSelection(), intplus(self.store_textCtrl375.GetValue())]]
        store_att[0] = store_data[0][0] + store_data[1][0] + store_data[2][0][7]
        store_att[11] = store_data[0][1] + store_data[1][1] + store_data[2][0][8] + store_data[3][1]
        store_att[1] = store_data[0][4] + store_data[1][4] + store_data[2][0][5]
        store_att[2] = store_data[0][3] + store_data[1][3] + store_data[2][0][4]
        store_att[3] = store_data[0][2] + store_data[1][2] + store_data[2][0][6]
        store_att[5] = store_data[2][0][0]
        store_att[6] = store_data[2][0][1]
        store_att[7] = store_data[2][0][2]
        store_att[8] = store_data[2][0][3]
        DataThread()
        event.Skip()


class Damage(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        #        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        gbSizer4 = wx.GridBagSizer(0, 0)
        gbSizer4.SetFlexibleDirection(wx.BOTH)
        gbSizer4.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.dm_staticText34 = wx.StaticText(self, wx.ID_ANY, u"伤害计算正在开发中...\r\n可是我不会啊...",
                                             wx.DefaultPosition, wx.DefaultSize, 0)
        self.dm_staticText34.Wrap(-1)
        gbSizer4.Add(self.dm_staticText34, wx.GBPosition(0, 1), wx.GBSpan(1, 1),
                     wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)


if __name__ == '__main__':
    app = wx.App(False)
    frame = wx.Frame(None, title="骚年上15吧     版本1.5", pos=wx.DefaultPosition, size=(800, 600))
    nb = wx.Notebook(frame)
    nb.AddPage(AutoPanel(nb), "Auto")
    #nb.AddPage(MatPanel(nb), "Mat")
    nb.AddPage(Simulation(nb), "simulation")
    nb.AddPage(Others(nb), "附魔出处")
    #nb.AddPage(MyPanel5(nb), "装备模拟")
    #nb.AddPage(Damage(nb), "Damage")
    frame.Show()
    app.MainLoop()
