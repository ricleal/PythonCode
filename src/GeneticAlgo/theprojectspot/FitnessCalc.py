class FitnessCalc():
  
    Solution = bytearray(64)

    @staticmethod
    def set_solution(solution_passed):
        for i in range(len(solution_passed)):
            FitnessCalc.Solution[i] = int(solution_passed[i])

    @staticmethod
    def get_max_fitness():
        return len(FitnessCalc.Solution)

