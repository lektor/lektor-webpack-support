import os
import threading

from lektor.pluginsystem import Plugin
from lektor.reporter import reporter
from lektor.utils import portable_popen


class WebpackSupportPlugin(Plugin):
    name = 'Webpack Support Plugin'
    description = 'Super simple plugin that runs a webpack watcher'

    def __init__(self, *args, **kwargs):
        Plugin.__init__(self, *args, **kwargs)
        self.npm_lock = threading.Lock()
        self.webpack_process = None

    def is_enabled(self, extra_flags):
        return bool(extra_flags.get('webpack'))

    def run_webpack(self, watch=False):
        webpack_root = os.path.join(self.env.root_path, 'webpack')
        args = [os.path.join(webpack_root, 'node_modules', '.bin', 'webpack')]
        if watch:
            args.append('--watch')
        return portable_popen(args, cwd=webpack_root)

    def npm_install(self):
        if self.npm_lock.acquire(False):
            reporter.report_generic('Running npm install')
            webpack_root = os.path.join(self.env.root_path, 'webpack')
            portable_popen(['npm', 'install'], cwd=webpack_root).wait()
        else:
            self.npm_lock.acquire()
        self.npm_lock.release()

    def on_server_spawn(self, **extra):
        extra_flags = extra.get("extra_flags") or extra.get("build_flags") or {}
        if not self.is_enabled(extra_flags):
            return
        self.npm_install()
        reporter.report_generic('Spawning webpack watcher')
        self.webpack_process = self.run_webpack(watch=True)

    def on_server_stop(self, **extra):
        if self.webpack_process is not None:
            reporter.report_generic('Stopping webpack watcher')
            self.webpack_process.kill()

    def on_before_build_all(self, builder, **extra):
        extra_flags = getattr(
            builder, "extra_flags", getattr(builder, "build_flags", None)
        )
        if not self.is_enabled(extra_flags) \
           or self.webpack_process is not None:
            return
        self.npm_install()
        reporter.report_generic('Starting webpack build')
        self.run_webpack().wait()
        reporter.report_generic('Webpack build finished')
