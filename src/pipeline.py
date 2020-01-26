from src.runnable import Runnable


class Pipeline:

    def __init__(self):
        self.pipeline = []

    def add(self, tasks: [Runnable]):
        self.pipeline += tasks

    def run(self, input):
        for task in self.pipeline:
            input = task.run(input)
        return input
