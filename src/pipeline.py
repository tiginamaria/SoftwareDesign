class Runnable:
    """ Interface for tasks to run in pipe"""

    def run(self, input):
        pass


class Pipeline:
    """ Class implement pattern pipeline to run tasks in consequently. """

    def __init__(self):
        self.pipeline = []

    def add(self, tasks: [Runnable]):
        """ Add tasks to pipeline.
        :param tasks: tasks to run
        """
        self.pipeline += tasks

    def run(self, input):
        """ Run tasks in pipeline.
        :param input: input for first task
        :return: output of last task
        """
        for task in self.pipeline:
            input = task.run(input)
        return input
