from tensorflow.keras.models import load_model
tf_model = load_model('/ai_learn/neural_wb.h5')


class Ai:
    def __init__(self):
        pass

    def predict(self, data):# предсказание кандидата для вакансии 0...1
        tf_model.predict(data)

    def predicts(self, datas):# предсказания кандидатов для вакансии [0...1, ...]
        return [self.predict(data)
         for data in datas] 
