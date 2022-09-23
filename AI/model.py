
class Ai:
    def __init__(self):
        pass

    def predict(self, vacancy, candidate):# предсказание кандидата для вакансии 0...1
        return 0 

    def predicts(self, vacancy, candidates):# предсказания кандидатов для вакансии [0...1, ...]
        return [self.predict(vacancy, candidate)
         for candidate in candidates] 
