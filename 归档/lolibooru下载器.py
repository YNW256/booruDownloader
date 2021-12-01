import requests
import re
import time
import urllib
import os
import urllib.request
import sys
import ssl

# 自定义区---------------------------------------------------------
# 请修改输出文件夹：
PATH='/Users/wangyining/Desktop/Picdownload'
# 每次访问的休息时间（秒）：
WAIT=3
#-----------------------------------------------------------------

# 图片保存---------------------------------------------------------
def save_img(img_url,file_name,file_path=PATH):
    try:
        if not os.path.exists(file_path):
            print ('文件夹',file_path,'不存在，重新建立')
            os.makedirs(file_path)
        file_suffix = os.path.splitext(img_url)[1]  # 获得图片后缀
        filename = '{}{}{}{}'.format(file_path,os.sep,file_name,file_suffix)  # 拼接图片名（包含路径）
        urllib.request.urlretrieve(img_url,filename=filename)  # 下载图片，并保存到文件夹中
    except IOError as e:
        print ('文件操作失败',e)
    except Exception as e:
        print ('错误 ：',e)
#-----------------------------------------------------------------

# 网络相关设置------------------------------------------------------
ssl._create_default_https_context = ssl._create_unverified_context # 关闭证书验证
headers = {
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36"
}
requests.DEFAULT_RETRIES = 5  # 增加重试连接次数
s = requests.session()
s.keep_alive = False  # 关闭多余连接
#-----------------------------------------------------------------

print('\n\033[1;31mlolibooru下载器v0.0.9\033[0m'+' by Youngwang')

print('\n当前下载文件夹路径：'+PATH)
print('当前访问休息时间：'+str(WAIT)+'秒')

# 索取tag-----------------------------------------------------------
tag = []
print('\n请输入检索tag（最多4项），跳过请按回车')

for i in range(1,5):
    tagtemp = input("请输入tag"+str(i)+':')
    if tagtemp == '' :
        break
    tag = tag + [tagtemp]

if input('是否开启安全检索？（输入y/n）') == 'y':
    tag = tag + ['rating%3As']

print('确认tag为：'+str(tag))
tag = tag + [''] + [''] + [''] + [''] + [''] + ['']
page = 1
#-----------------------------------------------------------------

# 测试访问，获取最大页数---------------------------------------------
url='https://lolibooru.moe/post?seed=1382483636&tags='+str(tag[0])+'+'+str(tag[1])+'+'+str(tag[2])+'+'+str(tag[3])+'+'+str(tag[4])+'+'+str(tag[5])+'&page='+str(page)
print('\n正在尝试访问URL：'+str(url))

response = requests.get(url,headers=headers,timeout=300) # 解析网页（用于查询最大页数）
pagelist=re.findall(r'&page=(.+?)\">',response.text) # 检索最大页数

#if len(pagelist) == 0 :
    #pagelist=re.findall(r'desktop-only\" href=\"\/posts\?page\=(.+?)&',response.text) # 检索最大页数

if len(pagelist) == 0 :
    imglist=re.findall(r'\"id\"\:(.+?)\,\"tags',response.text) # 判断是否只有一页
    if len(imglist) == 0 :
        print('无搜索结果')
        sys.exit()
    else:
        print('搜索到1页')
        down='1'
        up='2'

else:
    pagelist=map(int,pagelist)
    maxpage=str(max(pagelist))
    print('共搜索到'+maxpage+'页')

    # 索取下载范围------------------------------------------------------
    down=input("\n请输入起始页：")
    up=input("请输入结束页：")
    up=str(int(up)+1)
    #-----------------------------------------------------------------
#-----------------------------------------------------------------

input("\n\033[5;31m按回车以开始下载\033[0m")

# 主要模块---------------------------------------------------------
for page in range(int(down),int(up)): # 循环，下载某页图片

    print('\n\033[1;31m第'+str(page)+'页\033[0m')

    # 访问某页-----------------------------------------------------
    url='https://lolibooru.moe/post?seed=1382483636&tags='+str(tag[0])+'+'+str(tag[1])+'+'+str(tag[2])+'+'+str(tag[3])+'+'+str(tag[4])+'+'+str(tag[5])+'&page='+str(page)
    print('\n正在访问第'+str(page)+'页URL：'+str(url))
    #-------------------------------------------------------------

    # 查找本页图片ID------------------------------------------------
    pagelist=[] # 建立图片ID列表
    response = requests.get(url,headers=headers,timeout=300) # 解析网页
    imglist=re.findall(r'\"id\"\:(.+?)\,\"tags',response.text) # 查找图片ID

    if len(imglist) == 0 : # 判断是否查找到ID
        print('无图片ID，结束')
        sys.exit() # 结束程序

    print('解析到图片ID：')
    print('\t'+str(imglist))
    #-------------------------------------------------------------

    print('图片ID解析结束，开始尝试访问图片页')
    time.sleep(WAIT) # 等待
    za = 0 #重置每页第n张计数器

    #访问某页------------------------------------------------------
    for x in imglist: # 循环，下载某张图片
        
        za=za+1 # 每页第n张计数器+1
        timestart = time.time() # 记录下载开始时间
        print('\n第'+str(page)+'页，第'+str(za)+'张')
        print('\t尝试下载图片，ID：'+x)

        # 访问某张图片----------------------------------------------
        url='https://lolibooru.moe/post/show/'+x
        print('\t开始解析图片页URL：'+str(url))
        response = requests.get(url,headers=headers,timeout=300)# 解析网页
        #---------------------------------------------------------

        # 查找并处理文件链接-----------------------------------------
        html=re.findall(r'highres\" href=\"(.+?)\">Download',response.text) #查找文件链接方法1
        if len(html) == 0:
            html=re.findall(r'highres\" href=\"(.+?)\">Image',response.text) #查找文件链接方法2
        if len(html) == 0:
            html=re.findall(r'highres\" href=\"(.+?)\">Video',response.text) #查找文件链接方法3

        if len(html) == 0: # 判断有无找到
            print('查找链接失败')
        img=str(html) # 意义不明的转存
        img=img.replace('[','') # 去除[号
        img=img.replace(']','') # 去除]号
        img=img.replace('\'','') # 去除\号
        img=img.replace('\"','') # 去除\号
        img=img.replace(' ','%20') # 替换空格
        print('\t发现文件链接：'+img) # 显示处理后的下载链接
        #---------------------------------------------------------

        # 下载链接文件----------------------------------------------
        print('\t下载中')
        save_img(img,x) # 保存图片
        #---------------------------------------------------------

        print('\t第'+str(za)+'张处理结束')
        timeend = time.time() # 记录下载结束时间
        timer = round(timeend - timestart,2) # 计算下载时间
        print('\t用时：'+str(timer)+'秒，下一张在'+str(WAIT)+'秒后开始') # 输出下载时间
        time.sleep(WAIT) # 等待
    
    page += 1 # 页面计数器+1

print('\n\033[1;31m结束\033[0m\n')




