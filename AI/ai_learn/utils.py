import pandas as pd

def cit_new(x):
    if 'россия' in str(x).lower() or 'рф' in str(x).lower():
        return 'rf'
    elif 'nan'==str(x).lower():
        return 'nan'
    else:
        return 'other'

def new_age(x):
    if x >= 18 and x <= 100:
        return x
    else:
        return 0

def new_lang(x):
    rus = str(x).lower().find('русский')
    if 'родной' in str(x)[rus:rus+20].lower():
        return 'rus'
    elif 'nan' == str(x).lower():
        return 'nan'
    else:
        return 'other'

def new_lic(x):
    if str(x).lower() == 'nan':
        return 'nan'
    else:
        ans = ''
        if 'A' in x.upper():
            ans += 'A'
        if 'B' in x.upper():
            ans += 'B'
        if 'C' in x.upper():
            ans += 'C'
        if 'D' in x.upper():
            ans += 'D'
        if ans == '':
            if 'E' in x.upper():
                return 'BCD'
            else:
                return 'empty'
        else:
            return ans

def new_lic_v2(x):
    i = str(x).lower().find('категор')
    if str(x) == 'nan':
        return 'nan'
    else:
        ans = ''
        if 'A' in x[i:i+20].upper():
            ans += 'A'
        if 'B' in x[i:i+20].upper():
            ans += 'B'
        if 'C' in x[i:i+20].upper():
            ans += 'C'
        if 'D' in x[i:i+20].upper():
            ans += 'D'
        if ans == '':
            if 'E' in x[i:i+20].upper():
                return 'BCD'
            else:
                return 'nan'
        else:
            return ans

def new_stat(x):
    if str(x).lower() == 'nan':
        return 'nan'
    else:
        if 'приглашен' in x.lower() or 'принят' in x.lower() or 'заклчюч' in x.lower() or 'оформ' in x.lower():
            return 'accepted'
        elif 'отказ' in x.lower() or 'отклонен' in x.lower() or 'расторгн' in x.lower():
            return 'declined'
        else:
            return 'other'

def get_dummies_dl(x):
    l = [0, 0, 0, 0]
    if 'A' in x:
        l[0] = 1
    if 'B' in x:
        l[1] = 1
    if 'C' in x:
        l[2] = 1
    if 'D' in x:
        l[3] = 1
    return pd.Series(l)

def preprocess_data(df, test=False):
    n = len(df.columns)
    if not test:
        df['date'] = df[13]
        df['job_id'] = df[14]
        df['status'] = df[16].apply(new_stat)
    df['id'] = df[0]
    df['sex'] = df[2]
    df['citizenship'] = df[3].apply(cit_new)
    df['age'] = df[4].apply(new_age)/100
    df['salary'] = df[5].fillna(0)/150000
    df['lang'] = df[6].apply(new_lang)
    df['drive_lic'] = df[7].apply(new_lic)
    df['another_drive_lic'] = df[9].apply(new_lic_v2)
    df['drive_lic'] = df.apply(lambda x: x.another_drive_lic if x.drive_lic == 'nan' else x.drive_lic, axis=1)
    df.drop('another_drive_lic', axis=1, inplace=True)
    df['graf_1'] = df[10]
    df['graf_2'] = df[11]
    df['region'] = df[12]
    df.drop(list(range(n)), axis=1, inplace=True)
    if not test:
        data = df[(df.date.apply(lambda x: pd.to_datetime(x))>=pd.to_datetime('2021-01-01'))&(df.status.isin(['accepted', 'declined']))]
    else:
        data = df.copy()
    sex = pd.get_dummies(data.sex, drop_first=True, prefix='sex')
    citizenship = pd.get_dummies(data.citizenship, drop_first=True, prefix='citiz')
    lang = pd.get_dummies(data.lang, drop_first=True, prefix='lang')
    graf_1 = pd.get_dummies(data.graf_1, drop_first=False, prefix='graf_1')
    graf_2 = pd.get_dummies(data.graf_2, drop_first=False, prefix='graf_2')
    dl = data['drive_lic'].apply(get_dummies_dl)
    dl.columns = ['dl_A', 'dl_B', 'dl_C', 'dl_D']
    if not test:
        return pd.concat([data['id'], sex, citizenship, lang, dl, graf_1, graf_2, data[['age', 'salary', 'region', 'job_id', 'status']]], axis=1)
    else:
        return pd.concat([data['id'], sex, citizenship, lang, dl, graf_1, graf_2, data[['age', 'salary', 'region']]], axis=1)

def new_educ(x):
    if 'университет' in x.lower() or 'институт' in x.lower():
        return 'univ'
    elif any(e in x.lower() for e in ['академия', 'колледж', 'техникум', 'пту', 'училище', 'спец', 'профес']):
        return 'col'
    elif 'лицей' in x.lower() or 'школа' in x.lower():
        return 'sch'
    else:
        return 'other'

def remove_educ(x):
    nl = [0, 0, 0, 0]
    if x.educ_univ > 0:
        nl[0] = 1
    elif x.educ_col > 0:
        nl[1] = 1
    elif x.educ_sch > 0:
        nl[2] = 1
    elif x.educ_other > 0:
        nl[3] = 1
    return pd.Series(nl)

def preprocess_educ(df):
    df['id'] = df[0]
    df['educ'] = df[1].apply(new_educ)

    df = pd.concat([df['id'], pd.get_dummies(df.educ, prefix='educ')], axis=1)
    df = df.groupby('id').sum().reset_index()
    df[['educ_univ', 'educ_col', 'educ_sch', 'educ_other']] = df.apply(remove_educ, axis=1)

    return df

def new_cat(x):
    ans = ''
    desc = str(x[4]).lower()
    name = str(x[2]).lower()
    i = desc.lower().find('категор')
    j = desc[i+1:].lower().find('категор')
    k = desc[i+j+1:].lower().find('категор')
    desc_i = desc[i:i+35]
    desc_j = desc[i+j:i+j+35]
    desc_k = desc[i+j+k:i+j+k+35]
    if ('b' in desc_i) or ('b' in desc_j) or ('b' in desc_j):
        ans += 'B'
    if ('c' in desc_i) or ('c' in desc_j) or ('c' in desc_j):
        ans += 'C'
    if ('d' in desc_i) or ('d' in desc_j) or ('d' in desc_j):
        ans += 'D'
    if 'автобус' in name:
        if 'D' not in ans:
            ans += 'D'
    elif 'экспед' in name or 'груз' in name or 'фур' in name:
        if 'C' not in ans:
            ans += 'C'
    if 'водитель' in name and (ans == '' or ans == 'E'):
        if 'B' not in ans:
            ans += 'B'
    return ans

def get_dummies_job(x):
    l = [0, 0, 0]
    if 'B' in x:
        l[0] = 1
    if 'C' in x:
        l[1] = 1
    if 'D' in x:
        l[2] = 1
    return pd.Series(l)

def preprocess_job(df):
    df['job_id'] = df[0]
    df['region'] = df[3]
    df['job'] = df.apply(new_cat, axis=1)

    job = df.job.apply(get_dummies_job)
    job.columns = ['job_B', 'job_C', 'job_D']

    return pd.concat([df[['job_id', 'region']], job], axis=1)

def new_exp(x):
    if any(e in str(x).lower() for e in ['водитель', 'экспедит', 'такси', 'курьер', 'перегон']):
        return 'drive'
    elif any(e in str(x).lower() for e in ['авто', 'механик', 'инженер', 'техник']):
        return 'mech'
    else:
        return 'other'

def count_exp(x):
    if x[2] in [-1, 0]:
        return 0
    elif x[4] in [-1, 0]:
        return (2022 - x[2])*12 + 8 - x[3]
    else:
        return (x[4] - x[2])*12 + x[5] - x[3]

def preprocess_exp(df):
    df['job'] = df[1].apply(new_exp)
    df['exp'] = df.apply(count_exp, axis=1)
    df['id'] = df[0]
    return df[['id', 'job', 'exp']].drop_duplicates().groupby(['id', 'job'])['exp'].sum().reset_index().pivot_table(index='id', columns='job', values='exp').drop('other', axis=1).reset_index().fillna(0)

def preprocess_all_data(df, jobs, educ, work):
    df = preprocess_data(df)
    jobs = preprocess_job(jobs)
    educ = preprocess_educ(educ)
    work = preprocess_exp(work)

    work['drive'] = work.drive.apply(lambda x: x/600 if x<=600 else 1)
    work['mech'] = work.mech.apply(lambda x: x/600 if x<=600 else 1)

    merge = pd.merge(df, educ, on='id', how='left')
    merge = pd.merge(merge, work, on='id', how='left')
    merge = pd.merge(merge, jobs, on='job_id')
    merge['same_region'] = (merge.region_x==merge.region_y).astype(int)
    merge['status_v2'] = merge.status.apply(lambda x: 1 if x=='accepted' else 0)
    merge.drop(['region_x', 'region_y', 'id', 'job_id', 'status'], axis=1, inplace=True)
    merge.fillna(0, inplace=True)
    merge = merge.rename(columns={'status_v2': 'status'})
    return merge

def preprocess_test_data(df, jobs, educ, work):
    test = True
    df = preprocess_data(df, test)
    jobs = preprocess_job(jobs)
    educ = preprocess_educ(educ)
    work = preprocess_exp(work)

    work['drive'] = work.drive.apply(lambda x: x/600 if x<=600 else 1)
    work['mech'] = work.mech.apply(lambda x: x/600 if x<=600 else 1)

    merge = pd.merge(df, educ, on='id', how='left')
    merge = pd.merge(merge, work, on='id', how='left')

    merge_new = pd.DataFrame()
    for i in range(10):
        tmp = merge.copy()
        tmp['job_id'] = jobs.job_id.iloc[i]
        merge_new = pd.concat([merge_new, tmp])

    merge = pd.merge(merge_new, jobs, on='job_id')
    merge['same_region'] = (merge.region_x == merge.region_y).astype(int)
    merge.drop(['region_x', 'region_y'], axis=1, inplace=True)
    merge.fillna(0, inplace=True)
    return merge
