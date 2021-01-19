import glob
from PIL import Image
 
import matplotlib.pyplot as plt
import matplotlib.animation as animation


#該当フォルダから画像のリストを取得。読み込みたいファイル形式を指定。ここではpng 
picList = glob.glob("*.png")
picList.sort()

fig = plt.figure(figsize=(20,20),dpi=100)

#空のリスト作成
ims = []
     
#画像ファイルを空のリストの中に1枚ずつ読み込み
for i in range(len(picList)):
         
    #読み込んで付け加えていく
    tmp = Image.open(picList[i])
    ims.append([plt.imshow(tmp)])      

#アニメーション作成  
plt.axis('off')
ani = animation.ArtistAnimation(fig, ims, interval=1000)

#アニメーション保存。ファイル名を入れてください。ここではtest.gif
ani.save("test.gif", writer='pillow')