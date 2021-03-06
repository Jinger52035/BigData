import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from sklearn.cluster import MiniBatchKMeans, KMeans
from sklearn.metrics.pairwise import pairwise_distances_argmin
from sklearn.datasets.samples_generator import make_blobs
from mpl_toolkits.mplot3d import Axes3D

# In[82]:


## 设置属性防止中文乱码
mpl.rcParams['font.sans-serif'] = [u'SimHei']
mpl.rcParams['axes.unicode_minus'] = False

# In[93]:
centers = 3
X, Y = make_blobs(n_samples=500, n_features=3,centers=centers, cluster_std=0.5)



#df = pd.read_excel('E:/A/工作/聚类/聚类算法包ver3.0/聚类算法包/DBSCAN/test4.xlsx')

clusters = 3
k_means = KMeans(init='k-means++', n_clusters=clusters, random_state=28)
t0 = time.time() #当前时间
k_means.fit(X)  #训练模型
km_batch = time.time() - t0  #使用kmeans训练数据的消耗时间
print ("K-Means算法模型训练消耗时间:%.4fs" % km_batch)

#构建MiniBatchKMeans算法
batch_size = 100
mbk = MiniBatchKMeans(init='k-means++', n_clusters=clusters, batch_size=batch_size, random_state=28)
t0 = time.time()
mbk.fit(X)
mbk_batch = time.time() - t0
print ("Mini Batch K-Means算法模型训练消耗时间:%.4fs" % mbk_batch)

#预测结果
km_y_hat = k_means.predict(X)
mbkm_y_hat = mbk.predict(X)

'''
print(km_y_hat[:10])
print(mbkm_y_hat[:10])
print(k_means.cluster_centers_)
print(mbk.cluster_centers_)
'''

##获取聚类中心点并聚类中心点进行排序
k_means_cluster_centers = k_means.cluster_centers_#输出kmeans聚类中心点
mbk_means_cluster_centers = mbk.cluster_centers_#输出mbk聚类中心点
print ("K-Means算法聚类中心点:\ncenter=", k_means_cluster_centers)
print ("Mini Batch K-Means算法聚类中心点:\ncenter=", mbk_means_cluster_centers)
# pairwise_distances_argmin：默认情况下，该API的功能是，将X和Y中的元素按照从大到小做一个排序
# 然后将排序之后的X中的值和Y中的值两两组合；
# API实际返回的是针对于X中每个元素的对应的Y中的每个值的下标索引
order = pairwise_distances_argmin(X=k_means_cluster_centers,
                                  Y=mbk_means_cluster_centers)

## 画图

fig = plt.figure(figsize=(12, 6), facecolor='w')
cm = mpl.colors.ListedColormap(['#FFC2CC', '#C2FFCC', '#CCC2FF'])
cm2 = mpl.colors.ListedColormap(['#FF0000', '#00FF00', '#0000FF'])
plt.subplots_adjust(left=0.05, right=0.95, bottom=0.05, top=0.9)

ax = fig.add_subplot(221, projection='3d')
ax.scatter(X[:, 0], X[:, 1],X[:,2],alpha=0.3,c="#FF0000",s=np.random.randint(10,20, size=(20, 40)))     #生成散点.利用c控制颜色序列,s控制大小
plt.title(u'原始数据分布图')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
plt.grid(True)


ax2 = fig.add_subplot(222, projection='3d')
ax2.scatter(X[:, 0], X[:, 1],X[:,2], c=km_y_hat, s=6, cmap=cm,edgecolors='none')
ax2.scatter(k_means_cluster_centers[:,0], k_means_cluster_centers[:,1],k_means_cluster_centers[:,2],c=range(clusters),s=60,cmap=cm2,edgecolors='none')
plt.title(u'K-Means算法聚类结果图')
ax2.set_xlabel('X')
ax2.set_ylabel('Y')
ax2.set_zlabel('Z')
plt.grid(True)


ax3 = fig.add_subplot(223, projection='3d')
ax3.scatter(X[:,0], X[:,1],X[:,2], c=mbkm_y_hat, s=6, cmap=cm,edgecolors='none')
ax3.scatter(mbk_means_cluster_centers[:,0], mbk_means_cluster_centers[:,1], mbk_means_cluster_centers[:,2],c=range(clusters),s=60,cmap=cm2,edgecolors='none')
plt.title(u'Mini Batch K-Means算法聚类结果图')
ax3.set_xlabel('X')
ax3.set_ylabel('Y')
ax3.set_zlabel('Z')
plt.grid(True)



# 获取KMeans算法和MiniBatchKmeans算法预测不一致的样本数目
different = list(map(lambda x: (x!=0) & (x!=1) & (x!=2), mbkm_y_hat))
for k in range(clusters):
    different += ((km_y_hat == k) != (mbkm_y_hat == order[k]))
identic = np.logical_not(different)
different_nodes = len(list(filter(lambda x:x, different)))

ax4 = fig.add_subplot(224, projection='3d')
ax4.scatter(X[:,0], X[:,1],X[:,2], c="#000000", s=6,edgecolors='none')
ax4.scatter(X[different, 0], X[different, 1],X[different, 2],c="#FF0000",s=60,edgecolors='none' )
plt.title(u'Mini Batch K-Means和K-Means算法预测结果不同的点')
ax4.set_xlabel('X')
ax4.set_ylabel('Y')
ax4.set_zlabel('Z')
plt.grid(True)
plt.show()
