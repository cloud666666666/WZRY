#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##################################
# Author : cndaqiang             #
# Update : 2024-07-27            #
# Build  : 2023-11-10            #
# What   : WZRY                  #
##################################
try:
    from airtest_mobileauto.control import *
except ImportError:
    print("模块[airtest_mobileauto]不存在, 尝试安装")
    import pip

    try:
        pip.main(['install', 'airtest_mobileauto', '-i', 'https://pypi.tuna.tsinghua.edu.cn/simple'])
    except:
        print("安装失败")
        exit(1)
import sys
import os


class wzry_runinfo:
    # 备注
    # 运行参数信息
    # 主要用于保存上一步的运行信息,对本步进行调整
    def __init__(self):
        self.组队模式 = False
        self.房主 = True
        self.对战模式 = "5v5匹配"
        self.对战时间 = [5.0, 23]
        self.限时组队时间 = 7
        self.runstep = -1
        self.jinristep = -1
        self.青铜段位 = False
        self.标准模式 = False
        self.触摸对战 = False

    def printinfo(self):
        TimeECHO(f"RUNINFO")
        TimeECHO(f"\t 组队模式 = {str(self.组队模式)}")
        TimeECHO(f"\t 房主 = {str(self.房主)}")
        TimeECHO(f"\t 对战模式 = {str(self.对战模式)}")
        TimeECHO(f"\t 对战时间 = [{str(self.对战时间[0])},{str(self.对战时间[1])}]")
        TimeECHO(f"\t 限时组队时间 = {str(round(self.限时组队时间,2))}")
        TimeECHO(f"\t runstep = {str(self.runstep)}")
        TimeECHO(f"\t jinristep = {str(self.jinristep)}")
        TimeECHO(f"\t 青铜段位 = {str(self.青铜段位)}")
        TimeECHO(f"\t 标准模式 = {str(self.标准模式)}")
        TimeECHO(f"\t 触摸对战 = {str(self.触摸对战)}")

    def compare(self, other):
        if self.组队模式 != other.组队模式:
            TimeECHO(f"RUNINFO:组队模式变化->{str(self.组队模式)}")
            return False
        if self.对战模式 != other.对战模式:
            TimeECHO(f"RUNINFO:对战模式变化->{str(self.对战模式)}")
            return False
        # 对战模式没变时，模拟战不用判断了
        if "模拟战" in self.对战模式:
            return True
        if "5v5排位" in self.对战模式:
            return True
        if "5v5匹配" in self.对战模式:
            if self.青铜段位 == other.青铜段位:
                if self.标准模式 == other.标准模式:
                    return True
                else:
                    TimeECHO(f"RUNINFO:标准模式变化->{str(self.标准模式)}")
                    return False
            else:
                TimeECHO(f"RUNINFO:青铜段位变化->{str(self.青铜段位)}")
                return False
        TimeECHO(f"RUNINFO:对战参数没有变化")
        return True


class wzry_figure:
    # 图片元素信息,
    # 方便更新,
    # 以及用于统一更新图片传递给所有进程
    def __init__(self, Tool=None):
        self.Tool = DQWheel() if Tool == None else Tool
        # 一些图库, 后期使用图片更新
        self.网络不可用 = Template(r"tpl1720067196954.png", record_pos=(0.003, 0.045), resolution=(960, 540))
        self.登录界面开始游戏图标 = Template(r"tpl1692947242096.png", record_pos=(-0.004, 0.158), resolution=(960, 540), threshold=0.9)
        self.大厅对战图标 = Template(r"tpl1723219359665.png", record_pos=(-0.122, 0.133), resolution=(960, 540))
        self.大厅万象天工 = Template(r"tpl1723219381063.png", record_pos=(0.243, 0.14), resolution=(960, 540))
        self.王者模拟战图标 = Template(r"tpl1693660105012.png", record_pos=(-0.435, -0.134), resolution=(960, 540))
        self.大厅排位赛 = Template(r"tpl1723219371045.png", record_pos=(0.127, 0.127), resolution=(960, 540))
        self.进入排位赛 = Template(r"tpl1720065354455.png", record_pos=(0.29, 0.181), resolution=(960, 540))
        self.进入5v5匹配 = Template(r"tpl1689666019941.png", record_pos=(-0.401, 0.098), resolution=(960, 540))
        self.进入人机匹配 = Template(r"tpl1689666034409.png", record_pos=(0.056, 0.087), resolution=(960, 540))
        # 回忆礼册
        self.大厅回忆礼册 = Template(r"tpl1723334115249.png", record_pos=(0.206, 0.244), resolution=(960, 540))
        self.获取回忆之证 = Template(r"tpl1727227611850.png", record_pos=(0.428, 0.214), resolution=(960, 540))
        self.礼册记忆碎片 = Template(r"tpl1723334128219.png", record_pos=(0.355, 0.222), resolution=(960, 540))
        #
        self.大厅祈愿 = []
        self.大厅祈愿.append(Template(r"tpl1724317603873.png", record_pos=(0.443, -0.105), resolution=(960, 540)))
        self.大厅活动 = []
        self.大厅活动.append(Template(r"tpl1728168902804.png", record_pos=(0.463, -0.025), resolution=(960, 540)))

        # 这种活动图标总在变，直接写死成绝对坐标来避免识别
        #
        # 开始图标和登录图标等很接近, 不要用于房间判断
        self.房间中的开始按钮图标 = []
        self.房间中的开始按钮图标.append(Template(r"tpl1689666117573.png", record_pos=(0.096, 0.232), resolution=(960, 540), threshold=0.9))
        # 新年活动结束时,替换一个常规的取消准备按钮
        self.房间中的取消按钮图标 = []
        self.房间中的取消按钮图标.append(Template(r"tpl1699179402893.png", record_pos=(0.098, 0.233), resolution=(960, 540), threshold=0.9))
        self.大厅元素 = []
        self.大厅元素.append(self.大厅对战图标)
        self.大厅元素.append(self.大厅万象天工)
        self.大厅元素.append(self.大厅排位赛)
        self.房间元素 = []
        self.房间元素.append(Template(r"tpl1690442701046.png", record_pos=(0.135, -0.029), resolution=(960, 540)))
        self.房间元素.append(Template(r"tpl1700304317380.png", record_pos=(-0.38, -0.252), resolution=(960, 540)))
        self.房间元素.append(Template(r"tpl1691463676972.png", record_pos=(0.356, -0.258), resolution=(960, 540)))
        self.房间元素.append(Template(r"tpl1700304304172.png", record_pos=(0.39, -0.259), resolution=(960, 540)))
        # 对战页面元素
        self.普攻 = Template(r"tpl1689666416575.png", record_pos=(0.362, 0.2), resolution=(960, 540), threshold=0.9)
        self.移动 = Template(r"tpl1702267006237.png", record_pos=(-0.327, 0.16), resolution=(960, 540))
        self.钱袋 = Template(r"tpl1719485696322.png", record_pos=(-0.469, -0.059), resolution=(960, 540), threshold=0.9)
        self.普攻S = [self.普攻]  # 其他特色的攻击图标
        self.移动S = [self.移动]  # 其他特色的移动图标
        self.装备S = []
        #
        self.普攻S.append(Template(r"tpl1719546715992.png", record_pos=(0.366, 0.196), resolution=(960, 540)))
        self.普攻S.append(Template(r"tpl1719546725396.png", record_pos=(0.37, 0.197), resolution=(960, 540)))
        self.普攻S.append(Template(r"tpl1719546735621.png", record_pos=(0.369, 0.199), resolution=(960, 540)))
        self.普攻S.append(Template(r"tpl1719546976757.png", record_pos=(0.368, 0.201), resolution=(960, 540)))
        self.普攻S.append(Template(r"tpl1719546988763.png", record_pos=(0.366, 0.2), resolution=(960, 540)))
        self.普攻S.append(Template(r"tpl1719547004757.png", record_pos=(0.365, 0.198), resolution=(960, 540)))
        #
        self.装备S.append(Template(r"tpl1709220117102.png", record_pos=(0.401, -0.198), resolution=(960, 540)))
        self.装备S.append(Template(r"tpl1725075714801.png", record_pos=(0.398, -0.203), resolution=(960, 540)))
        self.装备S.append(Template(r"tpl1725076266344.png", record_pos=(0.399, -0.198), resolution=(960, 540)))
        #
        self.对战图片元素 = [self.钱袋]
        for i in self.普攻S[:1]:
            self.对战图片元素.append(i)
        for i in self.移动S:
            self.对战图片元素.append(i)
        self.对战图片元素.append(Template(r"tpl1719546803645.png", record_pos=(-0.005, 0.223), resolution=(960, 540)))
        #
        self.友方血条 = []
        self.敌方血条 = []
        self.敌方血条.append(Template(r"tpl1720003668795.png", record_pos=(0.082, -0.195), resolution=(960, 540)))
        self.敌方血条.append(Template(r"tpl1720003679285.png", record_pos=(0.083, -0.193), resolution=(960, 540)))
        self.敌方血条.append(Template(r"tpl1720003823052.png", record_pos=(-0.128, -0.191), resolution=(960, 540)))
        self.友方血条.append(Template(r"tpl1720004138271.png", record_pos=(0.151, -0.121), resolution=(960, 540)))
        self.友方血条.append(Template(r"tpl1720004235372.png", record_pos=(-0.342, -0.051), resolution=(960, 540)))
        self.友方血条.append(Template(r"tpl1720004340139.png", record_pos=(0.007, -0.224), resolution=(960, 540)))
        #
        self.钱袋子_模拟战 = Template(r"tpl1690546610171.png", record_pos=(0.391, 0.216), resolution=(960, 540))
        self.刷新金币_模拟战 = Template(r"tpl1690547053276.png", record_pos=(0.458, -0.045), resolution=(960, 540))
        self.关闭钱袋子_模拟战 = Template(r"tpl1690547457483.png", record_pos=(0.392, 0.216), resolution=(960, 540))
        self.对战图片元素_模拟战 = [self.钱袋子_模拟战, self.刷新金币_模拟战, self.关闭钱袋子_模拟战]
        self.对战图片元素_模拟战.append(Template(r"tpl1690546926096.png", record_pos=(-0.416, -0.076), resolution=(960, 540)))
        self.对战图片元素_模拟战.append(Template(r"tpl1690547491681.png", record_pos=(0.471, 0.165), resolution=(960, 540)))
        self.对战图片元素_模拟战.append(Template(r"tpl1690552290188.png", record_pos=(0.158, 0.089), resolution=(960, 540)))
        # 登录关闭按钮
        self.王者登录关闭按钮 = []
        self.王者登录关闭按钮.append(Template(r"tpl1692947351223.png", record_pos=(0.428, -0.205), resolution=(960, 540), threshold=0.9))
        self.王者登录关闭按钮.append(Template(r"tpl1699616162254.png", record_pos=(0.38, -0.237), resolution=(960, 540), threshold=0.9))
        self.王者登录关闭按钮.append(Template(r"tpl1692951432616.png", record_pos=(0.346, -0.207), resolution=(960, 540)))
        self.王者登录关闭按钮.append(Template(r"tpl1693271987720.png", record_pos=(0.428, -0.205), resolution=(960, 540), threshold=0.9))
        self.王者登录关闭按钮.append(Template(r"tpl1700294024287.png", record_pos=(0.465, -0.214), resolution=(1136, 640)))
        self.王者登录关闭按钮.append(Template(r"tpl1707232517229.png", record_pos=(0.394, -0.237), resolution=(960, 540)))
        self.王者登录关闭按钮.append(Template(r"tpl1719742718808.png", record_pos=(0.394, -0.241), resolution=(960, 540)))
        # 返回图标
        self.返回按钮 = []
        self.返回按钮.append(Template(r"tpl1694442171115.png", record_pos=(-0.441, -0.252), resolution=(960, 540)))
        self.返回按钮.append(Template(r"tpl1707399262936.png", record_pos=(-0.478, -0.267), resolution=(960, 540)))
        self.返回按钮.append(Template(r"tpl1694442136196.png", record_pos=(-0.445, -0.251), resolution=(960, 540)))
        self.返回按钮.append(Template(r"tpl1692949580380.png", record_pos=(-0.458, -0.25), resolution=(960, 540), threshold=0.9))
        self.返回按钮.append(Template(r"tpl1707301421376.png", record_pos=(-0.445, -0.253), resolution=(960, 540)))
        # 确定按钮
        # 不同模块的确定按钮位置不同，把record_pos相同的统一替换一下，其他的先不处理了
        self.蓝色确定按钮 = []
        self.蓝色确定按钮.append(Template(r"tpl1693660628972.png", record_pos=(-0.003, 0.118), resolution=(960, 540)))
        self.蓝色确定按钮.append(Template(r"tpl1689667950453.png", record_pos=(-0.001, 0.111), resolution=(960, 540)))
        self.蓝色确定按钮.append(Template(r"tpl1705069645193.png", record_pos=(-0.105, 0.165), resolution=(960, 540)))
        self.蓝色确定按钮.append(Template(r"tpl1700454996867.png", record_pos=(-0.099, 0.166), resolution=(960, 540)))
        self.蓝色确定按钮.append(Template(r"tpl1694441190629.png", record_pos=(0.0, 0.165), resolution=(960, 540)))
        self.蓝色确定按钮.append(Template(r"tpl1694487498294.png", record_pos=(-0.097, 0.24), resolution=(960, 540)))
        #
        self.金色确定按钮 = []
        self.金色确定按钮.append(Template(r"tpl1689666339749.png", record_pos=(0.421, 0.237), resolution=(960, 540)))
        self.金色确定按钮.append(Template(r"tpl1700454883635.png", record_pos=(0.098, 0.118), resolution=(960, 540)))
        self.金色确定按钮.append(Template(r"tpl1700454987098.png", record_pos=(0.1, 0.117), resolution=(960, 540)))
        self.金色确定按钮.append(Template(r"tpl1694441373245.png", record_pos=(-0.002, 0.116), resolution=(960, 540)))

        self.战绩页面元素 = []
        self.战绩页面元素.append(Template(r"tpl1699677816333.png", record_pos=(0.408, 0.226), resolution=(960, 540)))
        self.战绩页面元素.append(Template(r"tpl1699677826933.png", record_pos=(-0.011, -0.257), resolution=(960, 540)))
        self.战绩页面元素.append(Template(r"tpl1699766285319.png", record_pos=(-0.009, -0.257), resolution=(960, 540)))
        self.战绩页面元素.append(Template(r"tpl1689667038979.png", record_pos=(0.235, -0.125), resolution=(960, 540)))
        self.战绩页面元素.append(Template(r"tpl1689669071283.png", record_pos=(-0.001, -0.036), resolution=(960, 540)))
        self.结算页面元素 = []
        self.结算页面元素.append(Template(r"tpl1727234712515.png", record_pos=(-0.007, 0.018), resolution=(960, 540)))
        self.结算页面元素.append(Template(r"tpl1727237953837.png", record_pos=(-0.008, -0.009), resolution=(960, 540)))
        self.结算页面元素.append(Template(r"tpl1727231951999.png", record_pos=(0.433, -0.235), resolution=(960, 540)))
        self.结算页面元素.append(Template(r"tpl1727235773717.png", record_pos=(0.458, -0.24), resolution=(960, 540)))
        self.结算页面元素.append(Template(r"tpl1727235767022.png", record_pos=(0.028, 0.252), resolution=(960, 540)))
        self.结算页面元素.append(Template(r"tpl1727236520434.png", record_pos=(0.103, -0.067), resolution=(960, 540)))
        #
        self.返回房间按钮 = Template(r"tpl1689667226045.png", record_pos=(0.079, 0.226), resolution=(960, 540), threshold=0.9)
        self.房间我知道了 = Template(r"tpl1707519287850.png", record_pos=(-0.006, 0.191), resolution=(960, 540))
        # 这些活动翻页元素一般只显示一次，新的账户每次进入房间都会提示
        self.房间翻页活动元素 = []
        self.房间翻页活动元素.append(Template(r"tpl1707519278270.png", record_pos=(0.014, -0.191), resolution=(960, 540)))
        self.房间翻页活动元素.append(Template(r"tpl1707784321085.png", record_pos=(-0.004, -0.219), resolution=(960, 540)))
        self.房间翻页活动元素.append(Template(r"tpl1707787106337.png", record_pos=(-0.001, -0.22), resolution=(960, 540)))
        self.房间翻页活动元素.append(Template(r"tpl1708654174076.png", record_pos=(-0.001, -0.22), resolution=(960, 540)))
        self.房间翻页活动元素.append(Template(r"tpl1708826597289.png", record_pos=(0.002, -0.219), resolution=(960, 540)))
        self.房间翻页活动元素.append(Template(r"tpl1708826597289.png", record_pos=(0.002, -0.219), resolution=(960, 540)))
        self.房间翻页活动元素.append(Template(r"tpl1708829601719.png", record_pos=(0.001, -0.22), resolution=(960, 540)))
        self.房主头像 = Template(r"tpl1716782981770.png", record_pos=(0.354, -0.164), resolution=(960, 540), target_pos=9)
        self.房主房间 = Template(r"tpl1700284856473.png", record_pos=(0.312, -0.17), resolution=(1136, 640), target_pos=2)
        #
        # 头像数据
        self.英雄_海诺 = Template(r"tpl1701750143194.png", record_pos=(-0.36, 0.135), resolution=(960, 540))
        self.英雄_牙 = Template(r"tpl1701436836229.png", record_pos=(0.107, -0.085), resolution=(1136, 640))
        self.英雄_太乙 = Template(r"tpl1690442560069.png", record_pos=(0.11, 0.025), resolution=(960, 540))
        self.英雄_鬼谷子 = Template(r"tpl1701759712161.png", record_pos=(0.203, 0.026), resolution=(1136, 640))
        self.英雄_云中 = Template(r"tpl1701750390892.png", record_pos=(-0.172, 0.24), resolution=(1136, 640))
        self.英雄_八戒 = Template(r"tpl1701573854122.png", record_pos=(0.297, 0.135), resolution=(1136, 640))
        self.参战英雄线路_dict = {}
        self.参战英雄头像_dict = {}
        self.参战英雄线路_dict[0] = Template(r"tpl1689665490071.png", record_pos=(-0.315, -0.257), resolution=(960, 540))
        self.参战英雄头像_dict[0] = self.英雄_八戒
        self.参战英雄线路_dict[1] = Template(r"tpl1689665455905.png", record_pos=(-0.066, -0.256), resolution=(960, 540))
        self.参战英雄头像_dict[1] = self.英雄_海诺
        self.参战英雄线路_dict[2] = Template(r"tpl1689665540773.png", record_pos=(0.06, -0.259), resolution=(960, 540))
        self.参战英雄头像_dict[2] = self.英雄_牙
        self.参战英雄线路_dict[3] = Template(r"tpl1689665577871.png", record_pos=(0.183, -0.26), resolution=(960, 540))
        self.参战英雄头像_dict[3] = self.英雄_鬼谷子
        self.参战英雄线路_dict[4] = Template(r"tpl1686048521443.png", record_pos=(0.06, -0.259), resolution=(960, 540))
        self.参战英雄头像_dict[4] = self.英雄_云中
        self.参战英雄线路_dict[5] = Template(r"tpl1689665577871.png", record_pos=(0.183, -0.26), resolution=(960, 540))
        self.参战英雄头像_dict[5] = self.英雄_太乙
        #
        #
        # 礼包图库
        self.战令入口 = Template(r"tpl1721266385770.png", record_pos=(0.343, -0.105), resolution=(960, 540))
        # ------------------------------------------------------------------------------
        self.图片更新FILE = "WZRY.图片更新.txt"
        run_class_command(self=self, command=self.Tool.readfile(self.图片更新FILE))


class wzry_task:
    # 备注
    # 新账户,第一次打开各种模块,如万向天宫,会有动画等展示,脚本不做处理,手动点几下，之后就不会出现了
    # 需要传递中文时,由于精简后无法输入中文,在shell中建
    # redroid_arm64:/mnt/sdcard/Download # touch 诗语江南s4tpxWGu.txt

    def __init__(self):
        # device
        self.mynode = Settings.mynode
        self.totalnode = Settings.totalnode
        self.totalnode_bak = self.totalnode
        self.LINK = Settings.LINK_dict[Settings.mynode]
        #
        # ------------------------------------------------------------------------------
        # deviceOB
        self.移动端 = deviceOB(mynode=self.mynode, totalnode=self.totalnode, LINK=self.LINK)
        # APPOB
        self.设备类型 = self.移动端.设备类型
        self.APPID = "com.tencent.smoba" if "ios" in self.设备类型 else "com.tencent.tmgp.sgame"
        self.APPOB = appOB(APPID=self.APPID, big=True, device=self.移动端)
        # Tool
        self.Tool = DQWheel(var_dict_file=f"{self.移动端.设备类型}.var_dict_{self.mynode}.txt",
                            mynode=self.mynode, totalnode=self.totalnode)
        self.房主 = self.mynode == 0 or self.totalnode == 1
        # ------------------------------------------------------------------------------
        # DQWheel 框架的初始化
        if self.房主:
            self.Tool.init_clean()
        # 强制同步
        if self.totalnode_bak > 1:
            sleep(self.mynode*5)
            self.Tool.touch同步文件(self.Tool.辅助同步文件, "初始化强制同步")
            self.Tool.必须同步等待成功(self.mynode, self.totalnode, sleeptime=10)
        #
        # 统一本次运行的PID, 避免两个脚本同时运行出现控制冲突的情况
        self.WZRYPIDFILE = f".tmp.WZRY.{self.mynode}.PID.txt"
        hour, minu, sec = self.Tool.time_getHMS()
        self.myPID = f"{self.totalnode_bak}.{hour}{minu}{sec}"
        self.myPID = self.Tool.bcastvar(self.mynode, self.totalnode_bak, var=self.myPID, name="self.myPID")
        self.Tool.touchfile(self.WZRYPIDFILE, content=self.myPID)
        TimeECHO(f": 本次运行PID:[{self.myPID}]")
        #
        # ------------------------------------------------------------------------------
        # 对应的控制文件和参数的初始化
        self.只战一天FILE = "WZRY.oneday.txt"  # 今天执行完之后，直接结束程序。适用采用crontab等模式周期性运行脚本，而不采用本脚本自带的循环。
        self.今日休战FILE = "WZRY.tomorrow.txt"  # 今天不打了，明天开始，适合于离开办公室时运行脚本，但是不要执行任何命令，明天早上开始执行
        self.触摸对战FILE = "WZRY.TOUCH.txt"  # 在5v5的对战过程中,频繁触摸,提高金币数量
        self.标准模式触摸对战FILE = "WZRY.标准模式TOUCH.txt"  # 检测到该文件后该次对战使用5v5标准对战模式
        self.标准模式FILE = f"WZRY.{self.mynode}.标准模式.txt"  # 检测到该文件后该次对战使用5v5标准对战模式
        self.临时组队FILE = "WZRY.组队.txt"
        self.玉镖夺魁签到FILE = "玉镖夺魁签到.txt"
        self.免费商城礼包FILE = f"WZRY.{self.mynode}.免费商城礼包.txt"  # 检测到该文件后领每日商城礼包
        self.KPL每日观赛FILE = f"WZRY.KPL每日观赛FILE.txt"
        self.更新体验服FILE = f"WZRY.{self.mynode}.更新体验服.txt"  # 检测到该文件后登录体验服领取体验币
        # 注入命令的文件
        self.重新设置英雄FILE = f"WZRY.{self.mynode}.重新设置英雄.txt"
        self.临时初始化FILE = f"WZRY.{self.mynode}.临时初始化.txt"
        self.对战前插入FILE = f"WZRY.{self.mynode}.对战前插入.txt"
        # 初始化需要删除的文件 or 内部文件
        self.SLEEPFILE = "WZRY.SLEEP.txt"
        self.无法进行组队FILE = f"WZRY.无法进行组队FILE.txt"
        self.青铜段位FILE = f"WZRY.{self.mynode}.青铜段位.txt"  # 检测到该文件后该次对战使用5v5标准对战模式
        self.重新登录FILE = f"WZRY.{self.mynode}.重新登录FILE.txt"
        #
        self.初始化(init=True)
        # 自定义参数可以通过self.设置参数() 插入
        #
        # ------------------------------------------------------------------------------
        # 最后确定所有设备都已同步完成
        self.Tool.barriernode(self.mynode, self.totalnode, "WZRYinit")

    #
    # 从__init_摘过来的一些初始化命令，适用于每天的初始化
    def 初始化(self, init=False):
        # 清空文件
        self.Tool.removefile(self.SLEEPFILE)
        self.Tool.removefile(self.无法进行组队FILE)
        self.Tool.removefile(self.青铜段位FILE)
        self.Tool.removefile(self.重新登录FILE)
        # 图片初始化，这里的图片主要是一些图片列表，例如所有的大厅元素
        self.图片 = wzry_figure(Tool=self.Tool)
        分路长度 = len(self.图片.参战英雄线路_dict)
        self.shiftnode = 0 if init else self.shiftnode
        self.参战英雄线路 = self.图片.参战英雄线路_dict[(self.mynode+0+self.shiftnode) % 分路长度]
        self.参战英雄头像 = self.图片.参战英雄头像_dict[(self.mynode+0+self.shiftnode) % 分路长度]
        self.备战英雄线路 = self.图片.参战英雄线路_dict[(self.mynode+3+self.shiftnode) % 分路长度]
        self.备战英雄头像 = self.图片.参战英雄头像_dict[(self.mynode+3+self.shiftnode) % 分路长度]
        # 礼包初始化
        self.每日礼包(初始化=True)
        #
        # 开发测试的参数
        self.WZ新功能 = True    # 测试稳定版代码使用, 适用于赛季初，不同版本账户的功能界面不同时采用
        self.devmode = False if init else self.devmode  # 测试开发版代码时使用
        # 其他参数
        self.totalnode = self.totalnode_bak
        self.选择人机模式 = True  # 是否根据计算参数选择5v5的人机模式，不然就采用上一次的模式
        self.选择英雄 = True    # 是否根据参数选择英雄，不然就选择上一次使用的英雄
        self.对战结束返回房间 = True
        self.无法进行组队 = False
        #
        # 参数列表初始化
        self.组队模式 = self.totalnode > 1
        self.房主 = self.mynode == 0 or self.totalnode == 1
        self.对战模式 = "5v5匹配" if init else self.对战模式
        self.对战时间 = [0.1, 23.9] if init else self.对战时间
        self.限时组队时间 = 23 if init else self.限时组队时间
        self.runstep = 0 if init else self.runstep
        self.jinristep = 0
        self.青铜段位 = False
        self.标准模式 = False
        self.触摸对战 = False
        # 备份参数，用于比较计算参数是否发生变化
        self.本循环参数 = wzry_runinfo()
        self.上循环参数 = wzry_runinfo()
        self.构建循环参数(self.本循环参数)
        self.构建循环参数(self.上循环参数)
        #
        # 某些加速模块的初始化
        # 如果已经判断在房间中了,短时间内执行相关函数，不再进行判断
        self.当前界面 = "未知"
        self.当前状态 = "未知"  # ["领取礼包","对战状态","未知","重新启动","状态检查"] 根据状态, 减少一些界面的判断，只在主函数中进行设备，避免子函数设置带来的混乱
        self.Tool.timelimit(timekey="当前界面", init=True)

    # 用不到，当二次开发调用wzry_task时, 可在init后，设置这个设置参数
    def 设置参数(self, **kwargs):
        if not kwargs:
            return
        #
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.构建循环参数(self.本循环参数)

    # 保存运行信息
    def 构建循环参数(self, runinfo=None):
        if runinfo == None:
            runinfo = wzry_runinfo()
        # 定义要复制的属性列表
        attributes = [
            '组队模式', '房主', '对战模式', '对战时间', '限时组队时间',
            'runstep', 'jinristep', '青铜段位', '标准模式',
            '触摸对战'
        ]
        # 使用 getattr 和 setattr 循环设置属性
        for attr in attributes:
            setattr(runinfo, attr, getattr(self, attr))

    # 网络优化提示
    def 网络优化(self):
        if exists(Template(r"tpl1693669091002.png", record_pos=(-0.003, -0.015), resolution=(960, 540))):
            TimeECHO("网络优化提示")
            self.Tool.existsTHENtouch(Template(r"tpl1693669117249.png", record_pos=(-0.102, 0.116), resolution=(960, 540)), "下次吧")

    def 确定按钮(self):
        确定按钮 = []
        for i in self.图片.蓝色确定按钮:
            确定按钮.append(i)
        for i in self.图片.金色确定按钮:
            确定按钮.append(i)
        确定按钮 = self.Tool.uniq_Template_array(确定按钮)
        存在, 确定按钮 = self.Tool.存在任一张图(确定按钮, "确定按钮")
        if not 存在:
            return
        for i in 确定按钮:
            self.Tool.existsTHENtouch(i, f"确定{i}", savepos=False)

    def 关闭按钮(self):
        # 这个循环仅作为识别关闭按钮位置的循环
        # 主要用于: self.进入大厅时遇到的复杂的关闭按钮()
        self.图片.王者登录关闭按钮 = self.Tool.uniq_Template_array(self.图片.王者登录关闭按钮)
        存在, self.图片.王者登录关闭按钮 = self.Tool.存在任一张图(self.图片.王者登录关闭按钮, "王者登录关闭按钮")
        if not 存在:
            return
        for i in self.图片.王者登录关闭按钮:
            keyindex = f"王者登陆关闭按钮{i}"
            pos = exists(i)
            if pos:
                self.Tool.var_dict[keyindex] = pos
                self.Tool.existsTHENtouch(i, keyindex, savepos=True)
            else:
                TimeECHO("未识别到"+keyindex)
        #
        存在, self.图片.王者登录关闭按钮 = self.Tool.存在任一张图(self.图片.王者登录关闭按钮, "王者登录关闭按钮")
        if not 存在:
            return
        for i in self.图片.王者登录关闭按钮:
            self.Tool.LoopTouch(i, f"王者登录关闭按钮{i}", loop=3, savepos=False)
    #

    def 进入大厅时遇到的复杂的关闭按钮(self):
        self.关闭按钮()
        if self.判断大厅中():
            return True
        TimeECHO(": 未能进入大厅,有可能有新的关闭按钮,继续尝试关闭中")
        for key, value in self.Tool.var_dict.items():
            if "王者登陆关闭按钮" not in key:
                continue
            TimeECHO(":尝试touch:"+key)
            touch(value)
            if self.判断大厅中():
                return True
        return False
        #

    def 进入大厅(self, times=0):
        #
        if not self.check_run_status():
            return True
        #
        if self.set_timelimit(istep=times, init=times == 0, timelimit=60*30, nstep=10, touch同步=True):
            TimeECHO(f"进入大厅超时退出,更新图片资源库")
            self.图片 = wzry_figure(Tool=self.Tool)
            return False
        #
        times = times+1
        TimeECHO(f"{fun_name(2)}.尝试进入大厅{times}")
        #
        if not self.APPOB.前台APP(2):
            return self.进入大厅(times)
        #
        if self.判断大厅中():
            return True
        # 次数上限
        if times % 4 == 3:
            self.重启并登录(10)
            if self.判断大厅中():
                return True
            else:
                return self.进入大厅(times)
        #
        if not self.check_run_status():
            return True
        if "ios" in self.移动端.LINK:
            配件不支持 = Template(r"tpl1701523669097.png", record_pos=(-0.001, 0.002), resolution=(1136, 640))
            关闭配件不支持 = Template(r"tpl1701523677678.png", record_pos=(-0.004, 0.051), resolution=(1136, 640))
            if exists(配件不支持):
                self.Tool.existsTHENtouch(关闭配件不支持, "关闭配件不支持")
            if self.判断大厅中():
                return True
        if self.判断对战中():
            处理对战 = "模拟战" in self.对战模式
            if self.触摸对战:
                处理对战 = True
            while self.判断对战中(处理对战):
                TimeECHO("尝试进入大厅:对战sleep")
                sleep(15)  # sleep太久容易死
                if self.Tool.timelimit(timekey="结束对战", limit=60*15, init=False):
                    break
            self.结束人机匹配()
        if self.判断战绩页面():
            self.结束人机匹配()
        #
        if exists(self.图片.登录界面开始游戏图标):
            if not self.登录游戏(检测到登录界面=True):
                return self.进入大厅(times)
        self.网络优化()
        # 各种异常，异常图标,比如网速不佳、画面设置、
        self.Tool.existsTHENtouch(Template(r"tpl1692951507865.png", record_pos=(-0.106, 0.12), resolution=(960, 540), threshold=0.9), "关闭画面设置")
        # 更新资源
        WIFI更新资源 = Template(r"tpl1694357134235.png", record_pos=(-0.004, -0.019), resolution=(960, 540))
        if exists(WIFI更新资源):
            self.Tool.existsTHENtouch(Template(r"tpl1694357142735.png", record_pos=(-0.097, 0.116), resolution=(960, 540)))
        if self.判断大厅中():
            return True
        # 更新图形显示设置
        显示设置 = Template(r"tpl1694359268612.png", record_pos=(-0.002, 0.12), resolution=(960, 540))
        if exists(显示设置):
            self.Tool.existsTHENtouch(Template(r"tpl1694359275922.png", record_pos=(-0.113, 0.124), resolution=(960, 540)))
            if self.判断大厅中():
                return True
        #
        if not self.check_run_status():
            return True
        # 返回图标
        返回图标 = Template(r"tpl1692949580380.png", record_pos=(-0.458, -0.25), resolution=(960, 540), threshold=0.9)
        self.Tool.LoopTouch(返回图标, "返回图标", loop=5, savepos=False)
        if self.判断大厅中():
            return True
        self.确定按钮()
        if exists(Template(r"tpl1693886922690.png", record_pos=(-0.005, 0.114), resolution=(960, 540))):
            self.Tool.existsTHENtouch(Template(r"tpl1693886962076.png", record_pos=(0.097, 0.115), resolution=(960, 540)), "确定按钮")
            if self.判断大厅中():
                return True
            if not self.check_run_status():
                return True
        # 邀请
        if exists(Template(r"tpl1692951548745.png", record_pos=(0.005, 0.084), resolution=(960, 540))):
            关闭邀请 = Template(r"tpl1692951558377.png", record_pos=(0.253, -0.147), resolution=(960, 540), threshold=0.9)
            self.Tool.LoopTouch(关闭邀请, "关闭邀请", loop=5, savepos=False)
        # 老账号的友情提示
        if exists(Template(r"tpl1707377651759.png", record_pos=(-0.282, -0.032), resolution=(960, 540))):
            关闭邀请 = Template(r"tpl1707377671958.png", record_pos=(0.453, -0.205), resolution=(960, 540))
            self.Tool.LoopTouch(关闭邀请, "关闭友情对战推荐", loop=5, savepos=False)
        #
        if self.判断大厅中():
            return True
        #
        if not self.check_run_status():
            return True
        #
        # 健康系统直接重新同步
        if self.健康系统_常用命令():
            return True
        return self.进入大厅(times)

    def 登录游戏(self, times=0, 检测到登录界面=False):
        if times == 0:
            self.Tool.timelimit(timekey="登录游戏", limit=60*5, init=True)
            self.Tool.removefile(self.重新登录FILE)
        times = times+1
        if not self.check_run_status():
            return True
        if times > 1 and not 检测到登录界面:
            TimeErr(f"登录游戏:{times}次没有检测到登录界面")
        # 这里是为了避免，卡在游戏界面，定时重启一下
        if times % 4 == 3 or self.Tool.timelimit(timekey="登录游戏", limit=60*10, init=False):
            TimeErr(f"登录游戏:{times}次登录失败,重启设备")
            self.移动端.重启重连设备(10)
            检测到登录界面 = self.APPOB.前台APP(2)
        #
        if times > 8:
            TimeErr(f"登录游戏:{times}次登录失败,返回")
            return False
        TimeECHO(f"{fun_name(2)}>登录游戏{times}")
        if not self.APPOB.前台APP(2):
            return self.登录游戏(times, False)
        #
        if exists(self.图片.网络不可用):
            content = "网络不可用,取消登录,需要重启设备"
            self.创建同步文件(content)
            return True
        if self.判断大厅中():
            return True
        #
        # 更新公告
        更新公告 = Template(r"tpl1692946575591.png", record_pos=(0.103, -0.235), resolution=(960, 540), threshold=0.9)
        if exists(更新公告):
            检测到登录界面 = True
            for igengxin in np.arange(30):
                TimeECHO("更新中%d" % (igengxin))
                关闭更新 = Template(r"tpl1693446444598.png", record_pos=(0.428, -0.205), resolution=(960, 540), threshold=0.9)
                金色确定 = Template(r"tpl1692946738054.png", record_pos=(-0.002, 0.116), resolution=(960, 540), threshold=0.9)
                if self.Tool.existsTHENtouch(关闭更新, "关闭更新", savepos=False):
                    sleep(10)
                    self.Tool.existsTHENtouch(金色确定, "金色确定", savepos=True)
                    break
                if exists(Template(r"tpl1692946702006.png", record_pos=(-0.009, -0.014), resolution=(960, 540), threshold=0.9)):
                    TimeECHO("更新完成")
                    self.Tool.existsTHENtouch(金色确定, "金色确定", savepos=True)
                    sleep(60)
                    break
                elif not exists(更新公告):
                    TimeECHO("找不到更新公告.break")
                    break
                if exists(Template(r"tpl1692952266315.png", record_pos=(-0.411, 0.266), resolution=(960, 540), threshold=0.9)):
                    TimeECHO("正在下载资源包")
                sleep(60)
                self.确定按钮()
        同意游戏 = Template(r"tpl1692946883784.png", record_pos=(0.092, 0.145), resolution=(960, 540), threshold=0.9)
        if exists(Template(r"tpl1692946837840.png", record_pos=(-0.092, -0.166), resolution=(960, 540), threshold=0.9)):
            检测到登录界面 = True
            self.Tool.existsTHENtouch(同意游戏, "同意游戏", savepos=True)
            TimeECHO("同意游戏")
        #
        if self.Tool.existsTHENtouch(同意游戏, "同意游戏", savepos=False):
            检测到登录界面 = True
        #
        # 这里是账户被退出的界面，需要重新登录了
        if exists(Template(r"tpl1692946938717.png", record_pos=(-0.108, 0.159), resolution=(960, 540), threshold=0.9)):
            self.Tool.touchfile(self.重新登录FILE)
            #
            self.创建同步文件("需要重新登录")
            #
            return True
        #
        if exists(Template(r"tpl1692951324205.png", record_pos=(0.005, -0.145), resolution=(960, 540))):
            检测到登录界面 = True
            TimeECHO("关闭家长模式")
            touch(Template(r"tpl1692951358456.png", record_pos=(0.351, -0.175), resolution=(960, 540)))
            sleep(5)
        #
        if self.Tool.existsTHENtouch(self.图片.登录界面开始游戏图标, "登录界面.开始游戏", savepos=False):
            检测到登录界面 = True
            sleep(10)
            # 模拟器点击登陆后容易闪退
            if not self.APPOB.前台APP(0):
                return self.登录游戏(times, False)
            # 登陆后一般会有活动需要关闭
            self.关闭按钮()
            if self.判断大厅中():
                return True
        else:
            # 现在打开可能会放一段视频，这个随意点击也为了让界面换一下
            self.Tool.touch_record_pos(record_pos=(0, 0), resolution=self.移动端.resolution, keystr=f"{fun_name(1)}.屏幕中心")
        # 再检查一下登录情况
        取消 = Template(r"tpl1697785803856.png", record_pos=(-0.099, 0.115), resolution=(960, 540))
        关闭 = Template(r"tpl1719739199756.png", record_pos=(-0.059, 0.209), resolution=(960, 540))
        self.Tool.existsTHENtouch(取消, "取消按钮")
        self.Tool.existsTHENtouch(关闭, "关闭按钮")
        self.关闭按钮()
        self.Tool.existsTHENtouch(取消, "取消按钮")
        self.Tool.existsTHENtouch(关闭, "关闭按钮")
        #
        if self.Tool.existsTHENtouch(self.图片.登录界面开始游戏图标, "登录界面.开始游戏", savepos=False):
            检测到登录界面 = True
            sleep(10)
            # 模拟器点击登陆后容易闪退
            if not self.APPOB.前台APP(0):
                return self.登录游戏(times, False)
            self.关闭按钮()
        if self.判断大厅中():
            return True
        #
        # ..................................................................................
        # 第一次万一已经登录过了
        if not 检测到登录界面 and times > 1:
            return self.登录游戏(times, 检测到登录界面)
        # ..................................................................................
        # 下面是点击登录之后的一些处理
        #
        # 健康系统直接重新同步
        if self.健康系统_常用命令():
            return True
        havetouch = False
        # 动态下载资源提示
        回归礼物 = Template(r"tpl1699607355777.png", resolution=(1136, 640))
        if exists(回归礼物):
            havetouch = True
            self.Tool.existsTHENtouch(Template(r"tpl1699607371836.png", resolution=(1136, 640)))
        回归挑战 = Template(r"tpl1699680234401.png", record_pos=(0.314, 0.12), resolution=(1136, 640))
        self.Tool.existsTHENtouch(回归挑战, "不进行回归挑战")
        存在返回按钮, self.图片.返回按钮 = self.Tool.存在任一张图(self.图片.返回按钮, "登录返回按钮", savepos=True)
        if 存在返回按钮:
            havetouch = True
            self.Tool.existsTHENtouch(self.图片.返回按钮[0], "登录返回按钮", savepos=True)
            self.确定按钮()
        #
        if havetouch and self.判断大厅中():
            return True
        #
        self.关闭按钮()
        self.网络优化()
        # 各种异常，异常图标,比如网速不佳、画面设置、
        self.Tool.existsTHENtouch(Template(r"tpl1692951507865.png", record_pos=(-0.106, 0.12), resolution=(960, 540), threshold=0.9), "关闭画面设置")
        # 更新资源
        WIFI更新资源 = Template(r"tpl1694357134235.png", record_pos=(-0.004, -0.019), resolution=(960, 540))
        if exists(WIFI更新资源):
            self.Tool.existsTHENtouch(Template(r"tpl1694357142735.png", record_pos=(-0.097, 0.116), resolution=(960, 540)), "取消更新")
        #
        动态下载资源 = Template(r"tpl1697785792245.png", record_pos=(-0.004, -0.009), resolution=(960, 540))
        if exists(动态下载资源):
            self.Tool.existsTHENtouch(取消, "取消按钮")
        self.Tool.existsTHENtouch(取消, "取消按钮")
        # 活动界面
        self.进入大厅时遇到的复杂的关闭按钮()
        self.Tool.existsTHENtouch(取消, "取消按钮")
        if self.判断大厅中():
            return True
        #
        今日不再弹出 = Template(r"tpl1693272038809.png", record_pos=(0.38, 0.215), resolution=(960, 540), threshold=0.9)
        if exists(今日不再弹出):  # 当活动海报太大时，容易识别关闭图标错误，此时采用历史的关闭图标位置
            TimeECHO("今日不再弹出仍在")
            self.Tool.existsTHENtouch(取消, "取消按钮")
            self.进入大厅时遇到的复杂的关闭按钮()
            self.网络优化()
            if self.判断大厅中():
                return True
            else:
                sleep(10)
        #
        return self.登录游戏(times, 检测到登录界面)

    def 单人进入人机匹配房间(self, times=0):
        if not self.check_run_status():
            return True
        if "ios" in self.移动端.LINK:
            配件不支持 = Template(r"tpl1701523669097.png", record_pos=(-0.001, 0.002), resolution=(1136, 640))
            关闭配件不支持 = Template(r"tpl1701523677678.png", record_pos=(-0.004, 0.051), resolution=(1136, 640))
            if exists(配件不支持):
                self.Tool.existsTHENtouch(关闭配件不支持, "关闭配件不支持")
        if "模拟战" in self.对战模式:
            TimeECHO(f"首先进入人机匹配房间_模拟战{times}")
            return self.单人进入人机匹配房间_模拟战(times)
        if "5v5排位" == self.对战模式:
            TimeECHO(f"首先进入排位房间{times}")
            return self.单人进入排位房间(times)
        #
        # ... 状态检查和重置
        TimeECHO(f"首先进入人机匹配房间{times}")
        if self.判断对战中():
            self.结束人机匹配()
            if self.判断房间中(处理=False):
                return True
        if self.判断房间中():
            return True
        self.进入大厅()
        if not self.check_run_status():
            return True
        #
        if self.set_timelimit(istep=times, init=times == 0, timelimit=60*10, nstep=10, touch同步=True):
            content = "单人进入人机匹配房间超时"
            self.创建同步文件(content)
            return True
        #
        times = times+1
        #
        if not self.Tool.existsTHENtouch(self.图片.大厅对战图标, "大厅对战", savepos=True):
            return self.单人进入人机匹配房间(times)
        sleep(2)
        if not self.Tool.existsTHENtouch(self.图片.进入5v5匹配, "5v5王者峡谷", savepos=True):
            return self.单人进入人机匹配房间(times)
        sleep(2)
        if not self.Tool.existsTHENtouch(self.图片.进入人机匹配, "进入人机匹配", savepos=False):
            del self.Tool.var_dict["大厅对战"]
            del self.Tool.var_dict["5v5王者峡谷"]
            return self.单人进入人机匹配房间(times)
        sleep(2)
        #
        段位key = "青铜段位" if self.青铜段位 else "星耀段位"
        if self.选择人机模式:
            TimeECHO("选择对战模式")
            匹配模式 = {}
            匹配模式["标准模式"] = Template(r"tpl1702268393125.png", record_pos=(-0.35, -0.148), resolution=(960, 540))
            匹配模式["快速模式"] = Template(r"tpl1689666057241.png", record_pos=(-0.308, -0.024), resolution=(960, 540))
            key = "快速模式"
            if self.标准模式:
                key = "标准模式"
            if not self.Tool.existsTHENtouch(匹配模式[key], key):
                return self.单人进入人机匹配房间(times)
            # 选择难度
            段位图标 = {}
            段位图标["青铜段位"] = Template(r"tpl1689666083204.png", record_pos=(0.014, -0.148), resolution=(960, 540))
            段位图标["星耀段位"] = Template(r"tpl1689666092009.png", record_pos=(0.0, 0.111), resolution=(960, 540))
            self.Tool.existsTHENtouch(段位图标[段位key], "选择"+段位key, savepos=False)
        # 开始练习
        开始练习 = Template(r"tpl1689666102973.png", record_pos=(0.323, 0.161), resolution=(960, 540), threshold=0.9)
        开始练习 = Template(r"tpl1700298996343.png", record_pos=(0.326, 0.197), resolution=(1136, 640), threshold=0.9, target_pos=2)

        # 开始练习和下页的开始匹配太像了,修改一下
        if not self.Tool.existsTHENtouch(开始练习, "开始练习"):
            return self.单人进入人机匹配房间(times)
        #
        sleep(10)
        禁赛提示 = Template(r"tpl1700128026288.png", record_pos=(-0.002, 0.115), resolution=(960, 540))
        if exists(禁赛提示):
            content = "禁赛提示无法进行匹配"
            return self.创建同步文件(content)
        #
        # 段位限制
        if not self.青铜段位:  # 其他段位有次数限制
            if self.Tool.LoopTouch(开始练习, "开始练习", loop=3):
                TimeECHO(":高阶段位已达上限,采用青铜模式")
                self.青铜段位 = True
                self.选择人机模式 = True
                段位key = "青铜段位"
                self.Tool.existsTHENtouch(段位图标[段位key], "选择"+段位key, savepos=False)
                self.Tool.existsTHENtouch(开始练习, "开始练习")
                self.Tool.touchfile(self.青铜段位FILE)
                if self.组队模式:
                    TimeErr("段位不合适,创建同步文件")
                    self.Tool.touch同步文件(self.Tool.辅助同步文件)
                    return
                else:
                    return self.单人进入人机匹配房间(times)
        #
        if not self.判断房间中():
            # 有时候长时间不进去被禁赛了
            确定按钮 = Template(r"tpl1689667950453.png", record_pos=(-0.001, 0.111), resolution=(960, 540))
            while self.Tool.existsTHENtouch(确定按钮, "不匹配被禁赛的确定按钮"):
                sleep(20)
                if self.Tool.existsTHENtouch(开始练习, "开始练习"):
                    sleep(10)
                # 信誉分很低时，这里会被禁数十小时，此时不适合继续等待下去了
                if self.set_timelimit(istep=times, init=times == 0, timelimit=60*10, nstep=10, touch同步=True):
                    self.创建同步文件("不匹配被禁赛")
                    return True
                if not self.check_run_status():
                    return True
            return self.单人进入人机匹配房间(times)
        return True

    def 单人进入排位房间(self, times=0):
        if not self.check_run_status():
            return True
        # ... 状态检查和重置
        TimeECHO(f"首先进入排位房间{times}")
        if self.判断对战中():
            self.结束人机匹配()
            if self.判断房间中(处理=False):
                return True
        if self.判断房间中():
            return True
        self.进入大厅()
        if not self.check_run_status():
            return True
        #
        if self.set_timelimit(istep=times, init=times == 0, timelimit=60*10, nstep=30, touch同步=True):
            return True
        #
        times = times+1
        if not self.Tool.existsTHENtouch(self.图片.大厅排位赛, "大厅排位赛", savepos=False):
            TimeErr("找不到大厅排位赛")
            return self.单人进入排位房间(times)
        sleep(10)
        if not self.Tool.existsTHENtouch(self.图片.进入排位赛, "进入排位赛", savepos=False):
            TimeErr("找不到进入排位赛")
            return self.单人进入排位房间(times)
        #
        if not self.判断房间中():
            # 有时候长时间不进去被禁赛了
            确定按钮 = Template(r"tpl1689667950453.png", record_pos=(-0.001, 0.111), resolution=(960, 540))
            while self.Tool.existsTHENtouch(确定按钮, "不匹配被禁赛的确定按钮"):
                sleep(20)
                if self.set_timelimit(istep=times, init=times == 0, timelimit=60*10, nstep=30, touch同步=True):
                    self.创建同步文件("不匹配被禁赛, 超时无法进入")
                    return True
            return self.单人进入排位房间(times)
        return True
    #

    def 进入人机匹配房间(self):
        if not self.check_run_status():
            return True
        TimeECHO("进入人机匹配房间")
        self.单人进入人机匹配房间()
        if not self.组队模式:
            return
        TimeECHO("进入组队匹配房间")
        # 组队时,使用青铜模式进行, 前面应该已经配置好了青铜段位,这里进一步加强青铜段位确定
        if "5v5匹配" == self.对战模式 and not self.青铜段位 and self.房主:
            TimeECHO(":组队模式只在青铜段位进行,房主应该使用青铜段位建房间,重建房间中")
            self.青铜段位 = True
            self.进入大厅()
            self.单人进入人机匹配房间()
        # ...............................................................
        # 当多人组队模式时，这里要暂时保证是房间中，因为邀请系统还没写好
        self.Tool.barriernode(self.mynode, self.totalnode, "组队进房间")
        if not self.房主:
            sleep(self.mynode*10)
        self.Tool.timelimit(timekey=f"组队模式进房间{self.mynode}", limit=60*5, init=True)
        if not self.check_run_status():
            return True
        if not self.房主:
            找到取消按钮, self.图片.房间中的取消按钮图标 = self.Tool.存在任一张图(self.图片.房间中的取消按钮图标, "房间中的取消准备按钮")
            self.Tool.timelimit(timekey=f"辅助进房{self.mynode}", limit=60*5, init=True)
            while not 找到取消按钮:
                if self.Tool.timelimit(timekey=f"辅助进房{self.mynode}", limit=60*5, init=False):
                    self.Tool.touch同步文件(self.Tool.辅助同步文件, "辅助进房超时退出")
                    break
                if not self.check_run_status():
                    TimeErr("辅助进房失败")
                    return True
                #
                # 需要小号和主号建立亲密关系，并在主号中设置亲密关系自动进入房间
                TimeECHO("不在组队的房间中")
                if not self.判断房间中(处理=False):
                    self.单人进入人机匹配房间()
                # 这里给的是特殊账户的头像
                进房 = self.图片.房主头像
                self.Tool.timedict["当前界面"] = 0
                TimeECHO("准备进入组队房间")
                if not exists(进房):
                    TimeECHO("没找到房主头像, 采用通用房主头像")
                    进房 = Template(r"tpl1699181922986.png", record_pos=(0.46, -0.15), resolution=(960, 540), threshold=0.9)
                if self.Tool.existsTHENtouch(进房, "房主头像按钮", savepos=False):
                    取消确定 = Template(r"tpl1699712554213.png", record_pos=(0.003, 0.113), resolution=(960, 540))
                    取消 = Template(r"tpl1699712559021.png", record_pos=(-0.096, 0.115), resolution=(960, 540))
                    if exists(取消确定):
                        TimeECHO("点击房间错误,返回")
                        self.Tool.existsTHENtouch(取消, "取消错误房间")
                        continue
                    self.Tool.existsTHENtouch(取消, "取消错误房间")
                    # 这里给的是特殊账户的头像
                    进房间 = self.图片.房主房间
                    if not exists(进房间):
                        TimeECHO("没找到进房间按钮, 采用通用进房间按钮")
                        进房间 = Template(r"tpl1699181937521.png", record_pos=(0.348, -0.194), resolution=(960, 540), threshold=0.9)
                    if self.Tool.existsTHENtouch(进房间, "进房间按钮", savepos=False):
                        TimeECHO("尝试进入房间中")
                        sleep(10)
                        找到取消按钮, self.图片.房间中的取消按钮图标 = self.Tool.存在任一张图(self.图片.房间中的取消按钮图标, "房间中的取消准备按钮")
                        if not 找到取消按钮:
                            TimeECHO("进入房间失败,可能是今日更新太频繁,版本不一致无法进房,需要重新登录更新")
                else:
                    TimeECHO("未找到组队房间,检测主节点登录状态")

        self.Tool.barriernode(self.mynode, self.totalnode, "结束组队进房间")
        return

    def 单人进入人机匹配房间_模拟战(self, times=0):
        if not self.check_run_status():
            return True
        # ... 状态检查和重置
        TimeECHO(f"首先进入人机匹配房间{times}")
        if self.判断对战中():
            self.结束人机匹配()
            if self.判断房间中(处理=False):
                return True
        if self.判断房间中():
            return True
        self.进入大厅()
        if not self.check_run_status():
            return True
        #
        if self.set_timelimit(istep=times, init=times == 0, timelimit=60*30, nstep=30, touch同步=True):
            return True
        #
        times = times + 1
        #
        if self.判断对战中():
            self.结束人机匹配()
        # 模拟战的房间很干净，不用处理
        if self.判断房间中(处理=False):
            return True
        #
        self.进入大厅()
        TimeECHO("大厅中.开始进入模拟战房间")
        #
        任意位置继续 = Template(r"tpl1693660122898.png", record_pos=(0.001, 0.252), resolution=(960, 540))  # 多次
        任意位置继续2 = Template(r"tpl1693660165029.png", record_pos=(-0.001, 0.244), resolution=(960, 540))
        任意位置继续3 = Template(r"tpl1693660182958.png", record_pos=(-0.004, 0.25), resolution=(960, 540))
        邀请好友 = Template(r"tpl1693660666527.png", record_pos=(0.408, 0.166), resolution=(960, 540))  # 就是进入房间
        # 新手要跳过教学局,自己先跳过
        # 不要管是否识别成功，就是按，后面加一个检测，没有检测成果就是按失败了，再返回即可
        if self.Tool.existsTHENtouch(self.图片.大厅万象天工, "大厅万象天工", savepos=True):
            sleep(2)
        if self.Tool.existsTHENtouch(self.图片.王者模拟战图标, "王者模拟战图标", savepos=True):
            sleep(2)
        while self.Tool.existsTHENtouch(任意位置继续, "任意位置继续"):
            sleep(5)
        while self.Tool.existsTHENtouch(任意位置继续2, "任意位置继续"):
            sleep(5)
        while self.Tool.existsTHENtouch(任意位置继续3, "任意位置继续"):
            sleep(5)
        pos = exists(邀请好友)
        if not pos:
            TimeECHO(f"{fun_name(1)}.无法找到模拟对战入口")
            for delstr in list(set(self.Tool.var_dict.keys()) & set(["大厅万象天工", "王者模拟战图标"])):
                del self.Tool.var_dict[delstr]
        self.Tool.var_dict["模拟战.邀请好友"] = pos
        self.Tool.existsTHENtouch(邀请好友, "模拟战.邀请好友", savepos=True)
        if self.判断房间中(处理=False):
            return True
        else:
            return self.单人进入人机匹配房间(times)

    def 进行人机匹配(self, times=0):
        if not self.check_run_status():
            return True
        if times == 0:
            # 这里需要barrier一下,不然下面主节点如果提前点击领匹配,这里可能无法判断
            self.Tool.barriernode(self.mynode, self.totalnode, "人机匹配预判断房间")
        #
        if self.set_timelimit(istep=times, init=times == 0, timelimit=60*10, nstep=100, touch同步=True):
            return True
        #
        times = times+1
        self.APPOB.打开APP()
        #
        self.Tool.timelimit(timekey="确认匹配", limit=60*1, init=True)
        self.Tool.timelimit(timekey="超时确认匹配", limit=60*5, init=True)
        #
        自己确定匹配 = False
        loop = 0
        自己曾经确定过匹配 = False
        找到开始按钮 = False
        找到取消按钮 = False
        # 不同活动中,开始按钮的图标不同,这里进行排序寻找
        if self.房主:
            找到开始按钮, self.图片.房间中的开始按钮图标 = self.Tool.存在任一张图(self.图片.房间中的开始按钮图标, "开始匹配")
            房间中的开始按钮 = self.图片.房间中的开始按钮图标[0]
            # 记录历史上有的匹配按钮位置,历史上就执行一次
            if "房间中的开始匹配按钮" not in self.Tool.var_dict.keys():
                pos = exists(房间中的开始按钮)
                if pos:
                    self.Tool.var_dict["房间中的开始匹配按钮"] = pos
            if not 找到开始按钮:
                TimeECHO(f":没找到开始按钮,使用历史位置")
            self.Tool.existsTHENtouch(房间中的开始按钮, "房间中的开始匹配按钮", savepos=not 找到开始按钮)
        else:
            找到取消按钮, self.图片.房间中的取消按钮图标 = self.Tool.存在任一张图(self.图片.房间中的取消按钮图标, "房间中的取消准备按钮")
            房间中的取消按钮 = self.图片.房间中的取消按钮图标[0]

        while True:
            if self.Tool.存在同步文件():
                return True
            # 如果没找到就再找一次
            if self.房主 and not 找到开始按钮:
                找到开始按钮, self.图片.房间中的开始按钮图标 = self.Tool.存在任一张图(self.图片.房间中的开始按钮图标, "开始匹配")
                房间中的开始按钮 = self.图片.房间中的开始按钮图标[0]
                self.Tool.existsTHENtouch(房间中的开始按钮, "房间中的开始匹配按钮", savepos=False)
            #
            if self.Tool.timelimit(timekey="确认匹配", limit=60*1, init=False):
                TimeECHO("等待队友确认匹配中")
            if self.Tool.timelimit(timekey="超时确认匹配", limit=60*5, init=False):
                TimeErr("超时太久,退出匹配")
                return False
            自己确定匹配 = self.Tool.existsTHENtouch(Template(r"tpl1689666290543.png", record_pos=(-0.001, 0.152), resolution=(960, 540), threshold=0.8), "确定匹配按钮")
            自己曾经确定过匹配 = 自己曾经确定过匹配 or 自己确定匹配
            # if 自己确定匹配: sleep(15) #自己确定匹配后给流出时间
            队友确认5v5匹配 = False
            if 自己曾经确定过匹配:
                # 该界面用于判断是都5v5匹配成功，或者模拟战是否进错了模式
                队友确认5v5匹配 = self.Tool.existsTHENtouch(Template(r"tpl1689666324375.png", record_pos=(-0.297, -0.022), resolution=(960, 540)), "英雄界面检测", savepos=False)
            #
            if "模拟战" in self.对战模式:
                if 队友确认5v5匹配:
                    self.创建同步文件("模拟战误入5v5?")
                    return
                队友确认匹配 = False
                if 自己曾经确定过匹配:
                    队友确认匹配 = self.判断对战中()
                if 队友确认匹配:
                    TimeECHO(":队友确认匹配")
                    return True  # 模拟战确定匹配后就结束了
                else:
                    TimeECHO(":队友未确认匹配")
                    continue
            else:
                队友确认匹配 = 队友确认5v5匹配
            if 队友确认匹配:
                break
        #
        # 选择英雄
        if self.选择英雄:
            exit_code = run_class_command(self=self, command=self.Tool.readfile(self.重新设置英雄FILE), must_ok=True)
            if exit_code != 0:
                sleep(1)
                self.Tool.existsTHENtouch(self.参战英雄线路, "参战英雄线路", savepos=True)
                sleep(5)
                # 这里是用savepos的好处就是那个英雄的熟练度低点哪个英雄
                self.Tool.existsTHENtouch(self.参战英雄头像, "参战英雄头像", savepos=True)
                sleep(1)
            # 分路重复.png
            if exists(Template(r"tpl1689668119154.png", record_pos=(0.0, -0.156), resolution=(960, 540))):
                TimeECHO("分路冲突，切换英雄")
                # 分路重复取消按钮.png
                if self.Tool.existsTHENtouch(Template(r"tpl1689668138416.png", record_pos=(-0.095, 0.191), resolution=(960, 540)), "冲突取消英雄", savepos=False):
                    # 选择备选英雄
                    self.Tool.existsTHENtouch(self.备战英雄线路, "备战英雄线路", savepos=True)
                    self.Tool.existsTHENtouch(self.备战英雄头像, "备战英雄", savepos=True)
            # 确定英雄后一般要等待队友确定，这需要时间
            self.Tool.LoopTouch(Template(r"tpl1689666339749.png", record_pos=(0.421, 0.237), resolution=(960, 540)), "确定英雄", loop=6, savepos=False)
        # 加载游戏界面
        加载游戏界面 = Template(r"tpl1693143323624.png", record_pos=(0.003, -0.004), resolution=(960, 540))
        self.Tool.timelimit(timekey="加载游戏", limit=60*5, init=True)
        加载中 = exists(加载游戏界面)
        while True:
            加载中 = exists(加载游戏界面)
            if 加载中:
                TimeECHO("加载游戏中.....")
                if self.Tool.existsTHENtouch(Template(r"tpl1689666367752.png", record_pos=(0.42, -0.001), resolution=(960, 540)), "加油按钮", savepos=False):
                    sleep(2)
            else:
                break
            if self.Tool.timelimit(timekey="加载游戏", limit=60*10, init=False):
                content = "加载游戏时间过长.....创建同步文件"
                return self.创建同步文件(content)
        #
        关闭技能介绍1 = Template(r"tpl1692951432616.png", record_pos=(0.346, -0.207), resolution=(960, 540))
        关闭技能介绍2 = Template(r"tpl1700918628072.png", record_pos=(-0.059, 0.211), resolution=(960, 540))
        self.Tool.existsTHENtouch(关闭技能介绍1, "关闭技能介绍1", savepos=False)
        self.Tool.existsTHENtouch(关闭技能介绍2, "关闭技能介绍2", savepos=False)
        #

    def 结束人机匹配(self):
        TimeECHO(f"开始结束人机匹配:{self.对战模式}")
        if not self.check_run_status():
            return True
        if "模拟战" in self.对战模式:
            return self.结束人机匹配_模拟战()
        self.Tool.timelimit(timekey="结束人机匹配", limit=60*15, init=True)

        while True:
            if not self.check_run_status():
                return True
            addtime = 60*10 if self.本循环参数.标准模式 else 0
            if self.Tool.timelimit(timekey="结束人机匹配", limit=60*20 + addtime, init=False):
                content = "结束人机匹配时间超时"
                return self.创建同步文件(content)
            self.APPOB.打开APP()
            if self.Tool.timelimit(timekey="结束人机匹配", limit=60*10, init=False, reset=False):
                self.Tool.touch_record_pos(record_pos=(-0.002, 0.203), resolution=self.移动端.resolution, keystr=f"{fun_name(1)}.十分钟一次的点击")
            # 对战阶段，处理对战
            加速对战 = False
            if self.触摸对战:
                加速对战 = True
            if self.判断对战中(加速对战):
                sleep(30)
                continue
            # 已返回房间或大厅
            if self.判断房间中(处理=False):
                return
            if self.判断大厅中():
                return
            # 健康系统直接重新同步
            if self.健康系统_常用命令():
                return True
            #
            # S37 更新了结算动画
            self.Tool.touch_record_pos(record_pos=(0, 0), resolution=self.移动端.resolution, keystr=f"{fun_name(1)}.屏幕中心")
            点击此处继续 = Template(r"tpl1727232003870.png", record_pos=(-0.002, 0.203), resolution=(960, 540))
            存在, self.图片.结算页面元素 = self.Tool.存在任一张图(self.图片.结算页面元素, "对战.结算页面元素")
            if 存在:
                if not self.Tool.existsTHENtouch(点击此处继续, f"{fun_name(1)}.点击此处继续"):
                    TimeECHO(f"无法找到.点击此处继续.可能叠加了英雄图层的原因")
                    self.Tool.touch_record_pos(record_pos=(-0.002, 0.203), resolution=self.移动端.resolution, keystr=f"{fun_name(1)}.点击此处继续")
            self.Tool.existsTHENtouch(点击此处继续, f"{fun_name(1)}.点击此处继续")
            #
            # 对战结算时的弹窗
            每日任务进展 = Template(r"tpl1703772723321.png", record_pos=(0.004, -0.174), resolution=(960, 540))
            self.Tool.existsTHENtouch(每日任务进展, "新号每日任务进展", savepos=False)
            确定按钮 = Template(r"tpl1689667950453.png", record_pos=(-0.001, 0.111), resolution=(960, 540))
            self.Tool.LoopTouch(确定按钮, "回归对战|新赛季|友情币等奖励确定按钮", savepos=False)
            # 奇怪的结算画面
            游戏结束了 = Template(r"tpl1694360304332.png", record_pos=(-0.011, -0.011), resolution=(960, 540))
            if exists(游戏结束了):
                self.Tool.existsTHENtouch(Template(r"tpl1694360310806.png", record_pos=(-0.001, 0.117), resolution=(960, 540)))
            if not self.check_run_status():
                return
            # 有时候会莫名进入分享界面
            if exists(Template(r"tpl1689667038979.png", record_pos=(0.235, -0.125), resolution=(960, 540))):
                TimeECHO("分享界面")
                self.Tool.existsTHENtouch(Template(r"tpl1689667050980.png", record_pos=(-0.443, -0.251), resolution=(960, 540)))
                sleep(2)
                self.确定按钮()
            # 返回房间/大厅
            if self.对战结束返回房间:
                if self.Tool.existsTHENtouch(self.图片.返回房间按钮, "返回房间"):
                    sleep(10)
                # 万一返回房间后来一堆提示
                self.网络优化()
                if self.判断房间中(处理=False):
                    return
            else:
                if self.Tool.existsTHENtouch(Template(r"tpl1689667243845.png", record_pos=(-0.082, 0.221), resolution=(960, 540), threshold=0.9), "返回大厅"):
                    sleep(10)
                    if self.Tool.existsTHENtouch(Template(r"tpl1689667256973.png", record_pos=(0.094, 0.115), resolution=(960, 540)), "确定返回大厅"):
                        sleep(10)
                if self.判断大厅中():
                    return
    #

    def 结束人机匹配_模拟战(self):
        TimeECHO("准备结束本局模拟战")
        if not self.check_run_status():
            return True
        self.Tool.timelimit(timekey="结束模拟战", limit=60*20, init=True)
        while True:
            self.APPOB.打开APP()
            if self.Tool.timelimit(timekey="结束模拟战", limit=60*30, init=False) or self.健康系统() or self.判断大厅中():
                TimeErr("结束游戏时间过长 OR 健康系统 OR 大厅中")
                return self.进入大厅()
            # 模拟战在排队的时候就处在房间的界面，所以这里的判断可能会很早的退出去
            if self.判断房间中(处理=False):
                return
            点击屏幕继续 = Template(r"tpl1701229138066.png", record_pos=(-0.002, 0.226), resolution=(960, 540))
            self.Tool.existsTHENtouch(点击屏幕继续, "点击屏幕继续")
            if self.判断对战中(False):
                sleeploop = 0
                while self.判断对战中(True):  # 开始处理准备结束
                    sleep(10)
                    sleeploop = sleeploop+1
                    if not self.check_run_status():
                        return True
                    if sleeploop > 20:
                        break  # 虚拟机王者程序卡住了
                # ++++++滴哦
                for loop in range(30):  # 等待时间太长
                    TimeECHO("等待模拟战对战结束")
                    if exists(Template(r"tpl1690545494867.png", record_pos=(0.0, 0.179), resolution=(960, 540))):
                        TimeECHO("正在退出")
                        if self.Tool.existsTHENtouch(Template(r"tpl1690545545580.png", record_pos=(-0.101, 0.182), resolution=(960, 540)), "选择退出对战"):
                            TimeECHO("点击退出")
                            break
                    sleep(1)
            if exists(Template(r"tpl1690545494867.png", record_pos=(0.0, 0.179), resolution=(960, 540))):
                TimeECHO("检测到:[退出+观战]界面")
                self.Tool.existsTHENtouch(Template(r"tpl1690545545580.png", record_pos=(-0.101, 0.182), resolution=(960, 540)), "选择退出对战")
            if self.判断房间中(处理=False):
                return
            if self.判断大厅中():
                return
            # 为了避免识别错误，加一个强制点击的命令
            任意点击_monizhan = [Template(r"tpl1690545762580.png", record_pos=(-0.001, 0.233), resolution=(960, 540))]
            存在, 任意点击_monizhan = self.Tool.存在任一张图(任意点击_monizhan, "任意点击_monizhan", savepos=True)
            if not 存在:
                self.Tool.var_dict["任意点击_monizhan"] = (2, 2)
            self.Tool.existsTHENtouch(任意点击_monizhan[0], "任意点击_monizhan", savepos=True)
            #
            if self.Tool.existsTHENtouch(Template(r"tpl1690545762580.png", record_pos=(-0.001, 0.233), resolution=(960, 540))):
                TimeECHO("继续1")
                sleep(5)
            if self.Tool.existsTHENtouch(Template(r"tpl1690545802859.png", record_pos=(0.047, 0.124), resolution=(960, 540))):
                TimeECHO("继续2")
                sleep(5)
            if self.Tool.existsTHENtouch(Template(r"tpl1690545854354.png", record_pos=(0.002, 0.227), resolution=(960, 540))):
                TimeECHO("继续3")
                sleep(5)
            #
            if exists(Template(r"tpl1690545925867.png", record_pos=(-0.001, 0.241), resolution=(960, 540))):
                if self.对战结束返回房间:
                    if self.Tool.existsTHENtouch(self.图片.返回房间按钮, "返回房间", savepos=True):
                        sleep(10)
                        if self.判断房间中(处理=False):
                            break
            if self.判断房间中(处理=False):
                return
            if self.判断大厅中():
                return
    #

    def 每日礼包(self, 强制领取=False, 初始化=False):
        #
        if 初始化:
            # 刷新礼包的领取计时
            self.Tool.timelimit("领游戏礼包", limit=60*60*3, init=True)
            self.Tool.timelimit("领营地礼包", limit=60*60*3, init=True)
            self.Tool.timelimit("体验服更新", limit=60*60*3, init=True)
            self.强制领取礼包 = True
            self.活动礼包 = False
            self.祈愿礼包 = False
            self.玉镖夺魁签到 = os.path.exists(self.玉镖夺魁签到FILE)
            self.每日任务礼包 = True
            self.Tool.touchfile(self.免费商城礼包FILE)
            self.友情礼包_积分夺宝 = True
            self.友情礼包_皮肤碎片 = True
            self.友情礼包_英雄碎片 = True
            self.友情礼包_铭文碎片 = True
            self.友情礼包_皮肤宝箱 = True
            self.友情礼包_回城宝箱 = True
            self.友情礼包_击败宝箱 = True
            self.外置礼包_王者营地 = True
            self.外置礼包_体验服 = os.path.exists(self.更新体验服FILE)

            return
        #
        if 强制领取:
            self.Tool.timedict["领游戏礼包"] = 0
            self.Tool.timedict["领营地礼包"] = 0
            self.Tool.timedict["体验服更新"] = 0
        #
        # 在组队的过程中，不领取营地礼包，以及更新体验服
        if 强制领取 or not self.组队模式:
            if self.外置礼包_王者营地:
                self.每日礼包_王者营地()
            #
            if self.外置礼包_体验服:
                self.体验服更新()
        #
        # 王者APP礼包
        self.王者礼包()

    def 王者礼包(self):
        if self.Tool.timelimit("领游戏礼包", limit=60*60*3, init=False):
            if not self.check_run_status():
                TimeECHO("领礼包时.检测状态失败, 停止领取")
                return
            self.APPOB.打开APP()
            self.进入大厅()
            #
            if not self.check_run_status():
                TimeECHO("领礼包时.检测状态失败, 停止领取")
                return
            #
            if os.path.exists(self.免费商城礼包FILE):
                if self.商城免费礼包():
                    self.Tool.removefile(self.免费商城礼包FILE)
            #
            # 由于王者营地也可以领战令经验, 如果在这里把战令经验领到上限，营地的经验就不能领了
            # 所以加个控制参数决定是否领取
            if self.每日任务礼包:
                self.每日礼包_每日任务()
            if self.活动礼包:
                self.活动入口()
            if self.祈愿礼包:
                self.祈愿入口()
            # 以前的活动
            if self.玉镖夺魁签到:
                self.玉镖夺魁()
            else:
                TimeECHO("暂时不进行玉镖夺魁")
            # 回忆礼册. 不知道这个礼包会存在多久
            self.回忆礼册()
            # 友情礼包、邮件礼包、战队礼包不领取不会丢失,影响不大,最后领取
            self.每日礼包_邮件礼包()
            self.每日礼包_妲己礼物()
            self.友情礼包()
            self.战队礼包()
            TimeECHO("钻石夺宝、战令(动画多,很卡)没有代码需求,攒够了一起转")
            if self.Tool.存在同步文件():
                return True
            #
            if os.path.exists(self.KPL每日观赛FILE):
                TimeECHO("进行KPL观赛")
                self.进入大厅()
                try:
                    观赛时长 = int(self.Tool.readfile(self.KPL每日观赛FILE)[0])
                except:
                    traceback.print_exc()
                    观赛时长 = 60*15
                self.KPL每日观赛(times=1, 观赛时长=观赛时长)
        else:
            TimeECHO("时间太短,暂时不领取游戏礼包")
        #
        self.Tool.timelimit("领游戏礼包", limit=60*60*3, init=False)

    def 战队礼包(self):
        self.进入大厅()
        #
        # 战队礼包
        TimeECHO(f":战队礼包")
        self.Tool.existsTHENtouch(Template(r"tpl1700403158264.png", record_pos=(0.067, 0.241), resolution=(960, 540)), "战队")
        # @todo, 添加已阅战队赛
        sleep(10)
        self.Tool.existsTHENtouch(Template(r"tpl1700403166845.png", record_pos=(0.306, 0.228), resolution=(960, 540)), "展开战队")
        sleep(10)
        if not self.Tool.existsTHENtouch(Template(r"tpl1700403174640.png", record_pos=(0.079, 0.236), resolution=(960, 540)), "战队商店"):
            TimeECHO("找不到战队商店, 可能没有加战队, 返回")
        sleep(10)
        self.Tool.existsTHENtouch(Template(r"tpl1700403186636.png", record_pos=(0.158, -0.075), resolution=(960, 540), target_pos=8), "英雄碎片")
        sleep(10)
        self.Tool.existsTHENtouch(Template(r"tpl1700403207652.png", record_pos=(0.092, 0.142), resolution=(960, 540)), "领取")
        sleep(10)
        self.Tool.existsTHENtouch(Template(r"tpl1700403218837.png", record_pos=(0.098, 0.117), resolution=(960, 540)), "确定")
        sleep(10)
        return

    def 回忆礼册(self, times=0):
        #
        # 本函数作为快速礼包的模板
        # 其他函数都可以借鉴此函数的开头进行优化
        #
        if not self.check_run_status():
            return True
        self.进入大厅()
        if not self.check_run_status():
            return True
        #
        if self.set_timelimit(istep=times, init=times == 0, timelimit=60*10, nstep=10):
            return True
        #
        if times > 4:  # 1,2,3
            for delstr in list(set(self.Tool.var_dict.keys()) & set(["大厅回忆礼册", "获取回忆之证"])):
                del self.Tool.var_dict[delstr]
        #
        times = times+1
        #
        self.进入大厅()
        if not self.Tool.existsTHENtouch(self.图片.大厅回忆礼册, "大厅回忆礼册", savepos=True):
            return self.回忆礼册(times)
        sleep(2)
        if not self.Tool.existsTHENtouch(self.图片.获取回忆之证, "获取回忆之证", savepos=True):
            return self.回忆礼册(times)
        sleep(2)
        # 如果进入唤醒界面，跳回任务界面
        if self.Tool.existsTHENtouch(self.图片.礼册记忆碎片, "礼册记忆碎片"):
            sleep(2)
        金色一键领取 = Template(r"tpl1727229260477.png", record_pos=(0.394, 0.219), resolution=(960, 540))
        灰色一键领取 = Template(r"tpl1727229241093.png", record_pos=(0.392, 0.219), resolution=(960, 540))
        一键领取 = [金色一键领取, 灰色一键领取]
        存在, 一键领取 = self.Tool.存在任一张图(一键领取, "礼册.一键领取", savepos=True)
        if not 存在:
            TimeECHO(f"{fun_name}.没检测到界面,{times}+1")
            return self.回忆礼册(times)
        self.Tool.existsTHENtouch(一键领取[0], "礼册.一键领取", savepos=True)
        # .....
        # 下面的其实不用领取，手动去背包里领取也是可以的，因此下面的代码没进行充分测试
        self.确定按钮()  # 只有一个蓝色确定按钮，这个函数会遍历确定按钮，会拖慢一点点速度，但是10s内能结束，因此不优化了
        自动升级 = Template(r"tpl1723334201064.png", record_pos=(0.38, -0.242), resolution=(960, 540))
        self.Tool.LoopTouch(自动升级, "礼册.自动升级", loop=12, savepos=False)
        self.确定按钮()
        关闭按钮 = Template(r"tpl1723334229790.png", record_pos=(0.361, -0.194), resolution=(960, 540))
        返回按钮 = Template(r"tpl1723334241957.png", record_pos=(-0.439, -0.25), resolution=(960, 540))
        self.Tool.existsTHENtouch(关闭按钮, "回忆礼册关闭按钮", savepos=True)
        self.Tool.existsTHENtouch(返回按钮, "回忆礼册返回按钮", savepos=True)
        return

    # @todo,其他活动一键领取

    def 商城免费礼包(self, times=0):
        #
        if not self.check_run_status():
            return True
        self.进入大厅()
        if not self.check_run_status():
            return True
        #
        if self.set_timelimit(istep=times, init=times == 0, timelimit=60*10, nstep=10):
            return True
        #
        times = times+1
        #
        # 商城免费礼包
        TimeECHO(f"领任务礼包:每日任务{times}")
        if self.健康系统():
            return False
        #
        TimeECHO(f":商城免费礼包")
        # 做活动时，商城入口会变
        商城入口 = []
        商城入口.append(Template(r"tpl1705069544018.png", record_pos=(0.465, -0.173), resolution=(960, 540)))
        商城入口.append(Template(r"tpl1705718545013.png", target_pos=2, record_pos=(0.461, -0.115), resolution=(960, 540)))
        # 因为默认的商城进入后是特效很多的皮肤，影响了界面的识别，所以切到干净的促销入口进行识别
        促销入口 = Template(r"tpl1719455432184.png", record_pos=(-0.436, 0.075), resolution=(960, 540))
        免费图标 = Template(r"tpl1719455279197.png", record_pos=(-0.122, -0.252), resolution=(960, 540))
        免费领取 = Template(r"tpl1719455299372.png", record_pos=(0.035, 0.055), resolution=(960, 540), target_pos=8)
        确定购买 = Template(r"tpl1705069645193.png", record_pos=(-0.105, 0.165), resolution=(960, 540))
        商城界面 = []
        商城界面.append(促销入口)
        商城界面.append(免费图标)
        商城界面.append(Template(r"tpl1719455683640.png", record_pos=(-0.368, -0.25), resolution=(960, 540)))
        商城界面.append(Template(r"tpl1719455836014.png", record_pos=(-0.458, 0.19), resolution=(960, 540)))
        返回 = Template(r"tpl1694442171115.png", record_pos=(-0.441, -0.252), resolution=(960, 540))
        #
        找到商城入口 = False
        找到商城入口, 商城入口 = self.Tool.存在任一张图(商城入口, f"{fun_name(1)}商城入口", savepos=True)
        if not 找到商城入口:
            TimeECHO(f"无法找到商城入口, 尝试计算坐标")
            self.Tool.cal_record_pos(商城入口[0].record_pos, self.移动端.resolution, f"{fun_name(1)}商城入口", savepos=True)
        self.Tool.existsTHENtouch(商城入口[0], f"{fun_name(1)}商城入口", savepos=True)
        sleep(30)
        进入商城界面 = False
        # 注：如果实在无法识别，这里手动点击到促销界面，让程序savepos记住促销的位置
        for i in range(len(商城界面)):
            # 如果促销入口识别错了，手动 del self.Tool.var_dict["促销入口"] 掉
            self.Tool.existsTHENtouch(促销入口, f"新促销入口", savepos=True)
            sleep(20)
            TimeECHO(f"检测商城界面中...{i}")
            if exists(商城界面[i]):
                进入商城界面 = True
                break
        if self.健康系统():
            return False
        if not 进入商城界面:
            TimeECHO(f"未检测到商城界面, 重新进入商城")
            self.Tool.LoopTouch(返回, "返回")
            del self.Tool.var_dict[f"{fun_name(1)}商城入口"]
            TimeECHO("如果实在无法识别，手动点击到促销界面，让程序savepos记住促销的位置")
            return self.商城免费礼包(times=times)
        #
        领取成功 = False
        if self.Tool.existsTHENtouch(免费图标, "免费图标", savepos=False):
            sleep(5)
            领取成功 = self.Tool.existsTHENtouch(免费领取, "免费领取", savepos=False)
            sleep(10)
            self.Tool.LoopTouch(确定购买, "确定购买")
            self.关闭按钮()
            self.Tool.LoopTouch(返回, "返回")
            self.确定按钮()
        else:
            TimeECHO(f"没检测到免费图标,可能领取过了")
            self.Tool.LoopTouch(返回, "返回")
            return True
        if not 领取成功:
            TimeECHO(f"领取每日礼包失败")
        return True

    def 活动入口(self, times=0):
        # 进入活动界面，可以领取一些活动的枫叶、灯笼等，手动兑换一些钻石、积分
        #
        if not self.check_run_status():
            return True
        self.进入大厅()
        if not self.check_run_status():
            return True
        #
        if self.set_timelimit(istep=times, init=times == 0, timelimit=60*5, nstep=10):
            return True
        #
        if times > 4:  # 1,2,3
            for delstr in list(set(self.Tool.var_dict.keys()) & set(["大厅活动"])):
                del self.Tool.var_dict[delstr]
        #
        times = times+1
        #
        if "大厅活动" not in self.Tool.var_dict.keys():
            # savepos 如果找到会自动替换上一次的字典
            存在大厅活动, self.图片.大厅活动 = self.Tool.存在任一张图(self.图片.大厅活动, "大厅活动", savepos=True)
            if not 存在大厅活动:
                TimeECHO(f"{fun_name(1)}: 找不到活动入口, 尝试计算坐标")
                self.Tool.cal_record_pos(self.图片.大厅活动[0].record_pos, self.移动端.resolution, "大厅活动", savepos=True)
        if not self.Tool.existsTHENtouch(self.图片.大厅活动[0], "大厅活动", savepos=True):
            return self.祈愿入口(times)
        sleep(10)
        #
        self.关闭按钮()
        self.确定按钮()
        #
        # 开始随机点击活动的页面，遇到X号，则点击
        for i in range(20, -14, -7):
            record_pos = (-0.40, i/100.0)
            self.Tool.touch_record_pos(record_pos, self.移动端.resolution, f"活动({i})")
            sleep(1)
        #
        返回 = Template(r"tpl1694442171115.png", record_pos=(-0.441, -0.252), resolution=(960, 540))
        self.Tool.LoopTouch(返回, "返回")
        return True

    def 祈愿入口(self, times=0):
        # 进入祈愿界面，可以领取一些活动的祈愿币，手动兑换一些钻石、积分
        #
        if not self.check_run_status():
            return True
        self.进入大厅()
        if not self.check_run_status():
            return True
        #
        if self.set_timelimit(istep=times, init=times == 0, timelimit=60*5, nstep=10):
            return True
        #
        if times > 4:  # 1,2,3
            for delstr in list(set(self.Tool.var_dict.keys()) & set(["大厅祈愿"])):
                del self.Tool.var_dict[delstr]
        #
        times = times+1
        #
        if "大厅祈愿" not in self.Tool.var_dict.keys():
            # savepos 如果找到会自动替换上一次的字典
            存在大厅祈愿, self.图片.大厅祈愿 = self.Tool.存在任一张图(self.图片.大厅祈愿, "大厅祈愿", savepos=True)
            if not 存在大厅祈愿:
                TimeECHO(f"{fun_name(1)}: 找不到祈愿入口, 尝试计算坐标")
                self.Tool.cal_record_pos(self.图片.大厅祈愿[0].record_pos, self.移动端.resolution, "大厅祈愿", savepos=True)
        if not self.Tool.existsTHENtouch(self.图片.大厅祈愿[0], "大厅祈愿", savepos=True):
            return self.祈愿入口(times)
        sleep(10)
        #
        self.关闭按钮()
        self.确定按钮()
        #
        # 开始随机点击活动的页面，遇到X号，则点击
        for i in range(25, -20, -10):
            record_pos = (-0.44, i/100.0)
            self.Tool.touch_record_pos(record_pos, self.移动端.resolution, f"祈愿({i/100})")
            sleep(1)
        #
        返回 = Template(r"tpl1694442171115.png", record_pos=(-0.441, -0.252), resolution=(960, 540))
        self.Tool.LoopTouch(返回, "返回")
        return True

    def 玉镖夺魁(self, times=0):
        #
        if not self.check_run_status():
            return True
        self.进入大厅()
        if not self.check_run_status():
            return True
        #
        if self.set_timelimit(istep=times, init=times == 0, timelimit=60*10, nstep=10):
            return True
        #
        if times > 4:  # 1,2,3
            for delstr in list(set(self.Tool.var_dict.keys()) & set(["大厅祈愿", "玉镖夺魁入口"])):
                del self.Tool.var_dict[delstr]
        #
        times = times+1
        #
        if "大厅祈愿" not in self.Tool.var_dict.keys():
            # savepos 如果找到会自动替换上一次的字典
            存在大厅祈愿, self.图片.大厅祈愿 = self.Tool.存在任一张图(self.图片.大厅祈愿, "大厅祈愿", savepos=True)
            if not 存在大厅祈愿:
                TimeECHO(f"玉镖夺魁: 找不到祈愿入口, 尝试计算坐标")
                self.Tool.cal_record_pos(self.图片.大厅祈愿[0].record_pos, self.移动端.resolution, "大厅祈愿", savepos=True)
        if not self.Tool.existsTHENtouch(self.图片.大厅祈愿[0], "大厅祈愿", savepos=True):
            return self.玉镖夺魁(times)
        sleep(10)
        玉镖夺魁入口 = Template(r"tpl1724316055269.png", record_pos=(-0.436, -0.154), resolution=(960, 540))
        # 有则更新，无则用旧的
        self.Tool.存在任一张图([玉镖夺魁入口], "玉镖夺魁入口", savepos=True)
        if not self.Tool.existsTHENtouch(玉镖夺魁入口, "玉镖夺魁入口", savepos=True):
            return self.玉镖夺魁(times)
        sleep(10)
        夺魁页面元素 = []
        夺魁页面元素.append(Template(r"tpl1724316071716.png", record_pos=(-0.045, -0.218), resolution=(960, 540)))
        夺魁页面元素.append(Template(r"tpl1724316082074.png", record_pos=(-0.009, -0.183), resolution=(960, 540)))
        夺魁页面元素.append(Template(r"tpl1724316089651.png", record_pos=(0.274, -0.045), resolution=(960, 540)))
        存在夺魁页面, 夺魁页面元素 = self.Tool.存在任一张图(夺魁页面元素, "夺魁页面")
        if not 存在夺魁页面:
            self.Tool.LoopTouch(玉镖夺魁入口, "玉镖夺魁入口", savepos=True, loop=5)
            #
            存在夺魁页面, 夺魁页面元素 = self.Tool.存在任一张图(夺魁页面元素, "夺魁页面")
            if not 存在夺魁页面:
                return self.玉镖夺魁(times)
        # 王者本次更新，会自动领取，不用手动点击加号
        TimeECHO("开始领夺魁币")
        #
        领取加号 = []
        领取加号.append(Template(r"tpl1700803174309.png", record_pos=(0.227, -0.21), resolution=(960, 540), target_pos=2))
        领取加号.append(Template(r"tpl1700803136907.png", record_pos=(0.24, -0.243), resolution=(960, 540), target_pos=4))
        for i in 领取加号:
            if self.Tool.existsTHENtouch(i, f"领取加号{i}"):
                break
        领取按钮 = Template(r"tpl1700803185294.png", record_pos=(0.172, -0.067), resolution=(960, 540))
        self.Tool.existsTHENtouch(领取按钮, "领取按钮")
        self.Tool.existsTHENtouch(Template(r"tpl1700803983736.png", record_pos=(0.015, 0.101), resolution=(960, 540)), "确定")
        self.Tool.existsTHENtouch(领取按钮, "领取按钮")
        self.Tool.existsTHENtouch(Template(r"tpl1700803983736.png", record_pos=(0.015, 0.101), resolution=(960, 540)), "确定")
        self.Tool.existsTHENtouch(Template(r"tpl1700803191090.png", record_pos=(0.372, -0.184), resolution=(960, 540)))
        return

    def 友情礼包(self):
        self.进入大厅()
        #
        # 友情礼包,虽然每次只领取了一个,但是每周/日领取了多次,一周内是可以领完上限的
        TimeECHO(f":友情礼包")
        TimeECHO(f":对战友情币")
        if not self.Tool.existsTHENtouch(Template(r"tpl1700454802287.png", record_pos=(0.242, -0.251), resolution=(960, 540)), "友情双人入口"):
            return
        sleep(5)
        if not self.Tool.existsTHENtouch(Template(r"tpl1700454817255.png", record_pos=(-0.447, 0.166), resolution=(960, 540)), "友情文字入口"):
            return
        sleep(5)
        self.Tool.existsTHENtouch(Template(r"tpl1700454833319.png", record_pos=(0.416, 0.011), resolution=(960, 540)), "多次任务领取")
        self.Tool.existsTHENtouch(Template(r"tpl1700454842665.png", record_pos=(0.001, 0.163), resolution=(960, 540)), "确定领取友情币")
        # 奖励兑换
        if not self.Tool.existsTHENtouch(Template(r"tpl1700454852769.png", record_pos=(-0.332, 0.191), resolution=(960, 540)), "奖励兑换按钮"):
            return
        sleep(5)
        # 积分夺宝
        if self.友情礼包_积分夺宝 and self.Tool.existsTHENtouch(Template(r"tpl1700454863912.png", record_pos=(-0.124, -0.004), resolution=(960, 540)), "积分夺宝券"):
            sleep(5)
            if self.Tool.existsTHENtouch(Template(r"tpl1700454872767.png", record_pos=(0.32, 0.228), resolution=(960, 540)), "友情币兑换"):
                sleep(5)
            if self.Tool.existsTHENtouch(Template(r"tpl1700454883635.png", record_pos=(0.098, 0.118), resolution=(960, 540)), "金色确定兑换"):
                sleep(5)
            if self.Tool.existsTHENtouch(Template(r"tpl1694441190629.png", record_pos=(0.0, 0.165), resolution=(960, 540)), "蓝色确定兑换"):
                sleep(5)
        # 皮肤碎片
        if self.友情礼包_皮肤碎片 and self.Tool.existsTHENtouch(Template(r"tpl1700454908937.png", record_pos=(0.039, 0.004), resolution=(960, 540)), "皮肤碎片兑换"):
            sleep(5)
            if self.Tool.existsTHENtouch(Template(r"tpl1700454916324.png", record_pos=(0.317, 0.226), resolution=(960, 540)), "友情币兑换"):
                sleep(5)
            if self.Tool.existsTHENtouch(Template(r"tpl1700454883635.png", record_pos=(0.098, 0.118), resolution=(960, 540)), "金色确定兑换"):
                sleep(5)
            if self.Tool.existsTHENtouch(Template(r"tpl1694441190629.png", record_pos=(0.0, 0.165), resolution=(960, 540)), "蓝色确定兑换"):
                sleep(5)
        # 英雄碎片
        if self.友情礼包_英雄碎片 and self.Tool.existsTHENtouch(Template(r"tpl1700454935340.png", record_pos=(-0.28, 0.153), resolution=(960, 540)), "英雄碎片兑换"):
            sleep(5)
            if self.Tool.existsTHENtouch(Template(r"tpl1700454947514.png", record_pos=(0.321, 0.227), resolution=(960, 540)), "友情币兑换"):
                sleep(5)
            if self.Tool.existsTHENtouch(Template(r"tpl1700454883635.png", record_pos=(0.098, 0.118), resolution=(960, 540)), "金色确定兑换"):
                sleep(5)
            if self.Tool.existsTHENtouch(Template(r"tpl1694441190629.png", record_pos=(0.0, 0.165), resolution=(960, 540)), "蓝色确定兑换"):
                sleep(5)
        #
        # 铭文碎片
        if self.友情礼包_铭文碎片 and self.Tool.existsTHENtouch(Template(r"tpl1700455034567.png", record_pos=(-0.123, 0.155), resolution=(960, 540)), "铭文碎片兑换"):
            sleep(5)
            if self.Tool.existsTHENtouch(Template(r"tpl1700455039770.png", record_pos=(0.321, 0.226), resolution=(960, 540)), "友情币兑换"):
                sleep(5)
            if self.Tool.existsTHENtouch(Template(r"tpl1700454883635.png", record_pos=(0.098, 0.118), resolution=(960, 540)), "金色确定兑换"):
                sleep(5)
            if self.Tool.existsTHENtouch(Template(r"tpl1694441190629.png", record_pos=(0.0, 0.165), resolution=(960, 540)), "蓝色确定兑换"):
                sleep(5)
        #
        返回图标 = Template(r"tpl1707301421376.png", record_pos=(-0.445, -0.253), resolution=(960, 540))
        # 皮肤宝箱
        if self.友情礼包_皮肤宝箱 and self.Tool.existsTHENtouch(Template(r"tpl1700454970340.png", record_pos=(-0.12, -0.154), resolution=(960, 540)), "友情皮肤礼包兑换"):
            sleep(5)
            if self.Tool.existsTHENtouch(Template(r"tpl1700454978914.png", record_pos=(0.32, 0.228), resolution=(960, 540)), "友情币兑换"):
                sleep(5)
            if self.Tool.existsTHENtouch(Template(r"tpl1700454987098.png", record_pos=(0.1, 0.117), resolution=(960, 540)), "金色确定兑换"):
                sleep(5)
            if self.Tool.existsTHENtouch(Template(r"tpl1700454996867.png", record_pos=(-0.099, 0.166), resolution=(960, 540)), "蓝色确定兑换"):
                sleep(5)
            self.Tool.existsTHENtouch(返回图标, "友情礼包返回图标", savepos=True)
        # 回城宝箱
        if self.友情礼包_回城宝箱 and self.Tool.existsTHENtouch(Template(r"tpl1707301299599.png", record_pos=(0.035, -0.15), resolution=(960, 540)), "友情皮肤礼包兑换"):
            sleep(5)
            if self.Tool.existsTHENtouch(Template(r"tpl1707301267168.png", record_pos=(0.32, 0.228), resolution=(960, 540)), "友情币兑换"):
                sleep(5)
            if self.Tool.existsTHENtouch(Template(r"tpl1700454987098.png", record_pos=(0.1, 0.117), resolution=(960, 540)), "金色确定兑换"):
                sleep(5)
            if self.Tool.existsTHENtouch(Template(r"tpl1700454996867.png", record_pos=(-0.099, 0.166), resolution=(960, 540)), "蓝色确定兑换"):
                sleep(5)
            self.Tool.existsTHENtouch(返回图标, "友情礼包返回图标", savepos=True)
        # 击败宝箱
        if self.友情礼包_击败宝箱 and self.Tool.existsTHENtouch(Template(r"tpl1707301309821.png", record_pos=(-0.279, 0.005), resolution=(960, 540)), "友情皮肤礼包兑换"):
            sleep(5)
            if self.Tool.existsTHENtouch(Template(r"tpl1707301267168.png", record_pos=(0.32, 0.228), resolution=(960, 540)), "友情币兑换"):
                sleep(5)
            if self.Tool.existsTHENtouch(Template(r"tpl1700454987098.png", record_pos=(0.1, 0.117), resolution=(960, 540)), "金色确定兑换"):
                sleep(5)
            if self.Tool.existsTHENtouch(Template(r"tpl1700454996867.png", record_pos=(-0.099, 0.166), resolution=(960, 540)), "蓝色确定兑换"):
                sleep(5)
            self.Tool.existsTHENtouch(返回图标, "友情礼包返回图标", savepos=True)

    def KPL每日观赛(self, times=0, 观赛时长=20*60):
        # @todo,内部的timelimit
        if not self.check_run_status():
            return True
        self.进入大厅()
        if not self.check_run_status():
            return True
        #
        if self.set_timelimit(istep=times, init=times == 0, timelimit=观赛时长, nstep=100):
            return True
        times = times+1
        KPL观赛入口 = Template(r"tpl1707396642681.png", record_pos=(0.463, 0.126), resolution=(960, 540))
        KPL战令入口 = Template(r"tpl1707398684588.png", record_pos=(0.231, -0.231), resolution=(960, 540))
        KPL观赛界面 = []
        KPL观赛界面.append(Template(r"tpl1707396755590.png", record_pos=(-0.354, -0.264), resolution=(960, 540)))
        KPL观赛界面.append(Template(r"tpl1707398710560.png", record_pos=(-0.3, -0.269), resolution=(960, 540)))
        KPL观赛界面.append(KPL战令入口)
        self.Tool.existsTHENtouch(KPL观赛入口, "KPL观赛入口", savepos=True)
        进入观赛界面, KPL观赛界面 = self.Tool.存在任一张图(KPL观赛界面, "KPL观赛界面")
        if not 进入观赛界面:
            TimeECHO("准备进入KPL观赛入口")
            self.进入大厅()
            # 第一次识别失败时,更新观赛入口
            self.Tool.存在任一张图([KPL观赛入口], "KPL观赛入口", savepos=True)
            if not self.Tool.existsTHENtouch(KPL观赛入口, "KPL观赛入口", savepos=True):
                return self.KPL每日观赛(times, 观赛时长)
            sleep(30)
            for i in range(15):
                进入观赛界面, KPL观赛界面 = self.Tool.存在任一张图(KPL观赛界面, "KPL观赛界面")
                if 进入观赛界面:
                    break
                sleep(5)
        if not 进入观赛界面:
            TimeECHO(":没能进入KPL观赛入口,重新进入")
            return self.KPL每日观赛(times, 观赛时长)
        looptimes = 0
        while not self.set_timelimit(istep=times, init=times == 0, timelimit=观赛时长, nstep=100):
            TimeECHO(f":KPL观影中{looptimes*30.0/60}/{观赛时长/60}")
            sleep(30)
            looptimes = looptimes+1
        # 开始领战令礼包
        if not self.Tool.existsTHENtouch(KPL战令入口, "KPL战令入口", savepos=True):
            return
        KPL战令任务 = Template(r"tpl1707398869726.png", record_pos=(-0.441, -0.158), resolution=(960, 540))
        if not self.Tool.existsTHENtouch(KPL战令任务, "KPL战令任务", savepos=True):
            return
        KPL领取奖励 = Template(r"tpl1707398884057.png", record_pos=(0.359, -0.176), resolution=(960, 540))
        self.Tool.LoopTouch(KPL领取奖励, "KPL领取奖励", savepos=False)
        KPL战令返回 = Template(r"tpl1707399262936.png", record_pos=(-0.478, -0.267), resolution=(960, 540))
        self.Tool.LoopTouch(KPL战令返回, "KPL战令返回", savepos=False)
        return True

        #
    def 每日礼包_每日任务(self, times=0, 战令领取=True):
        #
        if not self.check_run_status():
            return True
        self.进入大厅()
        if not self.check_run_status():
            return True
        #
        if self.set_timelimit(istep=times, init=times == 0, timelimit=60*10, nstep=10):
            return True
        #
        times = times+1
        # 每日任务
        赛季任务界面 = []
        赛季任务界面.append(Template(r"tpl1703756264588.png", record_pos=(-0.407, -0.255), resolution=(960, 540)))
        赛季任务界面.append(Template(r"tpl1703756272809.png", record_pos=(0.373, 0.11), resolution=(960, 540)))
        赛季任务界面.append(Template(r"tpl1703755615130.png", record_pos=(-0.453, -0.058), resolution=(960, 540)))
        赛季任务界面.append(Template(r"tpl1706543181534.png", record_pos=(0.373, 0.173), resolution=(960, 540)))
        赛季任务界面.append(Template(r"tpl1706543217077.png", record_pos=(-0.255, 0.174), resolution=(960, 540)))
        赛季任务界面.append(Template(r"tpl1706543240746.png", record_pos=(0.352, 0.183), resolution=(960, 540)))
        任务 = Template(r"tpl1703755622899.png", record_pos=(-0.448, -0.027), resolution=(960, 540))
        任务列表 = Template(r"tpl1703757152809.png", record_pos=(-0.173, -0.18), resolution=(960, 540))
        确定按钮 = Template(r"tpl1694441190629.png", record_pos=(0.0, 0.165), resolution=(960, 540))
        self.进入大厅()
        self.Tool.existsTHENtouch(self.图片.战令入口, "战令入口", savepos=True)
        sleep(15)
        进入战令界面 = False
        进入战令界面, 赛季任务界面 = self.Tool.存在任一张图(赛季任务界面, "赛季任务界面")
        #
        if not 进入战令界面 and times > 2:
            进入战令界面 = not self.判断大厅中()
        #
        if not 进入战令界面:
            TimeECHO(f"未检测到战令界面, 重新进入领任务礼包")
            if "战令入口" in self.Tool.var_dict.keys():
                del self.Tool.var_dict["战令入口"]
            return self.每日礼包_每日任务(times=times, 战令领取=战令领取)
        #
        if 战令领取:
            TimeECHO(f"领取战令奖励测试中")
            战令一键领取 = Template(r"tpl1703765448167.png", record_pos=(0.293, 0.11), resolution=(960, 540), target_pos=6)
            if self.Tool.existsTHENtouch(战令一键领取, "战令一键领取", savepos=False):
                self.Tool.LoopTouch(确定按钮, "确定按钮")
                self.关闭按钮()
                self.确定按钮()
        # 正常每日礼包
        一键领取 = Template(r"tpl1693193500142.png", record_pos=(0.391, 0.224), resolution=(960, 540))
        # 新图标
        今日活跃 = Template(r"tpl1703758748236.png", record_pos=(-0.239, 0.233), resolution=(960, 540))
        本周活跃1 = Template(r"tpl1703758755430.png", record_pos=(-0.075, 0.232), resolution=(960, 540))
        本周活跃2 = Template(r"tpl1703758760425.png", record_pos=(-0.015, 0.232), resolution=(960, 540))
        #
        返回 = Template(r"tpl1694442171115.png", record_pos=(-0.441, -0.252), resolution=(960, 540))
        # 开始切换到任务界面,但是可能比较卡,要等
        进入任务界面 = False
        for i in range(60):
            self.Tool.existsTHENtouch(任务, "战令的每日任务", savepos=True)
            if exists(任务列表):
                进入任务界面 = True
                break
            if exists(一键领取):
                进入任务界面 = True
                break
            sleep(5)
            if self.set_timelimit(istep=times, init=times == 0, timelimit=60*10, nstep=10):
                return False
        if not 进入任务界面:
            TimeECHO(f"未检测到任务界面, 重新进入领任务礼包")
            if "战令的每日任务" in self.Tool.var_dict.keys():
                del self.Tool.var_dict["战令的每日任务"]
            return self.每日礼包_每日任务(times=times-1, 战令领取=战令领取)
        #
        # 开始正式领取
        if self.Tool.existsTHENtouch(一键领取, "一键领取 "):
            self.Tool.existsTHENtouch(确定按钮, "确定")
            sleep(5)
        # 这几个活跃，暂时没有找到位置，不确定是没发光的原因，还是图标变化
        # 这是使用savepos，下次换了新的领取位置记得清除这些dict
        if self.Tool.existsTHENtouch(今日活跃, "今日活跃 ", savepos=True):
            self.Tool.existsTHENtouch(确定按钮, "确定")
            sleep(5)
        if self.Tool.existsTHENtouch(本周活跃1, "本周活跃1", savepos=True):
            self.Tool.existsTHENtouch(确定按钮, "确定")
            sleep(5)
        if self.Tool.existsTHENtouch(本周活跃2, "本周活跃2", savepos=True):
            self.Tool.existsTHENtouch(确定按钮, "确定")
            sleep(5)
        #
        self.Tool.LoopTouch(确定按钮, "确定按钮")
        self.关闭按钮()
        self.确定按钮()
        #
        # 新赛季增加的领取入口
        本周任务 = Template(r"tpl1703755716888.png", record_pos=(-0.175, -0.192), resolution=(960, 540))
        本周签到 = Template(r"tpl1703755733895.png", record_pos=(0.244, 0.228), resolution=(960, 540))
        确定签到 = Template(r"tpl1703755744366.png", record_pos=(-0.001, 0.165), resolution=(960, 540))
        if self.Tool.existsTHENtouch(本周任务, "本周任务礼包", savepos=True):
            sleep(5)
            if self.Tool.existsTHENtouch(本周签到, "本周战令签到", savepos=False):
                self.Tool.LoopTouch(确定签到, "确定签到战令")
            if self.Tool.existsTHENtouch(一键领取, "一键领取 "):
                self.Tool.existsTHENtouch(确定按钮, "确定")
                sleep(5)
            self.Tool.LoopTouch(确定按钮, "确定按钮")
            self.关闭按钮()
            self.确定按钮()
        本期任务 = Template(r"tpl1703755722682.png", record_pos=(-0.068, -0.192), resolution=(960, 540))
        if self.Tool.existsTHENtouch(本期任务, "本期任务礼包", savepos=True):
            sleep(5)
            if self.Tool.existsTHENtouch(一键领取, "一键领取 "):
                self.Tool.existsTHENtouch(确定按钮, "确定")
                sleep(5)
            self.Tool.LoopTouch(确定按钮, "确定按钮")
            self.关闭按钮()
            self.确定按钮()
        #
        self.Tool.LoopTouch(返回, "返回")
        self.确定按钮()
        return True

    def 每日礼包_邮件礼包(self, times=0):
        #
        if not self.check_run_status():
            return True
        self.进入大厅()
        if not self.check_run_status():
            return True
        #
        if self.set_timelimit(istep=times, init=times == 0, timelimit=60*10, nstep=10):
            return True
        #
        times = times+1
        邮件图标 = Template(r"tpl1694441018032.png", record_pos=(0.35, -0.251), resolution=(960, 540))
        好友邮件 = Template(r"tpl1694441042380.png", record_pos=(-0.453, -0.188), resolution=(960, 540))
        收到邮件 = Template(r"tpl1694441057562.png", record_pos=(-0.31, -0.199), resolution=(960, 540))
        快速领取 = Template(r"tpl1694441070767.png", record_pos=(0.385, 0.23), resolution=(960, 540))
        下次吧 = Template(r"tpl1694443587766.png", record_pos=(-0.097, 0.118), resolution=(960, 540))
        金币确定 = Template(r"tpl1694443607846.png", record_pos=(0.002, 0.167), resolution=(960, 540))
        点击屏幕继续 = Template(r"tpl1694487484286.png", record_pos=(-0.006, 0.237), resolution=(960, 540))
        友情确定 = Template(r"tpl1694487498294.png", record_pos=(-0.097, 0.24), resolution=(960, 540))
        系统邮件 = Template(r"tpl1694441115819.png", record_pos=(-0.446, -0.127), resolution=(960, 540))
        系统快速领取 = Template(r"tpl1694451260084.png", record_pos=(0.415, 0.236), resolution=(960, 540))
        解锁语音界面 = Template(r"tpl1694441160296.png", record_pos=(-0.01, -0.015), resolution=(960, 540))
        我知道了 = Template(r"tpl1694441175302.png", record_pos=(-0.1, 0.116), resolution=(960, 540))
        系统礼物确定 = Template(r"tpl1694441190629.png", record_pos=(0.0, 0.165), resolution=(960, 540))
        黄色礼物确定 = Template(r"tpl1694441373245.png", record_pos=(-0.002, 0.116), resolution=(960, 540))
        系统礼物关闭 = Template(r"tpl1699626801240.png", record_pos=(0.34, -0.205), resolution=(960, 540))
        下次再选 = Template(r"tpl1704542576626.png", record_pos=(-0.099, 0.182), resolution=(960, 540))

        返回 = Template(r"tpl1694442171115.png", record_pos=(-0.441, -0.252), resolution=(960, 540))
        self.Tool.existsTHENtouch(邮件图标)
        if not exists(好友邮件):
            if not self.判断大厅中():
                self.进入大厅()
            if self.Tool.existsTHENtouch(邮件图标, "邮件图标"):
                sleep(10)
            if not exists(好友邮件):
                return self.每日礼包_邮件礼包(times)
        #
        if self.Tool.existsTHENtouch(好友邮件):
            self.Tool.existsTHENtouch(收到邮件, "收到邮件", savepos=False)
            self.Tool.existsTHENtouch(快速领取, "快速领取", savepos=False)
            # 缺少确定
            self.Tool.LoopTouch(下次吧, "下次吧", loop=10)
            self.Tool.existsTHENtouch(金币确定, "金币确定")
            self.Tool.existsTHENtouch(点击屏幕继续, "点击屏幕继续")
            self.Tool.existsTHENtouch(友情确定, "友情确定")
            #
        if self.Tool.existsTHENtouch(系统邮件):
            sleep(5)
            self.Tool.LoopTouch(系统礼物关闭, "系统礼物关闭", loop=5)
            self.Tool.existsTHENtouch(系统快速领取, "系统快速领取", savepos=False)
            self.Tool.LoopTouch(系统礼物关闭, "系统礼物关闭", loop=5)
            self.Tool.LoopTouch(黄色礼物确定, "黄色礼物确定", loop=10)
            self.Tool.existsTHENtouch(下次再选, "下次再选礼物")
            self.Tool.LoopTouch(系统礼物关闭, "系统礼物关闭", loop=5)
            while self.Tool.existsTHENtouch(系统礼物确定, "系统礼物确定"):
                if exists(解锁语音界面):
                    self.Tool.existsTHENtouch(我知道了, "我知道了")
                self.Tool.LoopTouch(系统礼物关闭, "系统礼物关闭", loop=5)
                self.Tool.LoopTouch(黄色礼物确定, "黄色礼物确定", loop=10)
                self.Tool.existsTHENtouch(下次再选, "下次再选礼物")
                self.Tool.existsTHENtouch(系统礼物关闭, "系统礼物关闭", savepos=False)
                if self.Tool.timelimit(timekey="领邮件礼包", limit=60*5, init=False):
                    TimeECHO("领邮件礼包超时.....")
                    return self.每日礼包_邮件礼包(times)
            self.Tool.LoopTouch(系统礼物确定, "系统礼物确定", loop=10)

        self.Tool.LoopTouch(返回, "返回")
        return True

        # 妲己礼物
    def 每日礼包_妲己礼物(self, times=0):
        #
        if not self.check_run_status():
            return True
        self.进入大厅()
        if not self.check_run_status():
            return True
        #
        if self.set_timelimit(istep=times, init=times == 0, timelimit=60*10, nstep=10):
            return True
        #
        times = times+1
        # 小妲己的图标会变化
        妲己图标 = []
        妲己图标.append(Template(r"tpl1694441259292.png", record_pos=(0.458, 0.21), resolution=(960, 540)))
        妲己图标.append(Template(r"tpl1703297029482.png", record_pos=(0.451, 0.207), resolution=(960, 540)))
        一键领奖 = Template(r"tpl1694442066106.png", record_pos=(-0.134, 0.033), resolution=(960, 540))
        去领取 = Template(r"tpl1694442088041.png", record_pos=(-0.135, 0.107), resolution=(960, 540))
        收下 = Template(r"tpl1694442103573.png", record_pos=(-0.006, 0.181), resolution=(960, 540))
        确定 = Template(r"tpl1694441190629.png", record_pos=(0.0, 0.165), resolution=(960, 540))
        返回 = Template(r"tpl1694442136196.png", record_pos=(-0.445, -0.251), resolution=(960, 540))
        能力测试关闭 = Template(r"tpl1699626801240.png", record_pos=(0.34, -0.205), resolution=(960, 540))
        #
        进入成功 = False
        for i in range(len(妲己图标)):
            if not self.判断大厅中():
                self.进入大厅()
            进入成功 = self.Tool.existsTHENtouch(妲己图标[i], f"妲己图标{i}")
            if 进入成功:
                break
        if not 进入成功:
            return self.每日礼包_妲己礼物(times)
        #
        if exists(一键领奖):
            self.Tool.existsTHENtouch(去领取, "去领取")
            self.Tool.LoopTouch(收下, "收下", loop=10)
            self.Tool.LoopTouch(确定, "确定", loop=10)
            self.Tool.LoopTouch(收下, "收下", loop=10)
            self.Tool.LoopTouch(确定, "确定", loop=10)
        self.Tool.existsTHENtouch(能力测试关闭, "能力测试关闭")
        self.Tool.LoopTouch(返回, "返回")
        self.确定按钮()
        return True
        #
    #

    def 每日礼包_王者营地(self):
        if self.Tool.timelimit("领营地礼包", limit=60*60*3, init=False):
            TimeECHO(f"{fun_name(1)}")
            self.APPOB.关闭APP()
            from wzyd import wzyd_libao
            ce = wzyd_libao()
            ce.run()
            ce.APPOB.关闭APP()
            return True
        else:
            TimeECHO(f"时间太短,暂时不{fun_name(1)}")
            return False
    #

    def 体验服更新(self):
        if self.Tool.timelimit("体验服更新", limit=60*60*3, init=False):
            TimeECHO(f"{fun_name(1)}")
            self.APPOB.关闭APP()
            from tiyanfu import tiyanfu
            ce = tiyanfu()
            ce.run()
            ce.APPOB.关闭APP()
            return True
        else:
            TimeECHO(f"时间太短,暂时不{fun_name(1)}")
            return False

# 状态判断
    #
    def quick判断界面(self, dt=60*60):
        """
        # 适合图片元素很多的情况，比如战绩页面、对战页面、房间页面
        #
        if self.quick判断界面() in [ "登录界面", "大厅中", "房间中", "对战中", "对战中_模拟战", "战绩页面"]:
            return False
        #
        """
        # 取出最容易的元素进行初筛
        # 这里的0都是被筛选过的元素
        大厅元素 = self.图片.大厅元素[0]
        房间元素 = self.图片.房间元素[0]
        对战元素 = self.图片.对战图片元素[0] if "5v5" in self.对战模式 else self.图片.对战图片元素_模拟战[0]
        对战tag = "对战中" if "5v5" in self.对战模式 else "对战中_模拟战"
        战绩元素 = self.图片.战绩页面元素[0]
        元素集合 = [大厅元素, 房间元素, 对战元素, 战绩元素]
        if self.当前界面 == "房间中":
            元素集合 = [房间元素, 对战元素, 大厅元素, 战绩元素]
        if self.当前界面 == 对战tag:
            元素集合 = [对战元素, 战绩元素, 大厅元素, 房间元素]
        if self.当前界面 == "战绩页面":
            元素集合 = [战绩元素, 房间元素, 大厅元素, 对战元素]
        #
        # 极短时间内不重复判断
        # 此处不能调用 self.Tool.timelimit(timekey="当前界面", limit=10, init=False)
        # 因为调用后，会立刻重置 self.Tool.timedict["当前界面"] ，而又没有修改 self.当前界面 的内容，会卡死循环
        # 因此采用复制时间戳的方式
        try:  # 直接读取字典容易错，采用try的方式
            self.Tool.timedict["quick判断界面"] = max(self.Tool.timedict["quick判断界面"], self.Tool.timedict["当前界面"])
        except:
            self.Tool.timedict["quick判断界面"] = 0
        #
        if not self.Tool.timelimit(timekey="quick判断界面", limit=10, init=False):
            return self.当前界面
        #
        存在, 元素集合 = self.Tool.存在任一张图(元素集合, f"{fun_name(2)}.quick判断界面")
        if not 存在:
            return "未知"
        #
        self.Tool.timelimit(timekey="quick判断界面", limit=10, init=True)
        # 存在的情况下，可以快速出结果
        if 元素集合[0] == 大厅元素:
            self.当前界面 = "大厅中"
        elif 元素集合[0] == 房间元素:
            self.当前界面 = "房间中"
        elif 元素集合[0] == 对战元素:
            self.当前界面 = 对战tag
        elif 元素集合[0] == 战绩元素:
            self.当前界面 = "战绩页面"
        self.Tool.timelimit(timekey="当前界面", limit=60*2, init=True)
        TimeECHO(f"{fun_name(2)}.quick判断界面:{self.当前界面}")
        return self.当前界面
        #
    #

    def 判断战绩页面(self):
        if self.当前状态 in ["领取礼包", "重新启动"]:
            TimeECHO(f"{fun_name(1)}: 当前状态 =  {self.当前状态}, return False")
            return False
        #
        if self.quick判断界面() in ["大厅中", "房间中", "对战中", "对战中_模拟战"]:
            return False
        #
        if not self.Tool.timelimit(timekey="当前界面", limit=60*2, init=False):
            if self.当前界面 in ["房间中", "大厅中", "登录界面"]:
                TimeECHO(f"{fun_name(1)}.采用历史的判断结果判定当前处在:{self.当前界面}")
                return False
        #
        存在, self.图片.战绩页面元素 = self.Tool.存在任一张图(self.图片.战绩页面元素, "战绩页面元素")
        if not 存在:
            存在, self.图片.结算页面元素 = self.Tool.存在任一张图(self.图片.结算页面元素, "结算页面元素")
        if 存在:
            self.当前界面 == "战绩页面"
            self.Tool.timelimit(timekey="当前界面", init=True)
        else:
            self.当前界面 = "未知"
        return 存在

    def 判断大厅中(self):
        #
        if self.当前界面 == "大厅中":
            if self.Tool.timelimit(timekey="当前界面", limit=60, init=False):
                self.当前界面 == "未知"
            else:
                TimeECHO(f"{fun_name(1)}.采用历史的判断结果判定当前处在:{self.当前界面}")
                return True
        elif self.当前界面 == "房间中":
            if not self.Tool.timelimit(timekey="当前界面", limit=30, init=False):
                TimeECHO(f"{fun_name(1)}.采用历史的判断结果判定当前处在:{self.当前界面}")
                return False
        elif self.当前界面 == "登录界面":
            if not self.Tool.timelimit(timekey="当前界面", limit=20, init=False):
                TimeECHO(f"{fun_name(1)}.采用历史的判断结果判定当前处在:{self.当前界面}")
                return False
        #
        if not self.APPOB.前台APP(0):
            self.当前界面 == "未知"
            return False
        存在, self.图片.大厅元素 = self.Tool.存在任一张图(self.图片.大厅元素, "大厅元素")
        #
        if 存在:
            self.当前界面 = "大厅中"
            # 减少判断次数,不用担心图片太少的问题,每日会重新更新图片
            del self.图片.大厅元素[1:]
            self.Tool.timelimit(timekey="当前界面", init=True)
        else:
            self.当前界面 = "未知"
        #
        return 存在

    def 判断房间中(self, 处理=True):
        if self.当前状态 in ["重新启动"]:
            TimeECHO(f"{fun_name(1)}: 当前状态 =  {self.当前状态}, return False")
            return
        #
        if self.quick判断界面() in ["大厅中", "对战中", "战绩页面", "对战中_模拟战"]:
            return False
        #
        if self.当前界面 == "房间中":
            if self.Tool.timelimit(timekey="当前界面", limit=60, init=False):
                self.当前界面 == "未知"
            else:
                TimeECHO(f"{fun_name(1)}.采用历史的判断结果判定当前处在:{self.当前界面}")
                return True
        elif self.当前界面 == "对战中":
            if not self.Tool.timelimit(timekey="当前界面", limit=30, init=False):
                TimeECHO(f"{fun_name(1)}.采用历史的判断结果判定当前处在:{self.当前界面}")
                return False
        elif self.当前界面 == "登录界面":
            if not self.Tool.timelimit(timekey="当前界面", limit=60, init=False):
                TimeECHO(f"{fun_name(1)}.采用历史的判断结果判定当前处在:{self.当前界面}")
                return False
        存在, self.图片.房间元素 = self.Tool.存在任一张图(self.图片.房间元素, "房间元素")
        if 存在:
            # 减少判断次数,不用担心图片太少的问题,每日会重新更新图片
            del self.图片.房间元素[1:]
        # 活动界面
        if 存在 and 处理:
            # 这些活动翻页元素一般只显示一次，新的账户每次进入房间都会提示
            存在翻页活动, self.图片.房间翻页活动元素 = self.Tool.存在任一张图(self.图片.房间翻页活动元素, "房间翻页活动元素")
            if 存在翻页活动:
                # 存在之后，这个活动只出现一次,可以删除这个变量了
                del self.图片.房间翻页活动元素[0]
                # 每天生成新的图片对象时会重新恢复原始图片的
                活动翻页 = Template(r"tpl1707787154169.png", record_pos=(0.393, -0.01), resolution=(960, 540))
                self.Tool.LoopTouch(活动翻页, "房间中活动翻页", savepos=False)
                self.Tool.existsTHENtouch(self.图片.房间我知道了, "我知道了:翻页活动", savepos=False)
            else:
                # 如果不存的话,也可以适当删除一些self.图片.房间翻页活动元素
                if len(self.图片.房间翻页活动元素) > 0:
                    if not exists(self.图片.房间翻页活动元素[-1]):
                        del self.图片.房间翻页活动元素[-1]
            #
            存在, self.图片.房间元素 = self.Tool.存在任一张图(self.图片.房间元素, "房间元素")
        #
        if 存在:
            self.当前界面 = "房间中"
            self.Tool.timelimit(timekey="当前界面", init=True)
        else:
            self.当前界面 = "未知"
        #
        return 存在

    def 判断对战中(self, 处理=False):
        if self.当前状态 in ["领取礼包", "重新启动"]:
            TimeECHO(f"{fun_name(1)}: 当前状态 =  {self.当前状态}, return False")
            return False
        #
        if "模拟战" in self.对战模式:
            return self.判断对战中_模拟战(处理)
        #
        if self.quick判断界面() in ["大厅中", "房间中", "战绩页面"]:
            return False
        #
        对战中 = False
        if self.当前界面 == "对战中":
            if self.Tool.timelimit(timekey="当前界面", limit=60, init=False):
                self.当前界面 == "未知"
            else:
                TimeECHO(f"{fun_name(1)}.采用历史的判断结果判定当前处在:{self.当前界面}")
                对战中 = True
        elif self.当前界面 == "大厅中":
            if not self.Tool.timelimit(timekey="当前界面", limit=30, init=False):
                TimeECHO(f"{fun_name(1)}.采用历史的判断结果判定当前处在:{self.当前界面}")
                return False
        elif self.当前界面 == "登录界面":
            if not self.Tool.timelimit(timekey="当前界面", limit=60, init=False):
                TimeECHO(f"{fun_name(1)}.采用历史的判断结果判定当前处在:{self.当前界面}")
                return False
        if not 对战中:
            对战中, self.图片.对战图片元素 = self.Tool.存在任一张图(self.图片.对战图片元素, "对战图片元素")
            if 对战中:
                self.当前界面 = "对战中"
                self.Tool.timelimit(timekey="当前界面", init=True)
            else:
                self.当前界面 = "未知"
        #
        if 对战中:
            TimeECHO(f"{fun_name(1)}:正在对战")
        if not 对战中:
            TimeECHO(f"{fun_name(1)}:没有对战")
        if not 处理 or not 对战中:
            return 对战中
        #
        # 开始处理加速对战
        TimeECHO("加速对战中:建议把自动买装备和自动技能加点打开,更真实一些")
        self.Tool.timelimit(timekey="endgame", limit=60*30, init=True)
        self.Tool.timelimit(timekey="check_run_status", limit=60, init=True)
        # 识别到的位置
        装备pos = False
        移动pos = False
        普攻pos = False
        装备poskey = f"装备pos({self.mynode})"
        移动poskey = f"移动pos({self.mynode})"
        普攻poskey = f"普攻pos({self.mynode})"
        # 开始模拟人手点击
        while self.判断对战中(处理=False):
            TimeECHO("加速对战中:对战按钮")
            if self.Tool.timelimit(timekey="check_run_status", limit=60, init=False):
                if not self.check_run_status():
                    return False
            if self.Tool.存在同步文件():
                return True
            # 不同账户出装位置不同, 这里随机识别一次，更新未位置
            if random.randint(1, 5) == 1:
                装备pos = False
            if not 装备pos:
                # 每一次尝试采用新的位置
                存在装备图标, self.图片.装备S = self.Tool.存在任一张图(self.图片.装备S, 装备poskey, savepos=True)
                if 存在装备图标:
                    装备pos = self.Tool.var_dict[装备poskey]
                # 如果找不到，就看看历史上使用的哪个位置
                elif 装备poskey in self.Tool.var_dict.keys():
                    装备pos = self.Tool.var_dict[装备poskey]
            #
            if not 移动pos:
                # 每一次尝试采用新的位置
                存在移动图标, self.图片.移动S = self.Tool.存在任一张图(self.图片.移动S, 移动poskey, savepos=True)
                if 存在移动图标:
                    移动pos = self.Tool.var_dict[移动poskey]
                # 如果找不到，就看看历史上使用的哪个位置
                elif 移动poskey in self.Tool.var_dict.keys():
                    移动pos = self.Tool.var_dict[移动poskey]
            #
            if not 普攻pos:
                # 每一次尝试采用新的位置
                存在普攻图标, self.图片.普攻S = self.Tool.存在任一张图(self.图片.普攻S, 普攻poskey, savepos=True)
                if 存在普攻图标:
                    普攻pos = self.Tool.var_dict[普攻poskey]
                # 如果找不到，就看看历史上使用的哪个位置
                elif 普攻poskey in self.Tool.var_dict.keys():
                    普攻pos = self.Tool.var_dict[普攻poskey]
            #
            if 装备pos:
                touch(装备pos)
            #
            if 移动pos:
                content = self.Tool.readfile(self.触摸对战FILE)
                # 如果有血条在第一行，则进行下面的测试代码
                # 很难判断成功
                if len(content) > 1:
                    if "血条" in content[0]:
                        del content[0]
                        # 针对血条调整运动方向
                        vector = None
                        存在敌方, self.图片.敌方血条 = self.Tool.存在任一张图(self.图片.敌方血条, "敌方血条元素")
                        if 存在敌方:
                            vector = [-0.2, random.random()/5]
                        else:
                            存在友方, self.图片.友方血条 = self.Tool.存在任一张图(self.图片.友方血条, "友方血条元素")
                            if 存在友方:
                                vector = [0.2, random.random()/5]
                        if vector:
                            TimeECHO("针对英雄调整位置")
                            for i in range(10):
                                swipe(移动pos, vector=[x, y])
                #
                # 随机移动和攻击
                TimeECHO("加速对战中:移动按钮")
                x = None
                inputxy = content
                if len(inputxy) > 1:
                    try:
                        x = float(inputxy[0])
                        y = float(inputxy[1])
                        TimeECHO(": x=%5.3f, y=%5.3f" % (x, y))
                    except:
                        TimeErr(f" not found x y in [{self.触摸对战FILE}]")
                for i in range(random.randint(1, 5)):
                    if not x:
                        x = 0.2+random.random()/5
                        y = -0.2+random.random()/5
                    swipe(移动pos, vector=[x, y])
                    #
                    if 普攻pos:
                        sleep(0.2)
                        touch(普攻pos)
            #
            if 普攻pos:
                touch(普攻pos)
            #
            if self.Tool.timelimit(timekey="endgame", limit=60*30, init=False):
                TimeErr("对战中游戏时间过长,重启游戏")  # 存在对战的时间超过20min,大概率卡死了
                self.重启并登录(10)
                self.进入大厅()
                return False
        return True

    def 判断对战中_模拟战(self, 处理=False):
        #
        if self.quick判断界面() in ["大厅中", "房间中", "战绩页面"]:
            return False
        #
        对战中 = False
        if self.当前界面 == "对战中_模拟战":
            if self.Tool.timelimit(timekey="当前界面", limit=60, init=False):
                self.当前界面 == "未知"
            else:
                TimeECHO(f"{fun_name(1)}.采用历史的判断结果判定当前处在:{self.当前界面}")
                对战中 = True
        elif self.当前界面 == "大厅中":
            if not self.Tool.timelimit(timekey="当前界面", limit=30, init=False):
                TimeECHO(f"{fun_name(1)}.采用历史的判断结果判定当前处在:{self.当前界面}")
                return False
        elif self.当前界面 == "登录界面":
            if not self.Tool.timelimit(timekey="当前界面", limit=60, init=False):
                TimeECHO(f"{fun_name(1)}.采用历史的判断结果判定当前处在:{self.当前界面}")
                return False
        if not 对战中:
            对战中, self.图片.对战图片元素_模拟战 = self.Tool.存在任一张图(self.图片.对战图片元素_模拟战, "对战图片元素_模拟战")
            if 对战中:
                self.当前界面 = "对战中_模拟战"
                self.Tool.timelimit(timekey="当前界面", init=True)
            else:
                self.当前界面 = "未知"
        #
        if 对战中:
            TimeECHO(f"{fun_name(1)}:正在对战")
        if not 对战中:
            TimeECHO(f"{fun_name(1)}:没有对战")
        if not 处理 or not 对战中:
            return 对战中
        #
        # 开始处理加速对战
        self.Tool.timelimit(timekey="endgame", limit=60*20, init=True)
        while self.判断对战中_模拟战(False):
            TimeECHO("处理对战中")
            self.Tool.LoopTouch(self.图片.钱袋子_模拟战, "LOOP钱袋子", loop=10)  # 点击结束后,应该变成X号
            self.Tool.LoopTouch(self.图片.刷新金币_模拟战, "LOOP刷新金币", loop=10)
            if not exists(self.图片.关闭钱袋子_模拟战) and not exists(self.图片.钱袋子_模拟战):
                return False
            if self.Tool.timelimit(timekey="endgame", limit=60*20, init=False):
                break
            sleep(10)
            if not self.check_run_status():
                return True
        return 对战中

    def 健康系统(self):
        if exists(Template(r"tpl1689666921933.png", record_pos=(0.122, -0.104), resolution=(960, 540))):
            TimeECHO("您已禁赛")
            确定 = Template(r"tpl1693660628972.png", record_pos=(-0.003, 0.118), resolution=(960, 540))
            self.Tool.existsTHENtouch(确定, "确定禁赛")
            return True
        return False

    def 健康系统_常用命令(self):
        if self.健康系统():
            self.APPOB.关闭APP()
            content = "检测到健康系统"
            return self.创建同步文件(content)
        else:
            return False

    def check_run_status(self):
        #
        self.组队模式 = self.组队模式 and not os.path.exists(self.无法进行组队FILE)
        #
        if os.path.exists(self.重新登录FILE):
            content = f"[{funs_name()}]失败:存在[{self.重新登录FILE}]"
            TimeECHO(content)
            self.Tool.touch同步文件(self.Tool.独立同步文件, content=content)
        #
        if self.Tool.存在同步文件(self.Tool.独立同步文件):
            content = f"[{funs_name()}]失败:存在[{self.Tool.独立同步文件}]"
            TimeECHO(content)
            if self.组队模式:
                self.Tool.touch同步文件(self.Tool.辅助同步文件, content=content)
            TimeECHO(content)
            return False
        if self.totalnode_bak > 1 and self.Tool.存在同步文件(self.Tool.辅助同步文件):
            TimeECHO(f"[{funs_name()}]失败:存在[{self.Tool.辅助同步文件}]")
            return False
        #
        if not connect_status():
            # 尝试连接一下,还不行就同步吧
            self.移动端.连接设备(times=1, timesMax=2)
            if not connect_status():
                # 单人模式创建同步文件后等待,组队模式则让全体返回
                content = f"[{funs_name()}]失败:无法connect"
                TimeECHO(content)
                self.创建同步文件(content)
                return False
        #
        return True
    #

    def set_timelimit(self, istep, init, timelimit, nstep, touch同步=False):
        """
        超时返回True
        对战函数相关时: touch同步=True
        领礼包的函数时: touch同步=False
        """
        content = f"{fun_name(2)}.运行.{istep}.次"
        if init:
            self.Tool.timelimit(timekey=f"{fun_name(2)}", limit=timelimit, init=True)
        elif self.Tool.timelimit(timekey=f"{fun_name(2)}", limit=timelimit, init=False) or istep > nstep:
            content = f"{content}...........超时"
            if touch同步:
                self.创建同步文件(content)
            else:
                TimeECHO(content)
            return True
        TimeECHO(f"{fun_name(1)}: "+content)
        return False
    #

    def 重启APP_acce(self, sleeptime=0):
        self.APPOB.重启APP(sleeptime=sleeptime)
        self.当前界面 = "登录界面"
        self.Tool.timelimit(timekey="当前界面", limit=60*2, init=True)
        return True
    #

    def 重启并登录(self, sleeptime=0):
        bakstate = self.当前状态
        self.当前状态 = "重新启动"
        self.重启APP_acce(sleeptime=sleeptime)
        result = self.登录游戏()
        self.当前状态 = bakstate
        return result
    #

    def 创建同步文件(self, content=""):
        """
        * 遇到问题,需要重启程序时,统一创建同步文件，而不是立即重启
        * 在主函数的开头，如果存在同步文件，则重启手机
        """
        content = f"{fun_name(2)}:{content}" if len(content) > 0 else f"{funs_name()}.创建同步文件"
        TimeECHO(content)
        if self.组队模式:
            self.Tool.touch同步文件(self.Tool.辅助同步文件, content=content)
            return True
        else:
            self.Tool.touch同步文件(self.Tool.独立同步文件, content=content)
            return True

# 开始运行

    def 进行人机匹配对战循环(self):
        # 初始化
        if not self.check_run_status():
            return
        #
        if self.房主:
            TimeECHO("人机匹配对战循环:"+"->"*10)
        # 进入房间
        self.进入人机匹配房间()
        if not self.check_run_status():
            return
        # 进行对战
        self.进行人机匹配()
        if not self.check_run_status():
            return
        加速对战 = False
        if "模拟战" in self.对战模式:
            加速对战 = True
        if self.触摸对战 and "5v5" in self.对战模式:
            加速对战 = True
        if self.判断对战中(加速对战):
            sleep(30)
        if not self.check_run_status():
            return
        # 结束对战
        self.结束人机匹配()
        #
        if not self.check_run_status():
            return
        #
        if self.mynode == 0:
            self.Tool.clean文件()
        if self.房主:
            TimeECHO("<-"*10)
        #
    #

    def STOP(self, content=""):
        """
        #立刻结束所有进程
        """
        self.END(content)
        self.Tool.touchstopfile(content)
        self.创建同步文件(content)
    #
    #

    def END(self, content=""):
        """
        # 立刻结束本进程
        """
        TimeECHO(f"立刻结束程序END.{content}")
        if self.totalnode_bak > 1:  # 让其他节点抓紧结束
            self.Tool.touchfile(self.无法进行组队FILE, content=content)
        self.APPOB.关闭APP()
        self.移动端.关闭设备()
        return

    #
    def RUN(self):  # 程序入口
        self.新的一天 = False
        if os.path.exists(self.只战一天FILE):
            try:
                self.runstep = int(self.Tool.readfile(self.只战一天FILE)[0].strip())
            except:
                self.Tool.touchfile(self.只战一天FILE, content=str(self.runstep))
        while True:
            self.当前状态 = "状态检查"
            # ------------------------------------------------------------------------------
            # 检测是否出现控制冲突,双脚本情况
            if self.myPID != self.Tool.readfile(self.WZRYPIDFILE)[0].strip():
                content = f": 本次运行PID[{self.myPID}]不同于[{self.WZRYPIDFILE}],退出中....."
                TimeErr(content)
                if self.totalnode_bak > 1:  # 让其他节点抓紧结束
                    self.Tool.touch同步文件(self.Tool.辅助同步文件, content=content)
                return True
            # ------------------------------------------------------------------------------
            run_class_command(self=self, command=self.Tool.readfile(self.临时初始化FILE))
            # ------------------------------------------------------------------------------
            # >>> 设备状态调整
            if self.Tool.stopnow():
                return self.END()
            if os.path.exists(self.无法进行组队FILE):
                self.组队模式 = False
                self.totalnode = 1
            # ------------------------------------------------------------------------------
            #
            if self.新的一天:
                TimeECHO(">>>>>>>>>>>>>>>新的一天>>>>>>>>>>>>>>>>>>>>")
                self.新的一天 = False
                if not connect_status():
                    self.移动端.连接设备()
                # 参数、礼包、图片、文件等的初始化
                self.初始化(init=False)
                if self.totalnode_bak > 1:
                    TimeECHO(":新的一天创建同步文件进行初次校准")
                    # 因为创建了同步文件之后，其他进程就会停下来
                    # **因此新一天的初始化命令必须放在前面处理同步的前面**
                    # 否则，其他进程就会进入到同步状态
                    # 同步之后再进入新的一天初始化，再同步，就有很多时间上的浪费
                    self.Tool.touch同步文件(content="新的一天初始化")
                else:
                    self.重启并登录(20)
            # ------------------------------------------------------------------------------
            # 健康系统禁赛、系统卡住、连接失败等原因导致check_run_status不通过，这里统一处理
            if self.Tool.存在同步文件():
                self.图片 = wzry_figure(Tool=self.Tool)
            if not self.check_run_status():
                #
                if not connect_status():
                    self.移动端.连接设备()
                #
                # 必须所有节点都能上线，否则并行任务就全部停止
                if not connect_status(times=2):
                    if self.totalnode_bak > 1:  # 让其他节点抓紧结束
                        content = "连接不上设备. 所有节点全部准备终止"
                        TimeErr(content)
                        # 这条命令一出，将强制结束所有的进程
                        return self.STOP(content)
                    else:
                        TimeErr("连接不上设备. 退出")
                        return True
                #
                content = self.Tool.readfile(self.Tool.辅助同步文件)[0]+self.Tool.readfile(self.Tool.独立同步文件)[0]
                TimeECHO(f"开始处理同步内容,同步原因:{content}")
                self.APPOB.关闭APP()
                # 如果个人能连上，检测是否有组队情况存在同步文件
                if self.totalnode_bak > 1:
                    # 判断是否存在self.Tool.辅助同步文件，若存在必须同步成功（除非存在stopfile）
                    TimeECHO(f"辅助同步内容:{content}")
                    sleeptime = 5*60 if "健康系统" in content else 10
                    self.Tool.必须同步等待成功(mynode=self.mynode, totalnode=self.totalnode_bak,
                                       同步文件=self.Tool.辅助同步文件, 不再同步=self.无法进行组队FILE,
                                       sleeptime=sleeptime)
                    if os.path.exists(self.无法进行组队FILE):
                        self.组队模式 = False
                        self.totalnode = 1
                        # 在创建self.Tool.辅助同步文件时，会自动创建self.Tool.独立同步文件
                        # 所以删除self.Tool.辅助同步文件没有问题
                        self.Tool.removefile(self.Tool.辅助同步文件)
                else:
                    TimeECHO(f"单账户重置完成")
                self.Tool.removefile(self.Tool.独立同步文件)
                # 重置完成
                if not self.组队模式 and "健康系统" in content:
                    self.每日礼包_王者营地()
                #
                # 检测账号登录状况
                if os.path.exists(self.重新登录FILE):
                    content = "存在重新登录文件"
                    TimeECHO(content)
                    # 让别的进程不要再执行组队代码
                    # 同时所有进程也不再创建和检测同步文件
                    self.组队模式 = False
                    self.Tool.touchfile(self.无法进行组队FILE, content=content)
                    #
                    if os.path.exists(self.只战一天FILE) and self.totalnode_bak > 1:
                        # 这条命令一出，将强制结束所有的进程
                        return self.STOP(content)
                    #
                    startclock = self.对战时间[0]
                    endclock = self.对战时间[1]
                    # 在对战时间内, 则尝试重新登录，或者关闭设备等待结束
                    if self.Tool.hour_in_span(startclock, endclock) == 0:
                        lefthour = self.Tool.hour_in_span(endclock, startclock)
                        if lefthour >= 4:
                            TimeECHO(f"存在[{self.重新登录FILE}],每4h重新登录一次")
                            self.移动端.重启重连设备(4*60*60)
                            self.重启并登录()
                            continue
                        else:
                            # 关闭设备，等待对战结束，执行本程序的结束程序
                            self.移动端.重启重连设备(lefthour*60*60)

                # 不存在登录文件的情况，就正常恢复单人对战
                else:
                    self.重启并登录(sleeptime=self.mynode*10)
                    # 如果账户正常，则登录
                    if not self.check_run_status() and self.Tool.hour_in_span(startclock, endclock) == 0:
                        sleep(20)
                        continue
                    #
            if self.Tool.stopnow():
                return self.END()
            #
            while os.path.exists(self.SLEEPFILE):
                TimeECHO(f"检测到{self.SLEEPFILE}, sleep(5min)")
                sleep(60*5)
            # ------------------------------------------------------------------------------
            # 这里做一个循环的判断，夜间不自动刷任务
            # 服务器5点刷新礼包和信誉积分等
            startclock = self.对战时间[0]
            endclock = self.对战时间[1]
            while self.Tool.hour_in_span(startclock, endclock) > 0 and not self.新的一天:
                # 万一其他节点因为bug卡在barrier,这里让他们别卡了
                self.组队模式 = False
                self.Tool.touchfile(self.无法进行组队FILE)
                只战一天 = os.path.exists(self.只战一天FILE)
                今日休战 = os.path.exists(self.今日休战FILE)
                self.当前状态 = "领取礼包"
                #
                if 只战一天:
                    TimeECHO("="*20)
                    TimeECHO("只战一天, 领取礼包后退出")
                    self.Tool.touchfile(self.只战一天FILE, content=str(self.runstep))
                    self.每日礼包(强制领取=self.强制领取礼包)
                    return self.END(content="只战一天,本进程结束")
                #
                # 还有多久开始，太短则直接跳过等待了
                leftmin = self.Tool.hour_in_span(startclock, endclock)*60.0
                self.新的一天 = True
                #
                if 今日休战:
                    TimeECHO("今日休战，明天再战")
                elif leftmin > 60:
                    TimeECHO("夜间停止刷游戏前领取礼包")
                    self.每日礼包(强制领取=self.强制领取礼包)
                    self.APPOB.关闭APP()
                elif leftmin < 10:
                    TimeECHO("剩余%d分钟进入新的一天" % (leftmin))
                    sleep(leftmin*60)
                    continue
                #
                # 避免还存在其他进行没有同步完成的情况
                head = ".tmp.night"
                foot = "txt"
                upfile = f"{head}.{self.myPID}.{self.mynode-1}.{foot}"
                dnfile = f"{head}.{self.myPID}.{self.mynode}.{foot}"
                fifile = f"{head}.{self.myPID}.{self.totalnode_bak-1}.{foot}"
                leftmin = self.Tool.hour_in_span(startclock, endclock)*60.0
                if leftmin > 60 and self.totalnode_bak > 1:
                    self.APPOB.关闭APP()
                    self.Tool.removefile(upfile)
                    self.Tool.removefile(fifile)
                    self.Tool.removefiles(head=head, body=f".{self.mynode}.", foot=foot)
                    looptime = range(1, 11)
                    timescale = 60.0/sum(looptime)
                    for itmp in looptime:
                        TimeECHO(f"夜间已关闭APP, 检测是否有多账户同步残留.{itmp}")
                        if self.mynode == 0 or os.path.exists(upfile):
                            self.Tool.touchfile(dnfile)
                        if os.path.exists(fifile):
                            break
                        sleep(itmp*timescale*60)
                #
                # 计算休息时间
                TimeECHO("准备休息")
                leftmin = self.Tool.hour_in_span(startclock, endclock)*60.0
                leftmin = leftmin+self.mynode*1.0  # 这里的单位是分钟,每个node别差别太大
                TimeECHO("预计等待%d min ~ %3.2f h" % (leftmin, leftmin/60.0))
                self.APPOB.关闭APP()
                self.移动端.重启重连设备(leftmin*60)
                # 其他
                self.Tool.removefile(self.今日休战FILE)
            # ------------------------------------------------------------------------------
            # 新的一天，回到开头进行初始化
            if self.新的一天:
                continue
            # ------------------------------------------------------------------------------
            # 下面就是正常的循环流程了
            self.当前状态 = "状态检查"
            if not self.check_run_status:
                continue
            # ------------------------------------------------------------------------------
            # 组队模式，单人模式判断
            # 各种原因无法组队判定
            if self.totalnode_bak > 1:
                self.无法进行组队 = os.path.exists(self.无法进行组队FILE)
                组队时间内 = not self.Tool.hour_in_span(startclock, self.限时组队时间) > 0
                可以组队 = not self.无法进行组队 and 组队时间内
                # 报告运行状态
                组队原因 = ""
                单人原因 = ""
                if self.组队模式 and self.无法进行组队:
                    单人原因 = f"检测到{self.无法进行组队FILE}"
                if self.组队模式 and not 组队时间内:
                    单人原因 = f"不在组队时间[{startclock},{self.限时组队时间}]内"
                if not self.组队模式 and 可以组队:
                    组队原因 = "进入组队模式"
                    self.组队模式 = True
                if len(单人原因) > 1:
                    TimeECHO(f"关闭组队功能:{单人原因}")
                if len(组队原因) > 1:
                    TimeECHO(f"{组队原因}")
                #
                if 可以组队:
                    self.组队模式 = True
                    self.totalnode = self.totalnode_bak
                    self.Tool.totalnode = self.totalnode
                else:
                    self.组队模式 = False
                    self.totalnode = 1
                    self.Tool.totalnode = 1
                    # 避免时间差导致的时间判断失误
                    self.Tool.touchfile(self.无法进行组队FILE, content=单人原因+组队原因)
            # ------------------------------------------------------------------------------
            # 运行前统一变量
            self.组队模式 = self.totalnode > 1
            if self.组队模式:
                self.runstep = self.Tool.bcastvar(self.mynode, self.totalnode, var=self.runstep, name="runstep")
                self.jinristep = self.Tool.bcastvar(self.mynode, self.totalnode, var=self.jinristep, name="jinristep")
                # 广播一些变量，这样就不用在每个文件中都写初始化参数了
                self.限时组队时间 = self.Tool.bcastvar(self.mynode, self.totalnode, var=self.限时组队时间, name="限时组队时间")
                #
                TimeECHO("组队模式")
            self.房主 = self.mynode == 0 or self.totalnode == 1
            TimeECHO(f"运行次数{self.runstep}|今日步数{self.jinristep}")
            #
            self.Tool.barriernode(self.mynode, self.totalnode, "准备进入战斗循环")
            #
            if self.Tool.存在同步文件():
                TimeECHO("准备进入战斗循环中遇到同步文件返回")
                continue
            # ------------------------------------------------------------------------------
            # 确保程序没有闪退
            if not self.APPOB.前台APP(2):
                content = "无法打开游戏, 可能闪退"
                self.创建同步文件(content)
                continue
            # ------------------------------------------------------------------------------
            # 计算参数设置
            self.runstep = self.runstep+1
            self.jinristep = self.jinristep+1
            if "5v5匹配" == self.对战模式:
                self.青铜段位 = os.path.exists(self.青铜段位FILE)
                self.标准模式 = os.path.exists(self.标准模式FILE)
                self.触摸对战 = os.path.exists(self.触摸对战FILE)
                if self.组队模式 and not self.青铜段位:
                    TimeECHO(f"组队时采用青铜段位")
                    self.青铜段位 = True
                # 希望在青铜局时进行触摸对战,而不是占据星耀刷熟练度的机会
                if not self.青铜段位:
                    if self.触摸对战:
                        TimeECHO(f"非青铜局不模拟人手触摸")
                        self.触摸对战 = False
            if "5v5排位" == self.对战模式:
                self.触摸对战 = os.path.exists(self.触摸对战FILE)
                if self.触摸对战:
                    TimeECHO(f"这是5v5排位, 小心你的信誉分啊喂")
                    TimeECHO(f"5v5的游戏被你完成4v5了, 会被系统检测到的")
            # ------------------------------------------------------------------------------
            # 若希望进行自动调整分路和设置触摸对战等参数，可以将相关指令添加到"self.对战前插入FILE",
            run_class_command(self=self, command=self.Tool.readfile(self.对战前插入FILE))
            # ------------------------------------------------------------------------------
            # 此处开始记录本步的计算参数，此参数目前的功能只用于判断前后两步的计算参数差异
            # 后续程序的控制，仍采用 self.触摸对战等参数
            self.构建循环参数(self.本循环参数)
            # 这里判断和之前的对战是否相同,不同则直接则进行大厅后重新开始
            self.本循环参数.printinfo()
            if not self.本循环参数.compare(self.上循环参数):
                TimeECHO(f"上步计算参数不同,回到大厅重新初始化")
                self.图片 = wzry_figure(Tool=self.Tool)
                self.进入大厅()
            # ------------------------------------------------------------------------------
            # 开始辅助同步,然后开始游戏
            self.当前状态 = "对战状态"
            self.进行人机匹配对战循环()
            # ------------------------------------------------------------------------------
            # 如果计算过程中对参数进行了更改，这里可以记录最新的参数
            self.构建循环参数(self.上循环参数)
            # ------------------------------------------------------------------------------
            if not self.check_run_status():
                TimeECHO("战斗结束,check_run_status失败,返回")
                continue
            # 礼包
            if self.runstep % 5 == 4:
                self.当前状态 = "领取礼包"
                self.每日礼包()
            #
            if self.移动端.实体终端 and self.Tool.timelimit("休息手机", limit=60*60, init=False):
                TimeECHO(":实体终端,休息设备")
                # self.APPOB.关闭APP()
                sleep(60*2)


if __name__ == "__main__":
    config_file = ""
    if len(sys.argv) > 1:
        config_file = str(sys.argv[1])
    # 如果使用AirTestIDE运行此脚本，在此处指定config_file=config文件
    # task_manager = TaskManager(config_file, None, None)
    task_manager = TaskManager(config_file, wzry_task, 'RUN')
    try:
        task_manager.execute()
    except KeyboardInterrupt:
        logger.info("Caught KeyboardInterrupt, terminating processes.")
    finally:
        # 这条命令用于调试寻找错误原因
        traceback.print_exc()
        # 这里可以放置清理代码
        logger.info("Cleaning up and exiting.")
        # sys.exit()  # 确保程序退出
    # 后面不能再跟其他指令，特别是exit()
    # 后面的命令会与task_manager.execute()中的多进程同时执行

# sleep(50)
