from tensorflow.keras.models import load_model
import numpy as np

class Ai:
    def __init__(self):
        pass
    def predict(self, x):
        model = load_model('neural_web2.h5')
        a = x[(x.job_B == 0) & (x.job_C == 0) & (x.job_D == 0)].job_id.unique()
        out = model.predict(np.asarray(x[x.columns[:-2]]))
        x = x[['id', 'job_id']].copy()
        x['cam'] = out
        x.loc[x.job_id.isin(a), 'cam'] = 0
        return x

    def predicts(self, datas):# предсказания кандидатов для вакансии [0...1, ...]
        return [self.predict(data)
         for data in datas] 
