import asyncio
import datetime
import logging
import sys
from asyncio.subprocess import PIPE, Process
from pathlib import Path
from typing import Optional

from aiohttp.web import Application

logger = logging.getLogger("app")


class RenderState(object):
    STATE_RENDER_IDLE = 'idle'
    STATE_RENDER_REQUESTED = 'requested'
    STATE_RENDER_FAILED = 'failed'
    command = [
        sys.executable,
        str(Path(__file__).with_name("render_notion_dependencies.py").resolve()),
        "--output", str(Path(__file__).resolve().parent / "static/rendered/steps.png"),
    ]

    def __init__(self):
        self.state: str = RenderState.STATE_RENDER_IDLE
        self.process: Optional[Process] = None
        self.stop_update_loop = False
        self.updated_at: str = self.get_date_str()

    def get_date_str(self) -> str:
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    async def request_render(self):
        self.process = await asyncio.create_subprocess_exec(*RenderState.command, stdout=PIPE, stderr=PIPE)

    def get_render_status(self):
        return self.state

    async def _run_update_loop(self):
        logger.info("Render State update loop started")
        while not self.stop_update_loop:
            if self.process is None:
                # no process started
                await asyncio.sleep(1)
                continue

            rc = self.process.returncode
            if rc is None:
                # process is running
                self.state = RenderState.STATE_RENDER_REQUESTED
                await asyncio.sleep(1)
                continue

            if rc == 0:
                # process successfully finished
                self.state = RenderState.STATE_RENDER_IDLE
                self.process = None
                self.updated_at = self.get_date_str()

                await asyncio.sleep(1)
                continue

            if rc != 0:
                # process failed
                self.state = RenderState.STATE_RENDER_FAILED

                stderr_b = await self.process.stderr.read()
                logger.error(f"{stderr_b.decode('ascii') if stderr_b else '<no stderr from process>'}")

                self.process = None

                await asyncio.sleep(1)
                continue

        logger.info("Render State update loop stopped")

    async def on_startup(self):
        asyncio.create_task(self.request_render())
        asyncio.create_task(self._run_update_loop())
        asyncio.create_task(self.configure_graphviz())

    async def on_cleanup(self):
        self.stop_update_loop = True

    async def configure_graphviz(self):
        await asyncio.create_subprocess_exec("dot", "-c")


def get_render_state(app: Application) -> RenderState:
    return app["render_state"]


def set_render_state(app: Application, state: RenderState):
    app["render_state"] = state


async def on_startup(app: Application):
    await get_render_state(app).on_startup()


async def on_cleanup(app: Application):
    await get_render_state(app).on_cleanup()


def setup_render_state(app: Application):
    set_render_state(app, RenderState())
