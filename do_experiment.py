from numpy import *
import scipy as Sci
import scipy.linalg
import os
import time
import rslib


class Options(object):
    def __init__(self,Q=10,P=100,mu=0.8,gamma=50):
        self.Q=int(Q)
        self.P=int(P)
        self.mu=float(mu)
        self.gamma=float(gamma)
class Result(object):
    def __init__(self):
        self.time=0.
        self.MAE=0.
        self.options=None
    def __str__(self):
        return 'MAE\ttime(sec)\tQ\tP\tmu\tgamma\n%s\t%s\t%s\t%s\t%s\t%s\n'%(self.MAE,self.time,self.options.Q,self.options.P,self.options.mu,self.options.gamma)

"""
    do the experiment
"""
def Start():
    time_start=time.time()
    options=Options(50,100,0.8,20)
    directory='./'
    data=loadtxt(directory+'/ml-100k/u.data')
    """
    random for data shuffle
    """
    directory=directory+time.strftime("%y%m%d-%H%M")+'/'
    os.mkdir(directory)
    M=5
    seed=1
    random.seed(seed)
    random.shuffle(data)
    data_boundary=int32(data.max(axis=0))
    totalMAE=0.0
    for k in range(0,M):
        test,train=SpiltData(data,M,k)
        tmp_directory=directory+str(k)+'/'
        os.mkdir(tmp_directory)
        MAE=rslib.Calculate(train,test,data_boundary,options,tmp_directory)
        print MAE
        totalMAE+=MAE
    time_end=time.time()
    result=Result()
    result.options=options
    result.MAE=totalMAE/M
    result.time=time_end-time_start
    open(directory+'result.txt','w').write(result.__str__())
    return
    
def SpiltData(data,M,K):
    split_helper=arange(data.shape[0])
    test_idx=(split_helper%M==K)
    train_idx=~test_idx
    train=data[train_idx,:]
    test=data[test_idx,:]        
    return test,train

def GetRecommend():
    rating_mat_file=raw_input("Please input the rating_mat you want to load:")
    rating_mat=loadtxt(rating_mat_file)
    rating_sort_idx=rating_mat.argsort(axis=1)
    while(True):
        user_id=int(raw_input("the id of user(0 is exit):"))
        if user_id==0:
            break
        elif user_id>rating_mat.shape[0]:
            print "INFO:user is not found"
        else:
            movie_cnt=int(raw_input("the count of recommend movies:"))
            movie_list=rating_sort_idx[user_id,-movie_cnt:]
            movie_list=movie_list[::-1]
            print 'RESULT:\n%s'%movie_list
