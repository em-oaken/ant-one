"""
Tau is Ant One's time engine.
Its purpose is to:
- Keep track of play time and real time
- Handle action progression
- Manage game speed

Name chosen after the greek letter regularly used for time in science.
"""

import asyncio
import datetime
import logging
import time


class Tau():
    def __init__(self):
        """Initiates time engine"""
        self.start_time = datetime.datetime.now()
        self.loopno = 0
        self.objects = []
        self.render = None
    
    def add_object(self, object):
        self.objects.append(object)
    
    def add_render(self, render):
        self.render = render

    async def event_loop_manager(self):
        """Manages the event loop"""
        t_fullloop = time.perf_counter()
        while True:
            t_active = time.perf_counter()
            self.loopno += 1
            self.looptime = datetime.datetime.now()

            for obj in self.objects:
                obj.live()
            self.render()
            
            # logging.info(f'Loop #{self.loopno} over\tRun {1000*(time.perf_counter()-t_active):4.1f}ms\tLoop {1000*(time.perf_counter()-t_fullloop):4.1f}ms')
            t_fullloop = time.perf_counter()
            await asyncio.sleep(0.03)

