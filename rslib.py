from numpy import *
import scipy as Sci
import scipy.linalg

"""
__author__ = "yzhuan"
__copyright__ = "Copyright 2014, www.yzhuan.net"
__license__ = "GPL"
__version__ = "1.0"
__email__ = "yzh465022947@gmail.com"
"""

"""
    create the user*movie matrix form the raw data
"""
def CreateDataMatrix(train,data_boundary,directory):
    print 'INFO:Create Data Matrix'
    #return loadtxt(directory+'/data.txt')
    user_cnt=data_boundary[0]
    movie_cnt=data_boundary[1]
    data=zeros((user_cnt+1,movie_cnt+1))
    #row 0 is user; row 1 is movie; row 2 is score; row 3 is time
    for row in train:
        data[row[0],row[1]]=row[2]
    savetxt(directory+'/data.txt',data,'%d')
    return data

"""
    train_mat n*p (n is number of user;p is number of movie; index is started by 1)
"""
def UserSimilarity(train_mat,data_boundary,options,directory):
    print 'INFO:Calculate User Similarity'
    #sim_mat=loadtxt(directory+'/sim_mat.txt')
    #avg_score_mat=loadtxt(directory+'/avg_score_mat.txt')
    #return sim_mat,avg_score_mat    
    user_cnt=data_boundary[0] #the length of row
    avg_score_mat=sum(train_mat,axis=1)/(sum(train_mat>0,axis=1))
    avg_score_mat=nan_to_num(avg_score_mat)
    savetxt(directory+'/avg_score_mat.txt',avg_score_mat,'%f')    
    sim_mat=zeros((user_cnt+1,user_cnt+1))
    """
    for selecting other user, I select sim_mat(u,u)=0
    So it is 'j in range(i+1,)'
    """
    for i in range(1,user_cnt+1):
        for j in range(i+1,user_cnt+1):
            u=train_mat[i,:]
            v=train_mat[j,:]
            u_idx=u>0
            v_idx=v>0
            com_uv=u_idx&v_idx
            ru=u[com_uv]-avg_score_mat[i]
            rv=v[com_uv]-avg_score_mat[j]
            sim_mat[i,j]=sim_mat[j,i]=Omega(com_uv,options.gamma)*abs(dot(ru,rv))/sqrt(dot(ru,ru)*dot(rv,rv))
    sim_mat=nan_to_num(sim_mat)
    savetxt(directory+'/sim_mat.txt',sim_mat,'%f')    
    return sim_mat,avg_score_mat

"""
    calculate the w parameter
"""
def Omega(com_uv,gamma):
    return min(sum(com_uv),gamma)/gamma

"""
    calculate the MAE
"""
def Calculate(train,test,data_boundary,options,directory):
    print 'INFO:Calculate MAE'
    train_mat=CreateDataMatrix(train,data_boundary,directory)
    sim_mat,avg_score_mat=UserSimilarity(train_mat,data_boundary,options,directory)
    rating_mat=CalculateRatingMat(train_mat,sim_mat,avg_score_mat,data_boundary,options,directory)
    #begin testing
    MAE=0.0
    for row in test:
        MAE+=abs(row[2]-rating_mat[row[0],row[1]])
    MAE=MAE/test.shape[0]
    return MAE
"""
    calculate the rating matrix
"""
def CalculateRatingMat(train_mat,sim_mat,avg_score_mat,data_boundary,options,directory):
    print 'INFO:Calculate Rating Matrix'
    #rating_mat=loadtxt(directory+'/rating_mat.txt')
    #return rating_mat
    sim_sort_idx=sim_mat.argsort(axis=1)
    sim_top_P=sim_sort_idx[:,-options.P:]
    user_cnt=data_boundary[0]
    movie_cnt=data_boundary[1]
    rating_mat=zeros((user_cnt+1,movie_cnt+1))
    for i in range(1,user_cnt+1):
        sim_u_P=sim_mat[i,:][sim_top_P[i,:]]
        sim_u_mean_P=mean(sim_u_P)
        #c2 has been sorted before(ascend)
        sim_u_c2=sim_top_P[i,:][sim_u_P>=sim_u_mean_P]
        #change as descend
        sim_u_c2=sim_u_c2[::-1]
        #select collection c3, N1, N2
        for j in range(1,movie_cnt+1):
            sim_u_N1=[]
            sim_u_N2=[]
            for k in sim_u_c2:
                if train_mat[k,j]>1e-6:
                    #print k,train_mat[k,j]
                    sim_u_N1.append(k)
                else:
                    sim_u_N2.append(k)
            sim_u_N1=sim_u_N1[:options.Q]   
            sim_u_N2_size=len(sim_u_N1)-options.Q
            if sim_u_N2_size>0:
                sim_u_N2=sim_u_N2[:sim_u_N2_size]
            else:
                sim_u_N2=[]
            
            if train_mat[i,j]<1e-6:
                rating_mat[i,j]=CalculateRating(i,j,sim_u_N1,sim_u_N2,train_mat,sim_mat,avg_score_mat,options.mu)
            
    savetxt(directory+'/rating_mat.txt',rating_mat,'%f')
    return rating_mat
"""
    calculate rating of each item
"""
def CalculateRating(u,m,N1,N2,train_mat,sim_mat,avg_score_mat,mu):
    score=avg_score_mat[u]
    if len(N1)>0:
        score+=dot((train_mat[N1,m]-avg_score_mat[N1]),sim_mat[u,N1])/sum(sim_mat[u,N1])*mu
    if len(N2)>0:
        score+=dot((train_mat[N2,m]-avg_score_mat[N2]),sim_mat[u,N2])/sum(sim_mat[u,N2])*(1-mu)
    return score
