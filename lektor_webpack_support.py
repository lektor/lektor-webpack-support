import os

from lektor.pluginsystem import Plugin
from lektor.reporter import reporter
from lektor.utils import locate_executable, portable_popen


class WebpackSupportPlugin(Plugin):
    name = 'Webpack Support Plugin'
    description = 'Super simple plugin that runs a webpack watcher'

    def __init__(self, *args, **kwargs):
        Plugin.__init__(self, *args, **kwargs)
        self.webpack_process = None

    def is_enabled(self, extra_flags):
        return bool(extra_flags.get('webpack'))

    def get_webpack_folder(self, *paths):
        return os.path.join(self.env.root_path, self.get_config().get("folder", "webpack"), *paths)

    def run_webpack(self, *extra_args):
        args = [self.get_webpack_folder('node_modules', '.bin', 'webpack')] + list(extra_args)
        return portable_popen(args, cwd=self.get_webpack_folder())

    def get_name(self):
        return self.get_config().get("name", "webpack")

    def run_package_manager(self, *args):
        # Use yarn over npm if it's availabe and there is a yarn lockfile
        has_yarn_lockfile = os.path.exists(self.get_webpack_folder('yarn.lock'))
        pkg_manager = 'npm'
        if locate_executable('yarn') is not None and has_yarn_lockfile:
            pkg_manager = 'yarn'
        reporter.report_generic('Running {} {}'.format(pkg_manager, " ".join(args)))
        return portable_popen([pkg_manager] + list(args), cwd=self.get_webpack_folder())

    def install_node_dependencies(self):
        self.run_package_manager('install').wait()

    def run_build(self):
        build_script = self.get_config().get("build_script")
        if build_script:
            self.run_package_manager('run', build_script).wait()
            return
        self.run_webpack().wait()

    def spawn_watch(self):
        watch_script = self.get_config().get('watch_script')
        if watch_script:
            return self.run_package_manager('run', watch_script)
        return self.run_webpack('--watch')

    def on_server_spawn(self, **extra):
        extra_flags = extra.get("extra_flags") or extra.get("build_flags") or {}
        if not self.is_enabled(extra_flags):
            return
        self.install_node_dependencies()
        reporter.report_generic('Spawning {} watcher'.format(self.get_name()))
        self.webpack_process = self.spawn_watch()

    def on_server_stop(self, **extra):
        if self.webpack_process is not None:
            reporter.report_generic('Stopping {} watcher'.format(self.get_name()))
            self.webpack_process.kill()

    def on_before_build_all(self, builder, **extra):
        extra_flags = getattr(
            builder, "extra_flags", getattr(builder, "build_flags", None)
        )
        if not self.is_enabled(extra_flags) \
           or self.webpack_process is not None:
            return
        self.install_node_dependencies()
        reporter.report_generic('Starting {} build'.format(self.get_name()))
        self.run_build()
        reporter.report_generic('{} build finished'.format(self.get_name()))