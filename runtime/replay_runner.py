class ReplayRunner:
    def __init__(self):
        self.engine_runner = None
        self.cycles = 0
        self.completed = False

    def set_engine_runner(self, engine_runner):
        self.engine_runner = engine_runner

    def run(self, replay_feed):
        while replay_feed.has_next():
            replay_feed.next_tick()
            self.engine_runner.run_cycle()
            self.cycles += 1

        self.completed = True
