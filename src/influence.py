from collections import defaultdict
import math

def compute_influence(df, codewords):

    composers = list(df.composer.unique())

    influences = defaultdict(lambda: defaultdict(None))
    
    for c in composers:
        pre_first = defaultdict(int)
        pre = defaultdict(lambda: defaultdict(int))

        pre_first_composer_c = defaultdict(int)
        pre_composer_c = defaultdict(lambda: defaultdict(int))

        c_start_year = min(df[df['composer']==c]['year'])

        influenced_idx = list(df[(df['year']>c_start_year)&(df['composer']!=c)].index)
        influenced_idx = sorted(influenced_idx, reverse=False)

        add_idx = []
        total_idx = []

        for song_j in influenced_idx:
            cws_j = codewords[song_j]
            year_j = df.loc[song_j,'year']
            c_j = df.loc[song_j,'composer']
            assert c_start_year < year_j
            
            pre_idx = list(df[(df['year']<year_j)&(df['composer']!=c_j)].index)
            add_idx = list(set(pre_idx)-set(total_idx))
            total_idx.extend(add_idx)
            
            for ii in add_idx:
                cws_ii = codewords[ii]
                if df.loc[ii,'composer']==c:
                    pre_first_composer_c[cws_ii[0]] += 1
                    for k in range(len(cws_ii[:-1])):
                        pre_composer_c[cws_ii[k]][cws_ii[k+1]] += 1

                pre_first[cws_ii[0]] += 1
                for k in range(len(cws_ii[:-1])): 
                    pre[cws_ii[k]][cws_ii[k+1]] += 1

            first_count = pre_first[cws_j[0]]
            first_count_composer_c = pre_first_composer_c[cws_j[0]]

            prob = 0
            numerator_first = math.log10(first_count + 1)
            denominator_first = math.log10(first_count - first_count_composer_c + 1)
            prob += (numerator_first - denominator_first)

            for kk in range(len(cws_j[:-1])):
                this = cws_j[kk]
                next_ = cws_j[kk+1]

                numerator = math.log10(pre[this][next_] + 1)
                denominator = math.log10(pre[this][next_]-pre_composer_c[this][next_] + 1)
                prob += (numerator-denominator)

            influence = prob / len(cws_j)
            influences[c][song_j] = influence # Influence of composer c on song_j
        
            if influence < 0:
                print('Influence is less than zero!!!')
                return influences
            
    return influences




