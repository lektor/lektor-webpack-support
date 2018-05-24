import os

from lektor.pluginsystem import Plugin
from lektor.reporter import reporter
from lektor.utils import locate_executable, portable_popen


class WebpackSupportPlugin(Plugin):
    name = 'Webpack Support Plugin'
    description = 'Super simple Lektor plugin that runs a webpack watcher'

    def __init__(self, *args, **kwargs):
        Plugin.__init__(self, *args, **kwargs)
        self.webpack_process = None

    def is_enabled(self, extra_flags):
        return bool(extra_flags.get('webpack'))

    def is_debug(self, build_flags):
        return bool(build_flags.get('debug'))

    def is_production(self, build_flags):
        return bool(build_flags.get('production'))

    def get_mode(self, build_flags):
        if self.is_debug(build_flags):
            return 'd'
        elif self.is_production(build_flags):
            return 'p'

    def run_webpack(self, watch=False, mode=None):
        webpack_root = os.path.join(self.env.root_path, 'webpack')
        args = [os.path.join(webpack_root, 'node_modules', '.bin', 'webpack')]
        env = os.environ.copy()
        if watch:
            args.append('--watch')
        if mode is 'd':
            args.append('-d')
        elif mode is 'p':
            args.append('-p')
            env['NODE_ENV'] = 'production'
        return portable_popen(args, cwd=webpack_root, env=env)

    def install_node_dependencies(self):
        webpack_root = os.path.join(self.env.root_path, 'webpack')

        # Use yarn over npm if it's availabe and there is a yarn lockfile
        has_yarn_lockfile = os.path.exists(os.path.join(
            webpack_root, 'yarn.lock'))
        pkg_manager = 'npm'
        if locate_executable('yarn') is not None and has_yarn_lockfile:
            pkg_manager = 'yarn'

        reporter.report_generic('Running {} install'.format(pkg_manager))
        portable_popen([pkg_manager, 'install'], cwd=webpack_root).wait()

    def on_server_spawn(self, **extra):
        extra_flags = extra.get("extra_flags") or extra.get("build_flags") or {}
        if not self.is_enabled(extra_flags):
            return
        self.install_node_dependencies()
        reporter.report_generic('Spawning webpack watcher')
        self.webpack_process = self.run_webpack(watch=True, mode=self.get_mode(build_flags))

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
        self.install_node_dependencies()
        reporter.report_generic('Starting webpack build')
        self.run_webpack(mode=self.get_mode(builder.build_flags)).wait()
        reporter.report_generic('Webpack build finished')
