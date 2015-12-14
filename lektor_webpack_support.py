import os

from lektor.pluginsystem import Plugin
from lektor.reporter import reporter
from lektor.utils import portable_popen


class WebpackSupportPlugin(Plugin):
    name = 'Webpack Support Plugin'
    description = 'Super simple plugin that runs a webpack watcher'

    def __init__(self, *args, **kwargs):
        Plugin.__init__(self, *args, **kwargs)
        self.webpack_process = None

    def is_enabled(self, build_flags):
        return bool(build_flags.get('webpack'))

    def run_webpack(self, watch=False):
        webpack_root = os.path.join(self.env.root_path, 'webpack')
        args = [os.path.join(webpack_root, 'node_modules', '.bin', 'webpack')]
        if watch:
            args.append('--watch')
        return portable_popen(args, cwd=webpack_root)

    def npm_install(self):
        reporter.report_generic('Running npm install')
        webpack_root = os.path.join(self.env.root_path, 'webpack')
        portable_popen(['npm', 'install'], cwd=webpack_root).wait()

    def on_server_spawn(self, build_flags, **extra):
        if not self.is_enabled(build_flags):
            return
        self.npm_install()
        reporter.report_generic('Spawning webpack watcher')
        self.webpack_process = self.run_webpack(watch=True)

    def on_server_stop(self, **extra):
        if self.webpack_process is not None:
            reporter.report_generic('Stopping webpack watcher')
            self.webpack_process.kill()

    def on_before_build_all(self, builder, **extra):
        if not self.is_enabled(builder.build_flags) \
           or self.webpack_process is not None:
            return
        self.npm_install()
        reporter.report_generic('Starting webpack build')
        self.run_webpack().wait()
        reporter.report_generic('Webpack build finished')
