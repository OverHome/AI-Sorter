
class Ai:
    def __init__(self):
        pass

    def predict(self, data):# предсказание кандидата для вакансии 0...1
        return 0 

    def predicts(self, datas):# предсказания кандидатов для вакансии [0...1, ...]
        return [self.predict(data)
         for data in datas] 
