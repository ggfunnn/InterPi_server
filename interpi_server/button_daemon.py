import daemon as d
import interpi_server

daemon = interpi_server.Button_daemon()

with d.DaemonContext():
    daemon.initialize()
    daemon.wait()
