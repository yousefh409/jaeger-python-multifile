import time
from opentelemetry import trace

tracer = trace.get_tracer(__name__)

def funcUtil():
    with tracer.start_as_current_span("funcUtil"):
        time.sleep(2)
        print("This will error")
        oops = 1 / 0