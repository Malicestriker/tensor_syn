import numpy as np

class SynTensor:
    def __init__(self, n, mlist, Plist):
        '''
        :param self:
        :param n: shape的个数
        :param mlist: [m1,...,mn]的list
        :param Plist: P[i][j]是从j到i的映射
        '''
        assert len(mlist) == n,'Length of mlist must equal to n'
        assert np.shape(Plist) == (n,n), 'Size of Plist must be (n,n)'

        self.n = n
        self.mList = mlist
        self.N = sum(mlist)

        # 构造索引序列,即前缀和
        self.indBegin = mlist
        s = 0
        for i in range(n):
            self.indBegin[i] = mlist[0] if i==0 else self.indBegin[i-1]+mlist[i]
        self.indEnd = [ self.indBegin[i+1] if i!= n-1 else N for i in range(n)  ]

        # 处理Plist的型状，让他变成mi*mj的
        self.Plist = np.zeros((n,n),np.ndarray)
        for i in range(n):
            for j in range(n):
                self.Plist[i][j] = np.array( Plist[0:mlist[j],0:mlist[i]] )

        self.buildP()
        self.buildC()
        self.buildR()
        self.Ax,self.Bx,self.Cx = self.get_init()

    def buildP(self):
        self.P = np.zeros([self.N,self.N],np.int)
        n = self.n
        for i in range(n):
            for j in range(n):
                self.P[self.indBegin[j]:self.indEnd[j],self.indBegin[i]:self.indEnd[i]] = self.Plist[i][j]


    def buildC(self):
        n = self.n
        self.C = np.zeros([n,n,n],np.ndarray)
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    tmp = np.dot(self.Plist[j][k],self.Plist[i][j])
                    tmp = np.dot(self.Plist[k][i],tmp)
                    d = np.diag(tmp)
                    d = np.diag(d)
                    self.C[i][j][k] = np.where(d > 0, 1,0)

    def getRijk(self,i,j,k):
        return np.dot(self.Plist[i][j],self.C[i][j][k])

    def buildR(self):
        n = self.n
        self.R = np.zeros([n,n,n],np.ndarray)
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    self.R[i][j][k] = self.getRijk(i,j,k)

