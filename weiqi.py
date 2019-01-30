#!/usr/bin/python3
# 41623216-傅聪-面向对象程序设计2大作业-围棋游戏
# 使用Python内置GUI模块tkinter
from tkinter import *
# ttk覆盖tkinter部分对象，ttk对tkinter进行了优化
from tkinter.ttk import *
# 深拷贝时需要用到copy模块
import copy
import tkinter.messagebox
# 围棋应用对象定义
class Application(Tk):
	# 初始化棋盘,默认九路棋盘
	def __init__(self,my_mode_num=9):
		Tk.__init__(self)
		# 模式，九路棋：9，十三路棋：13，十九路棋：19
		self.mode_num=my_mode_num
		# 窗口尺寸设置，默认：1.8
		self.size=1.8
		# 棋盘每格的边长
		self.dd=360*self.size/(self.mode_num-1)
		# 相对九路棋盘的矫正比例
		self.p=1 if self.mode_num==9 else (2/3 if self.mode_num==13 else 4/9)
		# 定义棋盘阵列,超过边界：-1，无子：0，黑棋：1，白棋：2
		self.positions=[[0 for i in range(self.mode_num+2)] for i in range(self.mode_num+2)]
		# 初始化棋盘，所有超过边界的值置-1
		for m in range(self.mode_num+2):
			for n in range(self.mode_num+2):
				if (m*n==0 or m==self.mode_num+1 or n==self.mode_num+1):
					self.positions[m][n]=-1
		# 拷贝三份棋盘“快照”，悔棋和判断“打劫”时需要作参考
		self.last_3_positions=copy.deepcopy(self.positions)
		self.last_2_positions=copy.deepcopy(self.positions)
		self.last_1_positions=copy.deepcopy(self.positions)
		# 记录鼠标经过的地方，用于显示shadow时
		self.cross_last=None
		# 当前轮到的玩家，黑：0，白：1，执黑先行
		self.present=0 
		# 初始停止运行，点击“开始游戏”运行游戏
		self.stop=True
		# 悔棋次数，次数大于0才可悔棋，初始置0（初始不能悔棋），悔棋后置0，下棋或弃手时恢复为1，以禁止连续悔棋
		self.regretchance=0
		# 图片资源，存放在当前目录下的/Pictures/中
		self.photoW=PhotoImage(file = "./Pictures/W.png")
		self.photoB=PhotoImage(file = "./Pictures/B.png")
		self.photoBD=PhotoImage(file = "./Pictures/"+"BD"+"-"+str(self.mode_num)+".png")
		self.photoWD=PhotoImage(file = "./Pictures/"+"WD"+"-"+str(self.mode_num)+".png")
		self.photoBU=PhotoImage(file = "./Pictures/"+"BU"+"-"+str(self.mode_num)+".png")
		self.photoWU=PhotoImage(file = "./Pictures/"+"WU"+"-"+str(self.mode_num)+".png")
		# 用于黑白棋子图片切换的列表
		self.photoWBU_list=[self.photoBU,self.photoWU]
		self.photoWBD_list=[self.photoBD,self.photoWD]
		# 窗口大小
		self.geometry(str(int(600*self.size))+'x'+str(int(400*self.size)))
		# 画布控件，作为容器
		self.canvas_bottom=Canvas(self,bg='#369',bd=0,width=600*self.size,height=400*self.size)
		self.canvas_bottom.place(x=0,y=0)
		# 几个功能按钮
		self.startButton=Button(self,text='开始游戏',command=self.start)
		self.startButton.place(x=480*self.size,y=200*self.size)
		self.passmeButton=Button(self,text='弃一手',command=self.passme)
		self.passmeButton.place(x=480*self.size,y=225*self.size)	
		self.regretButton=Button(self,text='悔棋',command=self.regret)
		self.regretButton.place(x=480*self.size,y=250*self.size)
		# 初始悔棋按钮禁用
		self.regretButton['state']=DISABLED
		self.replayButton=Button(self,text='重新开始',command=self.reload)
		self.replayButton.place(x=480*self.size,y=275*self.size)
		self.newGameButton1=Button(self,text=('十三' if self.mode_num==9 else '九')+'路棋',command=self.newGame1)
		self.newGameButton1.place(x=480*self.size,y=300*self.size)
		self.newGameButton2=Button(self,text=('十三' if self.mode_num==19 else '十九')+'路棋',command=self.newGame2)
		self.newGameButton2.place(x=480*self.size,y=325*self.size)
		self.quitButton=Button(self,text='退出游戏',command=self.quit)
		self.quitButton.place(x=480*self.size,y=350*self.size)
		# 画棋盘，填充颜色
		self.canvas_bottom.create_rectangle(0*self.size,0*self.size,400*self.size,400*self.size,fill='#c51')
		# 刻画棋盘线及九个点
		# 先画外框粗线
		self.canvas_bottom.create_rectangle(20*self.size,20*self.size,380*self.size,380*self.size,width=3)
		# 棋盘上的九个定位点，以中点为模型，移动位置，以作出其余八个点
		for m in [-1,0,1]:
			for n in [-1,0,1]:
				self.oringinal=self.canvas_bottom.create_oval(200*self.size-self.size*2,200*self.size-self.size*2,
				200*self.size+self.size*2,200*self.size+self.size*2,fill='#000')
				self.canvas_bottom.move(self.oringinal,m*self.dd*(2 if self.mode_num==9 else (3 if self.mode_num==13 else 6)),
				n*self.dd*(2 if self.mode_num==9 else (3 if self.mode_num==13 else 6)))
		# 画中间的线条
		for i in range(1,self.mode_num-1):
			self.canvas_bottom.create_line(20*self.size,20*self.size+i*self.dd,380*self.size,20*self.size+i*self.dd,width=2)
			self.canvas_bottom.create_line(20*self.size+i*self.dd,20*self.size,20*self.size+i*self.dd,380*self.size,width=2)
		# 放置右侧初始图片
		self.pW=self.canvas_bottom.create_image(500*self.size+11, 65*self.size,image=self.photoW)
		self.pB=self.canvas_bottom.create_image(500*self.size-11, 65*self.size,image=self.photoB)
		# 每张图片都添加image标签，方便reload函数删除图片
		self.canvas_bottom.addtag_withtag('image',self.pW)
		self.canvas_bottom.addtag_withtag('image',self.pB)
		# 鼠标移动时，调用shadow函数，显示随鼠标移动的棋子
		self.canvas_bottom.bind('<Motion>',self.shadow)
		# 鼠标左键单击时，调用getdown函数，放下棋子
		self.canvas_bottom.bind('<Button-1>',self.getDown)
		# 设置退出快捷键<Ctrl>+<D>，快速退出游戏
		self.bind('<Control-KeyPress-d>',self.keyboardQuit)
	# 开始游戏函数，点击“开始游戏”时调用
	def start(self):
		# 删除右侧太极图
		self.canvas_bottom.delete(self.pW)
		self.canvas_bottom.delete(self.pB)
		# 利用右侧图案提示开始时谁先落子
		if self.present==0:
			self.create_pB()
			self.del_pW()
		else:
			self.create_pW()
			self.del_pB()
		# 开始标志，解除stop
		self.stop=None
	# 放弃一手函数，跳过落子环节
	def passme(self):
		# 悔棋恢复
		if not self.regretchance==1:
			self.regretchance+=1
		else:
			self.regretButton['state']=NORMAL
		# 拷贝棋盘状态，记录前三次棋局
		self.last_3_positions=copy.deepcopy(self.last_2_positions)
		self.last_2_positions=copy.deepcopy(self.last_1_positions)
		self.last_1_positions=copy.deepcopy(self.positions)
		self.canvas_bottom.delete('image_added_sign')
		# 轮到下一玩家
		if self.present==0:
			self.create_pW()
			self.del_pB()
			self.present=1
		else:
			self.create_pB()
			self.del_pW()
			self.present=0
	# 悔棋函数，可悔棋一回合，下两回合不可悔棋
	def regret(self):
		# 判定是否可以悔棋，以前第三盘棋局复原棋盘
		if self.regretchance==1:
			self.regretchance=0
			self.regretButton['state']=DISABLED
			list_of_b=[]
			list_of_w=[]
			self.canvas_bottom.delete('image')
			if self.present==0:
				self.create_pB()
			else:
				self.create_pW()
			for m in range(1,self.mode_num+1):
				for n in range(1,self.mode_num+1):
					self.positions[m][n]=0
			for m in range(len(self.last_3_positions)):
				for n in range(len(self.last_3_positions[m])):
					if self.last_3_positions[m][n]==1:
						list_of_b+=[[n,m]]
					elif self.last_3_positions[m][n]==2:
						list_of_w+=[[n,m]]
			self.recover(list_of_b,0)
			self.recover(list_of_w,1)
			self.last_1_positions=copy.deepcopy(self.last_3_positions)
			for m in range(1,self.mode_num+1):
				for n in range(1,self.mode_num+1):
					self.last_2_positions[m][n]=0
					self.last_3_positions[m][n]=0
	# 重新加载函数,删除图片，序列归零，设置一些初始参数，点击“重新开始”时调用
	def reload(self):
		if self.stop==1:
			self.stop=0
		self.canvas_bottom.delete('image')
		self.regretchance=0
		self.present=0
		self.create_pB()
		for m in range(1,self.mode_num+1):
			for n in range(1,self.mode_num+1):
				self.positions[m][n]=0
				self.last_3_positions[m][n]=0
				self.last_2_positions[m][n]=0
				self.last_1_positions[m][n]=0
	# 以下四个函数实现了右侧太极图的动态创建与删除
	def create_pW(self):
		self.pW=self.canvas_bottom.create_image(500*self.size+11, 65*self.size,image=self.photoW)
		self.canvas_bottom.addtag_withtag('image',self.pW)
	def create_pB(self):
		self.pB=self.canvas_bottom.create_image(500*self.size-11, 65*self.size,image=self.photoB)
		self.canvas_bottom.addtag_withtag('image',self.pB)
	def del_pW(self):
		self.canvas_bottom.delete(self.pW)
	def del_pB(self):
		self.canvas_bottom.delete(self.pB)
	# 显示鼠标移动下棋子的移动
	def shadow(self,event):
		if not self.stop:
			# 找到最近格点，在当前位置靠近的格点出显示棋子图片，并删除上一位置的棋子图片
			if (20*self.size<event.x<380*self.size) and (20*self.size<event.y<380*self.size):
				dx=(event.x-20*self.size)%self.dd
				dy=(event.y-20*self.size)%self.dd
				self.cross=self.canvas_bottom.create_image(event.x-dx+round(dx/self.dd)*self.dd+22*self.p, event.y-dy+round(dy/self.dd)*self.dd-27*self.p,image=self.photoWBU_list[self.present])
				self.canvas_bottom.addtag_withtag('image',self.cross)
				if self.cross_last!=None:
					self.canvas_bottom.delete(self.cross_last)
				self.cross_last=self.cross
	# 落子，并驱动玩家的轮流下棋行为
	def getDown(self,event):
		if not self.stop:
			# 先找到最近格点
			if (20*self.size-self.dd*0.4<event.x<self.dd*0.4+380*self.size) and (20*self.size-self.dd*0.4<event.y<self.dd*0.4+380*self.size):
				dx=(event.x-20*self.size)%self.dd
				dy=(event.y-20*self.size)%self.dd
				x=int((event.x-20*self.size-dx)/self.dd+round(dx/self.dd)+1)
				y=int((event.y-20*self.size-dy)/self.dd+round(dy/self.dd)+1)
				# 判断位置是否已经被占据
				if self.positions[y][x]==0:
					# 未被占据，则尝试占据，获得占据后能杀死的棋子列表
					self.positions[y][x]=self.present+1
					self.image_added=self.canvas_bottom.create_image(event.x-dx+round(dx/self.dd)*self.dd+4*self.p, event.y-dy+round(dy/self.dd)*self.dd-5*self.p,image=self.photoWBD_list[self.present])
					self.canvas_bottom.addtag_withtag('image',self.image_added)
					# 棋子与位置标签绑定，方便“杀死”
					self.canvas_bottom.addtag_withtag('position'+str(x)+str(y),self.image_added)
					deadlist=self.get_deadlist(x,y)
					self.kill(deadlist)
					# 判断是否重复棋局
					if not self.last_2_positions==self.positions:
						# 判断是否属于有气和杀死对方其中之一
						if len(deadlist)>0 or self.if_dead([[x,y]],self.present+1,[x,y])==False:
							# 当不重复棋局，且属于有气和杀死对方其中之一时，落下棋子有效
							if not self.regretchance==1:
								self.regretchance+=1
							else:
								self.regretButton['state']=NORMAL
							self.last_3_positions=copy.deepcopy(self.last_2_positions)
							self.last_2_positions=copy.deepcopy(self.last_1_positions)
							self.last_1_positions=copy.deepcopy(self.positions)
							# 删除上次的标记，重新创建标记
							self.canvas_bottom.delete('image_added_sign')
							self.image_added_sign=self.canvas_bottom.create_oval(event.x-dx+round(dx/self.dd)*self.dd+0.5*self.dd, event.y-dy+round(dy/self.dd)*self.dd+0.5*self.dd,event.x-dx+round(dx/self.dd)*self.dd-0.5*self.dd, event.y-dy+round(dy/self.dd)*self.dd-0.5*self.dd,width=3,outline='#3ae')
							self.canvas_bottom.addtag_withtag('image',self.image_added_sign)
							self.canvas_bottom.addtag_withtag('image_added_sign',self.image_added_sign)
							if self.present==0:
								self.create_pW()
								self.del_pB()
								self.present=1
							else:
								self.create_pB()
								self.del_pW()
								self.present=0
						else:
							# 不属于杀死对方或有气，则判断为无气，警告并弹出警告框
							self.positions[y][x]=0
							self.canvas_bottom.delete('position'+str(x)+str(y))
							self.bell()
							self.showwarningbox('无气',"你被包围了！")
					else:
						# 重复棋局，警告打劫
						self.positions[y][x]=0
						self.canvas_bottom.delete('position'+str(x)+str(y))
						self.recover(deadlist,(1 if self.present==0 else 0))
						self.bell()
						self.showwarningbox("打劫","此路不通！")
				else:
					# 覆盖，声音警告
					self.bell()
			else:
				# 超出边界，声音警告
				self.bell()
	# 判断棋子（种类为yourChessman，位置为yourPosition）是否无气（死亡），有气则返回False，无气则返回无气棋子的列表
	# 本函数是游戏规则的关键，初始deadlist只包含了自己的位置，每次执行时，函数尝试寻找yourPosition周围有没有空的位置，有则结束，返回False代表有气；
	# 若找不到，则找自己四周的同类（不在deadlist中的）是否有气，即调用本函数，无气，则把该同类加入到deadlist，然后找下一个邻居，只要有一个有气，返回False代表有气；
	# 若四周没有一个有气的同类，返回deadlist,至此结束递归
	# def if_dead(self,deadlist,yourChessman,yourPosition):

	def if_dead(self,deadList,yourChessman,yourPosition):
		for i in [-1,1]:
			if [yourPosition[0]+i,yourPosition[1]] not in deadList:
				if self.positions[yourPosition[1]][yourPosition[0]+i]==0:
					return False
			if [yourPosition[0],yourPosition[1]+i] not in deadList:
				if self.positions[yourPosition[1]+i][yourPosition[0]]==0:
					return False
		if ([yourPosition[0]+1,yourPosition[1]] not in deadList) and (self.positions[yourPosition[1]][yourPosition[0]+1]==yourChessman):
			midvar=self.if_dead(deadList+[[yourPosition[0]+1,yourPosition[1]]],yourChessman,[yourPosition[0]+1,yourPosition[1]])
			if not midvar:
				return False
			else:
				deadList+=copy.deepcopy(midvar)
		if ([yourPosition[0]-1,yourPosition[1]] not in deadList) and (self.positions[yourPosition[1]][yourPosition[0]-1]==yourChessman):
			midvar=self.if_dead(deadList+[[yourPosition[0]-1,yourPosition[1]]],yourChessman,[yourPosition[0]-1,yourPosition[1]])
			if not midvar:
				return False
			else:
				deadList+=copy.deepcopy(midvar)
		if ([yourPosition[0],yourPosition[1]+1] not in deadList) and (self.positions[yourPosition[1]+1][yourPosition[0]]==yourChessman):
			midvar=self.if_dead(deadList+[[yourPosition[0],yourPosition[1]+1]],yourChessman,[yourPosition[0],yourPosition[1]+1])
			if not midvar:
				return False
			else:
				deadList+=copy.deepcopy(midvar)
		if ([yourPosition[0],yourPosition[1]-1] not in deadList) and (self.positions[yourPosition[1]-1][yourPosition[0]]==yourChessman):
			midvar=self.if_dead(deadList+[[yourPosition[0],yourPosition[1]-1]],yourChessman,[yourPosition[0],yourPosition[1]-1])
			if not midvar:
				return False
			else:
				deadList+=copy.deepcopy(midvar)
		return deadList	
	# 警告消息框，接受标题和警告信息			
	def showwarningbox(self,title,message):
		self.canvas_bottom.delete(self.cross)
		tkinter.messagebox.showwarning(title,message)
	# 落子后，依次判断四周是否有棋子被杀死，并返回死棋位置列表
	def get_deadlist(self,x,y):
		deadlist=[]
		for i in [-1,1]:
			if self.positions[y][x+i]==(2 if self.present==0 else 1) and ([x+i,y] not in deadlist):
				killList=self.if_dead([[x+i,y]],(2 if self.present==0 else 1),[x+i,y])
				if not killList==False:
					deadlist+=copy.deepcopy(killList)
			if self.positions[y+i][x]==(2 if self.present==0 else 1) and ([x,y+i] not in deadlist):		
				killList=self.if_dead([[x,y+i]],(2 if self.present==0 else 1),[x,y+i])
				if not killList==False:
					deadlist+=copy.deepcopy(killList)
		return deadlist
	# 恢复位置列表list_to_recover为b_or_w指定的棋子
	def recover(self,list_to_recover,b_or_w):
		if len(list_to_recover)>0:
			for i in range(len(list_to_recover)):
				self.positions[list_to_recover[i][1]][list_to_recover[i][0]]=b_or_w+1
				self.image_added=self.canvas_bottom.create_image(20*self.size+(list_to_recover[i][0]-1)*self.dd+4*self.p, 20*self.size+(list_to_recover[i][1]-1)*self.dd-5*self.p,image=self.photoWBD_list[b_or_w])
				self.canvas_bottom.addtag_withtag('image',self.image_added)
				self.canvas_bottom.addtag_withtag('position'+str(list_to_recover[i][0])+str(list_to_recover[i][1]),self.image_added)
	# 杀死位置列表killList中的棋子，即删除图片，位置值置0
	def kill(self,killList):
		if len(killList)>0:
			for i in range(len(killList)):
				self.positions[killList[i][1]][killList[i][0]]=0
				self.canvas_bottom.delete('position'+str(killList[i][0])+str(killList[i][1]))
	# 键盘快捷键退出游戏
	def keyboardQuit(self,event):
		self.quit()
	# 以下两个函数修改全局变量值，newApp使主函数循环，以建立不同参数的对象
	def newGame1(self):
		global mode_num,newApp
		mode_num=(13 if self.mode_num==9 else 9)
		newApp=True
		self.quit()
	def newGame2(self):
		global mode_num,newApp
		mode_num=(13 if self.mode_num==19 else 19)
		newApp=True
		self.quit()

# 声明全局变量，用于新建Application对象时切换成不同模式的游戏
global mode_num,newApp
mode_num=9
newApp=False	
if __name__=='__main__':
	# 循环，直到不切换游戏模式
	while True:
		newApp=False
		app=Application(mode_num)
		app.title('围棋')
		app.mainloop()
		if newApp:
			app.destroy()
		else:
			break