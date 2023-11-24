from collections import defaultdict
from tqdm import tqdm
import math

# 최종 H-novelty 코드
# 앞선 곡들에 대한 각 곡의 novelty 계산
def compute_H_novelty(df, codewords, num_unique_cws):
    idx = list(df.index)
    
    novelties = {i:None for i in range(df.shape[0])}
    
    num_of_earliest_year = list(df.year).count(min(df.year))

    add_idx = []
    total_idx = idx[:num_of_earliest_year] 
    
    pre_first = defaultdict(int)
    pre = defaultdict(lambda: defaultdict(int))
    
    for i in total_idx: 
        cws = codewords[i]
        pre_first[cws[0]] += 1
        for k in range(len(cws[:-1])): 
            pre[cws[k]][cws[k+1]] += 1
     
    for i in tqdm(idx[num_of_earliest_year:]): # cannot compute novelty of the songs composed in the earliest year
        year = df.loc[i,'year']
        pre_idx = list(df[df['year']<year].index)
        add_idx = list(set(pre_idx)-set(total_idx))
        total_idx.extend(add_idx)

        for ii in add_idx:
            cws = codewords[ii]
            pre_first[cws[0]] += 1
            for k in range(len(cws[:-1])): 
                pre[cws[k]][cws[k+1]] += 1
                            
        cws = codewords[i]
        
        first_count = pre_first[cws[0]]
        #prob_first = (first_count + 1) / (sum(pre_first.values()) + num_unique_cws)
        prob_first = (first_count + 1) / (sum(pre_first.values()) + 582)
        log_prob_first = math.log10(1/prob_first)

        log_generation_prob = 0
        for k in range(len(cws[:-1])):
            this = cws[k]
            next_ = cws[k+1]
            #prob = (pre[this][next_] + 1) / (sum(pre[this].values()) + num_unique_cws)
            prob = (pre[this][next_] + 1) / (sum(pre[this].values()) + 273515)
            log_generation_prob += math.log10(1/prob)

        novelty = (log_prob_first + log_generation_prob) / len(cws)
        novelties[i] = novelty
        #print(novelty)

    return novelties




# 최종 P-novelty 코드
# 해당 작곡가의 곡들에 대한 곡의 novelty 계산
def compute_P_novelty(df, codewords, num_unique_cws):  
    
    novelties = {c:[] for c in df.composer.unique()}
     
    for c in tqdm(df.composer.unique()):           
        c_songs = df[df['composer']==c].index
        
        for s in c_songs:
            P_pool_first = defaultdict(int)
            P_pool = defaultdict(lambda: defaultdict(int))
            
            others = [x for x in c_songs if df['year'][x] < df['year'][s]]
    
            for ot in others:
                cws = codewords[ot]
                P_pool_first[cws[0]] += 1
                for k in range(len(cws[:-1])):
                    P_pool[cws[k]][cws[k+1]] += 1

            cws = codewords[s]

            first_count = P_pool_first[cws[0]]
            prob_first = (first_count + 1) / (sum(P_pool_first.values()) + num_unique_cws)
            log_prob_first = math.log10(1/prob_first)

            log_generation_prob = 0
            for k in range(len(cws[:-1])):
                this = cws[k]
                next_ = cws[k+1]
                prob = (P_pool[this][next_] + 1) / (sum(P_pool[this].values()) + num_unique_cws)
                log_generation_prob += math.log10(1/prob)

            novelty = (log_prob_first + log_generation_prob) / len(cws)
            novelties[c].append(novelty)

    return novelties

