import requests
import re
import time
import urllib
import os
import urllib.request
import sys
import ssl

version='1.0'

# 自定义区---------------------------------------------------------
# 检索保存文件夹路径：
ROOT_PATH = os.path.abspath(os.path.dirname(__file__))
PATH = ROOT_PATH+'/Pic/'
if not os.path.exists(PATH):
    os.mkdir(PATH)
# 每次访问的休息时间（秒）：
WAIT = 3
#-----------------------------------------------------------------

# 网络相关设置------------------------------------------------------
headers = {
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36"
}
ssl._create_default_https_context = ssl._create_unverified_context # 关闭证书验证
requests.DEFAULT_RETRIES = 5  # 增加重试连接次数
#-----------------------------------------------------------------

# 初始化变量-------------------------------------------------------
modlist = [1,2,3]
modlisttext = ['danbooru'] + ['yande'] + ['lolibooru']
number = 0 # 通用计数器
page = 1 # 页数计数器
tag = []
pagelist = []
down = '1'
up = '1'
pic_id = '314198'
#-----------------------------------------------------------------


# 函数区··························································

# 图片保存---------------------------------------------------------
def save_img(img_url,file_name):
    try:
        file_suffix = os.path.splitext(img_url)[1]  # 获得图片后缀
        filename = '{}{}{}{}'.format(PATH,os.sep,file_name,file_suffix)  # 拼接图片名（包含路径）
        urllib.request.urlretrieve(img_url,filename=filename)  # 下载图片，并保存到文件夹中
    except IOError as e:
        print ('文件操作失败',e)
    except Exception as e:
        print ('错误 ：',e)
#-----------------------------------------------------------------

# 向用户请求tag----------------------------------------------------
def tag_get(tag):
    fun = str(site + '_tag') # 合成函数名
    tag = globals()[fun](tag) # 请求tag
    if input('\n\033[4m是否开启安全检索？（输入y/n）\033[0m：') == 'y':
        tag = tag + ['rating%3As']
    print('确认tag为：'+str(tag))
    tag = tag + [''] + [''] + [''] + [''] + [''] + [''] + ['']
    return(tag)
#-----------------------------------------------------------------

# 合成URL----------------------------------------------------------
def url_make(page,mode):
    if site_number == 1:
        if mode == 1:
            url = 'https://danbooru.donmai.us/posts?page='+str(page)+'&tags='+str(tag[0])+'+'+str(tag[1])+'+'+str(tag[2])+'+'
        elif mode == 2:
            url='https://danbooru.donmai.us/posts/'+pic_id

    elif site_number == 2:
        if mode == 1:
            url = 'https://yande.re/post?&tags='+str(tag[0])+'+'+str(tag[1])+'+'+str(tag[2])+'+'+str(tag[3])+'+'+str(tag[4])+'+'+str(tag[5])+'&page='+str(page)
        elif mode == 2:
            url='https://yande.re/post/show/'+pic_id

    elif site_number == 3:
        if mode == 1:
            url = 'https://lolibooru.moe/post?&tags='+str(tag[0])+'+'+str(tag[1])+'+'+str(tag[2])+'+'+str(tag[3])+'+'+str(tag[4])+'+'+str(tag[5])+'&page='+str(page)
        elif mode == 2:
            url='https://lolibooru.moe/post/show/'+pic_id
    return(url)
#-----------------------------------------------------------------

# 确认页面范围------------------------------------------------------
def page_check():
    global up
    global down
    global response
    url = url_make(1,1) # 合成第一页的URL
    print('\n正在尝试访问URL：'+str(url))
    try:
        response = requests.get(url, headers = headers, timeout = 300) # 解析网页（用于查询最大页数）
    except:
        print("\n\033[1;31m第一页访问错误！可能为网络故障\033[0m\n")
        sys.exit()
    fun = str(site + '_check') # 合成函数名
    pagelist = globals()[fun](response,0) # 获取页面数列表

    if len(pagelist) == 0 : # 判断是否只有一页
        fun = str(site + '_check') # 合成函数名
        imglist = globals()[fun](response,1) # 获取图片数列表
        if len(imglist) == 0 : # 如果没有图片
            print('\n无搜索结果\n')
            sys.exit()
        else:
            print('搜索到1页共'+str(len(imglist)) + '张图片')
            down = '1'
            up = '2'
    else: # 存在多页时询问用户
        pagelist = map(int,pagelist)
        maxpage = str(max(pagelist))
        print('共搜索到' + maxpage + '页')

        # 索取下载范围------------------------------------------------------
        down = input("\n请输入起始页：")
        up = input("请输入结束页：")
        if len(up) == 0:
            sys.exit()
        up = str(int(up) + 1)
        #-----------------------------------------------------------------
#-----------------------------------------------------------------

# 图片下载---------------------------------------------------------
def pic_download():
    fun = str(site + '_check')
    img = str(globals()[fun](response,2))
    if len(img) == 0: # 判断有无找到
        print('查找链接失败')
    else:
        img = URL_process(img) # 处理链接格式
        print('\t发现文件链接：' + img) # 显示处理后的下载链接
        print('\t下载中')
        save_img(img,pic_id) # 保存图片
#-----------------------------------------------------------------

# 下载链接文字处理--------------------------------------------------
def URL_process(img):
    img=img.replace('[','') # 去除[号
    img=img.replace(']','') # 去除]号
    img=img.replace('\'','') # 去除\号
    img=img.replace('\"','') # 去除\号
    img=img.replace(' ','%20') # 替换空格
    return(img)
#-----------------------------------------------------------------

# 请求tag(danbooru方法)--------------------------------------------
def danbooru_tag(tag):
    print('\n请输入检索tag（最多2项），跳过请按回车')
    for i in range(1,3):
        tagtemp = input('\033[4m请输入tag'+str(i)+'\033[0m:')
        if tagtemp == '' :
            break
        tag = tag + [tagtemp]
    return(tag)
#-----------------------------------------------------------------

# 请求tag(yande方法)-----------------------------------------------
def yande_tag(tag):
    print('\n请输入检索tag（最多4项），跳过请按回车')
    for i in range(1,5):
        tagtemp = input('\033[4m请输入tag'+str(i)+'\033[0m:')
        if tagtemp == '' :
            break
        tag = tag + [tagtemp]
    return(tag)
#-----------------------------------------------------------------

# 请求tag(lolibooru方法)-------------------------------------------
def lolibooru_tag(tag):
    print('\n请输入检索tag（最多4项），跳过请按回车')
    for i in range(1,5):
        tagtemp = input('\033[4m请输入tag'+str(i)+'\033[0m:')
        if tagtemp == '' :
            break
        tag = tag + [tagtemp]
    return(tag)
#-----------------------------------------------------------------

# 页面解析(danbooru方法)--------------------------------------------
def danbooru_check(response,mode):
    if mode == 0:
        pagelist=re.findall(r'hidden\" href\=\"\/posts\?page=(.+?)&',response.text) # 检索最大页数
        if len(pagelist) == 0 :
            pagelist=re.findall(r'desktop-only\" href=\"\/posts\?page\=(.+?)&',response.text) # 检索最大页数
        return(pagelist)
    elif mode == 1:
        imglist=re.findall(r'alt=\"post \#(.+?)\"',response.text) # 查找图片ID
        return(imglist)
    elif mode == 2:
        html=re.findall(r'href=\"(.+?)\?download',response.text) # 查找文件链接（danbooru方法）
        return(html)
#-----------------------------------------------------------------

# 页面解析(yande方法)-----------------------------------------------
def yande_check(response,mode):
    if mode == 0:
        pagelist=re.findall(r'\"Page (.+?)\"',response.text) # 检索最大页数
        return(pagelist)
    elif mode == 1:
        imglist=re.findall(r'\"id\"\:(.+?)\,\"tags',response.text) # 查找图片ID
        return(imglist)
    elif mode == 2:
        html=re.findall(r'highres\" href=\"(.+?)\">Download',response.text) #查找文件链接方法1
        if len(html) == 0:
            html=re.findall(r'highres\" href=\"(.+?)\">Image',response.text) #查找文件链接方法2
        if len(html) == 0:
            html=re.findall(r'highres\" href=\"(.+?)\">Video',response.text) #查找文件链接方法3 
        return(html)
#-----------------------------------------------------------------

# 页面解析(lolibooru方法)-------------------------------------------
def lolibooru_check(response,mode):
    if mode == 0:
        pagelist=re.findall(r'&page=(.+?)\">',response.text) # 检索最大页数
        return(pagelist)
    elif mode == 1:
        imglist=re.findall(r'\"id\"\:(.+?)\,\"tags',response.text) # 查找图片ID
        return(imglist)
    elif mode == 2:
        html=re.findall(r'highres\" href=\"(.+?)\">Download',response.text) #查找文件链接方法1
        if len(html) == 0:
            html=re.findall(r'highres\" href=\"(.+?)\">Image',response.text) #查找文件链接方法2
        if len(html) == 0:
            html=re.findall(r'highres\" href=\"(.+?)\">Video',response.text) #查找文件链接方法3 
        return(html)
#-----------------------------------------------------------------    

# 函数区结束·······················································

# 基础信息显示------------------------------------------------------
print('\n\033[1;31mdanbooru下载器' + version + '\033[0m' + ' by Youngwang')
#time.sleep(1)
print('\n当前下载文件夹路径：' + PATH)
print('当前访问休息时间：' + str(WAIT) + '秒')
#-----------------------------------------------------------------

# 向用户请求下载站点------------------------------------------------
print('\n目前已支持的下载站点：')

for p in modlist: # 逐个显示已支持的站点
    print('\033[1;31m站点' + str(p) + ':\033[0m ' + modlisttext[p-1])

try:
    site_number = int(input('\n\033[4m请输入需访问的站点数字\033[0m：\033[1;31m'))
except:
    print('\n输入有误，请重新启动程序\n')
    sys.exit ()
if site_number not in modlist:
    print('\n输入有误，请重新启动程序\n')
    sys.exit ()
else:
    site = str(modlisttext[site_number-1])
    print('\033[0m本次下载所选的站点：' + site)
#-----------------------------------------------------------------


tag = tag_get(tag)
page_check()
input("\n\033[5;31m按回车以开始下载\033[0m")

# 下载主程序--------------------------------------------------------
for page in range(int(down),int(up)): # 循环，下载某页图片
    print('\n\033[1;31m第'+str(page)+'页\033[0m')
    url = url_make(page,1)
    print('\n正在访问第'+str(page)+'页URL：'+str(url))

    try:
        response = requests.get(url,headers=headers,timeout=300) # 解析网页
        fun = str(site + '_check') # 合成函数名 
        imglist = globals()[fun](response,1) # 获取图片列表
    except:
            print("\n\033[1;31m引索页访问错误！\033[0m")

    if len(imglist) == 0 : # 判断是否查找到ID
        print('无图片ID，结束')
        sys.exit() # 结束程序

    print('解析到图片ID：')
    print(str(imglist))

    print('图片ID解析结束，开始尝试访问图片页')
    time.sleep(WAIT) # 等待
    za = 0 #重置每页第n张计数器

    for pic_id in imglist: # 循环，下载某个ID的图片

        za = za + 1 # 每页第n张计数器+1
        timestart = time.time() # 记录下载开始时间
        print('\n第'+str(page)+'页，第'+str(za)+'张')
        print('\t尝试下载图片，ID：'+pic_id)
        url = url_make(page,2) # 制作图片页URL

        try:
            response = requests.get(url, headers = headers, timeout = 300) # 解析网页
            pic_download()
        except:
            print("\n\033[1;31m下载错误！\033[0m")

        print('\t第' + str(za) + '张处理结束')
        timeend = time.time() # 记录下载结束时间
        timer = round(timeend - timestart, 2) # 计算下载时间
        print('\t用时：' + str(timer) + '秒，下一张在' + str(WAIT) + '秒后开始') # 输出下载时间
        time.sleep(WAIT) # 等待

    page += 1 # 页面计数器+1

print('\n\033[1;31m结束\033[0m\n')



















