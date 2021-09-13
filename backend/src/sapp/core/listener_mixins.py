class StartupListenerMixin:

    async def run_startup(self) -> None:
        pass


class ShutdownListenerMixin:

    async def run_shutdown(self) -> None:
        pass
