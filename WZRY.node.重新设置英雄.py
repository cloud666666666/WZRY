#tmp_参战英雄线路=Template(r"tpl1689665490071.png", record_pos=(-0.315, -0.257), resolution=(960, 540)) #对抗路
#tmp_参战英雄线路=Template(r"tpl1689665455905.png", record_pos=(-0.066, -0.256), resolution=(960, 540)) #中路
#tmp_参战英雄线路=Template(r"tpl1689665540773.png", record_pos=(0.06, -0.259), resolution=(960, 540))   #发育路
#tmp_参战英雄线路=Template(r"tpl1689665577871.png", record_pos=(0.183, -0.26), resolution=(960, 540))   #游走
#tmp_参战英雄线路=Template(r"tpl1686048521443.png", record_pos=(0.06, -0.259), resolution=(960, 540))   #打野


#多个英雄参与的活动
myrandom=random.randint(1, 2)
#kai
if myrandom==1: tmp_参战英雄线路=Template(r"tpl1689665490071.png", record_pos=(-0.315, -0.257), resolution=(960, 540))
if myrandom==1: tmp_参战英雄头像=Template(r"tpl1689665521942.png", record_pos=(0.108, -0.086), resolution=(960, 540))
#jia
if myrandom==2: tmp_参战英雄线路=Template(r"tpl1689665540773.png", record_pos=(0.06, -0.259), resolution=(960, 540))
if myrandom==2: tmp_参战英雄头像=Template(r"tpl1706323221604.png", record_pos=(0.015, -0.189), resolution=(960, 540))


savepos=False #是否更新原始字典文件
tag="tmp"
if savepos: tag=""
if tag+"参战英雄线路" in self.Tool.var_dict.keys(): del self.Tool.var_dict[tag+"参战英雄线路"]
if tag+"参战英雄头像" in self.Tool.var_dict.keys(): del self.Tool.var_dict[tag+"参战英雄头像"]
#
#
self.Tool.existsTHENtouch(tmp_参战英雄线路,tag+"参战英雄线路",savepos=savepos)
if not self.Tool.existsTHENtouch(tmp_参战英雄头像,tag+"参战英雄头像",savepos=savepos): sleep(2)
if not self.Tool.existsTHENtouch(tmp_参战英雄头像,tag+"参战英雄头像",savepos=savepos): sleep(2)
if not self.Tool.existsTHENtouch(tmp_参战英雄头像,tag+"参战英雄头像",savepos=savepos): sleep(2)
sleep(1)
#self.Tool.removefile(self.重新设置英雄FILE)
