def orthogonal(min, max, N):

    samples = N*N
    r = max - min

    scale = r/samples

    xlist = [[0 for i in range(N)] for j in range(N)]
    ylist = [[0 for i in range(N)] for j in range(N)]
    print(xlist)
    print(ylist)

    m=0
    for i in range(N):
        for j in range(N):
            xlist[i][j] = ylist[i][j] = m
            m+=1

    np.random.shuffle(xlist)
    np.random.shuffle(ylist)
    print(xlist)
    print(ylist)

    xvalues=[]
    yvalues=[]
    count=0
    for i in range(N):
        for j in range(N):
            count+=1
            print(min, scale, xlist[i][j])
            xvalues.append( min + (scale * (xlist[i][j])) + (np.random.uniform()*scale) )
            yvalues.append( min + (scale * (ylist[j][i])) +  (np.random.uniform()*scale) )

    print(count)


        '''
        lim = [min_v, max_v]
        r = max_v - min_v
        res = []
        for i in range(N):
            x_lim = [
                lim[0] + i * r/N,
                lim[0] + (i+1) * r/N
            ]
            for j in range(N):
                y_lim = [
                    lim[0] + j * r/N,
                    lim[0] + (j+1) * r/N
                ]
                res.append([
                    np.random.uniform(x_lim[0], x_lim[1], 1)[0],
                    np.random.uniform(y_lim[0], y_lim[1], 1)[0]
                ])
        return res
        '''
        
    return xvalues, yvalues
