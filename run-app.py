import config
import argparse

def get_app(service_name: str):
    if service_name == "logging":
        import loggingService.logging_controller
        return loggingService.logging_controller.app
    if service_name == "messages":
        import messagesService.messages_controller
        return messagesService.messages_controller.app
    if service_name == "facade":
        import facadeService.facade_controller
        return facadeService.facade_controller.app

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--service", type=str, choices=["logging", "messages", "facade"],
                                           default = "facade", help="Service to run: logging, messages, facade")
    parser.add_argument("-p", "--port", type=int, default=config.FACADE_SERVICE_PORT, help="Port number for the app service")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode for the service app")
    args = parser.parse_args()

    app = get_app(args.service)
    app.run(port=args.port, debug=args.debug)
