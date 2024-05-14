import utils
import argparse

def get_app(service_name: str):
    if service_name == "logging":
        import loggingService.logging_controller
        return loggingService.logging_controller.app, loggingService.logging_controller.register_service
    if service_name == "messages":
        import messagesService.messages_controller
        return messagesService.messages_controller.app, messagesService.messages_controller.register_service
    if service_name == "facade":
        import facadeService.facade_controller
        return facadeService.facade_controller.app, facadeService.facade_controller.register_service

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--service", type=str, choices=["logging", "messages", "facade"],
                                           default = "facade", help="Service to run: logging, messages, facade")
    parser.add_argument("-p", "--port", type=int, help="Port number for the app service")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode for the service app")
    parser.add_argument("--host", type=str, help="Host address for the app service")
    parser.set_defaults(host=utils.get_current_host())
    args = parser.parse_args()
    
    app, service = get_app(args.service)
    
    service.register_service()
    app.run(host=args.host, port=args.port, debug=args.debug)
