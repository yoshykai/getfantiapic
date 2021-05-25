from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import chromedriver_binary
import time
from bs4 import BeautifulSoup
import urllib.request

beforestr = ""
countnum=0

def login(driver):
	mail = "youremail@example.com"
	password = "your_password"
	driver.get('https://fantia.jp/sessions/signin/')
	ele = driver.find_element_by_id("user_email")
	ele.send_keys(mail)
	ele = driver.find_element_by_id("user_password")
	ele.send_keys(password)
	time.sleep(1)
	ele.submit()

def timecomp(a,b):
	aa=a.split("-")
	bb=b.split("-")
	for i in range(3):
		an=(int)(aa[i])
		bn=(int)(bb[i])
		if an>bn:
			return 0
		elif an<bn:
			return 1
	return 0

def findclassname(driver,str):
	return driver.find_elements_by_class_name(str)

def savefile(url,sourse):
	with urllib.request.urlopen(url) as web_file:
		data = web_file.read()
		with open(sourse, mode='wb') as local_file:
			local_file.write(data)


def info(driver,str1,str2,timee,btimee):
	global beforestr
	global countnum

	driver.get(str1)
	str3=""

	#投稿時間取得
	l=0
	names=[]
	while l<3:
		time.sleep(5)
		names = findclassname(driver,"post-date.text-muted")
		l=len(names)
	ttime = names[l//2].get_attribute("textContent")[:10].replace('/','-')

	l = timecomp(timee,ttime)
	if l==0:
		return 0
	l = timecomp(ttime,btimee)
	if l==0:
		return 1

	if beforestr==ttime:
		countnum+=1
	else:
		beforestr = ttime
		countnum=0
	if countnum>0:
		str3=str(countnum)+"-"
	ttime = ttime+"-"

	driver.execute_script("window.scrollTo(0, 1100);")
	time.sleep(1)

	#画像を大きく表示する
	btns = driver.find_elements_by_css_selector(".btn.btn-default.btn-md")
	l=len(btns)
	i=4
	while i<l:
		btns[i].click()
		i+=2

	#動画DLのリンク取得
	btnss = driver.find_elements_by_css_selector(".btn.btn-success.btn-very-lg")
	btns = [i.get_attribute("href") for i in btnss]
	names = findclassname(driver,"text-center.text-muted.ng-binding")
	mname = [i.get_attribute("textContent") for i in names]

	#画像取得
	urls = driver.find_elements_by_tag_name("img")
	url = [i.get_attribute("src") for i in urls]
	n=1
	for i in url:
		if i[0:10]=="https://cc":
			savefile(i,'picture/'+str2+ttime+str3+str(n)+'.png')
			# urllib.request.urlretrieve(url, str2+ttime+str(n)+'.png')
			n += 1
	#動画DL
	i=0
	for btn in btns:
		print(ttime,mname[i])
		driver.get(btn)
		i+=1
	return 1

now = "2021-03-31" #何日までさかのぼるか(その日は含まない)
before = "2021-04-31" #何日から取得するか(その日は含まない)
URL1,URL2 = 'https://fantia.jp/fanclubs/','/posts?q[s]=newer'
URL3,name = 'test','tetstt'
URL = URL1+URL3+URL2

"""options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome(chrome_options=options)"""

# ログイン
driver = webdriver.Chrome()
login(driver)
time.sleep(2)
loopFlg = True
j=1
while loopFlg:
	driver.get(URL+"&page="+str(j))
	time.sleep(5)
	hrefs = driver.find_elements_by_class_name("link-block")
	href = [i.get_attribute("href") for i in hrefs]

	for i in href:
		if i[18] == "p":
			print(i)
			z = info(driver,i,name,now,before)
			if z==0:
				loopFlg = False
				break
		time.sleep(5)
	j+=1

print("fin")
input()
driver.close()
driver.quit()
